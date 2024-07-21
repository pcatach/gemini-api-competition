"""
A script to test if the basic Model components are working.

TODO: make a proper test out of this
"""

import argparse
import google.generativeai as genai
import json

from src.camera import Camera, show_frame
from src.model import Model, ModelChoices
from src.utils import convert_frame_to_blob
from src.mongo_client import MongoClient, Scene


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", type=ModelChoices, choices=ModelChoices.values(), required=True
    )
    parser.add_argument("--api_token", type=str, required=True)
    parser.add_argument("--db", action="store_true")

    mutually_exclusive_group = parser.add_mutually_exclusive_group(required=True)
    mutually_exclusive_group.add_argument("--images", type=str, nargs="+", default=None)
    mutually_exclusive_group.add_argument("--live", action="store_true")

    return parser.parse_args()


def describe_from_paths(image_paths, model):
    responses = []
    print("---------------")
    for i, image_path in enumerate(image_paths):
        _, json = model.describe_image_from_path(image_path, verbose=True)
        print(f"({i}) ")
        print(json)
        print("---------------")
        responses.append(json)

    return responses


def describe_from_live_feed(model):
    camera = Camera()
    responses = []
    for frame in camera.frames():
        print("Press 'y' to send picture to Gemini, 'n' to retake or 'q' to quit")
        key = show_frame(frame)
        if key == ord("q"):
            break
        elif key == ord("n"):
            continue
        elif key == ord("y"):
            pass
        else:
            raise ValueError("Invalid input.")

        blob = convert_frame_to_blob(frame)
        json = model.describe_image_from_blob(blob)
        print(json)
        responses.append(json)

    return responses


def insert_database_responses(responses, db_uri=None):
    client = MongoClient(uri=db_uri)
    for res in responses:
        scene = Scene(json.loads(res))
        # workaround when response is missing parts
        # parts of the schema
        for key in Scene.__required_keys__:
            if key not in scene:
                scene[key] = []
        client.insert_scene(scene)


def main():
    args = parse_args()

    genai.configure(api_key=args.api_token)
    model = Model(args.model)

    responses = []
    if args.images:
        responses = describe_from_paths(args.images, model)
    elif args.live:
        responses = describe_from_live_feed(model)

    if args.db:
        try:
            insert_database_responses(responses)
        except Exception as e:
            print(f"Could not insert responses to database: {e}")
        else:
            print("Successful insertion of responses to database.")

    if args.images:
        print("Clearing uploads..")
        model.clear_uploads()


if __name__ == "__main__":
    main()
