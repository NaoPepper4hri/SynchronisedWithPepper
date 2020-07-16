from math import cos, sin, radians
from baseShape import baseShape
from common import windowHeight, windowLength


class Shape(baseShape):
    def __init__(self, steps=None):
        super(self.__class__, self).__init__()        
        
        self.increment = -radians(2.5)
        if steps:
            self.increment *= steps
        
        self.accRate = self.increment#-radians(1.0)
        self.radius = windowHeight/4 + 50
        self.angle_min = radians(0)
        self.angle_max = radians(360)
        self.centre_x = windowLength/2
        self.centre_y = windowHeight/2
        self.curr_angle = self.angle_max
        self.startX = self.centre_x - (self.radius * cos(self.curr_angle))
        self.startY = self.centre_y + (self.radius * sin(self.curr_angle))
        self.xmin = self.centre_x - self.radius
        self.ymin = self.centre_y - self.radius
        self.xmax = self.centre_x + self.radius
        self.ymax = self.centre_y + self.radius
        
        self.xSpan = self.xmax - self.xmin
        self.ySpan = self.ymax - self.ymin
        self.updateCurrSideLength()
        
    def accelerate(self, logger, ppCm, updateTime):
        
        if not self.varInc:
            self.varInc = self.accRate
        
        logger.info("Sync perception risk speed set to accelerated speed for next update")

    def doInitialLogs(self, logger, ppCm, updateTime, shapeFor="Canvas"):
        super(self.__class__, self).doInitialLogs(logger,
                                                  ppCm,
                                                  updateTime,
                                                  shapeFor)
        radiusInCm = self.radius /ppCm 
        logger.info("%s Shape circle radius : %spoints = %s cm" % (shapeFor,
                                                                  self.radius,
                                                                  radiusInCm))
        
        logger.info("%s Circumference: %s cm" % (shapeFor,
                                                self.currSideLength*radiusInCm))
        
        update_rate = (self.increment*radiusInCm*1000.00)/updateTime
        logger.info("%s UpdateSpeed: %s cm/sec" % (shapeFor,
                                                   update_rate))
        
        if shapeFor == "Robot":
            logger.info("The update speed of Robot is its steady drawing speed")
            logger.info("In asynchronous mode this maybe varied when the robot and participant gets in perfect anitphase")
            update_rate = ((self.accRate + self.increment)*radiusInCm*1000.00)/updateTime
            logger.info("The variably applied accelerated speed for asynchronous mode is %s cm/sec " % update_rate)

    def getDistanceCovered(self, ppCm):
        radiusInCm = self.radius /ppCm 
        return radiusInCm * self.currSideLength * (float(self.cycle) - (self.curr_angle/self.currSideLength))
                             
    
    def calculateNext(self):
        
        endX = self.startX
        endY = self.startY
        
        if self.curr_angle > self.angle_min:
            self.curr_angle += self.increment + self.varInc
            if self.curr_angle <= self.angle_min:
                self.cycle += 1  
                self.curr_angle += self.angle_max
            endX = self.centre_x - self.radius * cos(self.curr_angle)
            endY = self.centre_y + self.radius * sin(self.curr_angle)
            
        return endX, endY  
    
    def updateCurrSideLength(self):
        # Circle has only one side so in this case we are getting the angle
        # the full angle is 360
        self.currSideLength = radians(360)
    
    def getCoverage(self):
        #We are starting from 360 degrees and moving down 
        coveragePercent = ((self.currSideLength - self.curr_angle)*100.00)/self.currSideLength
        coverageString = "Cycle: %s, CycleProgress: %s" % (self.cycle,
                                                           coveragePercent)
                   
        return coverageString, coveragePercent       
        
            
                
            
        
        
