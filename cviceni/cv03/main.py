from pypylon import pylon
import cv2


class MZODCamera:
    def __init__(self):
        self.camera = None
        self.converter = None

    def init_camera(self):
        tl_factory = pylon.TlFactory.GetInstance()
        devices = tl_factory.EnumerateDevices()
        if not devices:
            raise Exception("No camera found")

        # connect to the last available camera
        for dev_info in devices:
            # do not connect to emulator
            if dev_info.GetModelName() != 'Emulation':
                self.camera = pylon.InstantCamera(tl_factory.CreateDevice(dev_info))

                print(f'camera model: {dev_info.GetModelName()}')

        # previous step failed
        if self.camera is None:
            raise Exception("No camera selected")

        self.camera.RegisterConfiguration(pylon.AcquireContinuousConfiguration(), pylon.RegistrationMode_ReplaceAll,
                                          pylon.Cleanup_Delete)
        self.camera.Open()
        self.camera.PixelFormat.SetValue('RGB8')
        self.camera.StartGrabbing(pylon.GrabStrategy_OneByOne)

        # converter
        self.converter = pylon.ImageFormatConverter()
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned


    def get_image(self):

        while True:
            if self.camera.GetGrabResultWaitObject().Wait(0):
                break

        # grab result
        grab_result = (self.camera.RetrieveResult(0, pylon.TimeoutHandling_Return))
        if grab_result is None:
            return None
        if not grab_result.GrabSucceeded():
            return None

        image = self.converter.Convert(grab_result).GetArray()
        cv2.namedWindow('MZOD', cv2.WINDOW_NORMAL)
        cv2.imshow('MZOD', image)
        key = cv2.waitKey(1)
        return key


if __name__ == '__main__':

    cam = MZODCamera()
    cam.init_camera()
    try:
        while True:
            kp = cam.get_image()
            if kp is not None:
                if kp == ord('q'):
                    break
    finally:
        if cam.camera:
            cam.camera.StopGrabbing()
            cam.camera.Close()
