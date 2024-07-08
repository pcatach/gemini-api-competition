"""
A script to test if the basic Model components are working.

TODO: make a proper test out of this
"""

import argparse
import google.generativeai as genai

from src.camera import Camera, show_frame
from src.model import ModelAPI, ModelChoices
from src.utils import convert_frame_to_blob


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", type=ModelChoices, choices=ModelChoices.values(), required=True
    )
    parser.add_argument("--api_token", type=str, required=True)

    mutually_exclusive_group = parser.add_mutually_exclusive_group(required=True)
    mutually_exclusive_group.add_argument("--images", type=str, nargs="+", default=None)
    mutually_exclusive_group.add_argument("--live", action="store_true")

    return parser.parse_args()

def describe_from_paths(image_paths, model):
    print("\n---------------\n")
    for i, image_path in enumerate(image_paths):
        _, json = model.describe_image_from_path(image_path, verbose=True)
        print(i)
        print(json)
        print("\n---------------\n")

def describe_from_live_feed(model):
    camera = Camera()
    for frame in camera.frames():
        print("Press 'y' to send picture go Gemini, 'n' to retake or 'q' to quit")
        key = show_frame(frame)
        if key == ord('q'):
            break
        elif key == ord('n'):
            continue
        elif key == ord('y'):
            pass
        else:
            raise ValueError("Invalid input.")

        blob = convert_frame_to_blob(frame)
        json = model.describe_image_from_blob(blob)
        print(json)



def main():
    args = parse_args()

    genai.configure(api_key=args.api_token)
    model = ModelAPI(args.model)

    if args.images:
        describe_from_paths(args.images, model)
    elif args.live:
        describe_from_live_feed(model)

    print("Clearing uploads..")
    model.clear_uploads()

if __name__ == "__main__":
    main()
