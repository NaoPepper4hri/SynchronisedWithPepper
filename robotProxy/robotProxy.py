import copy
import threading
import time
from naoqi import ALProxy
from common import (
                    thread_lock                    
                    )
from math import radians, degrees, acos, cos, sqrt
import motion

LEFT_MIRROR = 1   
LEFT_NO_MIRROR = 2 
RIGHT_NO_MIRROR = 3
RIGHT_MIRROR = 4

class baseProxy(threading.Thread):
    def __init__(self, xSpanCm, ySpanCm, synchTime, armOpt="R"):
        #self.robotIP = "192.168.1.162"  #Nao
        #self.robotIP = "192.168.1.163"  #Nao
        #self.robotIP = "192.168.1.164"  #Nao
        self.robotIP = "192.168.1.193"  #Pepper
        port = 9559
        threading.Thread.__init__(self)
        self.motionProxy = ALProxy("ALMotion", self.robotIP, port)
        self.postureProxy = ALProxy("ALRobotPosture", self.robotIP, port)
        self.autonomousLife = ALProxy("ALAutonomousLife", self.robotIP, port)
        self.basicAwareness = ALProxy("ALBasicAwareness", self.robotIP, port)
        self.motionProxy.setBreathConfig([['Bpm', 1.0], ['Amplitude', 0.2]])
        #self.autonomousLife.setState("disabled")
        self.motionProxy.wakeUp()
        try:
            self.basicAwareness.stopAwareness()
            self.motionProxy.setBreathEnabled ('Body', False)
        except Exception:
            pass
        self.postureProxy.goToPosture("Stand", 5.0)
                 
        self.armPitch = None
        self.armRoll = None
        self.syncTimeList = [synchTime, synchTime]
        self.follow_on = False        
	
	self.origTangentDist = self.motionProxy.getTangentialSecurityDistance()
	self.origOrthDist = self.motionProxy.getOrthogonalSecurityDistance()
	#print self.origTangentDist
        
        """
        LEFT_MIRROR = 1   
        LEFT_NO_MIRROR = 2 
        RIGHT_NO_MIRROR = 3
        
        if armOpt == "LM":
            self.armOption = LEFT_MIRROR
        elif armOpt == "L":
            self.armOption = LEFT_NO_MIRROR
        else:
            self.armOption = RIGHT_NO_MIRROR
        """
        if armOpt == "RM":
            #print "Right mirror"
            self.armOption = RIGHT_MIRROR
        else:
            #print "Right no mirror"
            self.armOption = RIGHT_NO_MIRROR
        
        if self.armOption == LEFT_MIRROR:
            self.setupKeys()
            self.setupLeftMirroring(xSpanCm, ySpanCm)
        elif self.armOption == LEFT_NO_MIRROR:
            self.setupKeys()
            self.setupLeftNoMirroring(xSpanCm, ySpanCm)
        elif self.armOption == RIGHT_MIRROR:
            self.setupKeys(leftArm=False)
            self.setupRightMirroring(xSpanCm, ySpanCm)
        else:
            self.setupKeys(leftArm=False)
            self.setupRightNoMirroring(xSpanCm, ySpanCm)
        
            
        
            
    def setupKeys(self, leftArm=True):
        prefix = 'L'
        self.elbowWristYaw = radians(-30)
        self.headYaw = radians(15)
        self.elbowRoll = radians(-2)
        if not leftArm:
            prefix = 'R'
            self.elbowWristYaw *= -1.0
            self.headYaw *= -1.0
            self.elbowRoll *= -1.0
        self.shoulderPitchKey = '%sShoulderPitch' % prefix 
        self.shoulderRollKey = '%sShoulderRoll' % prefix  
        self.elbowYawKey = '%sElbowYaw' % prefix 
        self.elbowRollKey =  '%sElbowRoll' % prefix
        self.wristYawKey = '%sWristYaw' % prefix
        self.handKey ='%sHand' % prefix
        
        
        
    def setupLeftMirroring(self, xSpanCm, ySpanCm):
        # Robot left arm going from  in to out
        # Robot left in angle < out angle
        if self.robotIP.startswith("192.168.1.16"):
            # This is Nao with arm length of roughly 25cm
            self.armLength = 25
            self.rollMin = radians(-10.0)
            self.pitchMin = radians(-10.0)
           
        else:
            # This is Pepper with arm length 45cm
            self.armLength = 40
            self.rollMin = radians(9.0)
            self.pitchMin = radians(20.0)
            
        
        self.rollMax = self.rollMin + self.getSwingAngle(xSpanCm)
        self.rollSpan = self.rollMax - self.rollMin
        
        self.pitchMax = self.pitchMin + self.getSwingAngle(ySpanCm)
        self.pitchSpan = self.pitchMax - self.pitchMin
        
    def setupLeftNoMirroring(self, xSpanCm, ySpanCm):
        
        # set up for left mirroring first and then invert x or roll
        self.setupLeftMirroring(xSpanCm, ySpanCm)
        
        # Robot left arm going from out to in
        # Robot left in angle < out angle
        
        # No mirroring so switch left roll min and max
        rollMinHold = self.rollMin
        self.rollMin = self.rollMax
        self.rollMax = rollMinHold
        self.rollSpan *= -1.0
        
    def setupRightNoMirroring(self, xSpanCm, ySpanCm):
        # right arm has to fo from in to out like left mirroring
        # so, set up for left mirroring first
        self.setupLeftMirroring(xSpanCm, ySpanCm)
        
        # right arm angles are negative of left arm
        self.rollMin *= -1.0
        self.rollMax *= -1.0
        self.rollSpan *= -1.0
        
    def setupRightMirroring(self, xSpanCm, ySpanCm):
        
        # set up for left mirroring first and then invert x or roll
        self.setupRightNoMirroring(xSpanCm, ySpanCm)
        
        # No mirroring so switch left roll min and max
        rollMinHold = self.rollMin
        self.rollMin = self.rollMax
        self.rollMax = rollMinHold
        self.rollSpan *= -1.0
        
        
        
    
        

            
            
    def getSwingAngle(self, coveringCm):
        
        twiceArmSquare = 2*self.armLength*self.armLength
        cosAngle = (twiceArmSquare - (coveringCm*coveringCm))/twiceArmSquare
        swingRadians = abs(acos(cosAngle))
        return swingRadians
    
    def switch_follow_on(self, switch_on=True):
                    
        arm_angle_keys = [self.shoulderPitchKey , 
                          self.shoulderRollKey,  
                          self.elbowYawKey, 
                          self.elbowRollKey,
                          self.wristYawKey,
                          self.handKey,
                          'HeadPitch',
                          'HeadYaw']
       
        angle_list = [self.armPitch,
                      self.armRoll,
                      self.elbowWristYaw,
                      self.elbowRoll,
                      self.elbowWristYaw,
                      0.25,
                      radians(15),
                      self.headYaw]
        time_list = [2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0,
                    2.0]
        self.follow_on = switch_on
        if switch_on:
            self.basicAwareness.stopAwareness()
            self.motionProxy.setBreathEnabled ('Body', False)
            self.motionProxy.angleInterpolation(arm_angle_keys, angle_list, time_list, True)
        
        
        
    def stand_return(self):
        print "Requested stand at ease"
        self.postureProxy.goToPosture("Stand", 4.0)
	self.motionProxy.setTangentialSecurityDistance(self.origTangentDist)
	self.motionProxy.setTangentialSecurityDistance(0.4)
        #mid experiment basic awareness stopping
        #self.basicAwareness.startAwareness()
        self.motionProxy.setBreathEnabled ('Body', True)
    
    def makeInteractive(self, makeAware):
        if makeAware == True:
            self.basicAwareness.setEngagementMode("SemiEngaged")
            self.autonomousLife.setState("solitary")    
        else:
            self.autonomousLife.setState("disabled")
            self.motionProxy.wakeUp()  
        
               
    
    def run(self):
        # moniotr how the robot should move
        
        angle_list = None
        sync_time = None
	self.motionProxy.setTangentialSecurityDistance(0.03)
	self.motionProxy.setOrthogonalSecurityDistance(0.05)
        while self.follow_on:
            try:
                thread_lock.acquire()
                angle_list = [self.armPitch, self.armRoll]
                sync_time = self.syncTimeList  
            finally:
                thread_lock.notify_all()
                thread_lock.release()
            #print"HERE :" + str(degrees(angle_list[1]))
            #print str(sync_time)
            self.update_robot(angle_list, sync_time)
            
            #time.sleep(0.5)
            
            
    def update_robot(self, angle_list, time_list):
        angle_keys = [self.shoulderPitchKey, 
                     self.shoulderRollKey]
        try:
            if angle_list:
                self.motionProxy.angleInterpolation(angle_keys, angle_list, time_list, True)
        except:
            raise
            pass
            
    def synchRobotToDrawing(self, x, y, time):
        """
        @param x: the fraction of the line covered in x direction
        @param y: the fraction of the line covered in y direction
        @param time: the time in which to execute the move
        """
        roll_angle = self.rollMin + (x * self.rollSpan)
        pitch_angle = self.pitchMin + (y * self.pitchSpan)
        # left hand rolls are negative so reverse the comparison
        if (self.armOption == LEFT_MIRROR and roll_angle < self.rollMin) or \
           (self.armOption in [LEFT_NO_MIRROR, RIGHT_NO_MIRROR] and roll_angle > self.rollMin):
            roll_angle = self.rollMin
        elif (self.armOption == LEFT_MIRROR and roll_angle > self.rollMax) or \
             (self.armOption in [LEFT_NO_MIRROR, RIGHT_NO_MIRROR] and roll_angle < self.rollMax) :
            roll_angle = self.rollMax
             
        if pitch_angle > self.pitchMax:
            pitch_angle = self.pitchMax
        elif pitch_angle < self.pitchMin:
            pitch_angle = self.pitchMin
            
        #sync_time = float(time)/1000.0
        
        try:
                thread_lock.acquire()
                self.armPitch = pitch_angle
                self.armRoll = roll_angle
                #self.syncTimeList = [sync_time, sync_time]
                
                """
                print "fracX=%s fracY=%s pitch=%s roll=%s" %(
                                    x,
                                    y,
                                    self.armPitch,
                                    self.armRoll)
                """
        finally:
            thread_lock.notify_all()
            thread_lock.release()    
            
    def getRobotError(self):
        """
        Arrived at the formula by trigonometry simplification
        distance between desired position and current position is given by
        distance = 2*armlength* sqrt(( 2 - cos(rollDiff) - cos(pitchDiff))/2) 
        """
        currPitch = self.motionProxy.getAngles(self.shoulderPitchKey, False)
        currRoll =  self.motionProxy.getAngles(self.shoulderRollKey, False)
        
        rollDiff = self.armPitch - currPitch[0]
        pitchDiff = self.armRoll - currRoll[0]
        
        distance = 2.0*self.armLength * sqrt((2 - cos(rollDiff) - cos(pitchDiff))/2)
        
        #print "distance in cm : %s" % distance
        return distance
    
        
        
        
