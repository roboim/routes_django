from django.urls import path
from rest_framework.routers import DefaultRouter

from forecast.views import read_routes_from_csv

app_name = 'forecast'

r = DefaultRouter()

urlpatterns = [
    path('route/', read_routes_from_csv, name='route'),
] + r.urls
