import argparse
from common import windowHeight, windowLength
from screen.msgWindow import msgWindow
from Tkinter import Tk

from synchDrawing import SINGLE_SCREEN
import webbrowser
import psutil
import time
#https://bangor.onlinesurveys.ac.uk/test_1-2

def get_arguments():
    """
    pareses the arguments provided
    """
    configParam = {"message": None,
                   "canContinue": False,
                   "participantNumber" : "",
                   "questionnaire1": None,
                   "questionnaire2": None}
    log_path = None
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--msg", type=str, default="",
                         help="The message to show on screen")
    parser.add_argument("--showContinue", type=bool, nargs='?', const=True, default=False,    
                        help="Participant is shown a continue button to click and progress when they are ready")
    parser.add_argument("--participantNumber", type=int,
                         help="Participant number")
    parser.add_argument("--questionnaire1", type=str, default="",
                         help="Optional questionnaire")
    parser.add_argument("--questionnaire2", type=str, default="",
                        help="Optional additional questionnaire")
    
    args = parser.parse_args()
    
    configParam["message"] = args.msg 
             
    if args.showContinue:
        configParam["canContinue"] = True
        
    configParam["participantNumber"] = args.participantNumber
    
    if args.questionnaire1:
        configParam["questionnaire1"] = args.questionnaire1
        
    if args.questionnaire2:
        configParam["questionnaire2"] = args.questionnaire2
    
        
    
    return configParam
    
def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    liveFire = None
    for p in psutil.process_iter(attrs=['name']):
        if p.info['name'] == name:
            liveFrire = p
            break;
    return liveFire


def showScreen(configParam):    
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    if SINGLE_SCREEN:
        screen_height = 0
    
    ex = msgWindow(configParam)    
    try:
        root.geometry("%sx%s+%s+%s" % (windowLength, 
                                       windowHeight, 
                                       0,
                                       screen_height))
        root.resizable(0, 0)
        root.protocol("WM_DELETE_WINDOW", ex.disable_event)
        if not configParam["canContinue"]:
            root.bind('P', ex.close_window)
            
       
        if configParam["questionnaire1"]:
            print "Opening questionnaire 1:"
            url1 = configParam["questionnaire1"] + "?token=%s&xx" % configParam["participantNumber"]
	    wb = webbrowser.get('C:/Program Files/Mozilla Firefox/firefox.exe %s')
            wb.open_new(url1)
            time.sleep(3)
            liveFirefox = find_procs_by_name('firefox.exe')
            while liveFirefox:
                print "Found a live firefox running"
                liveFirefox.wait()
                liveFirefox = find_procs_by_name('firefox.exe')
            print "Questionnaire 1 closed"
                
        if configParam["questionnaire2"]:
            print "Opening questionnaire 2:"
	    url2 = configParam["questionnaire2"] + "?token=%s&xx" % configParam["participantNumber"]
            wb = webbrowser.get('C:/Program Files/Mozilla Firefox/firefox.exe %s')
            wb.open_new(url2)
            time.sleep(3)
            liveFirefox = find_procs_by_name('firefox.exe')
            while liveFirefox:
                print "Found a live firefox running"
                liveFirefox.wait()
                liveFirefox = find_procs_by_name('firefox.exe')
            print "Questionnaire 2 closed"
        
        root.mainloop()
    finally:
        pass
        
    
    
if __name__ =='__main__':
    configParam = get_arguments()
    showScreen(configParam)
    