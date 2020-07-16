from common import thread_lock                    
from math import cos, acos, sinh, sin, asin, radians
#from multiprocessing.managers import BaseProxy
from robotProxy import baseProxy


class squareProxy(baseProxy):
    def __init__(self, xSpanCm, ySpanCm, synchTime):
        super(self.__class__, self).__init__(xSpanCm, ySpanCm, synchTime)
                 
        self.armPitch = self.pitchMin
        self.armRoll = self.rollMin
 
            
        
        
        
