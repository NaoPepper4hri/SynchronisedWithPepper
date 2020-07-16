from drawingWindow import shapeWindow
from shapeProxy.square import Shape as canvasShape
from Tkinter import  BOTH
from robotProxy.squareRobot import squareProxy as RobotProxy


class squareCanvas(shapeWindow):
    def __init__(self, configSettings):
        # update the drawingWindow
        super(self.__class__, self).__init__("Square", 
                                             configSettings["repeats"],
                                             configSettings["logger"])
        # setup the canvas
        self.initUI(configSettings)
        
    def initUI(self, configSettings):
        #define the shape to drawn on the canvas
        self.shape = canvasShape()
        robotShape = configSettings["robotShape"]
        practice = configSettings["practice"]
                
        # if the robot has to draw a different shape
        # load that
        if robotShape:
            steps = 1.0
            if robotShape == "square":
                steps = 2.75
            self.loadAsynchShape(robotShape,
                                 steps = steps,
                                 practice=practice)
            
        elif not practice:
            # The default drawing robot for synchronised drawing
            # the same shape as the one on the canvas
            self.logger.info("Running experiment synchronous mode")
            self.robot = RobotProxy(self.shape.xSpan/self.pointsPerCm,
                                    self.shape.ySpan/self.pointsPerCm,
                                    float(self.updateTime)/1000.0)  
        else:
            self.logger.info("Running practice synchronous mode")
        
        self.logger.info("Shape selected : Square")
        self.doInitialLogs(configSettings["participantID"])       
        
        # draw the shape on the canvas
        self.canvas.create_rectangle(self.shape.xmin, 
                                     self.shape.ymin, 
                                     self.shape.xmax, 
                                     self.shape.ymax, 
                                     dash=(4, 2), 
                                     outline="black")
        # move the metronome to the starting point
        self.locateMetronome()
        self.canvas.pack(fill=BOTH, expand=1)
        
        # Check and start the robot to get the robot hand in start position
        self.startRobot()
        
        

            
