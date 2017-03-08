import webcam
import numpy as np
import cv2

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
img_path = 'data-creator/User.'
id = raw_input("Enter name: ")
sampleNum = 0

while 1:
    capture = webcam.camera()
    image = cv2.imread(capture)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray,1.1,4)
    if len(faces)>0:
        print 'Face detected...'
        for(x,y,w,h) in faces:
            sampleNum +=1
            save_image = gray[y:y+h,x:x+w]
            cv2.imwrite(img_path+str(id)+'.'+str(sampleNum)+'.jpg',save_image)
        if sampleNum>20:
            break
    else:
        print 'No face detected...'
    




