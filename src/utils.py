from collections import Counter
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
    return s.replace("t-", "t").replace(" and ", ", ").replace("a ", "")


def summarise_scenes(scenes):
    """
    Returns a tuple with summarised persons and vehicles for collection of scenes.
    """

    persons = Counter()
    vehicles = Counter()
    for scene in scenes:
        persons += Counter(
            (p.get("gender"), sanitise_string(p.get("clothes")))
            for p in scene.get("persons")
        )
        vehicles += Counter(
            (v.get("type"), v.get("color")) for v in scene.get("vehicles")
        )

    return persons, vehicles
