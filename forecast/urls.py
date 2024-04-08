from django.urls import path
from rest_framework.routers import DefaultRouter

from forecast.views import read_routes_from_csv, update_routes_from_csv, bear_route

app_name = 'forecast'

r = DefaultRouter()

urlpatterns = [
    path('routes/', read_routes_from_csv, name='routes'),
    path('routes/update/', update_routes_from_csv, name='routes_update'),
    path('bearroute/', bear_route, name='bearroute'),
] + r.urls
