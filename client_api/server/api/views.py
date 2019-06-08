from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
import json

# Create your views here.


class GeoList(APIView):

    def get(self, request):
        with open('../test.json', 'r') as f:
            return Response(json.load(f))
