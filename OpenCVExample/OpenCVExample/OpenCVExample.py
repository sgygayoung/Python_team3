from PyQt4 import uic,QtGui,QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import numpy as np
import cv2
import sys

form_class = uic.loadUiType("mainframe.ui")[0]                 # Load the UI
class Form(QtGui.QMainWindow, form_class):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.FileButton.clicked.connect(self.file_button_clicked)
        self.SaveButton.clicked.connect(self.save_button_clicked)
        self.opacity = [0.5,0.5,0.5,0.5,0.5,0.5,0.5,]

    def save_button_clicked(self):
        cv2.imwrite("save.jpg",self.img)

    def update_image(self):
        self.scene = QGraphicsScene(self)
        testname = "processing.jpg"
        cv2.imwrite(testname,self.img)
        self.scene.addPixmap(QPixmap(testname).scaled(self.imageView.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
        self.imageView.setScene(self.scene)
        self.imageView.show()

    def face_extract(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        img_org = cv2.imread(self.fname)
        import copy
        self.img = copy.copy(img_org)
        cat = cv2.imread('cat2.png')
        gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.3,5)
        self.count=0
        for (x,y,w,h) in faces:
            cat_resized = cv2.resize(cat,(w,h),interpolation=cv2.INTER_AREA)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = self.img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            file_name = "face_"+str(self.count)+".png"
            cv2.imwrite(file_name,self.img[y:y+h,x:x+w])
            self.img[y:y+h,x:x+w]=cv2.addWeighted(self.img[y:y+h,x:x+w],self.opacity[self.count],cat_resized[:h,:w],1-self.opacity[self.count],0.0)
            self.count = self.count+1
        #print(self.opacity)
        self.update_image()

    def changeIndex(self):
        index = self.opacity_combobox.currentIndex()
        if index < self.opacity_combobox.count() - 1:
            self.opacity_combobox.setCurrentIndex(index + 1)
        else:
            self.opacity_combobox.setCurrentIndex(0)

    def handleActivated(self, text):
        print('handleActivated: %s' % text)

    def handleChanged(self, text):
        self.opacity_slider.setValue(self.opacity[int(text)-1]*100)
        print('handleChanged: %s' % text)

    def sliderChanged(self,value):
        self.opacity[self.opacity_combobox.currentIndex()] = float(value)/100.0
        print("opacity : %.2f"%self.opacity[self.opacity_combobox.currentIndex()])
        self.face_extract()
                   
    def file_button_clicked(self):
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
        self.img = cv2.imread(self.fname)
        self.update_image()
        self.face_extract()
     
        self.opacity_combobox.setEditable(True)
        for i in range(self.count):
            self.opacity_combobox.addItem(str(i+1))
        self.changeIndex()
        self.opacity_combobox.activated['QString'].connect(self.handleActivated)
        self.opacity_combobox.currentIndexChanged['QString'].connect(self.handleChanged)
        self.changeIndex()
        #QtCore.QtObject.connect(self.opacity_slider, QtCore.SIGNAL('valueChanged(int)'), self.sliderChanged)
        self.opacity_slider.valueChanged['int'].connect(self.sliderChanged)

def main():
    
    app = QtGui.QApplication(sys.argv)
    myWindow = Form(None)
    myWindow.show()
    #ex = Form()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


#import facemorpher

#facemorpher.morpher(['test.jpg','cat.png'], plot = True)
#for i in range(count):
#    file_name = "face_"+str(i)+".png"
#    #face = cv2.imread(file_name)
#    facemorpher.morpher([file_name,'cat.png'], plot = True)

#cv2.imshow('img',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()