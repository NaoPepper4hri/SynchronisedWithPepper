from Tkinter import Tk, Canvas, Frame, BOTH, Button,Label
from common import windowLength, windowHeight
from Tkconstants import BOTTOM

class msgWindow(Frame, object):
    def __init__(self, configSettings):
        super(msgWindow, self).__init__()
        self.master.title("")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, 
                             width=windowLength,
                             height=windowHeight - 300)
        self.canvas.grid(row=0, column=0)
        self.msgText = self.canvas.create_text(windowLength/2,
                                               (windowHeight-100)/2,
                                               font=("Arial", 15),
                                               text=configSettings['message'],
                                               fill="blue")
        
        
               
        self.button = None
        if configSettings['canContinue']:
            self.button = Button(self, 
                                  text ="Continue", 
                                  font=("Arial", 15),
                                  background="white",
                                  activebackground="green",
                                  bd=5,
                                  command = self.close_window)
            self.button.grid(row=2, column=0)
            #self.button.config(highlightbackground="blue")
            self.acceptOnCommandLine = False
        else:
            self.acceptOnCommandLine = True
            self.master.after(500, self.update)
            print("------- EXPERIMENTOR EXPLANATION REQUIRED -------")
            print("To continue to next part press capital P and then press Enter. Note that current window needs to be")
            print("on either the command window or the participant's drawing window when inputting 'P'. But the")
            print("'Enter-key' has to be pressed on the command line window.")
            
            
        self.canvas.pack(fill=BOTH, expand=0)
        if self.button:
            self.button.pack()
        
        
    def update(self):
        check = ''
        while check != 'P' and self.acceptOnCommandLine:
            check = raw_input("To continue to next part press capital P and Enter:")
        
        if self.acceptOnCommandLine:
            self.close_window()
            
            
    def disable_event(self, event=None):
        pass
    
        
    def close_window(self, event=None):
        self.acceptOnCommandLine = False
        self.master.destroy()
        
        