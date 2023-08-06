from gpiozero import Button
from gpiozero import LED
import time

import sys
# sys.path.append('/home/pi/gxf/python/spotii')
# sys.path.append('/home/pi/gxf/python/spotii/on_off')

from spotii.define import *


#powerButton = Button(define.POWER_BUTTON_PIN,True,None,None,define.POWER_BUTTON_HOLD_TIME)

if __name__ == "__main__":

    hub_reset=LED(HUB_RST_PIN)
    hub_reset.off()
    time.sleep(0.001)
    hub_reset.on()
    
    
