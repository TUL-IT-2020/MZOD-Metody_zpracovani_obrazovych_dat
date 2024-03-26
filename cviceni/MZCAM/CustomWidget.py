from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QGridLayout


class CustomWidget(QtWidgets.QWidget):
    def __init__(self, text, minimum, maximum, value):
        """
        CustomWidget

        Args:
            text (str): Label text
            minimum (int): Minimum value
            maximum (int): Maximum value
            value (int): Default value
        """
        super().__init__()
        self.text = text
        self.min = minimum
        self.max = maximum
        self.value = value

        self.CustomLabel = None
        self.CustomSlider = None
        self.CustomLabelValue = None
        self.initUI()

    def initUI(self):
        gl = QGridLayout(self)
        self.CustomLabel = QtWidgets.QLabel(self.text)
        self.CustomSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.CustomSlider.setRange(self.min, self.max)
        self.CustomSlider.setValue(self.value)
        self.CustomSlider.valueChanged.connect(self.valueChanged)
        self.CustomLabelValue = QtWidgets.QLabel(str(self.value))
        gl.addWidget(self.CustomLabel, 0, 0, 1, 1)
        gl.addWidget(self.CustomSlider, 0, 1, 1, 1)
        gl.addWidget(self.CustomLabelValue, 0, 2, 1, 1)

    def valueChanged(self):
        sl = self.sender()
        self.CustomLabelValue.setText(str(sl.value()))