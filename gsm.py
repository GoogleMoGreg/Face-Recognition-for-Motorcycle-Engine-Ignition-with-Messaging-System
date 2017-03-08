import serial
import RPi.GPIO as GPIO
import os, time
from gps import *
from time import *
import pyimgur



port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
CLIENT_ID = "35e99a18a53c221"
shawnNum = '9175488573'
gregNum = '9056075276'
laymarNum = '9276474165'
jonetNum = '9567427986'


def GSM_START():
    port.write('AT'+'\r\n')
    rcv = port.read(1)
    print rcv

    port.write('ATE0'+'\r\n')# Disable the Echo
    rcv = port.read(1)
    print rcv

    port.write('AT+CMGF=1'+'\r\n')# Select Message format as Text mode 
    rcv = port.read(10)
    print rcv


    port.write('AT+CMGL="ALL"'+'\r\n')# Select Message format as Text mode 
    rcv = port.read(10)
    print rcv

    return

def GSM_READSMS():
    port.write('AT+CMGL="REC UNREAD"'+'\r')# Select Message format as Text mode 
    rcv = port.readall()
    msg = rcv.split('\r\n')
    myList = [str(e) for e in msg]
    
    if len(myList)==8:
        output = myList[4]
        
    else:
        output = myList[2]
    if output == 'GO':
        port.write('AT+CMGDA="DEL ALL"\r\n')
        rcv = port.readall()
        print rcv
        print 'Deleting messages...'
    return output

def GSM_SENDPIC(path_file):
    print 'Sending pic...'
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(path_file, title ="Uploaded Intruder!")
    print (uploaded_image.title)
    MSG = uploaded_image.link
    print MSG

    port.write('AT+CMGF=1'+'\r\n')# Select Message format as Text mode 
    rcv = port.read(10)
    print rcv
    

    port.write('AT+CNMI=2,1,0,0,0'+'\r\n') # New SMS Message Indications
    rcv = port.read(10)
    print rcv
    
    # Sending a message to a particular Number
    port.write('AT+CMGS="'+shawnNum+'"'+'\r\n')
    rcv = port.read(10)
    print rcv
   

    port.write( str(MSG) +'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write("\nSomeone is trying to steal your ride..."+'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write("\x1A") # Enable to send SMS
    for i in range(10):
        rcv = port.read(10)
        print rcv
    print 'Successfully send a pic...'
        
    return

def GSM_GETLOC(latitude,longitude):
    port.write('AT+CMGS="'+shawnNum+'"'+'\r\n')
    rcv = port.read(10)
    print rcv
        
    print 'Sending location...'
        
    port.write('Your ride is located at:'+'\r\n')# Message
    rcv = port.read(10)
    print rcv
    
    #'''port.write('\nFor android users:\nhttps://www.google.com/maps/@'+str(latitude)+','+str(longitude)+',25z'+'\r\n')# Message
    #rcv = port.read(10)
    #print rcv'''


    port.write('\nFor iphone users:\nhttp://maps.apple.com/?q='+str(latitude)+','+str(longitude)+'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write("\x1A") # Enable to send SMS
    for i in range(10):
        rcv = port.read(10)
        print rcv

    print 'DELETING ALL MESSAGES...'
    port.write('AT+CMGDA="DEL ALL"\r\n')
    rcv = port.readall()
    print rcv

    return

def GSM_GETLOC_ENGINE_OFF(latitude,longitude):
    
    port.write('AT+CMGS="'+shawnNum+'"'+'\r\n')
    rcv = port.read(10)
    print rcv
        
    print 'Sending location...'

    port.write('Someone is stealing your ride...'+'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write('Your ride is located at:'+'\r\n')# Message
    rcv = port.read(10)
    print rcv
    
    #port.write('\nFor android users:\nhttps://www.google.com/maps/@'+str(latitude)+','+str(longitude)+',25z'+'\r\n')
    #rcv = port.readall(10)
    #print rcv


    port.write('\nFor iphone users:\nhttp://maps.apple.com/?q='+str(latitude)+','+str(longitude)+'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write("\x1A") # Enable to send SMS
    for i in range(10):
        rcv = port.read(10)
        print rcv

    print 'DELETING ALL MESSAGES...'
    port.write('AT+CMGDA="DEL ALL"\r\n')
    rcv = port.readall()
    print rcv

    return

def GSM_SUCCESS_REGISTER(person_name):

    port.write('AT+CMGS="'+shawnNum+'"'+'\r\n')
    rcv = port.read(10)
    print rcv
        
    print 'Success Verification...'
        
    port.write(person_name+' has been successfully registered!'+'\r\n')# Message
    rcv = port.read(10)
    print rcv
    

    port.write("\x1A") # Enable to send SMS
    for i in range(10):
        rcv = port.read(10)
        print rcv

    print 'DELETING ALL MESSAGES...'
    port.write('AT+CMGDA="DEL ALL"\r\n')
    rcv = port.readall()
    print rcv

    return

def GSM_NOTIF_SUCCESS(lat,lon):

    contact_person = [shawnNum,gregNum,laymarNum,jonetNum]

    #for index in range(len(contact_person)): 
    #contact_person[index-1]
    port.write('AT+CMGS="'+shawnNum+'"'+'\r\n')
    rcv = port.read(10)
    print rcv

    print 'Success Verification...'

    port.write('System all set...'+'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write('\nlatitude value: '+str(lat)+'\n'+'longitude value: '+str(lon)+'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write("\x1A") # Enable to send SMS
    for i in range(10):
        rcv = port.read(10)
        print rcv

    print 'DELETING ALL MESSAGES...'
    port.write('AT+CMGDA="DEL ALL"\r\n')
    rcv = port.readall()
    print rcv

    return

def GSM_NOTIF_DEBUG(e):

    contact_person = [shawnNum,gregNum,laymarNum,jonetNum]



    port.write('AT+CMGS="'+shawnNum+'"'+'\r\n')
    rcv = port.read(10)
    print rcv

    print 'Success Verification...'

    port.write('System crashed...'+'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write('\nError exception: '+str(e)+'\r\n')# Message
    rcv = port.read(10)
    print rcv

    port.write("\x1A") # Enable to send SMS
    for i in range(10):
        rcv = port.read(10)
        print rcv

    print 'DELETING ALL MESSAGES...'
    port.write('AT+CMGDA="DEL ALL"\r\n')
    rcv = port.readall()
    print rcv

    return


    
