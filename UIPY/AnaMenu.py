import sys
from  PyQt5.QtWidgets import QApplication,QMainWindow
from  PyQt5.QtGui import QIcon
from PyQt5 import uic 
from FaceRecognition import YuzKaydet
from FaceDetection import YuzTani
from Listofpeople import ListOfPeople

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.yuzKaydet = YuzKaydet()
        self.yuzTani = YuzTani()
        self.listofpeople = ListOfPeople()

    def initUI(self):
        uic.loadUi(r"UI\AnaMenu.ui",self)
        self.btYuzKaydet.clicked.connect(self.yuzKaydetAc)
        self.btYuzTani.clicked.connect(self.yuzTanimaAc)
        self.btKisiEkle.clicked.connect(self.listofAc)
        self.show()

    def yuzKaydetAc(self):
        self.yuzKaydet.show()

    def yuzTanimaAc(self):
        self.yuzTani.show()

    def listofAc(self):
        self.listofpeople.show()

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
        