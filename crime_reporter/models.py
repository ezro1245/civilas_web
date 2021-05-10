from django.contrib.gis.db import models as gis_models
from django.db.models import Manager as GeoManager
from django.contrib.gis import geos
from django.db import models


# Create your models here.
class CrimeType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Report(models.Model):
    type = models.ForeignKey(CrimeType, on_delete=models.PROTECT, db_column='type')
    location = gis_models.PointField(u"longitude/latitude", geography=True, blank=True, null=True)

    gis = GeoManager()
    objects = models.Manager()

    def __str__(self):
        return self.type.type





