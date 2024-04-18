import csv
import os
from datetime import datetime, timedelta
from pprint import pprint

from django.core.exceptions import BadRequest
from fpdf import FPDF

from forecast.models import Route, RouteWeather
from forecast.open_meteo_data import OpenMeteoData
from vk_api import VkGroupAdmin

DATA_CSV_FILE = os.getenv('DATA_CSV_FILE')


class RouteData:
    """Полное описание маршрута"""

    def __init__(self, route_n: int, route_db_n: int, name: str, area_p: str, start_point_p: str,
                 end_point_p: str,
                 distance_km_p: float, year_journey_p: int, qty_days_p: int, distance_from_city_p: float,
                 feature_p: str,
                 camping_places_p: str, coord_camping_places_p: str, picture_links_p: str,
                 coord_start_point_p: str, coord_end_point_p: str, category_p: int, name_p: str, temperature_p: float,
                 temperature_2m_max_p: str, temperature_2m_min_p: str, sunrise_p: str, sunset_p: str,
                 wind_p: float, wind_gust_p: float, clouds_p: float, description: str, description_p: str,
                 precipitation_sum_p: float, precipitation_sum_l: str, precipitation: str):
        self.route_n = route_n  # ['Маршрут']
        self.route_db_n = route_db_n  # ['№']
        self.name = name  # ['Река']
        self.area_p = area_p  # ['Область']
        self.start_point_p = start_point_p  # ['Место старта']
        self.end_point_p = end_point_p  # ['Место финиша']
        self.distance_km_p = distance_km_p  # ['Дистанция']
        self.year_journey_p = year_journey_p  # ['Год']
        self.qty_days_p = qty_days_p  # ['Кол-во дней']
        self.distance_from_city_p = distance_from_city_p  # ['От Москвы, км']
        self.feature_p = feature_p  # ['Особенность']
        self.camping_places_p = camping_places_p  # ['Стоянки']
        self.coord_camping_places_p = coord_camping_places_p  # ['Координаты стоянок']
        self.picture_links_p = picture_links_p  # ['Фотоотчёт']
        self.coord_start_point_p = coord_start_point_p  # ['Координаты старта']
        self.coord_end_point_p = coord_end_point_p  # ['Координаты финиша']
        self.category_p = category_p  # ['Категория']
        self.name_p = name_p  # ['Ответ сервера по месту прогноза']
        self.temperature_p = temperature_p  # ['Температура']
        self.temperature_2m_max_p = temperature_2m_max_p  # ['Максимальная температура по дням']
        self.temperature_2m_min_p = temperature_2m_min_p  # ['Минимальная температура по ночам']
        self.sunrise_p = sunrise_p  # ['Рассвет']
        self.sunset_p = sunset_p  # ['Закат']
        self.wind_p = wind_p  # ['Ветер']
        self.wind_gust_p = wind_gust_p  # ['Порыв ветра']
        self.clouds_p = clouds_p  # ['Облачность']
        self.description = description  # ['Погода по дням']
        self.description_p = description_p  # ['Погода']
        self.precipitation_sum_p = precipitation_sum_p  # ['Осадки']
        self.precipitation_sum_l = precipitation_sum_l  # ['Осадки по дням']
        self.precipitation = precipitation  # ['Осадки качественно']

    def route_clear(self) -> None:
        """Полностью очистить данные по маршруту"""
        self.route_n = 0  # ['Маршрут']
        self.route_db_n = 0  # ['№']
        self.name = ""  # ['Река']
        self.area_p = ""  # ['Область']
        self.start_point_p = ""  # ['Место старта']
        self.end_point_p = ""  # ['Место финиша']
        self.distance_km_p = 0  # ['Дистанция']
        self.year_journey_p = 0  # ['Год']
        self.qty_days_p = 0  # ['Кол-во дней']
        self.distance_from_city_p = 0  # ['От Москвы, км']
        self.feature_p = ""  # ['Особенность']
        self.camping_places_p = ""  # ['Стоянки']
        self.coord_camping_places_p = ""  # ['Координаты стоянок']
        self.picture_links_p = ""  # ['Фотоотчёт']
        self.coord_start_point_p = ""  # ['Координаты старта']
        self.coord_end_point_p = ""  # ['Координаты финиша']
        self.category_p = 0  # ['Категория']
        self.name_p = ""  # ['Ответ сервера по месту прогноза']
        self.temperature_p = 0.0  # ['Температура']
        self.temperature_2m_max_p = ""  # ['Максимальная температура по дням']
        self.temperature_2m_min_p = ""  # ['Минимальная температура по ночам']
        self.sunrise_p = ""  # ['Рассвет']
        self.sunset_p = ""  # ['Закат']
        self.wind_p = 0.0  # ['Ветер']
        self.wind_gust_p = 0.0  # ['Порыв ветра']
        self.clouds_p = 0.0  # ['Облачность']
        self.description = ""  # ['Погода по дням']
        self.description_p = ""  # ['Погода']
        self.precipitation_sum_p = 0.0  # ['Осадки']
        self.precipitation_sum_l = ""  # ['Осадки по дням']
        self.precipitation = ""  # ['Осадки качественно']

    def read_active_route(self, route_data) -> None:
        """Прочитать данные по маршруту"""
        self.route_n = route_data.id  # ['Маршрут']
        self.route_db_n = route_data.route_db_id  # ['№']
        self.name = route_data.name  # ['Река']
        self.area_p = route_data.area  # ['Область']
        self.start_point_p = route_data.start_point  # ['Место старта']
        self.end_point_p = route_data.end_point  # ['Место финиша']
        self.distance_km_p = route_data.distance_km  # ['Дистанция']
        self.year_journey_p = route_data.year_journey  # ['Год']
        self.qty_days_p = route_data.qty_days  # ['Кол-во дней']
        self.distance_from_city_p = route_data.distance_from_city  # ['От Москвы, км']
        self.feature_p = route_data.feature  # ['Особенность']
        self.camping_places_p = route_data.camping_places  # ['Стоянки']
        self.coord_camping_places_p = route_data.coord_camping_places  # ['Координаты стоянок']
        self.picture_links_p = route_data.picture_links  # ['Фотоотчёт']
        self.coord_start_point_p = route_data.coord_start_point  # ['Координаты старта']
        self.coord_end_point_p = route_data.coord_end_point_p  # ['Координаты финиша']
        self.category_p = route_data.category  # ['Категория']

    def copy_route(self, route_number, route_data) -> None:
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                setattr(self, attr, route_data[attr])

    def make_dict(self) -> dict:
        route_dict = dict()
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                route_dict[attr] = getattr(self, attr)
        return route_dict

    def write_route_forecast(self, route_weather) -> None:
        """Записать данные маршрута по погоде"""
        self.name_p = route_weather.name_p
        self.temperature_p = route_weather.temperature
        self.temperature_2m_max_p = route_weather.temperature_2m_max
        self.temperature_2m_min_p = route_weather.temperature_2m_min
        self.sunrise_p = route_weather.sunrise
        self.sunset_p = route_weather.sunset
        self.wind_p = route_weather.wind
        self.wind_gust_p = route_weather.wind_gust
        self.clouds_p = route_weather.clouds_p
        self.description = route_weather.description
        self.description_p = route_weather.description_p
        self.precipitation_sum_p = route_weather.precipitation_sum_p
        self.precipitation_sum_l = route_weather.precipitation_sum_l
        self.precipitation = route_weather.precipitation

    def route_pr(self) -> None:
        """Вывод названия реки и области"""
        pprint(self.name)
        pprint(self.area_p)


