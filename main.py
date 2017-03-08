import gpio
import time
import facerecog
import gsm
import gps_mod
import os
import cv2
import face_register
import trainer
import det_brightness
import engine_indicator


if __name__ == '__main__':
    restart = True
    is_running = True
    while restart == True:
        
        gpio.YELLOW_ON()
        gpio.FLASHLIGHT_ON()
        gpio.RED_ON()
        time.sleep(0.5)
        try:
            gsm.GSM_START()      
            while is_running:
                latitude,longitude =gps_mod.GPS_READ()
                print "latitude: "+str(latitude)
                print "longitude: "+str(longitude)
                
                if (latitude > 1.0 and longitude > 1.0) :
                    is_running = False
                    print "latitude: "+str(latitude)
                    print "longitude: "+str(longitude)
                    break
                    
                else:
                    is_running = True

                   
            gsm.GSM_NOTIF_SUCCESS(latitude,longitude) 
            gpio.FLASHLIGHT_OFF()
            gpio.YELLOW_OFF()
            gpio.RED_OFF()
            restart = False
        
        except Exception, e:
            restart = True
            print e
        
    while True:
        
        try:
            
            faceprint,id,predicted_conf,avgValue,image = facerecog.faceRecog()
            latitude,longitude =gps_mod.GPS_READ()
            buttonState = gpio.SWITCH()
            switch_state = gpio.MASTER_SWITCH()
            engine_state = gpio.ENGINE_SWITCH()
            output = gsm.GSM_READSMS()
            print 'Text Message: '
            if 'REG' in output:
                print 'Success...'
                name_list = output.split()
                print len(name_list)
                if len(name_list)==2 and name_list[0] == 'REG':
                    print 'Name: '+name_list[1]
                    person_name = name_list[1]
                    face_register.FACE_REGISTER(person_name)
                    gsm.GSM_SUCCESS_REGISTER(person_name)
                    print 'Saving to csv file...'
                    trainer.TRAIN_IMAGES()
                else:
                    print 'None...'
            
            if output == 'GO':
                print 'Engine start...'
                gpio.GREEN_ON()
                time.sleep(0.1)
                gpio.GREEN_OFF()
                gpio.FLASHLIGHT_OFF()

            if output == 'LOC':
                print 'Getting location...'
                gsm.GSM_GETLOC(latitude,longitude)

            if (switch_state == 'ON'):
                gpio.YELLOW_ON()
                print 'Switch state is '+switch_state
                if buttonState == 'ON':
                    gpio.FADE_YELLOW()
                    image_detect = 'debug.jpg'
                    if avgValue<4:
                        print 'Unlocked...'
                        print 'ID: '+id+',CONFIDENCE: '+str(predicted_conf)
                        print 'AVG. VALUE: '+str(avgValue)
                        gpio.FADE_YELLOW()
                        gpio.RED_OFF()
                        gpio.GREEN_ON()
                        time.sleep(0.5)
                        gpio.GREEN_OFF()
                        gpio.FLASHLIGHT_OFF()
                        engine_state = 'ON'

                
                    elif id == 'no name':
                        print faceprint
                        gpio.FADE_YELLOW()
                        gpio.RED_ON()
                        time.sleep(0.30)
                        gpio.RED_OFF()
                        time.sleep(0.30)
                        gpio.RED_ON()
                        time.sleep(0.30)
                        path_file = 'debug.jpg'
                        #gsm.GSM_SENDPIC(path_file)
                        gpio.RED_OFF()
                        time.sleep(0.30)

                    else:
                        print 'Not Registered'
                        print 'ID: '+id+',CONFIDENCE: '+str(predicted_conf)
                        print 'AVG. VALUE: '+str(avgValue)
                        gpio.FADE_YELLOW()
                        gpio.GREEN_OFF()
                        gpio.RED_ON()
                        img_no = img_no = sorted([int(fn[:fn.find('.')])for fn in os.listdir('unknowns')if fn[0]!='.']+[0])[-1]+1
                        path_file =  os.path.join('unknowns','%d.'%img_no+'Intruder.jpg')
                        cv2.imwrite(path_file,image)
                        gsm.GSM_SENDPIC(path_file)
                        time.sleep(0.5)
                        gpio.RED_OFF()
                    #det_brightness.DETECT_BRIGHTNESS(image_detect)
                    

                elif (engine_state == 'OFF'):
                        print 'Engine is '+ engine_state
                        while True:
                            switch_state = gpio.MASTER_SWITCH()
                            lat,lon = gps_mod.GPS_READ()
                            if lat or lon < 0 :
                                break
                            elif switch_state ==  'ON':
                                break
                        init_lat,init_lon = gps_mod.GPS_READ()
                    
                        while True:
                            output = gsm.GSM_READSMS()
                            switch_state = gpio.MASTER_SWITCH()
                            last_lat,last_lon = gps_mod.GPS_READ()
                            buttonState = gpio.SWITCH()
                            engine_state = gpio.ENGINE_SWITCH()
                            print 'Engine state is '+engine_state
                            m = gps_mod.GPS_ENGINE_OFF(init_lon,init_lat,last_lon,last_lat)
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
                                
                            if (engine_state == 'ON'):
                                break
                            
                            elif(buttonState == 'ON'):
                                break
                            
                            elif(switch_state == 'OFF'):
                                gpio.YELLOW_OFF()
                                gpio.RED_OFF()
                                gpio.FLASHLIGHT_OFF()
                                gpio.GREEN_OFF()
                                break
                                    
                            elif output == 'GO':
                                print 'Engine start...'
                                gpio.GREEN_ON()
                                time.sleep(0.5)
                                gpio.GREEN_OFF()
                                gpio.FLASHLIGHT_OFF()
                            
                            elif 'REG' in output:
                                print 'Success...'
                                name_list = output.split()
                                print len(name_list)
                                if len(name_list)==2 and name_list[0] == 'REG':
                                    print 'Name: '+name_list[1]
                                    person_name = name_list[1]
                                    face_register.FACE_REGISTER(person_name)
                                    gsm.GSM_SUCCESS_REGISTER(person_name)
                                    print 'Saving to csv file...'
                                    trainer.TRAIN_IMAGES()
                                    break

            if (switch_state == 'OFF'):
                   
                        gpio.YELLOW_OFF()
                        gpio.RED_OFF()
                        gpio.FLASHLIGHT_OFF()
                        gpio.GREEN_OFF()
                        print 'Master switch is off...'
                        print 'Engine is '+ engine_state
                        while True:
                            switch_state = gpio.MASTER_SWITCH()
                            lat,lon = gps_mod.GPS_READ()
                            if lat or lon < 0 :
                                break
                            elif switch_state ==  'ON':
                                break
                        init_lat,init_lon = gps_mod.GPS_READ()
                    
                        while True:
                                output = gsm.GSM_READSMS()
                                switch_state = gpio.MASTER_SWITCH()
                                last_lat,last_lon = gps_mod.GPS_READ()
                                m = gps_mod.GPS_ENGINE_OFF(init_lon,init_lat,last_lon,last_lat)
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
                                if (switch_state == 'ON'):
                                    break
   
             
        except Exception, e:
            print e
            gsm.GSM_NOTIF_DEBUG(e)
            gpio.RED_OFF()
            
                        
