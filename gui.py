import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class PhotoLabel(QLabel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n No image Loaded \n\n')
        self.setStyleSheet('''
        QLabel {
            border: 4px dashed #aaa;
        }''')

    def setPixmap(self, *args, **kwargs):
        super().setPixmap(*args, **kwargs)
        self.setStyleSheet('''
        QLabel {
            border: none;
        }''')


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

        # initialize toggles and labels
        btn1 = QPushButton('Browse For Left Image')
        btn1.clicked.connect(self.open_image_left)
        btn2 = QPushButton('Browse For Right Image')
        btn2.clicked.connect(self.open_image_right)


        left_layout.addWidget(btn1)
        left_layout.addWidget(self.photo_left)

        right_layout.addWidget(btn2)
        right_layout.addWidget(self.photo_right)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setAcceptDrops(False)
        self.resize(300, 200)

    def open_image_right(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
        
        self.photo_right.setPixmap(QPixmap(filename))

    def open_image_left(self, filename=None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, 'Select Photo', QDir.currentPath(), 'Images (*.png *.jpg)')
            if not filename:
                return
        
        self.photo_left.setPixmap(QPixmap(filename))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Template()
    gui.show()
    sys.exit(app.exec_())