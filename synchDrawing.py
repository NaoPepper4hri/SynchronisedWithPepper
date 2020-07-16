import argparse
import logging
import os
import sys
import time
from common import windowHeight, windowLength
from datetime import datetime
from importlib import import_module
from Tkinter import Tk
from blindSetup import asynchList, synchList


SINGLE_SCREEN = False #True

def add_logger(log_path, config_file=None):
    
    logger = logging.getLogger("DrawInSynch")
    logger.setLevel(logging.INFO)
    filename = "DrawInSynch_%s.log" % (datetime.now().strftime("%H%M%S_%d%m%Y"))
    filePath = os.path.join(log_path, filename)
    
    # create error file handler and set level to info
    handler = logging.FileHandler(os.path.join(log_path, filename),"w", encoding=None, delay="true")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    
    # add file handler to log
    logger.addHandler(handler)
    if config_file:
        logger.info("Using config : %s" % config_file)
    return logger

def get_arguments():
    shapeChoices = ['circle',
                    'oval',
                   'square']
    
    configParam = {"userShape": None,
                   "robotShape": None,
                   "practice":False,
                   "robotIP:":"192.168.1.193",
                   "port":9559,
                   "repeats":1,
                   "logger":None,
                   "participantID":None}
    log_path = None
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.193", help="Robot ip address [NOT BEING USED]")
    parser.add_argument("--port", type=int, default=9559, help="Robot port number [NOT BEING USED]")
    parser.add_argument("--participantNumber", type=int, default=0,
                         help="Participant number is required in non practice mode to blind-select asynch/synch drawing with same shape") 
    parser.add_argument("--shape", type=str, choices=shapeChoices, required=True, 
                        help="Shape that Participant must draw")
    
    parser.add_argument("--robotShape", type=str, default="", choices=shapeChoices, required=False, 
                        help="Define Asynchronous shape for Robot, even if it is same as participant.\n Absence implies synchronous mode if participant number is not provided or invalid.")
    parser.add_argument("--repeats", type=int, default=3, required=False, 
                        help="Number of times the participant has to repeat the shape")
    parser.add_argument("--practice", type=bool, nargs='?', const=True, default=False,    
                        help="Activate practice round without robot.")
    parser.add_argument("--log", type=str, default="./logs", 
                        help="Entire log directory path. The filename is defined by the code")
    args = parser.parse_args()
    
    # Check log option entered and directory
   
    log_path = args.log
    
    if not log_path  or not os.path.isdir(log_path):
        print("Please create the log directory '%s' on your system." % log_path)
        print("If you want to log at an alternative location use --log=<log_path> to enter it")
        exit(0)
    else:
        if args.participantNumber:
            log_path = os.path.join(log_path, '%s' % args.participantNumber)
            if not os.path.isdir(log_path):
                os.mkdir(log_path)
        configParam["logger"] = add_logger(log_path)     
        
    # Check shape to draw and get module prefix
    configParam["userShape"] = args.shape.lower()
    if configParam["userShape"]=="semicircle":
        configParam["userShape"] = "semiCircle"
    
    if args.robotShape:
        configParam["robotShape"] = args.robotShape.lower()
        if configParam["robotShape"]=="semicircle":
             configParam["robotShape"] = "semiCircle"
             
    if not args.practice and not args.participantNumber>0:
        print("EXPERIMENT MODE!!!: Participant number is required in non-practice mode")
        exit(0)
             
    if args.participantNumber:
        if args.participantNumber in synchList:
            configParam["robotShape"] = None
            configParam["participantID"] = args.participantNumber
        elif args.participantNumber in asynchList:
            configParam["robotShape"] = configParam["userShape"]
            configParam["participantID"] = args.participantNumber
        else:
            print("WARNING!!!: participant number provided has not been setup for blinding. \n")
            print("We will use the commandline as provided.")    
             
    if args.practice:
        configParam["practice"] = True
        
    configParam["robotIP"] = args.ip
    configParam["port"] = args.port
    configParam["repeats"] = args.repeats  
    
        
    return configParam
    


def startExperiment(configParam):    
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    if SINGLE_SCREEN:
        screen_height = 0
    
    #print "width %s, height %s" % (screen_width, screen_height)
    canvasName = "%sCanvas" % configParam["userShape"]
    moduleName = "screen.%sWindow" % configParam["userShape"]
    
    shapeCanvasModule = import_module(moduleName)
    exCanvas = getattr(shapeCanvasModule, canvasName)
    ex = exCanvas(configParam)    
    try:
        root.geometry("%sx%s+%s+%s" % (windowLength, 
                                       windowHeight, 
                                       0,
                                       screen_height))
        root.resizable(0, 0)
        root.bind('<Motion>', ex.motion)
        root.bind('<ButtonRelease-1>', ex.pointerClick)
        root.bind('<Escape>', ex.stopExcercise)
        #ex.startExercise()
        root.mainloop()
    finally:
        try:
            ex.stopExcercise()
        except:
            pass
        
    
    
if __name__ =='__main__':
    configParam = get_arguments()
    startExperiment(configParam)