def read_routes(file_csv) -> dict:
    """ Чтение csv через rDictReader.
    # особенности: читаем только построчно, файл закрывать нельзя, можно читать сколь угодно большие файлы
    # не нужно считать номера колонок, т.к. у них теперь есть имена
    """
    with open(file_csv, "r", encoding="UTF-8") as f:
        routes_reader = csv.DictReader(f)
        count = 0
        data_routes = dict()
        for row in routes_reader:
            count += 1
            data_routes.setdefault(count, row)
            # for field in row:
            # print(field)
            # print(row[field])
    # print(data_routes)
    print(f"В этом файле указано количество маршрутов: {count}")
    return data_routes


def manual_input(test_value) -> dict:
    """Обработка входящего запроса"""
    data_request = dict()
    if test_value == 0:
        weekend = input("\nТребуется прогноз на ближайшие субботу и воскресенье на 2 дня до 160 км от Москвы? ")
        weekend = weekend.lower()
        if weekend == "да" or weekend == "1":
            test_value = 1
        else:
            test_value = 0
    if test_value == 0:
        target_days = input("\nУкажите количество дней:")
        try:
            target_days = int(target_days)
            data_request.setdefault("target_days", target_days)
        except ValueError:
            print("Некорректный ввод")
            exit(101)
        if int(target_days) > 14:
            target_days = "14"
        start_day = input("\nУкажите дату начала маршрута(ГГГГ-ММ-ДД):")
        try:
            start_day = str(start_day)
            data_request.setdefault("start_day", start_day)
        except ValueError:
            print("Некорректный ввод")
            exit(1001)
        start_day_d = datetime.strptime(start_day, "%Y-%m-%d").date()
        finish_day = start_day_d + timedelta(int(target_days) - 1)
        data_request.setdefault("finish_day", finish_day)
        today_now = datetime.now().date()
        finish_max_day = today_now + timedelta(14)
        if today_now > start_day_d or start_day_d > finish_max_day or today_now > finish_day or finish_day > finish_max_day:
            print(f"\nДата начала и завершения маршрута должны быть в интервале: {today_now} - {finish_max_day}")
            exit(1002)
        target_distancemin_km = input("\nУкажите минимальную удалённость от Москвы в км:")
        try:
            target_distancemin_km = int(target_distancemin_km)
            data_request.setdefault("target_distancemin_km", target_distancemin_km)
        except ValueError:
            print("Некорректный ввод")
            exit(102)
        target_distancemax_km = input("\nУкажите максимальную удалённость от Москвы в км:")
        try:
            target_distancemax_km = int(target_distancemax_km)
            data_request.setdefault("target_distancemax_km", target_distancemax_km)
        except ValueError:
            print("Некорректный ввод")
            exit(103)
        print("\n")
    elif test_value == 1:
        # Ближайшая суббота
        d_start = datetime.today().strftime('%Y-%m-%d')
        d = datetime.strptime(d_start, '%Y-%m-%d')
        t = timedelta((7 + 5 - d.weekday()) % 7)

        target_days = "2"
        start_day = (d + t).strftime('%Y-%m-%d')
        start_day_d = datetime.strptime(start_day, "%Y-%m-%d").date()
        finish_day = start_day_d + timedelta(int(target_days) - 1)
        target_distancemin_km = "1"
        target_distancemax_km = "300"  # 300 км

        data_request.setdefault("target_days", target_days)
        data_request.setdefault("start_day", start_day)
        data_request.setdefault("finish_day", finish_day)
        data_request.setdefault("target_distancemin_km", target_distancemin_km)
        data_request.setdefault("target_distancemax_km", target_distancemax_km)

    # pprint(data_request)
    return data_request


