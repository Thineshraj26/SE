from django.contrib import admin
from CatDatabase.models import Cat, Treatment, Appointment, Medication, Report

# Register your models here.
admin.site.register(Cat)
admin.site.register(Treatment)
admin.site.register(Appointment)
admin.site.register(Medication)
admin.site.register(Report)