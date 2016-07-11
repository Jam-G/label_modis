from __future__ import print_function
from PyQt4 import QtCore, QtGui
import random
from PIL import Image


class ImageViewer(QtGui.QMainWindow):
    def __init__(self, keyboard_callback, crop_size=20, random_zone=100, random_num= 10):
        super(ImageViewer, self).__init__()

        self.printer = QtGui.QPrinter()
        self.scaleFactor = 0.0
        self.crop_size = crop_size
        self.random_zone = random_zone
        self.random_num = random_num
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.mouseDoubleClickEvent = self.double_click

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)

        self.keyboard_callback = keyboard_callback

    def open(self, filename):
        if filename:

        
            image = QtGui.QImage(filename)
            print('here!')
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % filename)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.imageLabel.adjustSize()
            print(self.imageLabel.width(), self.imageLabel.height())

            self.img_name = filename
            self.setWindowTitle(filename)

    def double_click(self, event):
        from crop_img import CropImgView
        print(event.x(), event.y())
        img = self.imageLabel.pixmap()

        big_size = self.random_zone
        half_size = int(big_size / 2)
        half_crop = int(self.crop_size / 2)
        rect = QtCore.QRect(event.x()-half_size, event.y()-half_size, big_size, big_size)
        crop_img = img.copy(rect)
        label = 'none';
        civ = CropImgView(crop_img, self.img_name, event.x(), event.y(),self.crop_size,big_size,label)
        civ.exec_()
        rx = random.sample(range(half_crop,self.random_zone - half_crop),self.random_num)
        ry = random.sample(range(half_crop,self.random_zone - half_crop),self.random_num)
        label = civ.label
        startx = event.x() - int(self.random_zone / 2)
        starty = event.y() - int(self.random_zone / 2)
        for i in range(self.random_num):
            x = startx + rx[i]
            y = starty + ry[i]
            rect = QtCore.QRect(x-half_size, y-half_size, big_size, big_size)
            crop_img = img.copy(rect)
            civ = CropImgView(crop_img, self.img_name, x , y,self.crop_size,big_size,label)

    def keyPressEvent(self, event):
        self.keyboard_callback(self, event)


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    imageViewer.open("tmp/MOD02QKM.A2000056.1100.005.2010030002804_band2.jpg")
    sys.exit(app.exec_())