def prepare_query(request):
    data_request = dict()
    target_days = request.GET.get('days')
    start_day = request.GET.get('start')
    target_distancemin_km = request.GET.get('min_km')
    target_distancemax_km = request.GET.get('max_km')
    return data_request


def split_lat_lon(coord_str) -> dict:
    """Разделить строку на широту и долготу"""
    coords = coord_str.split(', ')
    coords_d = dict()
    coords_d.setdefault("lat", coords[0])
    coords_d.setdefault("lon", coords[1])
    return coords_d


def route_info_print(best_offer_r, route_r, i_r) -> list:
    """Вывод информации в файл прогноз.txt"""
    wmo_dict = {"0": "Чистое небо",
                "1": "В основном ясно",
                "2": "Переменная облачность",
                "3": "Пасмурная погода",
                "45": "Туман",
                "48": "Туман осаждающийся в иней",
                "51": "Моросящий дождь: легкий",
                "53": "Моросящий дождь: умеренный",
                "55": "Моросящий дождь: густой и интенсивный",
                "56": "Моросящий дождь: лёгкой интенсивности",
                "57": "Моросящий дождь: высокой интенсивности",
                "61": "Дождь: небольшой",
                "63": "Дождь: умеренный",
                "65": "Дождь: сильной интенсивности",
                "66": "Ледяной дождь: лёгкой интенсивности",
                "67": "Ледяной дождь: высокой интенсивности",
                "71": "Выпадение снега: незначительное",
                "73": "Выпадение снега: умеренное",
                "75": "Снегопад: большая интенсивность",
                "77": "Ледяной снег",
                "80": "Ливневые дожди: незначительные",
                "81": "Ливневые дожди: умеренные",
                "82": "Ливневые дожди: сильные",
                "85": "Небольшой снегопад",
                "86": "Сильный снегопад",
                "95": "Гроза: слабая или умеренная",
                "96": "Гроза с небольшим градом",
                "99": "Гроза с сильным градом",
                }
    name = best_offer_r[route_r]['name']
    area_p = best_offer_r[route_r]['area_p']
    start_point_p = best_offer_r[route_r]['start_point_p']
    end_point_p = best_offer_r[route_r]['end_point_p']
    distance_km_p = best_offer_r[route_r]['distance_km_p']
    year_journey_p = best_offer_r[route_r]['year_journey_p']
    qty_days_p = best_offer_r[route_r]['qty_days_p']
    distance_from_city_p = best_offer_r[route_r]['distance_from_city_p']
    feature_p = best_offer_r[route_r]['feature_p']
    camping_places_p = best_offer_r[route_r]['camping_places_p']
    coord_camping_places_p = best_offer_r[route_r]['coord_camping_places_p']
    picture_links_p = best_offer_r[route_r]['picture_links_p']
    coord_start_point_p = best_offer_r[route_r]['coord_start_point_p']
    coord_end_point_p = best_offer_r[route_r]['coord_end_point_p']
    name_p = best_offer_r[route_r]['name_p']
    temperature_p = best_offer_r[route_r]['temperature_p']
    temperature_2m_max_p = best_offer_r[route_r]['temperature_2m_max_p']
    temperature_2m_min_p = best_offer_r[route_r]['temperature_2m_min_p']
    sunrise_p = best_offer_r[route_r]['sunrise_p']
    sunset_p = best_offer_r[route_r]['sunset_p']
    wind_p = best_offer_r[route_r]['wind_p']
    wind_gust_p = best_offer_r[route_r]['wind_gust_p']
    clouds_p = best_offer_r[route_r]['clouds_p']
    description_p = best_offer_r[route_r]['description_p']
    try:
        description_data = description_p[1:-1]
        description_data = str.replace(description_data, ' ', '')
        description_list = description_data.split(',')
        description_worst_case = max(description_list)
        # description = [wmo_dict[str(x)] for x in description_p]
        description = wmo_dict[str(description_worst_case)]
    except KeyError:
        description = "Что-то неизвестное по коду погоды"
    precipitation_sum_p = best_offer_r[route_r]['precipitation_sum_p']
    precipitation_sum_l = best_offer_r[route_r]['precipitation_sum_l']
    precipitation_p = best_offer_r[route_r]['precipitation']

    list_out = dict()
    list_out['Маршрут №'] = str(i_r)
    list_out['Важно'] = precipitation_p
    list_out['Маршрут по'] = name
    list_out['Нитка маршрута'] = start_point_p + " - " + end_point_p + "."
    list_out['на'] = str(qty_days_p) + " дня(ей)."
    list_out['Длина маршрута'] = str(distance_km_p) + " км."
    list_out['Важные комментарии'] = feature_p + "."
    list_out['Область'] = area_p + "."
    list_out['Координаты старта'] = coord_start_point_p
    list_out['Координаты финиша'] = coord_end_point_p
    list_out['Расположен примерно в'] = str(distance_from_city_p) + " км от Москвы."
    list_out['Координаты стоянки'] = coord_camping_places_p + "."
    list_out['Стоянок'] = camping_places_p + "."
    list_out['Погода'] = str(description) + "."
    list_out['Осадки'] = str(precipitation_sum_l) + "."
    list_out['Температура в пункте'] = name_p
    list_out['днём до'] = str(temperature_2m_max_p) + " гр,"
    list_out['ночью до'] = str(temperature_2m_min_p) + " гр,"
    # list_out['среднее значение'] = str(temperature_p) + " гр,"
    list_out['облачность'] = str(clouds_p)[0:5] + ","
    list_out['скорость ветра'] = str(wind_p)[0:5] + " м/с,"
    list_out['с порывами до'] = str(wind_gust_p)[0:5] + " м/с,"
    list_out['в часовом поясе МСК время восхода'] = str(sunrise_p) + ","
    list_out['заката'] = str(sunset_p) + "."
    list_out['Фотоотчёт'] = picture_links_p + ","
    list_out['пройден в'] = str(year_journey_p) + " г."
    links = make_helpful_link(coord_start_point_p, coord_end_point_p)
    list_out['Brouter'] = links['Brouter']
    list_out["Прогноз от Яндекс.Погоды на ближайшие 10 дней"] = links['Прогноз от Яндекс.Погоды на ближайшие 10 дней']

    # Файл больше не создаём, интерфейс - браузер.
    # with open("прогноз.txt", "a", encoding='UTF-8') as file1:
    #     file1.write(str_forecast)

    route_item_p = [name, start_point_p, end_point_p, list_out]
    return route_item_p


