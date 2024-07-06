""" 
A script to test if the basic Model components are working.

TODO: make a proper test out of this
"""

import argparse
import google.generativeai as genai

from src.model import ModelAPI, ModelChoices


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", type=ModelChoices, choices=ModelChoices.values(), required=True
    )
    parser.add_argument("--images", type=str, nargs="+", required=True)
    parser.add_argument("--api_token", type=str, required=True)

    return parser.parse_args()


def main():
    args = parse_args()

    genai.configure(api_key=args.api_token)
    model = ModelAPI(args.model)

    print("\n---------------\n")
    for i, image_path in enumerate(args.images):
        _, json = model.describe_image(image_path, verbose=True)
        print(i)
        print(json)
        print("\n---------------\n")

    print("Clearing uploads..")
    model.clear_uploads()


if __name__ == "__main__":
    main()
