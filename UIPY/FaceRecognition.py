

import sys
from  PyQt5.QtWidgets import QApplication,QWidget
from  PyQt5.QtCore import QTimer
from PyQt5 import uic
from PyQt5.QtGui import QImage,QPixmap
import cv2
from PIL import Image
import os,json

class YuzKaydet(QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        uic.loadUi(r"UI\FaceRecognition.ui",self)
        self.btOpen.clicked.connect(self.KameraAc)
        self.btClose.clicked.connect(self.Kapat)
  

    def Kapat(self):
        try:
            self.cam.release()
        except:
            pass
        self.timer.stop()
        self.close()


    def KameraAc(self):
        if not self.timer.isActive():
            self.cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            self.timer.start(3)
            self.Gosterim()
        else:
            self.cam.release()
            self.timer.stop()

    def Gosterim(self):
        tani = cv2.face.LBPHFaceRecognizer_create()
        tani.read('trainer.yml')
        detector = cv2.CascadeClassifier("cascades\haarcascade_frontalface_default.xml")

        font = cv2.FONT_HERSHEY_SIMPLEX
        id = 0

        dictionary = {}
        names = []
        dosya = open('ids.json',"r")
        dictionary = json.load(dosya)
        for key,values in dictionary.items():
            names.append(key)
      
        while True:
            ret,frame = self.cam.read()
            frame = cv2.flip(frame,1)
           
            buyumeFaktor = 0.5
            frame = cv2.resize(frame,None,fx=buyumeFaktor,fy=buyumeFaktor,
            interpolation=cv2.INTER_AREA)
            gri = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gri,scaleFactor=1.3,minNeighbors=5)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                id,oran = tani.predict(gri[y:y+h,x:x+w])
                if oran>70:
                    id = names[id]
                cv2.putText(frame,str(id)+str(round(oran,2))+"%",(x+5,y-5),font,1,(255,255,255),2)
            heigth,width,channel = frame.shape
            step = channel*width
            qImg = QImage(frame.data,width,heigth,step,QImage.Format_BGR888)
            self.lbCamera.setPixmap(QPixmap.fromImage(qImg))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.cam.release()
        self.timer.stop()

    
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = YuzKaydet()
    ex.show()
    sys.exit(app.exec_())        
