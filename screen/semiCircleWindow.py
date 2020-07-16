from Tkinter import Tk, Canvas, Frame, BOTH
import time
from math import cos, sin, radians
from common import windowHeight, windowLength
from drawingWindow import shapeWindow
#from robotProxy.circleRobot import circleProxy as RobotProxy


class semiCircleCanvas(shapeWindow):
    def __init__(self, robotShape, target):
        super(self.__class__, self).__init__("Semi Circle", target)
        self.initUI(robotShape)
        
    def initUI(self, robotShape):       
        self.side = 0
        self.increment = radians(1.0)
        self.lineInc = 4
        self.radius = windowHeight/4
        self.angle_min = radians(90)
        self.angle_max = radians(270)
        self.sideLength = windowHeight/2
        self.xmin = (windowLength - self.sideLength)/2
        self.ymin = (windowHeight - self.sideLength)/2
        self.xmax = (windowLength + self.sideLength)/2
        self.ymax = (windowHeight + self.sideLength)/2
        self.centre_x = windowLength/2
        self.centre_y = windowHeight/2
        self.curr_angle = self.angle_min
        self.cornersX = [self.centre_x + (self.radius * cos(self.angle_max)),
                         self.centre_x + (self.radius * cos(self.angle_min)),]
        self.cornersY = [self.centre_y + (self.radius * sin(self.angle_max)),
                         self.centre_y + (self.radius * sin(self.angle_min))]
        self.startX = self.cornersX[0]
        self.startY = self.cornersY[0]
        self.xmin = self.centre_x - self.radius
        self.ymin = self.centre_y - self.radius
        if robotShape:    
            self.robot = RobotProxy()
        self.coOrd = self.xmin, self.ymin, self.xmax, self.ymax
        
        
        self.canvas.create_arc(self.coOrd, 
                                start=90, 
                                extent=180,
                                dash=(4, 2), 
                                outline="black",
                                fill ='')
        self.canvas.move(self.metronome, self.startX, self.startY)
        
        self.canvas.pack(fill=BOTH, expand=1)
        self.startRobot()
        
    def drawing(self): 
        if not self.moveMetronome:
            return
       
        try:
            endX = self.startX
            endY = self.startY
            if self.side == 0:
                # straight side
                if endY <= self.cornersY[1]:
                    endY += self.lineInc
                    if endY >= self.cornersY[1]:
                        #setup for curve side
                        endY = self.cornersY[1]
                        self.curr_angle = self.angle_min + self.increment
                        self.side = 1
            else:                        
                     
                if self.curr_angle <= self.angle_max:
                    self.curr_angle += self.increment
                    if self.curr_angle > self.angle_max:
                        self.curr_angle = self.angle_max
                    endX = self.centre_x + self.radius * cos(self.curr_angle)
                    endY = self.centre_y + self.radius * sin(self.curr_angle)
                    if self.curr_angle >= self.angle_max:  
                        # Move to straight side
                        print "Cycle completed : %s" % self.cycle
                        if self.cycle >= self.target:
                            self.stopExcercise()
                            return
                        self.cycle += 1
                        self.side = 0
                    angleRad = self.curr_angle
                    if self.robot:
                        self.robot.synchRobotToCircleDrawing(angleRad, self.updateTime)
                       
                else:
                    self.stopExcercise()
                    pass
            self.canvas.move(self.metronome, 
                                 endX-self.startX,
                                 endY-self.startY)
            self.startX = endX
            self.startY = endY
           
            self.master.after(self.updateTime, self.drawing) 
          
        except Exception:
            print "detected stop request"
            self.stopExcercise()
            raise
            
                
            
        
        
