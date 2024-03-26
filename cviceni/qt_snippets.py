import os
import sys
import re
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QGridLayout


class CustomWidget(QtWidgets.QWidget):
    def __init__(self, text, minimum, maximum, value):
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

class SnippetWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.central_widget = None
        self.grid_layout = None

        self.button = None
        self.combobox = None
        self.label_combobox = None
        self.lineedit = None
        self.slider = None
        self.label_slider = None
        self.checkbox = None
        self.spinbox = None
        self.doublespinbox = None
        self.timer = None
        self.timer_cnt = 0

        self.cw = None

        self.setup_ui()

    def setup_ui(self):
        self.resize(1200, 800)
        self.central_widget = QtWidgets.QWidget(self)
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)

        # button snippet
        self.button = QtWidgets.QPushButton(self)
        self.button.setText('Hello World')
        self.button.clicked.connect(self.button_clicked)
        # creating a grid in here, pos y, pos x, height, width
        self.grid_layout.addWidget(self.button, 0, 0, 1, 2)

        # combobox snippet
        self.combobox = QtWidgets.QComboBox(self)
        for i in range(4):
            self.combobox.addItem(f'Item{i}')
        self.combobox.currentIndexChanged.connect(self.combobox_idx_changed)
        self.label_combobox = QtWidgets.QLabel(self)
        self.grid_layout.addWidget(self.combobox, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.label_combobox, 1, 1, 1, 1)

        # line edit snippet
        self.lineedit = QtWidgets.QLineEdit(self)
        self.lineedit.textEdited.connect(self.lineedit_edited)
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 5)
        self.lineedit.setValidator(onlyInt)
        self.grid_layout.addWidget(self.lineedit, 2, 0, 1, 2)

        # slider snippet
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(10)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.slider_changed)
        self.label_slider = QtWidgets.QLabel(self)
        self.grid_layout.addWidget(self.slider, 3, 0, 1, 1)
        self.grid_layout.addWidget(self.label_slider, 3, 1, 1, 1)

        # checkbox snippet
        self.checkbox = QtWidgets.QCheckBox(self)
        self.checkbox.setText('this one has its own label')
        self.checkbox.stateChanged.connect(self.checkbox_changed)
        self.grid_layout.addWidget(self.checkbox, 4, 0, 1, 2)

        # spinbox snippet
        self.spinbox = QtWidgets.QSpinBox(self)
        self.spinbox.setRange(0, 50)
        self.spinbox.setSingleStep(3)
        self.spinbox.valueChanged.connect(self.spinbox_changed)

        # double spinbox snippet
        self.doublespinbox = QtWidgets.QDoubleSpinBox(self)
        self.doublespinbox.setRange(0.0, 50.0)
        self.doublespinbox.setSingleStep(3.0)
        self.doublespinbox.valueChanged.connect(self.doublespinbox_changed)

        self.grid_layout.addWidget(self.spinbox, 6, 0, 1, 1)
        self.grid_layout.addWidget(self.doublespinbox, 6, 1, 1, 1)

        # timer snippet
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(int(1000 / 30))
        self.timer.timeout.connect(self.timer_handler)
        self.timer.start()

        self.cw = CustomWidget('hello', 0, 100, 50)
        self.grid_layout.addWidget(self.cw, 7, 0, 1, 1)

        # !!! CONFIDENTIAL !!!
        # !!! HIDE FROM PUBLIC AT ANY COSTS !!!
        # !!! DO NOT UNCOMMENT !!!
        # nb = QtWidgets.QLCDNumber(self)
        # self.grid_layout.addWidget(nb, 7, 0, 1, 2)

        self.setCentralWidget(self.central_widget)

    # advanced button clicked snippet
    def button_clicked(self):
        btn = self.sender()
        btn.setText('Hello World @{:.3f}'.format(self.timer_cnt/self.timer.interval()))

    # cool combobox clicked snippet
    def combobox_idx_changed(self):
        cb = self.sender()
        self.label_combobox.setText(f'{cb.currentText()} @ {cb.currentIndex()}')

    # lineedit edited polite snippet
    def lineedit_edited(self, text):
        # no code here, sir, as you may have noticed
        # go away
        # please
        pass

    # Awesome slider changed code snippet
    def slider_changed(self):
        sl = self.sender()
        self.label_slider.setText(f'{sl.value()}')

    # What a snippet for a checkbox changed signal !!!
    def checkbox_changed(self):
        ch = self.sender()
        ch.setText(f'this one has its own label and is{"" if ch.isChecked() else " not"} checked')

    # A miraculous perpetuum mobile spinbox snippets
    # Will these two run forever?
    # Execute now and find out!
    def spinbox_changed(self):
        sb = self.sender()
        self.doublespinbox.setValue(float(sb.value()))

    def doublespinbox_changed(self):
        dsb = self.sender()
        self.spinbox.setValue(int(dsb.value()))

    # it is a timer handler snippet time
    def timer_handler(self):
        self.setWindowTitle('{:.3f}'.format(self.timer_cnt / self.timer.interval()))
        self.timer_cnt += 1

class SnippetsApp:
    def __init__(self, argv):
        self.app = QtWidgets.QApplication(argv)
        self.app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        self.ui = SnippetWindow()
        self.ui.setup_ui()

    def run(self):
        self.ui.show()
        sys.exit(self.app.exec_())




if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    MZCAMgui = SnippetsApp(sys.argv)
    MZCAMgui.run()