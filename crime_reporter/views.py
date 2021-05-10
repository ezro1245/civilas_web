from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis import geos, measure
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import Point
from django.core import serializers
from django.contrib.gis.geos import GEOSGeometry

from geopy import *
import json

from .models import Report, CrimeType
from keys import maps_key


# Create your views here.

# Give me an address (str) and I´ll return a set of longitude and latitude corresponding to that point
#
def geocode_address(address):

    address = address.encode('utf-8')
    geocoder = GoogleV3(api_key=maps_key)
    try:
        _, latitude_longitude = geocoder.geocode(address)
    except ValueError:
        return None
    else:
        return latitude_longitude


@csrf_exempt
def add_report(request):

    address = request.GET.get('address')
    type_crime = request.GET.get('type')

    if not (address is None):
        point_location = geocode_address(address)
        crime_object = CrimeType.objects.get(type=type_crime)
        data_coordinates = [[point_location[1], point_location[0]]]

        for coordinate in data_coordinates:

            point = {
                "type": "Point",
                "coordinates": coordinate
            }

            Report.objects.create(type=crime_object, location=GEOSGeometry(json.dumps(point)))

    return render(
        request,
        'add_report.html'
    )