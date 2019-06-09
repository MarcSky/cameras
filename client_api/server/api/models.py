from django.contrib.gis.db.models import Model, PolygonField, PointField

class Advertising(Model):
    figure = PolygonField(srid=4326, unique=True)

class Buildings(Model):
    figure = PolygonField(srid=4326, unique=True)

class Green(Model):
    figure = PointField(srid=4326, unique=True)

class Ntopoly(Model):
    figure = PolygonField(srid=4326, unique=True)
