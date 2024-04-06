# Generated by Django 5.0.4 on 2024-04-06 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Список категорий',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_db_id', models.PositiveIntegerField(verbose_name='Внешний номер')),
                ('name', models.CharField(max_length=50, verbose_name='Название реки')),
                ('area', models.CharField(max_length=50, verbose_name='Область')),
                ('start_point', models.CharField(max_length=50, verbose_name='Место старта')),
                ('end_point', models.CharField(max_length=50, verbose_name='Место финиша')),
                ('distance_km', models.CharField(max_length=50, verbose_name='Дистанция')),
                ('year_journey', models.IntegerField(verbose_name='Год')),
                ('qty_days', models.IntegerField(verbose_name='Кол-во дней')),
                ('distance_from_city', models.DecimalField(decimal_places=1, max_digits=6, verbose_name='От Москвы, км')),
                ('feature', models.CharField(max_length=200, verbose_name='Особенность')),
                ('camping_places', models.CharField(max_length=200, verbose_name='Стоянки')),
                ('coord_camping_places', models.CharField(max_length=200, verbose_name='Координаты стоянок')),
                ('picture_links', models.CharField(max_length=200, verbose_name='Фотоотчёт')),
                ('coord_start_point', models.CharField(max_length=30, verbose_name='Координаты старта')),
                ('coord_end_point_p', models.CharField(max_length=30, verbose_name='Координаты финиша')),
                ('name_p', models.CharField(max_length=200, verbose_name='Ответ сервера по месту прогноза')),
                ('temperature', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='Температура')),
                ('temperature_2m_max', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='Максимальная температура по дням')),
                ('temperature_2m_min', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='Минимальная температура по ночам')),
                ('sunrise', models.CharField(max_length=50, verbose_name='Рассвет')),
                ('sunset', models.CharField(max_length=50, verbose_name='Закат')),
                ('wind', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='Ветер')),
                ('wind_gust', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='Порыв ветра')),
                ('clouds_p', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Облачность')),
                ('description', models.CharField(max_length=200, verbose_name='Погода по дням')),
                ('description_p', models.CharField(max_length=200, verbose_name='Погода')),
                ('precipitation_sum_p', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Осадки')),
                ('precipitation_sum_l', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='Осадки по дням')),
                ('precipitation', models.CharField(max_length=50, verbose_name='Осадки_качественно')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='forecast.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Маршрут',
                'verbose_name_plural': 'Список маршрутов',
                'ordering': ('-name',),
            },
        ),
    ]
