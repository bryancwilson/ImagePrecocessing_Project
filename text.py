
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

app = QApplication(sys.argv)

# Create two QPixmap objects
pixmap1 = QPixmap("lena.png")
pixmap2 = QPixmap("moon.jpg")

# Create a new QPixmap to hold the combined images
combined_pixmap = QPixmap(pixmap1.size())
combined_pixmap.fill(Qt.transparent)

# Create a QPainter to draw on the combined pixmap
painter = QPainter(combined_pixmap)

# Draw the first pixmap
painter.drawPixmap(0, 0, pixmap1)

# Draw the second pixmap on top
painter.drawPixmap(0, 0, pixmap2)

painter.end()

# Create a QLabel to display the combined pixmap
label = QLabel()
label.setPixmap(combined_pixmap)
label.show()

sys.exit(app.exec_())