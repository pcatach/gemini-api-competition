from datetime import datetime, timezone

from pydantic import BaseModel as PydanticModel
from pymongo import MongoClient as PymongoClient
from pymongo import ASCENDING, DESCENDING

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

    def _get_scene(self, db_collection=None, reverse=True, verbose=False):

        order = -1 if reverse else 1
        res = db_collection.find_one(sort={"timestamp": order}) or {}
        if verbose:
            return res.get("scene"), res.get("timestamp")
        return res.get("scene")

    def get_first_scene(self, db=None, collection=None, verbose=False):
        """
        Retrieve the first scene from the database

        :param db: str: mongo database name (if not provided, uses object default)
        :param collection: str: mongo collection name (if not provided, uses object default)
        """
        pymongo_collection = self.get_collection(db=db, collection=collection)
        return self._get_scene(
            db_collection=pymongo_collection, reverse=False, verbose=verbose
        )

    def get_latest_scene(self, db=None, collection=None, verbose=False):
        """
        Retrieve the latest scene from the database

        :param db: str: mongo database name (if not provided, uses object default)
        :param collection: str: mongo collection name (if not provided, uses object default)
        """
        pymongo_collection = self.get_collection(db=db, collection=collection)
        return self._get_scene(db_collection=pymongo_collection, verbose=verbose)

    def get_scenes_in_timerange(
        self, start_time, end_time=None, db=None, collection=None, verbose=False
    ):
        """
        Retrieve the scenes from the database with timestamp within a range.

        :param start_time: datetime: left side of timestamp range
        :param end_time: datetime: right side of timestamp range (if not provided, uses now)
        :param db: str: mongo database name (if not provided, uses object default)
        :param collection: str: mongo collection name (if not provided, uses object default)
        """

        pymongo_collection = self.get_collection(db=db, collection=collection)

        end_time = end_time or datetime.now(tz=timezone.utc)
        # Might need to convert times if timezone-naive to timezone-aware
        if start_time.tzinfo is None:
            start_time = datetime.fromtimestamp(start_time.timestamp(), timezone.utc)
        if end_time.tzinfo is None:
            end_time = datetime.fromtimestamp(end_time.timestamp(), timezone.utc)
        assert start_time < end_time, "Not a valid timestamp range!"

        res = pymongo_collection.find(
            {"timestamp": {"$gte": start_time, "$lte": end_time}}
        )
        if verbose:
            return [(doc["scene"], doc["timestamp"]) for doc in res]
        return [doc["scene"] for doc in res]

    def get_collection(self, db=None, collection=None):
        db = db or self.default_db
        assert (
            db not in self.protected_db_names
        ), f"Please use a db name not in {self.protected_db_names}"
        collection = collection or self.default_collection

        return self._client[db][collection]
