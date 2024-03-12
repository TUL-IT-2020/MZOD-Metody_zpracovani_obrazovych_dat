import cv2
import numpy as np

import imagewidget
import json
import os
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from pypylon import pylon


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.default_settings = {
            'camera': None
        }
        settings = self.load_settings()
        self.settings = settings if settings else self.default_settings

        self.central_widget = None
        self.grid_layout = None
        self.combo_box_cameras = None

        self.button_connect = None

        self.ref_pixmap = None
        self.gb_image = None
        self.image = None

        # list of camera names
        self.cameras = None
        # basler tl_factory devices
        self.devices = None
        self.tl_factory = None
        # basler converter
        self.converter = None
        # basler camera instance
        self.camera = None

        self.timer = None

    def setup_ui(self):
        self.resize(1200, 800)
        self.central_widget = QtWidgets.QWidget(self)
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)

        # camera select box
        self.combo_box_cameras = QtWidgets.QComboBox(self)
        self.cameras = self.get_available_cameras()
        for cam in self.cameras:
            self.combo_box_cameras.addItem(cam)
        if self.settings['camera'] in self.cameras:
            self.combo_box_cameras.setCurrentText(self.settings['camera'])
        self.grid_layout.addWidget(self.combo_box_cameras, 0, 0, 1, 1)

        # camera connect button
        self.button_connect = QtWidgets.QPushButton(self)
        self.button_connect.setText('Connect')
        self.grid_layout.addWidget(self.button_connect, 0, 1, 1, 1)
        self.button_connect.clicked.connect(self.cam_connect)

        # camera refresh timer
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(int(1000/30))
        self.timer.timeout.connect(self.cam_grab)

        # camera image display
        self.ref_pixmap = QtGui.QPixmap('micro.png')
        self.gb_image, self.image = self.create_groupbox_image(self, 'Captured Image', self.ref_pixmap)
        self.grid_layout.addWidget(self.gb_image, 1, 0, 1, 2)

        self.setCentralWidget(self.central_widget)

    @staticmethod
    def load_settings():
        if os.path.exists('settings.json'):
            try:
                with open('settings.json', 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(e)
                return None

    def save_settings(self):
        try:
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(e)

    # creates image in the center of the groupbox
    # returns groupbox and image widget
    @staticmethod
    def create_groupbox_image(parent, name, ref_pixmap):
        gb = QtWidgets.QGroupBox(parent)
        gb.setTitle(name)
        gb.setMinimumHeight(400)
        layout = QtWidgets.QGridLayout(gb)
        scroll = QtWidgets.QScrollArea(gb)
        scroll.setWidgetResizable(True)
        image = imagewidget.MZCAM_image(parent=gb)
        image.load_pixmap(ref_pixmap)
        image.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        image.setAlignment(QtCore.Qt.AlignCenter)
        scroll.setWidget(image)
        layout.addWidget(scroll, 0, 0, 1, 1)
        return gb, image

    # returns models names list
    # populates devices prop.
    def get_available_cameras(self):
        self.tl_factory = pylon.TlFactory.GetInstance()
        self.devices = self.tl_factory.EnumerateDevices()
        if not self.devices:
            raise Exception("No camera found")
        model_name_list = []
        # return list of all cameras
        for dev_info in self.devices:
            # do not connect to emulator
            model_name_list.append(dev_info.GetModelName())
        return model_name_list

    # connects to the camera and starts grabbing
    def cam_connect(self):
        if self.camera is not None:
            # disconnect
            self.camera.StopGrabbing()
            self.camera.Close()
            self.button_connect.setText('Connect')
            self.image.load_pixmap(self.ref_pixmap)
            self.camera = None
            return
        # connect
        if self.combo_box_cameras.currentIndex() >= 0:
            for dev_info in self.devices:
                # connect to devices with selected model name
                if self.combo_box_cameras.currentText() == dev_info.GetModelName():
                    self.camera = pylon.InstantCamera(self.tl_factory.CreateDevice(dev_info))

            # success
            if not self.camera:
                raise Exception('Failed to connect to the camera')

            # register configuration for continuous grabbing
            self.camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll,
                                              pylon.Cleanup_Delete)
            # self.camera.RegisterConfiguration(pylon.AcquireContinuousConfiguration(), pylon.RegistrationMode_ReplaceAll,
            #                                  pylon.Cleanup_Delete)
            # open camera, set output format
            # todo: configurable
            self.camera.Open()
            self.camera.PixelFormat.SetValue('RGB8')
            self.camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

            # converter
            # todo: configurable
            self.converter = pylon.ImageFormatConverter()
            self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
            self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

            # grab each Xms
            # todo: configurable
            self.timer.start(int(1000/60))
            self.button_connect.setText('Disconnect')

    # grab frame from camera
    def cam_grab(self):

        trigger_time = 200

        if self.camera:

            # run only once and only in trigger mode
            if 'sw_trigger' not in self.settings:
                self.settings['sw_trigger'] = True
                try:
                    self.camera.WaitForFrameTriggerReady(trigger_time, pylon.TimeoutHandling_ThrowException)
                except pylon.GenericException as ex:
                    self.settings['sw_trigger'] = False

            if self.settings['sw_trigger']:
                if self.camera.WaitForFrameTriggerReady(trigger_time, pylon.TimeoutHandling_Return):
                    self.camera.ExecuteSoftwareTrigger()
            else:
                # should do some trigger time loop
                self.camera.ExecuteSoftwareTrigger()

            while True:
                if self.camera.GetGrabResultWaitObject().Wait(0):
                    break

            # grab result
            grab_result = (self.camera.RetrieveResult(0, pylon.TimeoutHandling_Return))
            if grab_result is None:
                return None
            if not grab_result.GrabSucceeded():
                return None

            # TODO: to get raw array
            # grab_result.GetArray()
            # TODO: custom conversion
            frame = self.converter.Convert(grab_result).GetArray()

            self.button_connect.setText('Disconnect')

            # conversion to QImage
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QtGui.QImage(frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888).rgbSwapped()
            self.image.load_pixmap(QtGui.QPixmap(q_img))

    # camera stop
    def cam_stop(self):
        if self.timer:
            self.timer.stop()
        if self.camera:
            self.camera.StopGrabbing()

    # on close
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.camera:
            self.camera.disconnect()
        if self.combo_box_cameras.currentIndex() >= 0:
            self.settings['camera'] = self.combo_box_cameras.currentText()
        self.save_settings()
        a0.accept()


class MZCAMApp:
    def __init__(self, argv):
        self.app = QtWidgets.QApplication(argv)
        self.app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        self.ui = MainWindow()
        self.ui.setup_ui()

    def run(self):
        self.ui.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    MZCAMgui = MZCAMApp(sys.argv)
    MZCAMgui.run()
