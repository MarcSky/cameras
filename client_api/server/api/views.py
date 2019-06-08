import json
import geojson
import shapefile
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Advertising, Buildings, Green, Ntopoly
from shapely.geometry import shape
from django.core.serializers import serialize
from django.contrib.gis.geos import Polygon


class GeoList(APIView):
    def get(self, request):
        with open('../test.json', 'r') as f:
            return Response(json.load(f))


def getGeom(bbox):
    bbox = bbox.split(',')
    return Polygon.from_bbox(bbox=(float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])))


def getResponse(object):
    return serialize(
        'geojson',
        object,
        geometry_field='figure',
        fields=('figure')
    )


class GreenView(APIView):
    def get(self, request):
        bbox = request.GET.get('bbox')

        if bbox is not None:
            try:
                object = Green.objects.filter(figure__contained=getGeom(bbox=bbox))
            except Exception as e:
                return Response(e)
        else:
            object = Green.objects.all()

        return Response(
            json.loads(getResponse(object=object)),
            content_type='application/json'
        )


class AdvertisingView(APIView):
    def get(self, request):
        bbox = request.GET.get('bbox')

        if bbox is not None:
            try:
                object = Advertising.objects.filter(figure__contained=getGeom(bbox=bbox))
            except Exception as e:
                return Response(e)
        else:
            object = Advertising.objects.all()

        return Response(
            json.loads(getResponse(object=object)),
            content_type='application/json'
        )


class BuildingsView(APIView):
    def get(self, request):
        bbox = request.GET.get('bbox')

        if bbox is not None:
            try:
                object = Buildings.objects.filter(figure__contained=getGeom(bbox=bbox))
            except Exception as e:
                return Response(e)
        else:
            object = Buildings.objects.all()

        return Response(
            json.loads(getResponse(object=object)),
            content_type='application/json'
        )


class NtopolyView(APIView):
    def get(self, request):
        bbox = request.GET.get('bbox')

        if bbox is not None:
            try:
                object = Ntopoly.objects.filter(figure__contained=getGeom(bbox=bbox))
            except Exception as e:
                return Response(e)
        else:
            object = Ntopoly.objects.all()

        return Response(
            json.loads(getResponse(object=object)),
            content_type='application/json'
        )


class ParserView(APIView):
    def get(self, request):

        def converter(points):
            result = []
            for p in points:
                r = [p[0], p[1]]
                result.append(r)
            return [result]

        sf = shapefile.Reader("../parser/data/advertising/advertising.shp")
        shapes = sf.shapes()
        for i in range(len(shapes)):
            s = json.dumps({
                "coordinates": converter(shapes[i].points),
                "type": "Polygon"
            })
            Advertising.objects.create(figure=shape(geojson.loads(s)).wkt)
        sf.close()
        del shapes

        sf = shapefile.Reader("../parser/data/green/green.shp")
        shapes = sf.shapes()
        for i in range(len(shapes)):
            s = json.dumps({
                "coordinates": converter(shapes[i].points),
                "type": "Point"
            })
            Green.objects.create(figure=shape(geojson.loads(s)).wkt)
        sf.close()
        del shapes

        sf = shapefile.Reader("../parser/data/ntopoly/ntopoly.shp")
        shapes = sf.shapes()
        for i in range(len(shapes)):
            s = json.dumps({
                "coordinates": converter(shapes[i].points),
                "type": "Polygon"
            })
            Ntopoly.objects.create(figure=shape(geojson.loads(s)).wkt)
        sf.close()
        del shapes

        sf = shapefile.Reader("../parser/data/buildings/buildings.shp")
        shapes = sf.shapes()
        for i in range(len(shapes)):
            s = json.dumps({
                "coordinates": converter(shapes[i].points),
                "type": "Polygon"
            })
            Buildings.objects.create(figure=shape(geojson.loads(s)).wkt)
        sf.close()
        del shapes

        return Response("ok")
