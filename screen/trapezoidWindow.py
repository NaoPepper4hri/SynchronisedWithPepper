from Tkinter import  BOTH
import time
from math import tan, radians
from drawingWindow import shapeWindow
#from robotProxy.squareRobot import squareProxy as RobotProxy
from common import windowHeight, windowLength
root = None

class trapezoidCanvas(shapeWindow):
    def __init__(self, robotShape, target):
        super(self.__class__, self).__init__("Trapezoid", target)
        self.initUI(robotShape)
        
    def initUI(self, robotShape):
        self.side = 0
        self.step = 0
        self.increment = 4
        self.slope =  1
        self.baseLength = windowLength/2 + 100
        self.height = windowHeight/4 + 20
        
        self.xmin = (windowLength - self.baseLength)/2
        self.xmax = (windowLength + self.baseLength)/2
        self.ymin = (windowHeight - self.height)/2
        self.ymax = (windowHeight + self.height)/2
        
        self.cornerX =[self.xmin + self.height,
                       self.xmax - self.height,
                       self.xmax,
                       self.xmin] 
        
        self.cornerY =[self.ymin,
                       self.ymin,
                       self.ymax,
                       self.ymax]
    
        self.startX = self.cornerX[0] 
        self.startY = self.cornerY[0]
        if robotShape:
            self.robot = RobotProxy()
        
        self.canvas.create_polygon(self.cornerX[0], 
                                   self.cornerY[0], 
                                   self.cornerX[1], 
                                   self.cornerY[1],
                                   self.cornerX[2], 
                                   self.cornerY[2],
                                   self.cornerX[3], 
                                   self.cornerY[3],
                                   dash=(4, 2), 
                                   outline="black",
                                   fill='')
        
        self.canvas.move(self.metronome, self.startX, self.startY)
        self.canvas.pack(fill=BOTH, expand=1)
        self.startRobot()
        
        
        
    def drawing(self):  
        if not self.moveMetronome:
            return
        
        try:   
            if self.side >= 4:  
                # For repeat
                print "Cycle completed : %s" % self.cycle
                if self.cycle >= self.target:
                    self.stopExcercise()
                    return
                self.cycle += 1
                self.side = 0

                
            if self.side < 4:
                
                if self.side == 0:
                    endX = self.startX + self.increment
                    endY = self.startY
                    #print"x:%s  y:%s slope:%s" % (endX, endY, self.slope) 
                    if endX >= self.cornerX[1]:
                        endX = self.cornerX[1]
                        endY = self.cornerY[1]
                        self.side += 1
                elif self.side == 1:
                    endX = self.startX + self.increment
                    endY = self.startY + self.increment
                    #print"x:%s  y:%s slope:%s" % (endX, endY, self.slope) 
                    if endX >= self.cornerX[2]:
                        endX = self.cornerX[2]
                        endY = self.cornerY[2]
                        self.side += 1
                elif self.side == 2:
                    endX = self.startX - self.increment
                    endY = self.startY
                    #print"x:%s  y:%s slope:%s" % (endX, endY, self.slope) 
                    if endX <= self.cornerX[3]:
                        endX = self.cornerX[3]
                        endY = self.cornerY[3]
                        self.side += 1      
                else:
                    endX = self.startX + self.increment
                    endY = self.startY - self.increment 
                    if endX >= self.cornerX[0]:
                        endX = self.cornerX[0]
                        endY = self.cornerY[0]
                        self.side += 1      
                
                #xFrac = float(endX - self.xmin)/float(self.xSpan)
                #yFrac = float(endY - self.ymin)/float(self.ySpan)
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
            
