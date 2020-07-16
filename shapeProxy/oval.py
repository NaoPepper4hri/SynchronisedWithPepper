from math import cos, sin, radians, sqrt
from baseShape import baseShape
from common import windowHeight, windowLength


class Shape(baseShape):
    def __init__(self, steps=None):
        super(self.__class__, self).__init__()        
        
        self.increment = -radians(2.0)
        if steps:
            self.increment *= steps
            
        self.radiusX = windowLength/6
        self.radiusY = windowHeight/2 - 100
        self.angle_min = radians(0)
        self.angle_max = radians(360)
        self.centre_x = windowLength/2
        self.centre_y = windowHeight/2
        self.curr_angle = self.angle_max
        self.startX = self.centre_x - (self.radiusX * cos(self.curr_angle))
        self.startY = self.centre_y + (self.radiusY * sin(self.curr_angle))
        self.xmin = self.centre_x - self.radiusX
        self.ymin = self.centre_y - self.radiusY
        self.xmax = self.centre_x + self.radiusX
        self.ymax = self.centre_y + self.radiusY
        
        self.xSpan = self.xmax - self.xmin
        self.ySpan = self.ymax - self.ymin
        self.updateCurrSideLength()
    
    def doInitialLogs(self, logger, ppCm, updateTime, shapeFor="Canvas"):
        super(self.__class__, self).doInitialLogs(logger,
                                                  ppCm,
                                                  updateTime,
                                                  shapeFor)
        radiusXInCm = self.radiusX /ppCm 
        radiusYInCm = self.radiusY /ppCm
        logger.info("%s shape oval short radius : %spoints = %s cm" % (shapeFor,
                                                                        self.radiusX,
                                                                        radiusXInCm))
        
        logger.info("%s shape oval long radius : %spoints = %s cm" % (shapeFor,
                                                                        self.radiusY,
                                                                        radiusYInCm))
        h = (radiusYInCm - radiusXInCm)/(radiusXInCm + radiusYInCm )
        h *= h 
        perimeter = radians(180)*(radiusXInCm + radiusYInCm)*(1+ (3*h/(10+sqrt(4-3*h))))
        logger.info("%s oval circumference: %s cm" % (shapeFor,
                                                perimeter))
        
        update_rate = (self.increment*perimeter*1000.00)/(self.currSideLength *updateTime)
        logger.info("%s oval update speed: %s cm/sec" % (shapeFor,
                                                   update_rate))
        
        
    def calculateNext(self):
        
        endX = self.startX
        endY = self.startY
        
        if self.curr_angle >= self.angle_min:
            self.curr_angle += self.increment
            if self.curr_angle <= self.angle_min:
                self.cycle += 1  
                self.curr_angle = self.angle_max
            endX = self.centre_x - self.radiusX * cos(self.curr_angle)
            endY = self.centre_y + self.radiusY * sin(self.curr_angle)
            
        return endX, endY  
    
    def updateCurrSideLength(self):
        # Circle has only one side so in this case we are getting the angle
        # the full angle is 360
        self.currSideLength = radians(360)
    
    def getCoverage(self):
        #We are starting from 360 degrees and moving down 
        coveragePercent = ((self.currSideLength - self.curr_angle)*100.00)/self.currSideLength
        coverageString = "Cycle: %s, Cycle Progress: %s" % (self.cycle,
                                                           coveragePercent)
                   
        return coverageString           
        
            
                
            
        
        
