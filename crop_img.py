from PyQt4 import QtCore, QtGui
from os import path
import os
from functools import partial

labels = ["sea", "block ice", "paper cloud", "thick cloud", "trash ice"]

img_path = "imgs"
if not path.exists(img_path):
    os.mkdir(img_path)

img_path_pri = "imgs_pri"
if not path.exists(img_path_pri):
    os.mkdir(img_path_pri)

for label in labels:
    label_img_path = path.join(img_path, label)
    if not path.exists(label_img_path):
        os.mkdir(label_img_path)


for label in labels:
    label_img_path_pri = path.join(img_path_pri, label)
    if not path.exists(label_img_path_pri):
        os.mkdir(label_img_path_pri)


def circle(img,sx,sy,ex,ey):


    img = img.toImage()
    #color = (255,0,0)
    #color = 45567
    color = int('0xFFFF00',16)
    for i in range(sx,ex):
        img.setPixel(i, sy, color)

    for i in range(sx,ex):
        img.setPixel(i, ey, color)

    for i in range(sy,ey):
        img.setPixel(sx, i, color)

    for i in range(sy,ey):
        img.setPixel(ex, i, color)
    return img



class CropImgView(QtGui.QDialog):
    def __init__(self, crop_img, img_name, x, y,crop_size,big_size,label):
        super(CropImgView, self).__init__()

        self.img_name = path.splitext(path.basename(img_name))[0]
        self.x = x
        self.y = y
        self.label = label
        self.crop_size = crop_size
        self.big_size = big_size
        self.matrix = QtGui.QMatrix();
        self.layout = QtGui.QVBoxLayout()

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setPixmap(crop_img)
        self.imageLabel.resize(crop_img.width(), crop_img.height())

        self.layout.addWidget(self.imageLabel)
        if label == 'none':
        	for label in labels:
        		b = QtGui.QPushButton(label)
        		self.layout.addWidget(b)
        		b.clicked.connect(partial(self.click_label, label=label,first = 1))
        else:		
        	self.click_label(label,0)
        self.setLayout(self.layout)
        # self.layout.addStretch()
        # self.resize(256, 500)

    def click_label(self, label,first):
        self.label = label;
        img = self.imageLabel.pixmap()
        angles = [0,15,30,45,60,75,90]
        oneimagepath = path.join(img_path, label,self.img_name +
		                     "_{}_{}".format(self.x, self.y))
        if not path.exists(oneimagepath):
        	os.mkdir(oneimagepath)
        if first == 1:
        	oneimagepath_pri = path.join(img_path_pri, label,self.img_name +
		                     "_{}_{}_pri_1".format(self.x, self.y))
        else:
        	oneimagepath_pri = path.join(img_path_pri, label,self.img_name +
		                     "_{}_{}_pri".format(self.x, self.y))
        if not path.exists(oneimagepath_pri):
        	os.mkdir(oneimagepath_pri)
        #save_path_pri = path.join(oneimagepath_pri,self.img_name +
	#                     "_{}_{}.jpg".format(self.x, self.y))
        #img.save(save_path_pri)
        #print(save_path_pri)
        for ang in angles:
        	save_path = path.join(oneimagepath,str(ang) + '.jpg')
        	save_path_pri = path.join(oneimagepath_pri,str(ang) + '.jpg')
        	self.matrix.rotate(ang);
        	pixmap = img.transformed(self.matrix);
        	psize = pixmap.size();
        	pheight = psize.height()
        	pwidth = psize.width()
        	startx = int(pheight / 2 - self.crop_size/2);
        	starty = int(pwidth / 2 - self.crop_size/2);
        	rect = QtCore.QRect(startx, starty, self.crop_size, self.crop_size)
        	crop_img = pixmap.copy(rect)
        	crop_img.save(save_path)
        	pixmap = circle(pixmap,startx,starty,startx + self.crop_size,starty + self.crop_size)
        	pixmap.save(save_path_pri)
        	print(save_path)
        	self.close()
