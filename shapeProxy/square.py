from baseShape import baseShape
from common import windowHeight, windowLength

class Shape(baseShape):
    def __init__(self, steps=None):
        super(self.__class__, self).__init__()
        self.side = 0
        self.sideLength = windowHeight/2 + 100
        self.xmin = (windowLength - self.sideLength)/2
        self.ymin = (windowHeight - self.sideLength)/2
        self.xmax = (windowLength + self.sideLength)/2
        self.ymax = (windowHeight + self.sideLength)/2
        self.xSpan = self.xmax - self.xmin
        self.ySpan = self.ymax - self.ymin
        self.startX = self.xmin
        self.startY = self.ymin
        
        self.cornerX =[self.xmin,
                       self.xmax,
                       self.xmax,
                       self.xmin] 
        
        self.cornerY =[self.ymin,
                       self.ymin,
                       self.ymax,
                       self.ymax]
        
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
            if self.side % 2 == 0 :
                endX += self.increment
                if self.increment < 0 and \
                         endX <= self.xmin:
                    endX = self.xmin
                    self.side += 1
                    self.updateCurrSideLength()
                    if self.side == 2:
                        self.increment *= -1
                elif self.increment > 0 and \
                       endX >= self.xmax: 
                    endX = self.xmax
                    self.side += 1
                    self.updateCurrSideLength()
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
                        self.updateCurrSideLength()
                elif self.increment > 0 and \
                       endY >= self.ymax: 
                    endY = self.ymax
                    self.side += 1
                    if self.side == 2:
                        self.increment *= -1
                        self.updateCurrSideLength()
                        
        # Check for cycle completion
        if self.side >= 4:  
            # For repeat
            self.cycle += 1
            self.side = 0
            self.updateCurrSideLength()
            self.increment *= -1
            
                       
        return endX, endY
    
   
   
        
    
               
               
                
            
