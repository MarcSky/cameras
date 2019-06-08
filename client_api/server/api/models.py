from django.contrib.gis.db import models

class Advertising(models.Model):
    figure = models.PolygonField()

    class Meta():
        managed=False
        db_table = 'advertising'

class Buildings(models.Model):
    figure = models.PolygonField()

    class Meta():
        managed=False
        db_table = 'buildings'

class Green(models.Model):
    figure = models.PolygonField()

    class Meta():
        managed=False
        db_table = 'green'

class Ntopoly(models.Model):
    figure = models.PolygonField()

    class Meta():
        managed=False
        db_table = 'ntopoly'
