from PyQt4 import QtGui, QtCore
from os import path
import yaml
import os
import sys
from PIL import Image

from modis_read import read_band
from img_view import ImageViewer

paths = []
index = 0

#hdf
'''
def gen_img_path(modis_path):
    global paths
    for file in os.listdir(modis_path):
        if file.endswith("hdf"):
            file_path = path.join(modis_path, file)
            band1, band2 = read_band(file_path)
            paths.append(band1)
            paths.append(band2)
'''

def gen_img_path(modis_path):
    global paths
    for file in os.listdir(modis_path):
        if file.endswith("tif"):
            file_path = path.join(modis_path, file)
            # band = Image.open(file_path)
            paths.append(file_path)

def next(imageViewer):
    global index
    n = len(paths)
    index = (index + 1) % n
    imageViewer.open(paths[index])


def prev(imageViewer):
    global index
    n = len(paths)
    index = (index + n - 1) % n
    imageViewer.open(paths[index])


def keyPressEvent(imageViewer, event):
    key = event.key()
    if key == QtCore.Qt.Key_1:
        prev(imageViewer)
    if key == QtCore.Qt.Key_2:
        next(imageViewer)


if __name__ == "__main__":
    with open("config.yaml")as f:
        config = yaml.load(f)

    modis_path = config["modis_path"]
    crop_size = config["crop_size"]
    random_zone = config["random_zone"]
    random_num = config["random_num"]
    gen_img_path(modis_path)

    app = QtGui.QApplication(sys.argv)
    imageViewer = ImageViewer(keyPressEvent, crop_size=crop_size, random_zone=random_zone, random_num=random_num)
    imageViewer.show()
    imageViewer.open(paths[index])

    sys.exit(app.exec_())
