from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Список категорий"
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Route(models.Model):
    route_db_id = models.PositiveIntegerField(verbose_name='Внешний номер')
    name = models.CharField(max_length=50, verbose_name='Название реки')
    area = models.CharField(max_length=50, verbose_name='Область')
    start_point = models.CharField(max_length=50, verbose_name='Место старта')
    end_point = models.CharField(max_length=50, verbose_name='Место финиша')
    distance_km = models.DecimalField(max_digits=6, decimal_places=1, verbose_name='Дистанция')
    year_journey = models.IntegerField(verbose_name='Год')
    qty_days = models.IntegerField(verbose_name='Кол-во дней')
    distance_from_city = models.DecimalField(max_digits=6, decimal_places=1, verbose_name='От Москвы, км')
    feature = models.CharField(max_length=200, verbose_name='Особенность')
    camping_places = models.CharField(max_length=200, verbose_name='Стоянки')
    coord_camping_places = models.CharField(max_length=200, verbose_name='Координаты стоянок')
    picture_links = models.CharField(max_length=200, verbose_name='Фотоотчёт')
    coord_start_point = models.CharField(max_length=30, verbose_name='Координаты старта')
    coord_end_point_p = models.CharField(max_length=30, verbose_name='Координаты финиша')
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='routes', blank=True,
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = "Список маршрутов"
        ordering = ('-name',)

    def __str__(self):
        return f'{self.pk}'
        # return f'Маршрут: {self.name}, внешний номер: {self.route_db_id}, год прохождения:  {self.year_journey}'


class RouteWeather(models.Model):
    route = models.ForeignKey(Route, verbose_name='Маршрут', related_name='route_weathers', blank=False,
                                 on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    start_day = models.DateField(blank=False)
    finish_day = models.DateField(blank=False)
    name_p = models.CharField(max_length=200, verbose_name='Ответ сервера по месту прогноза')
    temperature = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name='Температура')
    temperature_2m_max = models.CharField(max_length=200, verbose_name='Максимальная температура по дням')
    temperature_2m_min = models.CharField(max_length=200, verbose_name='Минимальная температура по ночам')
    sunrise = models.CharField(max_length=6, verbose_name='Рассвет')
    sunset = models.CharField(max_length=6, verbose_name='Закат')
    wind = models.DecimalField(max_digits=4, decimal_places=1,  default=0, verbose_name='Ветер')
    wind_gust = models.DecimalField(max_digits=4, decimal_places=1,  default=0, verbose_name='Порыв ветра')
    clouds_p = models.DecimalField(max_digits=5, decimal_places=1,  default=0, verbose_name='Облачность')
    description = models.CharField(max_length=200, verbose_name='Погода по дням')
    description_p = models.CharField(max_length=200, verbose_name='Погода')
    precipitation_sum_p = models.DecimalField(max_digits=5, decimal_places=1,  default=0, verbose_name='Осадки')
    precipitation_sum_l = models.CharField(max_length=200, verbose_name='Осадки по дням')
    precipitation = models.CharField(max_length=20, verbose_name='Осадки качественно')

    class Meta:
        verbose_name = 'Прогноз на маршрут'
        verbose_name_plural = "Прогнозы для маршрутов"
        ordering = ('-route_id',)

    def __str__(self):
        return (f''
                f'{self.pk} {self.route} {self.dt}')
