"""
This module schedules model calls.

Every 30 seconds it will take a picture and invoke the model.
We could do something like:
while True:
    do_thing()
    time.sleep(30)
but this is blocking and we want to be able to handle network requests in the meantime.
Thus using Twisted. In twisted, the "reactor" is the event loop. We attach "callbacks"
to the event loop that get called on certain events (like a time interval) and then
return control to the event loop.

NOTE: requires setting the GOOGLE_API_KEY envvar
"""
import os

import google.generativeai as genai
from twisted.internet import reactor, task

from camera import Camera, show_frame
from model import ModelAPI, ModelChoices
from utils import convert_frame_to_blob

TIME_INTERVAL = 5

model = ModelAPI(ModelChoices.PRO)
camera = Camera()

def send_picture():
    print("Sending picture...")
    frame = camera.read_frame()
    show_frame(frame)
    blob = convert_frame_to_blob(frame)
    print(model.describe_image_from_blob(blob))

# this attaches our function to the event loop as a callback
loop = task.LoopingCall(send_picture)
loop.start(TIME_INTERVAL)

reactor.run()