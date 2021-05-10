from django.contrib import admin
from .models import CrimeType, Report

# Register your models here.
admin.site.register(CrimeType)
admin.site.register(Report)