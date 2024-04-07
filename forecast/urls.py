from django.urls import path
from rest_framework.routers import DefaultRouter

from forecast.views import read_routes_from_csv, update_routes_from_csv

app_name = 'forecast'

r = DefaultRouter()

urlpatterns = [
    path('routes/', read_routes_from_csv, name='routes'),
    path('routes/update/', update_routes_from_csv, name='routes_update'),
] + r.urls
