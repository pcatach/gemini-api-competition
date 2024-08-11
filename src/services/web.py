import json

from twisted.web import resource

from src.mongo_client import MongoClient
from src.utils import today_start, summarise_scenes


class CCTVLoggerServer(resource.Resource):
    isLeaf = True
    client = MongoClient()

    def render_GET(self, request):
        scene_data = self.client.get_latest_scene()
        # repeated_counts = self._check_repeated()
        response = {
            "scene_data": scene_data,
            # "repeated_counts": repeated_counts
        }
        request.setHeader("Content-Type", "application/json")
        return json.dumps(response, default=str).encode("utf-8")

    def _check_repeated(self, start_time=None, end_time=None, thresh=5):
        """
        Returns a tuple with persons and vehicles that repeatedly show up in time range.

        :param start_time: datetime: left side of timestamp range (default: start of today)
        :param end_time: datetime: right side of timestamp range (default: now)
        :param thresh: int: minimum number of counts to consider a repeat pattern 'common'
            (default: 5)
        """
        start_time = today_start if start_time is None else start_time
        scenes_in_range = self.client.get_scenes_in_timerange(start_time, end_time)
        persons, vehicles = summarise_scenes(scenes_in_range, thresh)

        common_persons = {p: count for p, count in persons.items() if count > thresh}
        common_vehicles = {v: count for v, count in vehicles.items() if count > thresh}
        return common_persons, common_vehicles
