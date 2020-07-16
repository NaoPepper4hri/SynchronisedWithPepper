from math import sqrt

class baseShape(object):
    def __init__(self):
        self.increment = 8.0
        self.varInc = 0.0
        self.xmin = None
        self.ymin = None
        self.xmax = None
        self.ymax = None
        self.xSpan = None
        self.ySpan = None
        self.startX = None
        self.startY = None
        self.cornerX =[]
        self.cornerY = []
        self.side = 0
        self.currSideLengtth = 0
        self.cycle = 1
        
    def doInitialLogs(self, logger, ppCm, updateTime, shapeFor="Canvas"):
        logger.info("%s Shape Minimum X coordinates point: %s" % (shapeFor,
                                                                      self.xmin))
        logger.info("%s Shape Maximum X coordinates point: %s" % (shapeFor,
                                                                      self.xmax))
        logger.info("%s Shape Minimum Y coordinate point: %s" % (shapeFor,
                                                                      self.ymin))
        logger.info("%s Shape Maximum Y coordinate point: %s" % (shapeFor,
                                                                      self.ymax))
        endPoint = len(self.cornerX)
        if endPoint:
            logger.info("%s Shape  Number of corners: %s" % (shapeFor,
                                                             endPoint))
            i = 0
            for items in self.cornerX:
                logger.info("%s Shape Corner %s (x,y) coordinate: (%s, %s)" % (shapeFor,
                                                                        i+1,
                                                                        self.cornerX[i],
                                                                        self.cornerY[i]))
                i += 1
            
            
            i = 0
            while i<endPoint:
                j = (i + 1) % 4
                Xdiff = (self.cornerX[j] - self.cornerX[i])
                Ydiff = (self.cornerY[j] - self.cornerY[i])
                logger.info("%s Shape Length of side %s: %s cm" % (shapeFor,
                                                                      i+1,
                                                           sqrt(Xdiff*Xdiff + Ydiff*Ydiff)/ppCm))
                i += 1
                
            update_rate = (self.increment*1000.00)/(ppCm*updateTime)
            logger.info("%s UpdateSpeed: %s cm/sec" % (shapeFor,
                                                      update_rate))
        
        
    def accelerate(self):
        pass
    
    def updateCurrSideLength(self):
        nextSide = (self.side + 1) % 4
        Xdiff = self.cornerX[nextSide] - self.cornerX[self.side]
        Ydiff = self.cornerY[nextSide] - self.cornerY[self.side]
        
        self.currSideLength = sqrt(Xdiff*Xdiff + Ydiff*Ydiff)
    
        
    def getRelativeXY(self, endX, endY):
         xFrac = float(endX - self.xmin)/float(self.xSpan)
         yFrac = float(endY - self.ymin)/float(self.ySpan)
         
         return xFrac, yFrac
     
    def updateCurrPoint(self, endX, endY):
        self.startX = endX
        self.startY = endY
        
    def getCoverage(self):
        Xdiff = self.startX - self.cornerX[self.side]
        Ydiff = self.startY - self.cornerY[self.side]
        distanceMoved = sqrt(Xdiff*Xdiff + Ydiff*Ydiff)
        coveragePercent = (distanceMoved*100.00)/self.currSideLength
        
        coverageString = "Cycle: %s, Side: %s, SideProgress: %s" % (self.cycle,
                                                                    self.side + 1,
                                                                    coveragePercent)
        return coverageString 
        
    
        