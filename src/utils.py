import cv2
import google.generativeai as genai


def convert_frame_to_blob(frame: "np.ndarray") -> genai.protos.Blob:
    """Converts an array representing a frame to a Blob object."""
    _, buffer = cv2.imencode(".png", frame)
    return genai.protos.Blob(mime_type="image/png", data=buffer.tobytes())
