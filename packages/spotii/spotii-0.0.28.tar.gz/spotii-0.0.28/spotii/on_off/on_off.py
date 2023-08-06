import subprocess
import threading
from gpiozero import Button

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from define import *
#from .takePhoto import takePhoto
powerButton = Button(POWER_BUTTON_PIN,True,None,None,POWER_BUTTON_HOLD_TIME)
def shutDown():
    print("shut down now")
    subprocess.Popen(['shutdown','-h','now'])

class OnOffThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run (self):
        powerButton.when_held=shutDown #takePhoto
            