def make_helpful_link(coord_start_p, coord_end_p) -> dict:
    """Создание ссылок для создания нитки маршрута и прогноза погоды"""
    p1 = split_lat_lon(coord_start_p)
    p2 = split_lat_lon(coord_end_p)
    # https://brouter.de/brouter-web/#map=5/57.140/41.950/standard&lonlats=33.713608,58.107636;33.802872,58.137824&profile=river
    value_1 = "https://brouter.de/brouter-web/#map=5/57.140/41.950/standard&lonlats=" + p1["lon"] + "," + p1["lat"] + \
              ";" + p2["lon"] + "," + p2["lat"] + "&profile=river"
    # https://yandex.ru/pogoda/details/10-day-weather?lat=57.6638&lon=34.7665&via=ms#8
    value_2 = "https://yandex.ru/pogoda/details/10-day-weather?lat=" + p1["lat"] + "&lon=" + p1["lon"] + "&via=ms#8"
    dict_out = dict()
    dict_out['Brouter'] = value_1
    dict_out["Прогноз от Яндекс.Погоды на ближайшие 10 дней"] = value_2
    return dict_out


def make_pdf(text, filename) -> None:
    """Создать pdf файл"""
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 12
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', fontsize_pt)

    with open(text, "r", encoding='UTF-8') as f:
        for x in f:
            pdf.cell(50, 5, txt=x, ln=1, align='L')
    pdf.output(filename)


