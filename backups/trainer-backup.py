import os
import cv2
import numpy as np
import PIL
from PIL import Image

recognizer = cv2.createLBPHFaceRecognizer()
path = 'data-creator'

def getImages(path):
        imagesPaths = [os.path.join(path,f)
        for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagesPaths:
                faceImg = Image.open(imagePath).convert('L')
                faceNP = np.array(faceImg,'uint8')
                ID = int(os.path.split(imagePath)[-1].split('.')[1])
                faces.append(faceNP)
                print ID
                IDs.append(ID)
                print 'Training images... '+str(ID)
        return IDs,faces

Ids,faces = getImages(path)
recognizer.train(faces,np.array(Ids))
recognizer.save('recognizer/trainingData.yml')
print 'Successfully trained images...'
