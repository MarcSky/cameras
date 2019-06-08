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


class FigureList(APIView):
    def get(self, request):
        t = request.GET.get('t')
        bbox = request.GET.get('bbox')

        if t == 'green':
            if bbox is not None:
                bbox = bbox.split(',')
                geom = Polygon.from_bbox(bbox=(float(bbox[0]),float(bbox[1]),float(bbox[2]),float(bbox[3])))
                object = Green.objects.filter(figure__contained=geom)
            else:
                object = Green.objects.all()
        elif t == 'ntopoly':
            if bbox is not None:
                bbox = bbox.split(',')
                geom = Polygon.from_bbox(bbox=(float(bbox[0]),float(bbox[1]),float(bbox[2]),float(bbox[3])))
                object = Ntopoly.objects.filter(figure__contained=geom)
            else:
                object = Ntopoly.objects.all()
        elif t == 'advertising':
            if bbox is not None:
                bbox = bbox.split(',')
                geom = Polygon.from_bbox(bbox=(float(bbox[0]),float(bbox[1]),float(bbox[2]),float(bbox[3])))
                object = Advertising.objects.filter(figure__contained=geom)
            else:
                object = Advertising.objects.all()
        else:
            if bbox is not None:
                bbox = bbox.split(',')
                geom = Polygon.from_bbox(bbox=(float(bbox[0]),float(bbox[1]),float(bbox[2]),float(bbox[3])))
                object = Advertising.objects.filter(figure__contained=geom)
            else:
                object = Advertising.objects.all()


        data = serialize(
            'geojson',
            object,
            geometry_field='figure',
            fields=('figure')
        )

        return Response(
            json.loads(data),
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
