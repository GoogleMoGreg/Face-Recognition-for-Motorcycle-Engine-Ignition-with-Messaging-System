import cv2
import cv2.cv as cv
import numpy as np
import webcam
from os import listdir

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

sub = 0
images,labels = [],[]
people = []
path = 'data-creator'
for subdir in listdir(path):
    for image in listdir(path+"/"+subdir):
        img=cv2.imread(path+"/"+subdir+"/"+image,cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img,(256,256))

        images.append(np.asarray(img,dtype=np.uint8))
        labels.append(sub)
    people.append(subdir)
    sub+=1
labels = np.asarray(labels,dtype = np.int32)
recognizer = cv2.createLBPHFaceRecognizer()
recognizer.train(images,labels)

print 'Successfully loaded data...'

def faceRecog():
    cap = webcam.camera()
    image = cv2.imread(cap)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray,
                                        scaleFactor = 1.3,
                                        minNeighbors = 4,
                                        minSize = (30,30),
                                        flags=cv.CV_HAAR_SCALE_IMAGE)
    if len(faces)>0:
        faceprint = 'Face detected...'
        for(x,y,w,h) in faces:
            new_image = gray[y:y+h,x:x+w]
            #new_image = cv2.equalizeHist(new_image)
            new_image = cv2.resize(new_image,(256,256))
            cv2.imwrite('debug_crop.jpg',new_image)
            predict_label,predicted_conf = recognizer.predict(np.asarray(new_image))
            avg_conf = predicted_conf*.100
            id = people[predict_label]
    else:
        faceprint = 'No face detected...'
        id = 'no name'
        predicted_conf = '10000'
        avg_conf = '10000'
 

    return faceprint,id,predicted_conf,avg_conf,image
        
