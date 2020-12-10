

import sys
import os
sys.path.append(os.getcwd() + os.sep+ "DB")
from  PyQt5.QtWidgets import QApplication,QWidget
from  PyQt5.QtCore import QTimer
from PyQt5 import uic
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.Qt import Qt
import cv2
from DB import DBTool
import numpy as np

class YuzTani(QWidget):
    def __init__(self):
        super().__init__()
        self.sayac = 0
        self.yol = ""
        self.timer = QTimer()
        self.db = DBTool(dbAdres=r"DB\facedb.db",tabloAdi="")
        uic.loadUi(r"UI\FaceDetection.ui",self)
        self.kisilerDoldur()
        self.btOpen.clicked.connect(self.KameraAc)
        self.btClose.clicked.connect(self.Kapat)
        self.btTake.clicked.connect(self.getImage)
        self.cmbkisiler.currentIndexChanged.connect(self.klasor)
        self.btEgit.clicked.connect(self.egitim)
    
    def kisilerDoldur(self):
        self.cmbkisiler.addItem("Seçiniz")
        self.db.tabloAdi = "FACES"
        self.kisiler = self.db.select()
        for item in self.kisiler:
            self.cmbkisiler.addItem(item[1])

    def Kapat(self):
        try:
            self.cam.release()
        except:
            pass
        self.timer.stop()
        self.close()

    def klasor(self):
        try:
            self.sayac=0
            isim = self.cmbkisiler.currentText()
            if isim != "Seçiniz":
                os.mkdir("DATASET"+os.sep+isim)
        except:
            pass
        finally:
            if isim != "Seçiniz":
                self.yol = "DATASET"+os.sep+isim


    def egitim(self):
        import cv2
        import os
        sys.path.append(os.getcwd() + os.sep+ "DATASET")
        import numpy as np
        from PIL import Image
        import os,json


        yol = "DATASET"
        tani = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(r"cascades\haarcascade_frontalface_default.xml")

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


    def KameraAc(self):
        if not self.timer.isActive():
            self.cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
            self.timer.start(3)
            self.Gosterim()

        else:
            self.cam.release()
            self.timer.stop()

    def Gosterim(self):
        while True:
            ret,frame = self.cam.read()
            buyumeFaktor = 0.4
            frame = cv2.resize(frame,None,fx=buyumeFaktor,fy=buyumeFaktor,
            interpolation=cv2.INTER_AREA)

            heigth,width,channel = frame.shape
            step = channel*width
            qImg = QImage(frame.data,width,heigth,step,QImage.Format_BGR888)
            self.lbCamera.setPixmap(QPixmap.fromImage(qImg))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self.cam.release()
        self.timer.stop()

    def getImage(self):
        pix = self.lbCamera.pixmap()
        import io
        from PIL import Image
        from PyQt5.QtGui import QImage
        from PyQt5.QtCore import QBuffer
        
        img = pix.toImage()
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)
        img.save(buffer, "JPG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        pil_im.save(f"{self.yol}{os.sep}{self.sayac}.jpg")
        self.sayac+=1
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = YuzTani()
    ex.show()
    sys.exit(app.exec_())        
