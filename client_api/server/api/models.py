from django.contrib.gis.db.models import Model, PolygonField, PointField

class Advertising(Model):
    figure = PolygonField(srid=4326)

class Buildings(Model):
    figure = PolygonField(srid=4326)

class Green(Model):
    figure = PointField(srid=4326)

class Ntopoly(Model):
    figure = PolygonField(srid=4326)
