from math import cos, acos, sin, asin, radians, degrees
from robotProxy import baseProxy
from common import (
                    thread_lock                    
                    )

ROLL_MIN = radians(-11.0)
RADIUS_BY_ARM = 2.0 / 10.0
ROLL_CORRECT = ROLL_MIN + asin(RADIUS_BY_ARM)

class circleProxy(baseProxy):
    def __init__(self, xSpanCm, ySpanCm, synchTime, armOpt="R"):
        super(self.__class__, self).__init__(xSpanCm, 
                                             ySpanCm, 
                                             synchTime,
                                             armOpt)
       

        self.armPitch = self.pitchMin + (0.5 * self.pitchSpan)
        self.armRoll = self.rollMin

