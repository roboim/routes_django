import csv
import os
from pprint import pprint
from datetime import datetime, timedelta

from forecast.open_meteo_data import OpenMeteoData
from vk_api import VkGroupAdmin


class RouteData:
    """Полное описание маршрута"""

    def __init__(self, route_n: int, route_db_n: int, river_name_p: str, area_p: str, start_point_p: str,
                 end_point_p: str,
                 distance_km_p: str, year_journey_p: str, qty_days_p: str, distance_from_city_p: str, feature_p: str,
                 camping_places_p: str, coord_camping_places_p: str, picture_links_p: str,
                 coord_start_point_p: str, coord_end_point_p: str, name_p: str, temperature_p: float,
                 temperature_2m_max_p: list, temperature_2m_min_p: list, sunrise_p: str, sunset_p: str,
                 wind_p: float, wind_gust_p: float, clouds_p: float, description: list, description_p: list,
                 precipitation_sum_p: float, precipitation_sum_l: list, precipitation: str):
        self.route_n = route_n  # ['Маршрут']
        self.route_db_n = route_db_n  # ['№']
        self.river_name_p = river_name_p  # ['Река']
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
        self.precipitation = precipitation  # Осадки_качественно

    def route_clear(self) -> None:
        """Полностью очистить данные по маршруту"""
        self.route_n = 0  # ['Маршрут']
        self.route_db_n = 0  # ['№']
        self.river_name_p = ""  # ['Река']
        self.area_p = ""  # ['Область']
        self.start_point_p = ""  # ['Место старта']
        self.end_point_p = ""  # ['Место финиша']
        self.distance_km_p = ""  # ['Дистанция']
        self.year_journey_p = ""  # ['Год']
        self.qty_days_p = ""  # ['Кол-во дней']
        self.distance_from_city_p = ""  # ['От Москвы, км']
        self.feature_p = ""  # ['Особенность']
        self.camping_places_p = ""  # ['Стоянки']
        self.coord_camping_places_p = ""  # ['Координаты стоянок']
        self.picture_links_p = ""  # ['Фотоотчёт']
        self.coord_start_point_p = ""  # ['Координаты старта']
        self.coord_end_point_p = ""  # ['Координаты финиша']
        self.name_p = ""  # ['Ответ сервера по месту прогноза']
        self.temperature_p = 0.0  # ['Температура']
        self.temperature_2m_max_p = []  # ['Максимальная температура по дням']
        self.temperature_2m_min_p = []  # ['Минимальная температура по ночам']
        self.sunrise_p = ""  # ['Рассвет']
        self.sunset_p = ""  # ['Закат']
        self.wind_p = 0.0  # ['Ветер']
        self.wind_gust_p = 0.0  # ['Порыв ветра']
        self.clouds_p = 0.0  # ['Облачность']
        self.description = []  # ['Погода по дням']
        self.description_p = []  # ['Погода']
        self.precipitation_sum_p = 0.0  # ['Осадки']
        self.precipitation_sum_l = []  # ['Осадки по дням']
        self.precipitation = ""  # Осадки_качественно

    def read_active_route(self, route_number, route_data) -> None:
        """Прочитать данные по маршруту"""
        self.route_n = route_number
        self.route_db_n = route_data['№']
        self.river_name_p = route_data['Река']
        self.area_p = route_data['Область']
        self.start_point_p = route_data['Место старта']
        self.end_point_p = route_data['Место финиша']
        self.distance_km_p = route_data['Дистанция']
        self.year_journey_p = route_data['Год']
        self.qty_days_p = route_data['Кол-во дней']
        self.distance_from_city_p = route_data['От Москвы, км']
        self.feature_p = route_data['Особенность']
        self.camping_places_p = route_data['Стоянки']
        self.coord_camping_places_p = route_data['Координаты стоянок']
        self.picture_links_p = route_data['Фотоотчёт']
        self.coord_start_point_p = route_data['Координаты старта']
        self.coord_end_point_p = route_data['Координаты финиша']

    def write_route_forecast(self, route_data) -> None:
        """Записать данные маршрута по погоде"""
        route_data['Ответ сервера по месту прогноза'] = self.name_p
        route_data['Температура'] = self.temperature_p
        route_data['Максимальная температура по дням'] = self.temperature_2m_max_p
        route_data['Минимальная температура по ночам'] = self.temperature_2m_min_p
        route_data['Рассвет'] = self.sunrise_p
        route_data['Закат'] = self.sunset_p
        route_data['Ветер'] = self.wind_p
        route_data['Порыв ветра'] = self.wind_gust_p
        route_data['Облачность'] = self.clouds_p
        route_data['Погода по дням'] = self.description
        route_data['Погода'] = self.description_p
        route_data['Осадки'] = self.precipitation_sum_p
        route_data['Осадки по дням'] = self.precipitation_sum_l
        route_data['Осадки_качественно'] = self.precipitation

    def route_pr(self) -> None:
        """Вывод названия реки и области"""
        pprint(self.river_name_p)
        pprint(self.area_p)


def read_routes(file_csv) -> dict:
    """ чтение csv через rDictReader.
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
        finish_day = start_day_d + timedelta(int(target_days)-1)
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
        finish_day = start_day_d + timedelta(int(target_days)-1)
        target_distancemin_km = "1"
        target_distancemax_km = "160" # 160 км

        data_request.setdefault("target_days", target_days)
        data_request.setdefault("start_day", start_day)
        data_request.setdefault("finish_day", finish_day)
        data_request.setdefault("target_distancemin_km", target_distancemin_km)
        data_request.setdefault("target_distancemax_km", target_distancemax_km)

    # pprint(data_request)
    return data_request


def get_routes() -> dict:
    # Moscow lat="55.6595",lon="37.7937"
    # unixtime += 10800 # Время МСК
    test_seting = 0
    # 2 - get_open_meteo_data
    meteo_API = 2
    print_pdf = False
    data_file_csv = "data.csv"
    vk_admin = VkGroupAdmin(os.getenv('VK_TOKEN', 'token'), os.getenv('VK_API_VERSION', 'version'),
                            os.getenv('VK_GROUP_ID', 'group_id'))
    route_forecast = OpenMeteoData()
    active_route = RouteData(0, 0, "", "", "", "",
                             "", "", "", "", "",
                             "", "", "",
                             "", "", "", 0.0,
                             [], [], "", "",
                             0.0, 0.0, 0.0, [], [],
                             0.0, [], "")
    routes_forecast = dict()

    data_routes = read_routes(data_file_csv)
    view_set = data_routes

    input_data_w = manual_input(test_seting)
    # best_offer_r = check_and_sort_routes(active_route, meteo_API, route_forecast, input_data_w, data_routes, routes_forecast)
    # view_set = print_sorted_routes(data_routes, meteo_API, input_data_w, best_offer_r, print_pdf)

    # result_vk = vk_admin.post_forecast("TEST 1")
    # print(result_vk)

    return view_set


if __name__ == '__main__':
    pass
