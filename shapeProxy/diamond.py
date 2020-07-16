from math import cos, sin, radians
from baseShape import baseShape
from common import windowHeight, windowLength

class Shape(baseShape):
    def __init__(self, steps=None):
        super(self.__class__, self).__init__()
        self.side = 0
        upSlopeAngle = radians(60)
        downSlopeAngle = radians(45)
        self.upSlope =  1.75
        self.downSlope = 1
        self.sideLength = windowHeight/2
        self.xmid = windowLength/2  
        self.ymid = windowHeight/2 + 70
        self.xmin = (windowLength - self.sideLength)/2
        self.xmax = (windowLength + self.sideLength)/2        
        self.ymin = round(self.ymid - self.sideLength * sin(upSlopeAngle))
        self.ymax = round(self.ymid + self.sideLength/2.0)
        self.xSpan = self.xmax - self.xmin
        self.ySpan = self.ymax - self.ymin
        
        self.cornerX = [self.xmid,
                      self.xmax, 
                      self.xmid, 
                      self.xmin]
        self.cornerY = [self.ymin,
                      self.ymid,
                      self.ymax, 
                      self.ymid]
        #print self.cornerX, self.cornerY
        self.startX = self.cornerX[0] 
        self.startY = self.cornerY[0]
        self.increment = 4.0
        if steps:
            self.increment *= steps
            
        self.updateCurrSideLength()
        
        
        
    def calculateNext(self):
        """
        calculates the next position to which the metronome should move
        """     
        endX = self.startX
        endY = self.startY
        if self.side < 4:
            if self.side == 0:
                endX = self.startX + self.increment
                endY = self.startY + self.upSlope * self.increment
                #print"x:%s  y:%s slope:%s" % (endX, endY, self.slope) 
                if endX >= self.cornerX[1]:
                    endX = self.cornerX[1]
                    endY = self.cornerY[1]
                    self.side += 1
            elif self.side == 1:
                endX = self.startX - self.increment
                endY = self.startY + self.downSlope * self.increment
                #print"x:%s  y:%s slope:%s" % (endX, endY, self.slope) 
                if endX <= self.cornerX[2]:
                    endX = self.cornerX[2]
                    endY = self.cornerY[2]
                    self.side += 1
            elif self.side == 2:
                endX = self.startX - self.increment
                endY = self.startY - self.downSlope * self.increment
                #print"x:%s  y:%s slope:%s" % (endX, endY, self.slope) 
                if endX <= self.cornerX[3]:
                    endX = self.cornerX[3]
                    endY = self.cornerY[3]
                    self.side += 1      
            else:
                endX = self.startX + self.increment
                endY = self.startY - self.upSlope * self.increment 
                if endX >= self.cornerX[0]:
                    endX = self.cornerX[0]
                    endY = self.cornerY[0]
                    self.side += 1
                        
        # Check for cycle completion
        if self.side >= 4:  
            # For repeat
            self.cycle += 1
            self.side = 0
            self.updateCurrSideLength()
           
            
                       
        return endX, endY
    
   
   
        
    
               
               
                
            
