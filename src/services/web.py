import json

from collections import Counter
from twisted.web import resource

from src.mongo_client import MongoClient
from src.utils import today_start, sanitise_string


class CCTVLoggerServer(resource.Resource):
    isLeaf = True
    client = MongoClient()

    def render_GET(self, request):
        scene = self.client.get_latest_scene()
        response = {"data": scene}
        request.setHeader("Content-Type", "application/json")
        # warning: remove in production!
        request.setHeader("Access-Control-Allow-Origin", "*")
        return json.dumps(response).encode("utf-8")

    def _check_repeated(self, start_time=None, end_time=None, thresh=5):
        """
        Returns a tuple with persons and vehicles that repeateldy shwo up in time range.

        :param start_time: datetime: left side of timestamp range (default: start of today)
        :param end_time: datetime: right side of timestamp range (default: now)
        :param thresh: int: minimum number of counts to consider a repeat pattern 'common'
            (default: 5)
        """
        start_time = today_start if start_time is None else start_time
        scenes_in_range = self.client.get_scenes_in_timerange(start_time, end_time)
        persons = Counter()
        vehicles = Counter()
        for scene in scenes_in_range:
            persons += Counter(
                sanitise_string(p.get("clothes")) for p in scene.get("persons")
            )
            vehicles += Counter(
                (v.get("type"), v.get("color")) for v in scene.get("vehicles")
            )

        common_persons = {p: count for p, count in persons.items() if count > thresh}
        common_vehicles = {p: count for p, count in persons.items() if count > thresh}
        return common_persons, common_vehicles
