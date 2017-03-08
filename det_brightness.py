import cv2
from PIL import Image,ImageStat
import gpio

def DETECT_BRIGHTNESS(image):
    print 'Opening image...'
    im = Image.open(image).convert('L')
    bright_value = ImageStat.Stat(im)
    print bright_value.rms[0]
    
    if(bright_value.rms[0]<30):
        #print 'Opening flashlight...'
        gpio.FLASHLIGHT_ON()
    else:
        #print 'Closing flashlight...'
        gpio.FLASHLIGHT_OFF()
        
    return
