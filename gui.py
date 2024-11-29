import sys
import typing
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

class Mask(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 400, 300)

    def paintEvent(self):
        painter = QPainter(self)
        painter.drawRect(100, 15, 300, 100)
        

class PhotoLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n No image Loaded \n\n')
        self.setStyleSheet('''
        QLabel {
            border: 4px dashed #aaa;
        }''')

        self.pc = None

    def createMask(self):

        mask = QPixmap(self.image.size())
        mask.fill(Qt.transparent)

        painter = QPainter(mask)
        painter.setBrush(QBrush(QColor(0, 0, 0, 128)))  # Semi-transparent black
        painter.drawEllipse(50, 50, 200, 200)  # Example: Draw a circular mask
        painter.end()

        return mask


    def setPixmap(self, pc):

        self.pc = pc
        super().setPixmap(self.pc)


        self.setStyleSheet('''
        QLabel {
            border: none;
        }''')

        self.begin, self.destination = QPoint(), QPoint()
        
    # Function to Allow User to Draw
    def paintEvent(self, event):
        painter = QPainter(self)
        if self.pc != None:
            painter.drawPixmap(QPoint(), self.pc)

            if not self.begin.isNull() and not self.destination.isNull():
                painter.setPen(QPen(Qt.white, 5))
                painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))

                rect = QRect(self.begin, self.destination)
                painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.begin = event.pos()
            self.destination = self.begin
            self.update()
        
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.destination = event.pos()
            print(self.destination)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self.pc)
            painter.drawRect(rect.normalized())

            self.begin, self.destination - QPoint(), QPoint()
            self.update()

    def ret_crop(self):
        x1, y1 = self.begin.x(), self.begin.y()
        x2, y2 = self.destination.x(), self.destination.y()

        cropped_pixmap = self.pc.copy(x1, y1, x2 - x1, y2 - y1)

        image = cropped_pixmap.toImage()
        bits = image.bits()
        bits.setsize(image.height() * image.width() * 4)  # 4 bytes per pixel (RGBA)
        array = np.frombuffer(bits, np.uint8).reshape((image.height(), image.width(), 4))
        
        # convert image to greyscale
        grey_array = rgb2gray(grey_array)

        return grey_array


class Template(QWidget):

    def __init__(self):
        super().__init__()

        # set the overall horizontal layout
        layout = QHBoxLayout(self)

        # set inner vertical layouts
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.photo_left = PhotoLabel()
        self.photo_right = PhotoLabel()

        # flags
        self.pic_left_exists = False
        self.pic_right_exists = False

        # initialize toggles and labels
        btn1 = QPushButton('Browse For Left Image')
        btn1.clicked.connect(self.open_image_left)
        merge1 = QPushButton('Merge Mask Left')
        merge1.clicked.connect(self.merge)

        btn2 = QPushButton('Browse For Right Image')
        btn2.clicked.connect(self.open_image_right)
        merge2 = QPushButton('Merge Mask Right')
        merge2.clicked.connect(self.merge)

        left_layout.addWidget(btn1)
        left_layout.addWidget(self.photo_left)
        left_layout.addWidget(merge1)

        right_layout.addWidget(btn2)
        right_layout.addWidget(self.photo_right)
        right_layout.addWidget(merge2)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setAcceptDrops(False)
        self.resize(1000, 800)


    def open_image_right(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
        
        self.pic_right_exists = True
        self.photo_right.setPixmap(QPixmap(filename))

    def open_image_left(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
        self.pic_left_exists = True
        pc = QPixmap(filename)
        # pc.fill(Qt.transparent)

        self.photo_left.setPixmap(pc)

    def merge(self, event):
        self.photo_left.ret_crop()
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Template()
    gui.show()
    sys.exit(app.exec_())