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
from crime_reporter import forms
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


# Give me a set of longitude and latitude and I´ll return a set of reports in a radius around the point
#
def get_reports(longitude, latitude):

    # We transform the longitude and latitude values to a geos point
    current_point = geos.fromstr("POINT(%s %s)" % (longitude, latitude))
    # Radius value to get crime reports from
    distance_from_point = {'km': 1}

    # We get the crime reports inside the radius given above
    reports = Report.gis.filter(
                    location__distance_lte=(
                            current_point, measure.D(**distance_from_point)
                    )).annotate(
                        distance=Distance('location', current_point)
                    ).order_by('distance')

    # Parse the reports into a JSON response readable by the front end
    for report in reports:
        distance_from_point = str(report.distance)
        distance_from_point = distance_from_point.replace('m', '')
        distance_from_point = float(distance_from_point)

        report.distance = distance_from_point

    return reports


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


@csrf_exempt
def index(request):

    address_string = request.GET.get('address')

    if not (address_string is None):
        is_json = True
    else:
        is_json = False

    reports = []

    if not is_json:
        form = forms.AddressForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            point_location = geocode_address(address)
            if location:
                latitude, longitude = point_location
                reports = get_reports(longitude, latitude)

        return render(
            request,
            'index.html',
            {'reports': reports}
        )

    elif is_json:
        point_location = geocode_address(address_string)
        if location:
            latitude, longitude = point_location
            reports = get_reports(longitude, latitude)

        reports_dict = {}
        i = 1
        for x in reports:

            print(type(x))

            report = {i: str(x.type)}
            reports_dict.update(report)

            i += 1

        reports_final = {"results": reports_dict, "status": "OK"}

        reports_json = json.dumps(reports_final, indent=4, ensure_ascii=False)

        print(reports_json)

        return HttpResponse(
            reports_json, content_type='application/json'
        )