def load_or_get_weather_data(active_route, route_forecast, start_day, finish_day):
    """Проверить полученные ранее данные, если они были не так давно записаны, то выгружать из БД"""
    try:

        # a = RouteWeather.objects.create(route_id=active_route.route_n, start_day=start_day, finish_day=finish_day)
        # a.save()
        coord_data = split_lat_lon(active_route.coord_start_point_p)
        route_weather = RouteWeather.objects.filter(route_id=active_route.route_n, start_day=start_day,
                                                    finish_day=finish_day)  # .order_by('-dt')
        if route_weather:
            result = route_weather.latest('dt')
            print(result.dt)
            target_time = datetime.now() - timedelta(hours=4)
            target_time = target_time.astimezone()
            delta_time = result.dt - target_time
            print(delta_time)
            if delta_time > timedelta(seconds=0):
                return result

        forecast_get = route_forecast.get_open_meteo_data(coord_data['lat'], coord_data['lon'], start_day, finish_day)
        create_forecast_item = create_route_weather_forecast(active_route, start_day, finish_day, forecast_get)
        return create_forecast_item

    except Exception as error:
        print(error)
        return True


def create_route_weather_forecast(active_route, start_day, finish_day, result):
    try:
        start_day_d = datetime.strptime(start_day, "%Y-%m-%d").date()
        name = str(result['latitude'])
        name += ", " + str(result['longitude'])
        temperature_l = result['hourly']['temperature_2m']
        temperature = sum(temperature_l) / len(temperature_l)
        temperature_2m_max = str(result['daily']['temperature_2m_max'])
        temperature_2m_min = str(result['daily']['temperature_2m_min'])
        precipitation_sum_l = result['daily']['precipitation_sum']
        precipitation_sum = sum(precipitation_sum_l) / len(precipitation_sum_l)
        sunrise = result['daily']['sunrise'][0][11:]
        sunset = result['daily']['sunset'][0][11:]
        wind_l = result['hourly']['windspeed_10m']
        wind = sum(wind_l) / len(wind_l)
        wind_gust_l = result['hourly']['windgusts_10m']
        wind_gust = sum(wind_gust_l) / len(wind_gust_l)
        clouds_l = result['hourly']['cloudcover']
        clouds = sum(clouds_l) / len(clouds_l)
        description = result['daily']['weathercode']
        description = str(description)
        precipitation = "ОСАДКИ!" if precipitation_sum > 0.2 or max(precipitation_sum_l) > 0.2 else "Нет осадков."
        precipitation_sum_l = str(precipitation_sum_l)
        cur_forecast = RouteWeather.objects.create(route_id=active_route.route_n,
                                                   start_day=start_day_d,
                                                   finish_day=finish_day,
                                                   name_p=name,
                                                   temperature=temperature,
                                                   temperature_2m_max=temperature_2m_max,
                                                   temperature_2m_min=temperature_2m_min,
                                                   sunrise=sunrise,
                                                   sunset=sunset,
                                                   wind=wind,
                                                   wind_gust=wind_gust,
                                                   clouds_p=clouds,
                                                   description=description,
                                                   description_p=description,
                                                   precipitation_sum_p=precipitation_sum,
                                                   precipitation_sum_l=precipitation_sum_l,
                                                   precipitation=precipitation)
        return cur_forecast

    except Exception as error:
        print(error)
        return False


