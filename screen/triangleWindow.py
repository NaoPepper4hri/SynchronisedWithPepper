from Tkinter import  BOTH
import time
from math import tan, radians
from drawingWindow import shapeWindow
#from robotProxy.squareRobot import squareProxy as RobotProxy
from common import windowHeight, windowLength
root = None

class triangleCanvas(shapeWindow):
    def __init__(self, robotShape, target):
        super(self.__class__, self).__init__("Triangle", target)
        self.initUI(robotShape)
        
    def initUI(self, robotShape):
        self.side = 0
        self.step = 0
        self.increment = 2
        self.slope =  1.75 #tan(radians(60))
        self.sideLength = windowHeight/2
        self.xmin = (windowLength - self.sideLength)/2
        self.xmax = (windowLength + self.sideLength)/2
        self.xSpan = self.xmax - self.xmin
        self.ymax = (windowHeight + self.sideLength)/2
        
        self.ymin = round(self.ymax - (self.slope/2) * self.xSpan)
        
        self.ySpan = self.ymax - self.ymin
        
        self.xCord = [self.xmin, (self.xmin + self.xmax)/2, self.xmax]
        self.yCord = [self.ymax, self.ymin, self.ymax]
        self.startX = self.xmin 
        self.startY = self.ymax
        if robotShape:
            self.robot = RobotProxy()
        
        
        
        self.canvas.create_polygon(self.xCord[0], 
                                   self.yCord[0], 
                                   self.xCord[1], 
                                   self.yCord[1],
                                   self.xCord[2], 
                                   self.yCord[2],
                                   dash=(4, 2), 
                                   outline="black",
                                   fill='')
        
        # The metronome is pushed 2 points on the left for x axis because
        # otherwise it does not align to the triangle sides
        self.canvas.move(self.metronome, self.startX - 2, self.startY)
        self.canvas.pack(fill=BOTH, expand=1)
        self.startRobot()
        
        
        
    def drawing(self):  
        if not self.moveMetronome:
            return
        
        try:   
            if self.side >= 3:  
                print "Cycle completed : %s" % self.cycle
                if self.cycle >= self.target:
                    self.stopExcercise()
                    return
                # For repeat
                self.cycle += 1
                self.side = 0
                self.step = 0
                
                
            if self.side < 3:
                
                if self.side == 0:
                    endX = self.startX + self.increment
                    endY = round(self.ymax - self.slope * self.step * self.increment)
                    self.step += 1
                    #print"x:%s  y:%s slope:%s" % (endX, endY, self.slope) 
                    if endX >= self.xCord[1]:
                        endX = self.xCord[1]
                        endY = self.yCord[1]
                        self.step = 0
                        self.side += 1
                elif self.side == 1:
                    endX = self.startX + self.increment
                    endY = round(self.ymin + self.slope * self.step * self.increment)
                    self.step += 1
                    #print"x:%s  y:%s slope:%s" % (endX, endY, self.slope) 
                    if endX >= self.xCord[2]:
                        endX = self.xCord[2]
                        endY = self.yCord[2] 
                        self.step = 0
                        self.side += 1
                        
                else:
                    endX = self.startX - 2*self.increment
                    endY =  self.yCord[0] 
                    if endX <= self.xCord[0]:
                        endX = self.xCord[0]
                        self.side += 1
                
                xFrac = float(endX - self.xmin)/float(self.xSpan)
                yFrac = float(endY - self.ymin)/float(self.ySpan)
                if self.robot:
                    self.robot.synchRobotToDrawing(xFrac, yFrac, self.updateTime)
                
                self.canvas.move(self.metronome, 
                                 endX - self.startX,
                                 endY - self.startY)
                self.startX = endX
                self.startY = endY
               
                self.master.after(self.updateTime, self.drawing)
            else:
                self.stopExcercise()
                
        except Exception:
            print "detected stop request"
            self.stopExcercise()
            raise
            
