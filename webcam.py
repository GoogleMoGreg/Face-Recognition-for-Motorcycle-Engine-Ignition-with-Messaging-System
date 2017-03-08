import time
from subprocess import call
import cv2

def camera():
    
    call(["fswebcam","-r","600x600","--no-banner",
      "/home/pi/BAK/LBH_METHOD_WEBCAMERA/debug.jpg"])
    image =   "debug.jpg"
    return image

