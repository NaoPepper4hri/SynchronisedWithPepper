from Tkinter import  BOTH
import time
from drawingWindow import shapeWindow
from robotProxy.squareRobot import squareProxy as RobotProxy
from common import windowHeight, windowLength
root = None

class rectangleCanvas(shapeWindow):
    def __init__(self, robotShape, target):
        super(self.__class__, self).__init__("Rectangle", target)
        self.initUI(robotShape)
        
    def initUI(self,robotShape):
        self.side = 0
        
        self.increment = 4
        self.sideLength = windowHeight/2 + 100
        self.sideHeight = windowHeight/4 + 100
        self.xmin = (windowLength - self.sideLength)/2
        self.ymin = (windowHeight - self.sideHeight)/2
        self.xmax = (windowLength + self.sideLength)/2
        self.ymax = (windowHeight + self.sideHeight)/2
        self.xSpan = self.xmax - self.xmin
        self.ySpan = self.ymax - self.ymin
        self.startX = self.xmin
        self.startY = self.ymin
        if robotShape:
            self.robot = RobotProxy()
        
        
        
        self.canvas.create_rectangle(self.xmin, 
                                     self.ymin, 
                                     self.xmax, 
                                     self.ymax, 
                                     dash=(4, 2), 
                                     outline="black")
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
                self.increment *= -1
                
            if self.side < 4:
                endX = self.startX
                endY = self.startY
                if self.side % 2 == 0 :
                    endX += self.increment
                    if self.increment < 0 and \
                             endX <= self.xmin:
                        endX = self.xmin
                        self.side += 1
                        if self.side == 2:
                            self.increment *= -1
                    elif self.increment > 0 and \
                           endX >= self.xmax: 
                        endX = self.xmax
                        self.side += 1
                        if self.side == 2:
                            self.increment *= -1
                else:
                    endY += self.increment
                    if self.increment < 0 and \
                             endY <= self.ymin:
                        endY = self.ymin
                        self.side += 1
                        if self.side == 2:
                            self.increment *= -1
                    elif self.increment > 0 and \
                           endY >= self.ymax: 
                        endY = self.ymax
                        self.side += 1
                        if self.side == 2:
                            self.increment *= -1
                xFrac = float(endX - self.xmin)/float(self.xSpan)
                yFrac = float(endY - self.ymin)/float(self.ySpan)
                if self.robot:
                    self.robot.synchRobotToDrawing(xFrac, yFrac, self.updateTime)
                
                self.canvas.move(self.metronome, 
                                 endX-self.startX,
                                 endY-self.startY)
                self.startX = endX
                self.startY = endY
               
                self.master.after(self.updateTime, self.drawing)
            else:
                self.stopExcercise()
                
        except Exception:
            print "detected stop request"
            self.stopExcercise()
            raise
            
