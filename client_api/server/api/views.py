from django.shortcuts import render
from django.http import Http404
import json
import geojson
import shapefile
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Advertising, Buildings, Green, Ntopoly
from django.contrib.gis.geos import Point, GeometryCollection
from shapely.geometry import shape
import shapely.wkt
from django.core.serializers import serialize

class GeoList(APIView):

    def get(self, request):
        with open('../test.json', 'r') as f:
            return Response(json.load(f))

class FigureList(APIView):

    def get(self, request):
        # response = []
        # figures = Advertising.objects.all()
        # for f in figures:
        #     g1 = shapely.wkt.loads(f.figure)
        #     g2 = shapely.geometry.mapping(g1)
        #     response.append(g2)
        # return Response(geojson.dumps(response))
        return Response(serialize('geojson', Advertising.objects.all(),
                  geometry_field='point',
                  fields=('figure',)))


def converter(points):
    result = []
    for p in points:
        r = [p[0],p[1]]
        result.append(r)
    result = [result]
    return result

class ParserView(APIView):

    def get(self, request):
        from django.contrib.gis.geos import GEOSGeometry

        sf = shapefile.Reader("../parser/data/advertising/advertising.shp")
        shapes = sf.shapes()
        for i in range(len(shapes)):
            s = json.dumps({
                "coordinates": converter(shapes[i].points),
                "type": "Polygon"
            })
            g1 = geojson.loads(s)
            g2 = shape(g1)
            Advertising.objects.create(figure=g2.wkt)
        sf.close()
        del shapes
        return Response()

        # sf = shapefile.Reader("../parser/data/green/green.shp")
        # shapes = sf.shapes()
        # for i in range(len(shapes)):
        #     green = Green()
        #     green.figure = shapes[i].points
        #     green.save()
        # sf.close()
        # del shapes

        sf = shapefile.Reader("../parser/data/ntopoly/ntopoly.shp")
        shapes = sf.shapes()
        for i in range(len(shapes)):
            print(type(shapes[i].points))
        sf.close()
        del shapes

        sf = shapefile.Reader("../parser/data/buildings/buildings.shp")
        shapes = sf.shapes()
        for i in range(len(shapes)):
            print(type(shapes[i].points))
        sf.close()
        del shapes

        return Response()
