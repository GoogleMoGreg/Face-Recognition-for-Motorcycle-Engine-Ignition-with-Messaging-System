import gps_mod
import gsm
import gpio
import time
def ENGINE_STATE(engine_state):
    print 'Engine state is '+engine_state
    if engine_state == 'OFF':
        while True:
                           
            lat,lon = gps_mod.GPS_READ()
            if lat or lon < 0 :
                    break
            elif engine_state ==  'ON':
                break
                
        init_lat,init_lon = gps_mod.GPS_READ()
        print 'Engine state is '+ engine_state

        
        while True:
                button_state = gpio.SWITCH()
                switch_state = gpio.MASTER_SWITCH()
                output = gsm.GSM_READSMS()
                last_lat,last_lon = gps_mod.GPS_READ()
                m = gps_mod.GPS_ENGINE_OFF(init_lon,init_lat,last_lon,last_lat)
                gpio.YELLOW_ON()
                print 'init lat: ' + str(lat)+'\ninit lon: '+ str(lon)
                print 'last lat: ' + str(last_lat) +'\nlast lon:'+str(last_lon)
                print 'meter value: '+str(m)
                
                if output == 'LOC':
                    print 'Getting location...'
                    gsm.GSM_GETLOC(latitude,longitude)
                
                if m>0.02:
                    print 'Someone is stealing your ride...'
                    gsm.GSM_GETLOC_ENGINE_OFF(last_lat,last_lon)
                    time.sleep(0.05)
                    
                elif m>0.05:
                    print 'Someone is stealing your ride (check distance)...'
                    gsm.GSM_GETLOC_ENGINE_OFF(last_lat,last_lon)
                    time.sleep(0.05)
                if button_state == 'ON':
                    break
                if switch_state == 'OFF':
                    print 'engine is '+ switch_state
                    engine_state = 'OFF'
                if output == 'GO':
                    print 'Engine start...'
                    gpio.GREEN_ON()
                    time.sleep(0.5)
                    gpio.GREEN_OFF()
                    gpio.FLASHLIGHT_OFF()
                    engine_state = 'ON'
                    break
                
    return engine_state
