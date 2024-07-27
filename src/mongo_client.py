from datetime import datetime, timezone

from pydantic import BaseModel as PydanticModel
from pymongo import MongoClient as PymongoClient

from src.schemas import Scene


class MongoDocument(PydanticModel):
    scene: Scene
    timestamp: datetime


class MongoClient:
    "Wrapper around pymongo client for interacting with MongoDB"

    protected_db_names = ("admin", "config", "local")
    default_db = "cctv_logger"
    default_collection = "camera0"

    def __init__(self, uri=None):
        uri = uri or "mongodb://localhost:27017/"
        self._client = PymongoClient(uri)

    def insert_scene(self, scene, timestamp=None, db=None, collection=None):
        """
        Insert a scene as captured by model into database

        :param scene: Scene: scene description as outputted by model
        :param timestamp: datetime: time when scene was captured (if not provided, uses now())
        :param db: str: mongo database name (if not provided, uses object default)
        :param collection: str: mongo collection name (if not provided, uses object default)
        """
        pymongo_collection = self.get_collection(db=db, collection=collection)
        timestamp = timestamp or datetime.now(tz=timezone.utc)

        # Pydantic performs validation for us
        document = MongoDocument(scene=scene, timestamp=timestamp)

        res = pymongo_collection.insert_one(document.dict())
        return res

    def get_latest_scene(self, db=None, collection=None):
        """
        Retrieve the latest scene from the database

        :param db: str: mongo database name (if not provided, uses object default)
        :param collection: str: mongo collection name (if not provided, uses object default)
        """
        pymongo_collection = self.get_collection(db=db, collection=collection)

        res = pymongo_collection.find_one(sort={"timestamp": -1}) or {}
        return res.get('scene')

    def get_collection(self, db=None, collection=None):
        db = db or self.default_db
        assert (
            db not in self.protected_db_names
        ), f"Please use a db name not in {self.protected_db_names}"
        collection = collection or self.default_collection

        return self._client[db][collection]