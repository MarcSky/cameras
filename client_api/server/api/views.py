import json
from rest_framework.views import APIView
from rest_framework.response import Response


class GeoList(APIView):

    def get(self):
        with open('../test.json', 'r') as f:
            return Response(json.load(f))
