
import robocam as robocam
import numpy as np

class Test():
    def __init__(self) -> None:
        r = robocam.RoboCam()
        r.cameraStreamInit()
        r.cameraStream()

        r.facedetectorInit()
        r.facedetectStart()
        
        # r.arucoDetectorInit()
        # r.arucoDetectorStart()

        # r.setEventHandler(robocam.CameraEvents.RECV_ARUCO_POINT, self.RecvPoint)

        # r.sketchdetectorInit()
        # r.sketchdetectStart()

        # r.numberRecognizerInit()
        # r.numberRecognizerStart()

        while True:
            s = input('command : ')

            if s == 't':
                r.TrainSketchData()
            elif s =='m':
                r.mosaicMode(30)
            else:
                r.SketchCapture(s)

    def RecvNames(self, names:np.ndarray):
        print(names)

    def RecvPoint(self, point:np.array):
        print(point)
t = Test()