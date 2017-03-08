import os
from gps import *
from time import *
import time
import threading
from math import radians,cos,sin,asin,sqrt


gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
os.system('clear') #clear the terminal (optional)


class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

  def run(self):
    while True:
      gpsd.next()

def GPS_READ():
      #gpsp = GpsPoller()
      #gpsp.start()
      #lattitude = gpsd.fix.latitude
      #longitude = gpsd.fix.longitude
      lattitude = 14.5878346
      longitude = 120.9845951
      time.sleep(1)


      return lattitude,longitude

def GPS_ENGINE_OFF(init_lon,init_lat,last_lon,last_lat):
    lon1,lat1,lon2,lat2 = map(radians,[init_lon,init_lat,last_lon,last_lat])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    time.sleep(1)
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    new_val = abs(a)
    print 'a value: '+str(new_val)
    c = 2 * asin(sqrt(new_val))
    km = 6371 * c

    m = km
    return m
