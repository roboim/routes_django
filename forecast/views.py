from django.http import HttpResponse
from django.shortcuts import render

from forecast.engine import get_routes


# Create your views here.
def read_routes_from_csv(request):
    prepared_data = get_routes()
    # header = prepared_data.pop('header')
    routes = [route for number, route in prepared_data.items()]

    # return HttpResponse(f'<br/> {routes}')
    # return HttpResponse(f'{header} <br/> {routes}')
    return render(request, 'forecast/default_routes.html', {'header': 'Доступные маршруты', 'routes': routes})
    # return render(request, 'forecast/default_routes.html', {'header': header, 'routes': routes})