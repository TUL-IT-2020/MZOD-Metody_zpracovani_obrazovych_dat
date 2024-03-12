from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np


class MZCAM_image(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, *args, **kwargs)
        self.mouse_pos = None
        self.scale = 1
        self.pixmap = None
        self._painter = QtGui.QPainter()
        self.setMouseTracking(True)
        self.line = None

    def wheelEvent(self, event):
        if not self.pixmap:
            super(MZCAM_image, self).wheelEvent(event)
            return
        if event:
            if event.angleDelta().y() < 0:
                self.scale *= 0.8
            elif event.angleDelta().y() > 0:
                self.scale /= 0.8
        pm = self.pixmap
        pm = pm.scaled(int(pm.width() * self.scale), int(pm.height() * self.scale), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        if event:
            self.line = None
        self.setPixmap(pm)
        self.update()

    def load_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.wheelEvent(None)
