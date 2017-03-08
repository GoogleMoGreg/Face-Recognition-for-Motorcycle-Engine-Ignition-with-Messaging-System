import cv2
import numpy as np
import webcam

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load("recognizer/trainingData.yml")
print 'Successfully loaded data...'

id = 0
numConf = []
index = 0
while True:
    cap = webcam.camera()
    image = cv2.imread(cap)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray,1.1,4)
    if len(faces)>0:
        print 'face detected...'
        for(x,y,w,h) in faces:
            new_image = gray[y:y+h,x:x+w]
            id,conf = recognizer.predict(new_image)
            avgValue = conf*.100
            print 'Confidence is:'+str(conf)
            print 'ID: '+str(id)+' CONFIDENCE: '+str(avgValue)
    else:
        print 'no face detected...'
