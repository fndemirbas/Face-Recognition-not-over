import os
class Tools():
    def __init__(self,yol):
        self.curDir = os.getcwd()
        self.yol = yol

    def openFolder(self,isim):
        os.chdir(self.yol)
        os.mkdir(isim)
        os.chdir(self.curDir)
