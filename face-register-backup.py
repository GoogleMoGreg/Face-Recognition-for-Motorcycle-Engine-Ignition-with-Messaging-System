import webcam
import numpy as np
import cv2.cv as cv
import cv2
import os
import crop_face
from PIL import Image

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
img_path = 'data-creator'
person_name = raw_input("Enter name: ")
path_join = os.path.join(img_path,person_name)
if not os.path.isdir(path_join):
    os.mkdir(path_join)
sampleNum = 0

while 1:
    capture = webcam.camera()
    image = cv2.imread(capture)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray,
                                        scaleFactor = 1.3,
                                        minNeighbors = 4,
                                        minSize = (30,30),
                                        flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(faces)>0:
        print 'Face detected...'
        for(x,y,w,h) in faces:
            sampleNum +=1
            save_image = gray[y:y+h,x:x+w]
            #save_image = cv2.equalizeHist(save_image)
            save_image = cv2.resize(save_image,(256,256))
            cv2.imwrite('data-creator/'+person_name+'/'+person_name+'.'+
                        str(sampleNum)+'.jpg',save_image)
            
        if sampleNum>9:
            break
    else:
        print 'No face detected...'
    




