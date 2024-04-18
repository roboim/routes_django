import os

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response

from forecast.engine import read_routes, get_routes
from forecast.models import Route, Category

DATA_CSV_FILE = os.getenv('DATA_CSV_FILE')


# Create your views here.
def read_routes_from_csv(request) -> render:
    data_routes = read_routes(DATA_CSV_FILE)
    routes = [route for number, route in data_routes.items()]
    return render(request, 'forecast/default_routes.html', {'header': 'Доступные маршруты', 'routes': routes})


def update_routes_from_csv(request) -> render:
    """
    Обновление маршрута происходит по месту старта и финиша
    """
    response_routes = list()
    category = request.GET.get('filter')
    if category:
        category_db, _ = Category.objects.get_or_create(name=category)
        data_routes = read_routes(DATA_CSV_FILE)
        for route, route_details in data_routes.items():
            route_db_id = int(route_details['\ufeff№'])
            name = route_details['Река']
            area = route_details['Область']
            start_point = route_details['Место старта']
            end_point = route_details['Место финиша']
            distance_km = float(route_details['Дистанция'])
            year_journey = int(route_details['Год']) if route_details['Год'] else 0
            qty_days = int(route_details['Кол-во дней'])
            distance_from_city = float(route_details['От Москвы, км'])
            feature = route_details['Особенность']
            camping_places = route_details['Стоянки']
            coord_camping_places = route_details['Координаты стоянок']
            picture_links = route_details['Фотоотчёт']
            coord_start_point = route_details['Координаты старта']
            coord_end_point_p = route_details['Координаты финиша']
            try:
                cur_route = Route.objects.get(start_point=start_point, end_point=end_point)
                if cur_route:
                    if year_journey > cur_route.year_journey:
                        cur_route.route_db_id = route_db_id
                        cur_route.name = name
                        cur_route.area = area
                        cur_route.distance_km = distance_km
                        cur_route.year_journey = year_journey
                        cur_route.qty_days = qty_days
                        cur_route.distance_from_city = distance_from_city
                        cur_route.feature = feature
                        cur_route.camping_places = camping_places
                        cur_route.picture_links = picture_links
                        cur_route.coord_start_point = coord_start_point
                        cur_route.coord_end_point_p = coord_end_point_p
                        cur_route.save()
                        response_routes.append(cur_route)
            except Exception as error:
                new_route = Route.objects.create(route_db_id=route_db_id, name=name, area=area,
                                                 start_point=start_point,
                                                 end_point=end_point, distance_km=distance_km,
                                                 year_journey=year_journey, qty_days=qty_days,
                                                 distance_from_city=distance_from_city, feature=feature,
                                                 camping_places=camping_places,
                                                 coord_camping_places=coord_camping_places,
                                                 picture_links=picture_links, coord_start_point=coord_start_point,
                                                 coord_end_point_p=coord_end_point_p, category=category_db)
                response_routes.append(new_route)

        return render(request, 'forecast/updated_routes.html',
                      {'header': f'Добавлены маршруты категории: {category}.', 'routes': response_routes})


def bear_route(request):
    return select_input_data(request, 1)


def query_route(request):
    return select_input_data(request, 2)


def select_input_data(request, input_mode: int):
    prepared_data = get_routes(input_mode, 2, False, request)
    if 'error' in prepared_data.keys():
        return JsonResponse(prepared_data)
    header = prepared_data.pop('header')
    info = prepared_data.pop('info')
    top_routes = [top_route for number, top_route in prepared_data['top_routes'].items()]
    routes = [route for number, route in prepared_data['routes'].items()]
    return render(request, 'forecast/best_routes.html',
                  {'header': header, 'routes': routes, 'info': info, 'top_routes': top_routes})


def error_prompt(status_data: bool, error_data: str, code_data: int) -> Response:
    """
    Вернуть сообщение об ошибке
    """
    return Response({'Status': status_data, 'Error': error_data}, status=code_data)
