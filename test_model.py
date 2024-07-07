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
    parser.add_argument("--images", type=str, nargs="+", default=None)
    parser.add_argument("--api_token", type=str, required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    genai.configure(api_key=args.api_token)
    model = ModelAPI(args.model)

    if args.images is not None:
        print("\n---------------\n")
        for i, image_path in enumerate(args.images):
            _, json = model.describe_image_from_path(image_path, verbose=True)
            print(i)
            print(json)
            print("\n---------------\n")

        print("Clearing uploads..")
        model.clear_uploads()
    else:
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

            json = model.describe_image_from_array(frame)
            print(json)



if __name__ == "__main__":
    main()
