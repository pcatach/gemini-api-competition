import logging

from src.camera import Camera
from src.model import Model, ModelChoices
from src.utils import convert_frame_to_blob

LOG = logging.getLogger("cctv_logger")


class CCTVLoggerServiceAdaptor:
    """The adaptor integrates the logic for:
    1. Taking a picture with the camera
    2. Sending it to the model
    3. Persisting the response to the database

    It must implement a run() method that will be invoked
    by the twisted service, for instance
    internet.TimerService(step=30, callable = adaptor.run)
    """

    def __init__(self):
        self.model = Model(ModelChoices.PRO)
        self.camera = Camera()

    def run(self):
        LOG.info("Sending picture...")
        frame = self.camera.read_frame()
        blob = convert_frame_to_blob(frame)
        response = self.model.describe_image_from_blob(blob)
        LOG.info("Response:")
        LOG.info(response)
        # ...
