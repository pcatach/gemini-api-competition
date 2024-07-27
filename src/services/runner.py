import json
import logging

from src.camera import Camera
from src.model import Model, ModelChoices
from src.mongo_client import MongoClient
from src.schemas import Scene
from src.utils import convert_frame_to_blob

LOG = logging.getLogger("cctv_logger")


class CCTVLoggerRunner:
    """The runner integrates the logic for:
    1. Taking a picture with the camera
    2. Sending it to the model
    3. Persisting the response to the database

    It must implement a run() method that will be invoked
    by the twisted service, for instance
    internet.TimerService(step=30, callable=runner.run)
    """

    def __init__(self):
        self.model = Model(ModelChoices.PRO)
        self.camera = Camera()
        self.client = MongoClient()

    def run(self):
        LOG.info("Sending picture...")
        frame = self.camera.read_frame()
        blob = convert_frame_to_blob(frame)
        response = self.model.describe_image_from_blob(blob)
        LOG.info("Response:")
        LOG.info(response)

        scene = Scene(json.loads(response))
        for key in Scene.__required_keys__:
            if key not in scene:
                scene[key] = []
        self.client.insert_scene(scene)
        # ...
