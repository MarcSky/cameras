from django.contrib.gis.db.models import Model, PolygonField

class Advertising(Model):
    figure = PolygonField(srid=4326)


class Buildings(Model):
    figure = PolygonField()

class Green(Model):
    figure = PolygonField()

class Ntopoly(Model):
    figure = PolygonField()
