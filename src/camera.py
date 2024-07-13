"""
Module for interacting with the video capturing device.

>> for frame in Camera().frames():
>>     key = show_frame(frame)
>>     if key == ord('q'):
>>         break

>> camera = Camera()
>> camera.show_feed()
"""
import time

import cv2
import numpy as np

# The device ID is an integer that identifies which
# video capturing device to use.
VIDEO_CAPTURING_DEVICE_ID = 0


class FrameNotFoundError(Exception):
    pass


def show_frame(frame: np.ndarray) -> int:
    """For debugging purposes.

    Creates a new window, displays the frame until any key is pressed.
    Returns the ord() of the key that was pressed (useful if you want to
    break out of a loop).
    """
    cv2.namedWindow("frame")
    cv2.imshow("frame", frame)

    # wait for any key press and stop displaying the frame
    key = cv2.waitKey(0)
    cv2.destroyWindow("frame")
    # wait 1ms and destroy the window
    # program hangs indefinitely if we don't call waitKey here.
    cv2.waitKey(1)
    return key


class Camera:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(VIDEO_CAPTURING_DEVICE_ID)

    def frames(self) -> "Iterable[np.ndarray]":
        while True:
            try:
                yield self.read_frame()
            except FrameNotFoundError:
                raise StopIteration

    def read_frame(self) -> np.ndarray:
        returned, frame = self.video_capture.read()
        if not returned:
            raise FrameNotFoundError(
                f"Could not grab frames from device {VIDEO_CAPTURING_DEVICE_ID}"
            )
        return frame

    def close(self):
        """Close capturing device.

        If this is not called the device will remain busy - won't be
        able to invoke cv2.VideoCapture() again.
        NOTE: release() is automatically called by VideoCapture destructor
        when the program exits.
        """
        self.video_capture.release()

    def is_open(self):
        return self.video_capture.isOpened()

    def show_current_frame(self):
        """For debugging purposes."""
        frame = self.read_frame()
        show_frame(frame)

    def show_feed(self):
        """For debugging purposes.

        Displays captured frame every 100ms until key 'q' is pressed
        """
        cv2.namedWindow("feed")
        cv2.resizeWindow("feed", 400, 300)

        while True:
            frame = self.read_frame()
            cv2.imshow("feed", frame)

            key = cv2.waitKey(100)
            if key == ord('q'):
                break
        cv2.destroyWindow("feed")
        cv2.waitKey(1)