def check_and_sort_routes(active_route, meteo_API, route_forecast, input_data, data_routes_r,
                          routes_forecast_r) -> dict:
    """Проверка и сортировка маршрутов по средней температуре"""
    list_offer = dict()
    major_points = list()
    for route_number_r, route_data_r in data_routes_r.items():
        active_route.route_clear()
        active_route.copy_route(route_number_r, route_data_r)
        try:

            check_flag = active_route.coord_start_point_p + active_route.coord_end_point_p
            if check_flag not in major_points:
                major_points.append(check_flag)
                print(f'\nЗагружается маршрут: {active_route.route_db_n}')
                if meteo_API == 2:
                    weather_data = load_or_get_weather_data(active_route, route_forecast,
                                                            input_data['start_day'],
                                                            input_data['finish_day'])
                    active_route.write_route_forecast(weather_data)
                    route_offer = active_route.make_dict()

                    list_offer.setdefault(route_number_r, route_offer)

        except IndexError:
            print(f"Не введены координаты старта для маршрута {active_route.name_p}: "
                  f"{active_route.start_point_p} - {active_route.end_point_p}.")

    best_offer = dict(sorted(list_offer.items(), key=lambda item: item[1]['temperature_p'], reverse=True))

    return best_offer


def print_sorted_routes(meteo_API, input_data, best_offer_p, print_pdf_p) -> dict:
    """Вывод рекомендуемых маршрутов"""
    routes_info = dict()
    list_best_offer = list(best_offer_p)

    str_file = "Сортировка выполнена по температуре, указано наличие или отсутствие дождя."

    routes_info['header'] = str_file.replace('\n', '<br/>')

    routes_info['info'] = {
        'Дата начала': str(input_data['start_day']),
        'Длительность в днях': str(input_data['target_days']),
        'Минимальная удалённость от Москвы': str(input_data['target_distancemin_km'] + " км."),
        'Максимальная удалённость от Москвы': str(input_data['target_distancemax_km'] + " км.")
    }
    # Файл больше не создаём, интерфейс - браузер.
    # with open("прогноз.txt", "w", encoding='UTF-8') as file1:
    #     file1.write(str_file)

    i = 1
    route_item = ['', '', '']
    route_info = dict()
    top_routes = dict()
    for route in list_best_offer:
        if (route_item[0] == best_offer_p[route]['name'] and
                route_item[1] == best_offer_p[route]['start_point_p'] and route_item[2] == best_offer_p[route][
                    'end_point_p']):
            pass
        else:
            if meteo_API == 2:
                route_item = route_info_print(best_offer_p, route, i)
                pass
                route_info[i] = route_item[3]
                if i < 6:
                    top_routes[i] = {
                        'Маршрут №': route_item[3]['Маршрут №'] + '. ' + route_item[3]['Маршрут по'] + '-> ' +
                                     route_item[3]['Нитка маршрута'] + ' Длина маршрута: ' + route_item[3]['Длина маршрута'],
                        'Важно': route_item[3]['Важно'],
                        'Область': route_item[3]['Область'],
                        'Brouter': route_item[3]['Brouter'],
                        'Прогноз': route_item[3]['Прогноз от Яндекс.Погоды на ближайшие 10 дней'],
                        }
            i += 1
    routes_info['routes'] = route_info
    routes_info['top_routes'] = top_routes
    # Файл больше не создаём, интерфейс - браузер.
    # if print_pdf_p is True:
    #     input_filename = 'прогноз.txt'
    #     output_filename = 'прогноз.pdf'
    #     make_pdf(input_filename, output_filename)

    return routes_info


