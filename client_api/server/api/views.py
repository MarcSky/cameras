import json
import geojson
import shapefile
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Advertising, Buildings, Green, Ntopoly
from shapely.geometry import shape
from django.core.serializers import serialize
from django.contrib.gis.geos import Polygon, GeometryCollection
from django.views.generic import TemplateView
from camera_utils.camera import Camera
from shapely.geometry import LineString, Point, Polygon
import shapely.wkt


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
            try:
                s = json.dumps({
                    "coordinates": converter(shapes[i].points),
                    "type": "Polygon"
                })
                Advertising.objects.create(figure=shape(geojson.loads(s)).wkt)
            except Exception:
                continue
        sf.close()
        del shapes

        sf = shapefile.Reader("../parser/data/green/green.shp")
        shapes = sf.shapes()
        for i in range(len(shapes)):
            try:
                s = json.dumps({
                    "coordinates": converter(shapes[i].points),
                    "type": "Point"
                })
                Green.objects.create(figure=shape(geojson.loads(s)).wkt)
            except Exception:
                continue
        sf.close()
        del shapes

        sf = shapefile.Reader("../parser/data/ntopoly/ntopoly.shp")
        shapes = sf.shapes()
        for i in range(len(shapes)):
            try:
                s = json.dumps({
                    "coordinates": converter(shapes[i].points),
                    "type": "Polygon"
                })
                Ntopoly.objects.create(figure=shape(geojson.loads(s)).wkt)
            except Exception:
                continue
        sf.close()
        del shapes

        sf = shapefile.Reader("../parser/data/buildings/buildings.shp")
        shapes = sf.shapes()
        for i in range(len(shapes)):
            try:
                s = json.dumps({
                    "coordinates": converter(shapes[i].points),
                    "type": "Polygon"
                })
                Buildings.objects.create(figure=shape(geojson.loads(s)).wkt)
            except Exception:
                continue
        sf.close()
        del shapes

        return Response("ok")


class CameraList(APIView):
    def get(self, request):
        cameras = []
        c = Camera(Point(39.7154195712994, 47.2292907934691), LineString([(0, 0), (1, 1)]))
        c.refresh_polygon()
        cameras.append(c)

        c = Camera(Point(39.7144617668104, 47.2288999456851), LineString([(0, 0), (-3, -1)]))
        c.refresh_polygon()
        cameras.append(c)

        from shapely.ops import polygonize
        for points in Buildings.objects.all():
            # t = [(point.x, point.y) for point in points.figure]
            # return(points.figure.coords)
            # print(points.figure.coords)
            # for p in points.figure.coords:
            # print(points.figure.coords)
            # return
            for c in cameras:
                for points in points.figure.coords:
                    c.screen_building(Polygon(points))
                # c.screen_building(Polygon((
                #     (39.7143746, 47.22885759),
                #     (39.71446177, 47.22889995),
                #     (39.71434411, 47.22922511),
                #     (39.71481775, 47.22932136),
                # )))
                # c.screen_building(Polygon((
                #     (100, 100),
                #     (100, 800),
                #     (200, 800),
                #     (200, 100),
                # )))

        object = []
        for c in cameras:
            object.append(c.polygon)

        gc = GeometryCollection(object)
        print(gc)
        return Response(gc)


class IndexView(TemplateView):
    template_name = 'api/index.html'
