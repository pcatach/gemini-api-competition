import time

import cv2
import numpy as np
from PIL import Image

VIDEO_CAPTURING_DEVICE_ID = 0

class Camera:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(VIDEO_CAPTURING_DEVICE_ID)

    def close(self):
        self.video_capture.release()

    def is_open(self):
        return self.video_capture.isOpened()

    def read_frame(self):
        returned, frame = self.video_capture.read()
        if not returned:
            raise OSError(f"Could not grab frames from device {VIDEO_CAPTURING_DEVICE_ID}")
        return frame

    def show_frame(self):
        frame = self.read_frame()
        image = Image.fromarray(frame, 'RGB')
        image.show()

    def show_feed(self):
        cv2.namedWindow("feed")

        while True:
            frame = self.read_frame()
            cv2.imshow("feed", frame)
            if cv2.waitKey(100):
                break

        cv2.destroyWindow("feed")
        self.close()
