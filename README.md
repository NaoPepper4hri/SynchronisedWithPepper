# Synchronised Movement (Drawing) With Pepper
In this setup participants would be following the movement of a target metronome along a circular path with a digital pen on a drawing tablet. A Pepper robot would be stood next to the participant also making the drawing movement synchronysed with the metronome. This is for the purpose of achieving orchastrated synchrony. The aim was to see if synchronous movement could predict social liking in line with social synchrony.

For the experiment setup a set number of participants were to have Pepper synchronizing to their drawing while others were to be drawing in an asyncronous manner to the metronome. The participant number was used to predetermine the condition the participant was going to get. The list was stored in the blindSetup.py so the experimentor did not know the condition that a participant in case the influence their decision inadvertently. The blinding list can be created using the randomList.py script.

The batch file experimen.bat needs to be run with the participant number to take the participant through the practice mode and the experiment blocks and rest.

## Requirement
Python 2.7(32-bit) installed with pynaoqi as instructed by [Aldebaran](http://doc.aldebaran.com/2-5/dev/python/install_guide.html)
Nao or Pepper robot. 
Change the IP address in robotProxy.py to the robot's IP
