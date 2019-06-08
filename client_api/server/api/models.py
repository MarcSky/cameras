from django.contrib.gis.db import models

class Zipcode(models.Model):
    code = models.CharField(max_length=5)
    poly = models.PolygonField()

    class Meta():
        managed=False
        db_table = 'public\".\"zipcode'


class Elevation(models.Model):
    name = models.CharField(max_length=100)
    rast = models.RasterField()
    class Meta():
        managed=False
        db_table = 'public\".\"elevation'
