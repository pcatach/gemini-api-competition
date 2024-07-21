"""
Module for interacting with Google's Gemini models.

See e.g. list(genai.list_models()) for a comprehensive list.
"""

import json
import mimetypes
from enum import Enum

import google.generativeai as genai

from src.schemas import Scene

IMAGE_MIMETYPES = ["image/png", "image/jpeg", "image/webp", "image/heic", "image/heif"]


class ModelChoices(str, Enum):
    "Supported models"

    ONE = "1.0"
    FLASH = "1.5_flash"
    PRO = "1.5_pro"

    @staticmethod
    def api_name(choice):
        "Converts convenient enum string to api-readable string"

        map_to_api_name = {
            "1.0": "gemini-1.0-pro-latest",
            "1.5_flash": "gemini-1.5-flash",
            "1.5_pro": "gemini-1.5-pro",
        }
        return map_to_api_name[choice]

    @classmethod
    def values(cls):
        return [c.value for c in cls]


class Model:
    """
    Basic Class for interfacing with Google's Gemini Models.
    """

    BASIC_PROMPT = """
    Enumerate and describe all the individuals and vehicles in this image. Wherever possible, say the individuals' clothing, and the vehicles color and model.
    """

    JSON_PROMPT = """
    Use this JSON schema for individuals:
      Person = {
        "clothes": str
      }
    Use this JSON schema for vehicles:
      Vehicle = {
        "type": str,
        "color": str,
        "model": str,
      }
    Return a `list[Person|Vehicle]`
    """

    def __init__(self, model_choice: ModelChoices):
        # Set the relevant JSON response if using newest models
        config = {}
        if model_choice == ModelChoices.FLASH:
            config["response_mime_type"] = "application/json"
            self.default_prompt = self.BASIC_PROMPT + self.JSON_PROMPT
        elif model_choice == ModelChoices.PRO:
            # formal response schema declaration is supposed to work better
            config["response_mime_type"] = "application/json"
            config["response_schema"] = Scene
            # for PRO should work without JSON_PROMPT in fact
            self.default_prompt = self.BASIC_PROMPT + self.JSON_PROMPT
        else:  # 1.0 cannot process images
            raise ValueError(
                "Model Gemini 1.0 cannot read images, so not supproted yet"
            )

        self._model = genai.GenerativeModel(
            ModelChoices.api_name(model_choice), generation_config=config
        )
        self.uploaded_files = []

    def describe_image_from_path(self, image_path, prompt=None, verbose=False):
        """
        Describes image using Google's model given a file path.
        Keeps pointer to image uploaded in object's cache.

        :param image_path: str: path for image
        :param prompt: str: prompt for the model. model-dependent default set by class and __init__
        :param verbose: bool: whether to be verbose about file upload

        :return: tuple containing uploaded file and model response
        """
        mime, _ = mimetypes.guess_type(image_path)
        assert mime in IMAGE_MIMETYPES, f"Unsupported filetype: {mime}"

        uploaded_file = genai.upload_file(path=image_path)
        self.uploaded_files.append(uploaded_file)
        if verbose:
            print(
                f"Uploaded file '{uploaded_file.display_name}' as: {uploaded_file.uri}"
            )

        # Recommendation is to place prompt after image if using a single image
        prompt = prompt or self.default_prompt
        response = self._model.generate_content([uploaded_file, prompt])

        return uploaded_file, response.text

    def describe_image_from_blob(self, image_blob, prompt=None):
        """
        Describes image using Google's model given a blob object
        representing a PNG image.

        :param image_blob: genai.protos.Blob: Blob representing a PNG image
        :param prompt: str: prompt for the model. model-dependent default set by class and __init__

        :return: model response
        """
        prompt = prompt or self.default_prompt
        response = self._model.generate_content([image_blob, prompt])

        return response.text

    def clear_uploads(self):
        """
        Deletes uploaded images from server and resets the cache
        """
        for file in self.uploaded_files:
            genai.delete_file(file.name)
        self.uploaded_files = []

    @staticmethod
    def parse_json(maybe_json):
        try:
            parsed_json = json.loads(maybe_json)
            return parsed_json
        except ValueError as e:
            print(f"{e}: Not a JSON, you might want to check it properly..")
            return None
