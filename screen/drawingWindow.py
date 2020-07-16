"""
The drawingWindow is the base class and is the main thread for the 
controlling the user canvas update, the metronome for the user and keeping track 
of the robot thread

The drawingWindow are extended by the shape-specific canvas to define the shape  
to be drawn on the canvas, the update function and control the position of the 
metronome at each update.
It also defines the robotProxy depending on the shape the robot has to draw.
In synchronouse drawing mode the robot has to draw the same shape as the user 
and at the same speed, so the user metronome position is updated to the robot.
In asynchronous mode the robot has to draw a different shape from the user or 
the same shape as the user but at a different speed. In this case a different 
robot-shape and the correct robot proxy is defined for that shape.

There is also a practice mode in which the robot will not be doing any drawing 
so the robot proxy will not be defined at all.
The robot proxy runs on it's own thread to move the robot hand based on the 
update received from the shape canvas. There is a different robotProxy based on 
the shape the robot has to draw. 
"""
import time
from common import windowLength
from importlib import import_module
from math import sqrt, floor
from Tkinter import Tk, Canvas, Frame, BOTH

class baseWindow(Frame, object):
    def __init__(self, frameTitle, target, logger):
        super(baseWindow, self).__init__()
        self.master.title(frameTitle)
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.shape = None               # The shape to be drawn on canvas
        self.robotShape = None          # The shape that the robot should draw        
        self.robot = None               # The robot updater
        self.logger = logger
        
        self.updateTime = 180
        self.metronomeRadius = 20
        self.metronome = self.canvas.create_oval(-self.metronomeRadius,
                                                 -self.metronomeRadius,
                                                 self.metronomeRadius,
                                                 self.metronomeRadius,
                                                 outline="",
                                                 fill="blue")
        self.metMiddle = self.canvas.create_oval(-self.metronomeRadius/2,
                                                 -self.metronomeRadius/2,
                                                 self.metronomeRadius/2,
                                                 self.metronomeRadius/2,
                                                 outline="",
                                                 fill="white")
        self.distanceToMetronome = 0.0
        
        self.warningText = None
        self.msgText = self.canvas.create_text(windowLength/2,
                                               70,
                                               font=("Arial", 15),
                                               text="Tap once on dot and wait to start",
                                               fill="black") 
        self.moveMetronome = False
        self.target = target
        self.pointsPerCm = 39.76608 #calculated manually from screen resolution and size  
        self.pointerX = 0
        self.pointerY = 0
        self.pointerDistancedRefreshed = False
        self.updateCount = 0
        self.playerDist = 0.0
        self.playerOffDist = 0.0
        self.playerOffAtUpdateCount = 0.0
        self.playerOffCount = 0.0
        self.playerOffRecordingDistance = 0.0
        self.isPlayerOnMetronome = True
        self.robotProgress = -1
        
    def doInitialLogs(self, participantID):
        self.logger.info("Target number of cycles for user: %s " % self.target)
        self.logger.info("Target canvas update time: %s msec" % self.updateTime)
        self.logger.info("Metronome radius: %s cm" % (self.metronomeRadius/self.pointsPerCm))
        self.logger.info("Participant Number: %s" % participantID)
        self.shape.doInitialLogs(logger = self.logger, 
                                 ppCm = self.pointsPerCm,
                                 updateTime = self.updateTime)
        if self.robotShape:
            self.robotShape.doInitialLogs(logger=self.logger, 
                                          shapeFor="Robot",
                                          ppCm = self.pointsPerCm,
                                          updateTime = self.updateTime)
        
    def loadAsynchShape(self, robotShape, steps=1.0, practice=False):
        # in asynch mode the robot will have different shape
        # or same shape at different drawing speed
        robotShapeModule = import_module("shapeProxy.%s" % robotShape)
        robotShapeClass = getattr(robotShapeModule, "Shape")
        self.robotShape =  robotShapeClass(steps)            
        
        
        if not practice:
            self.logger.info("Running experiment asynchronous mode")
            # if not in practice mode load and define the correct
            # robot proxy for the shape the robot has to draw
            roboProxytModule = import_module("robotProxy.%sRobot" % robotShape)
            robotProxyClass = getattr(roboProxytModule, "%sProxy" % robotShape)
            self.robot = robotProxyClass(self.robotShape.xSpan/self.pointsPerCm,
                                         self.robotShape.ySpan/self.pointsPerCm,
                                         float(self.updateTime)/1000.0,
                                         'RM')   # Right mirror drawing for asynch
                                         
        else:
            self.logger.info("Running practice asynchronous mode")
            
    def startRobot(self):
        """
        set up robot to start position
        """
        if self.robot:
            self.robot.switch_follow_on()
            time.sleep(2.0)
    
    def startExercise(self):
        """
        start the exercise 
        """
        if not self.moveMetronome:
            if self.shape.cycle > self.target:
                return
            if self.msgText:
                self.canvas.delete(self.msgText)
                self.msgText = None
                self.canvas.update()
            if self.robot:
                #start the robot thread to update robot
                # arm movement
                self.robot.start()
                self.logger.info("Robot ready to move along the shape")
            time.sleep(2.0)
            # schedule an update
            self.master.after(self.updateTime, self.drawing)
            # set the metronome to move
            self.moveMetronome = True
            self.logger.info("Metronome ready to move along the shape")
            self.startTimer = time.time()
        
            
    
    def stopExcercise(self, event=None):
        # set the metronome not to move
        
            
        if self.robot:
            # switch of robot to stop following arm update
            self.robot.switch_follow_on(switch_on=False)
            self.logger.info("Robot instructed to stop")
        if self.moveMetronome:
            self.moveMetronome = False
            self.logger.info("Metronome stopped")
            self.doEndLog()
        time.sleep(1.0)
        try:
            # wait for the robot thread to join
            if self.robot:
                self.robot.join()
                self.logger.info("Robot thread has stopped")
                # This line will ensure that the metronome does not restart if paused
                self.cycle += self.target
        except:
            pass            
            
        if self.robot:
            # return robot to standing position
            self.robot.stand_return()
        time.sleep(2)
        self.master.destroy()
            
    def doEndLog(self):
        self.logger.info("Number of updates : %s " % self.updateCount)
        if self.robotShape:
            finalRobotSpeed = self.robotShape.getDistanceCovered(ppCm=self.pointsPerCm)*1000.00/((self.updateCount+1)*self.updateTime)
            self.logger.info("Average robot speed: -%s cm/sec" % (finalRobotSpeed))
        #print "Number of updates : %s " % self.updateCount
        if self.updateCount:
            self.logger.info("Average distance of player from metronome: %s cm" % (self.playerDist/self.updateCount))
            #print "Average distance of player from metronome: %s cm" % (self.playerDist/self.updateCount)
            
        self.logger.info("Number of times player was off metronome at update (time) : %s " % self.playerOffAtUpdateCount)
        #print "Number of times player was off metronome at update (time) : %s " % self.playerOffAtUpdateCount
        if self.playerOffAtUpdateCount:
            avgOffAtUpdate = self.playerOffDist/self.playerOffAtUpdateCount
            self.logger.info("Average distance of player off metronome at update: %s cm" % avgOffAtUpdate)
            #print "Average distance of player off metronome at update: %s cm" % avgOffAtUpdate
            
        self.logger.info("Number of times player off metronome recorded (count): %s " % self.playerOffCount)
        #print "Number of times player off metronome recorded (count): %s " % self.playerOffCount
        if self.playerOffCount:
            avgOffAtRecording = self.playerOffRecordingDistance/self.playerOffCount
            self.logger.info("Average distance of player off metronome: %s cm" % avgOffAtRecording)
            #print "Average distance of player off metronome: %s cm" % avgOffAtRecording
        if self.playerOffCount or self.playerOffAtUpdateCount:
            combineErrorCount = self.playerOffCount + self.playerOffAtUpdateCount
            totalAvgOff = (self.playerOffDist + self.playerOffRecordingDistance)/combineErrorCount
            self.logger.info("Combined error (count + time) : %s" % combineErrorCount)
            #print "Combined error (count + time) : %s" % combineErrorCount
            self.logger.info("Combined avgerage distance of player off metronome: %s cm" % totalAvgOff)
            #print "Combined avgerage distance of player off metronome: %s cm" % totalAvgOff
    
    def motion(self, event=None):
        """
        This is the pointer move callback
        """
        if event:
            self.pointerX = event.x
            self.pointerY = event.y
        if self.moveMetronome:
            self.updatePointerToMetronome()
            if self.distanceToMetronome > 1.1*self.metronomeRadius:
                self.isPlayerOnMetronome = False
                # if we are off the metronome
                if not self.warningText:
                    distanceCm = self.distanceToMetronome/self.pointsPerCm
                    self.logger.info("Player gone off metronome")
                    self.logger.info("Player gone off recorded at: %s cm" % distanceCm)
                    self.playerOffCount += 1.0
                    self.playerOffRecordingDistance += distanceCm
                    # Show warning text if it is not already showing
                    self.warningText = self.canvas.create_text(windowLength/2,
                                                               50,
                                                               font=("Arial", 15),
                                                               text="PLEASE STAY ON THE DOT!",
                                                               fill="blue") 
                    
            else:
                # We are on the metronome
                self.isPlayerOnMetronome = True
                if self.warningText:
                    self.logger.info("Player returned on metronome")
                    # remove warning text if it is showing
                    self.canvas.delete(self.warningText)
                    self.warningText = None
        elif self.warningText:
            self.isPlayerOnMetronome = True
            self.canvas.delete(self.warningText)
            self.warningText = None 
            
    def locateMetronome(self):
        self.canvas.move(self.metronome, self.shape.startX, self.shape.startY)
        self.canvas.move(self.metMiddle, self.shape.startX, self.shape.startY)
    
    def updatePointerToMetronome(self):
        xDiff = self.pointerX - self.shape.startX
        yDiff = self.pointerY - self.shape.startY
        self.distanceToMetronome = sqrt(xDiff*xDiff + yDiff*yDiff)
        self.pointerDistancedRefreshed = True
        #print "offset = %s" % distance
         
    
    def pointerClick(self, event):
        """
        Pointer left click callback
        """
        # Check how far the pointer is from the curr point of 
        # of shape i.e. where the metronome is
        xDiff = abs(event.x - self.shape.startX)
        yDiff = abs(event.y - self.shape.startY)
        if xDiff<=self.metronomeRadius and yDiff<=self.metronomeRadius:
            # If we are in the metronome start the exercise
            self.startExercise()
            
    def drawing(self): 
        """
        The update function
        """
        xFrac = None
        yFrac = None
        
        if self.shape.cycle > self.target:
            # if we have stop the metronome and 
            # robot
            self.logger.info("All cycles completed : %s" % self.target)
            if self.warningText:
                self.canvas.delete(self.warningText)
                self.warningText = None
            displayText = "      Current block complete.\nPlease take and break and continue."
            if not self.robot:
                displayText = "      Practice block complete.\nExperimenter will be with you shortly."
            self.msgText = self.canvas.create_text(windowLength/2,
                                               70,
                                               font=("Arial", 15),
                                               text=displayText,
                                               fill="black",
                                               anchor="center")
            
            self.canvas.update() 
            self.stopExcercise()
        if not self.moveMetronome:
            # metronome is not moving yet. Do nothing
            return
        
        if self.robot:
            self.logger.info("Robot off mark by %s cm" % self.robot.getRobotError())
        
        
        try:
            # record which cycle we are running
            currCycle = self.shape.cycle
            
            # Calculate where the metronome should move next
            endX, endY = self.shape.calculateNext()
            
            if self.robotShape:
                # If the robot is working with its own shape
                # Record the curr cycle that the robot shape is on 
                robotCycle = self.robotShape.cycle
                # Calculate the next point the robot should be on 
                robotX, robotY = self.robotShape.calculateNext()
                if self.robotShape.cycle > robotCycle:
                    # If the robot has moved to the next cycle log
                    # the cycle completed for Robot
                    self.logger.info("Robot cycle completed : %s" % robotCycle)
                #Get the relative positions for updating the robot arm
                xFrac, yFrac = self.robotShape.getRelativeXY(robotX, robotY)
                # update the robot shape point to the next point
                # note this is not the robot proxy
                self.robotShape.updateCurrPoint(robotX, robotY)
                coverageString, self.robotProgress = self.robotShape.getCoverage()
                self.logger.info("Robot Metronome: %s" % coverageString)
            else:    
                # In synchronous  mode
                # So get the relative position for the robot arm
                # from the canvas shape
                xFrac, yFrac = self.shape.getRelativeXY(endX, endY)
                
            if self.robot:
                # Check because for subject practice there may be no robot
                # Tell the robot proxy the relative x y position for the robot arm
                self.robot.synchRobotToDrawing(xFrac, yFrac, self.updateTime)
            
            # move the metronome to the new position on canvas
            self.canvas.move(self.metronome, 
                             endX-self.shape.startX,
                             endY-self.shape.startY)
            self.canvas.move(self.metMiddle, 
                             endX-self.shape.startX,
                             endY-self.shape.startY)
            
            # update the canvas shape to the new position
            self.shape.updateCurrPoint(endX, endY)
            coverageString, userProgress = self.shape.getCoverage()
            self.logger.info("User Metronome: %s" % coverageString)
            if not self.pointerDistancedRefreshed:
                # pointer not in motion would result in no refresh. Try to force a refresh
                self.motion()    
            
            if self.robotShape:
                check = abs(self.robotProgress - userProgress)
                if 90.0 < check or check < 9.0:
                    # User and robot in perfect phase/antiphase location
                    # so speed up the robot
                    if not self.robotShape.varInc:
                        self.robotShape.accelerate(logger=self.logger, 
                                               ppCm = self.pointsPerCm,
                                               updateTime = self.updateTime)
                elif self.robotShape.varInc:
                    # Robot and user definitely not in the same place 
                    # get back to steady speed
                    self.robotShape.varInc = 0.0
                    self.logger.info("Risk corrected, return robot to steady speed")
                    
            distanceInCm =  self.distanceToMetronome/self.pointsPerCm
            self.logger.info("User pointer off metronome by: %s cm" % distanceInCm)
            
            self.updateCount += 1.0
            self.playerDist += distanceInCm
            if not self.isPlayerOnMetronome:
                self.playerOffDist += distanceInCm
                self.playerOffAtUpdateCount += 1.0
                
            # distance recorded now mark it false for a refresh before next update
            self.pointerDistancedRefreshed = False 
            
            if self.shape.cycle > currCycle:
                # Check if the shape has moved to a new cycle
                # and log cycle completion
                self.logger.info("Cycle completed : %s" % currCycle)
                
                print "To do: %s cycles" %(self.target - currCycle)
                # Check if we have completed target number
                # of cycles
                
                    
            
            # This indicates the excercise is still running.
            # Schedule the next update              
            self.master.after(self.updateTime, self.drawing)
                   
        except Exception:
            print "detected exception"
            self.stopExcercise()
            raise
        
    def makeRobotAlive(self):
        if self.robot:
            self.robot.makeInteractive()