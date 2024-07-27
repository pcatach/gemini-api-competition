import json

from twisted.web import resource

from src.mongo_client import MongoClient


class CCTVLoggerServer(resource.Resource):
    isLeaf = True
    client = MongoClient()

    def render_GET(self, request):
        scene = self.client.get_latest_scene()
        response = {"data": scene}
        request.setHeader("Content-Type", "application/json")
        return json.dumps(response).encode("utf-8")