def get_appropriate_routes(qty_days: str, distance_min: str, distance_max: str) -> dict:
    appropriate_routes = dict()
    qty_days = int(qty_days)
    distance_min = float(distance_min)
    distance_max = float(distance_max)
    qty_days += 1
    distance_min -= 0.1
    distance_max += 0.1

    db_appropriate_routes = Route.objects.filter(qty_days__lt=qty_days, distance_from_city__gt=distance_min,
                                                 distance_from_city__lt=distance_max).distinct()
    for i, route_id in enumerate(db_appropriate_routes):
        appropriate_routes.setdefault(i + 1, route_id)
    return appropriate_routes


def create_main_routes_data(route_id_dict: dict, active_route: RouteData) -> dict:
    routes_dict = dict()
    try:
        for num, route_id in route_id_dict.items():
            active_route.route_clear()
            route_cur = Route.objects.get(pk=route_id.id)
            active_route.read_active_route(route_cur)
            route_data = dict()
            for attr in dir(active_route):
                if not callable(getattr(active_route, attr)) and not attr.startswith("__"):
                    route_data[attr] = getattr(active_route, attr)
            routes_dict.setdefault(num, route_data)
    except Exception as error:
        print(f'Ошибка чтения маршрутов. Загружены: {routes_dict}')
        exit(104)
    return routes_dict


def get_routes(test_seting: int, meteo_API: int, print_pdf: bool, request) -> dict:
    # Moscow lat="55.6595",lon="37.7937"
    # unixtime += 10800 # Время МСК
    # meteo_API == 2 - get_open_meteo_data
    vk_admin = VkGroupAdmin(os.getenv('VK_TOKEN', 'token'), os.getenv('VK_API_VERSION', 'version'),
                            os.getenv('VK_GROUP_ID', 'group_id'))
    route_forecast = OpenMeteoData()
    active_route = RouteData(0, 0, "", "", "", "",
                             0, 0, 0, 0, "",
                             "", "", "",
                             "", "", 0, "", 0.0,
                             "", "", "", "",
                             0.0, 0.0, 0.0, "", "",
                             0.0, "", "")
    routes_forecast = dict()
    if test_seting == 0 or test_seting == 1:
        input_data_w = manual_input(test_seting)
    elif test_seting == 2:
        input_data_w = prepare_query(request)
    else:
        return {'error': 'unkown test_seting'}

    route_ids = get_appropriate_routes(input_data_w['target_days'], input_data_w['target_distancemin_km'],
                                       input_data_w['target_distancemax_km'])
    data_routes = create_main_routes_data(route_ids, active_route)
    best_offer_r = check_and_sort_routes(active_route, meteo_API, route_forecast, input_data_w, data_routes,
                                         routes_forecast)
    view_set = print_sorted_routes(meteo_API, input_data_w, best_offer_r, print_pdf)

    # result_vk = vk_admin.post_forecast("TEST 1")
    # print(result_vk)

    return view_set


if __name__ == '__main__':
    pass
