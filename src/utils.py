from datetime import datetime, timezone

import cv2
import google.generativeai as genai


def convert_frame_to_blob(frame: "np.ndarray") -> genai.protos.Blob:
    """Converts an array representing a frame to a Blob object."""
    _, buffer = cv2.imencode(".png", frame)
    return genai.protos.Blob(mime_type="image/png", data=buffer.tobytes())


def today_start():
    today = datetime.now().date()
    return datetime(today.year, today.month, today.day, tzinfo=timezone.utc)


def sanitise_string(s):
    return s.replace("t-", "").replace("and ", "")
