import cv2
import os
import sys
sys.path.append(os.getcwd() + os.sep+ "DATASET")
import numpy as np
from PIL import Image
import os,json


yol = "DATASET"
tani = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("cascades\haarcascade_frontalface_default.xml")

def getImageAndLabels(yol):
    faceSamples = []
    ids = []
    labels = []
    folders = os.listdir(yol)
    dictionary = {}

    for i,kl in enumerate(folders):
        dictionary[kl]=int(i)

    f = open("ids.json","w")
    a = json.dump(dictionary,f)
    f.close()

    for kl in folders:
        for res in os.listdir(os.path.join(yol,kl)):
            PIL_img = Image.open(os.path.join(yol,kl,res)).convert('L')
            img_numpy = np.array(PIL_img,'uint8')
            id = int(dictionary[kl])
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
    return faceSamples,ids


faces,ids = getImageAndLabels(yol)
tani.train(faces,np.array(ids))
tani.write('trainer.yml')