# Generated by Django 5.0.4 on 2024-04-09 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routeweather',
            name='clouds_p',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='Облачность'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='precipitation',
            field=models.CharField(max_length=20, verbose_name='Осадки качественно'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='precipitation_sum_l',
            field=models.CharField(max_length=200, verbose_name='Осадки по дням'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='precipitation_sum_p',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5, verbose_name='Осадки'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_weathers', to='forecast.route', verbose_name='Маршрут'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='sunrise',
            field=models.CharField(max_length=6, verbose_name='Рассвет'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='sunset',
            field=models.CharField(max_length=6, verbose_name='Закат'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='temperature',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4, verbose_name='Температура'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='temperature_2m_max',
            field=models.CharField(max_length=200, verbose_name='Максимальная температура по дням'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='temperature_2m_min',
            field=models.CharField(max_length=200, verbose_name='Минимальная температура по ночам'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='wind',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4, verbose_name='Ветер'),
        ),
        migrations.AlterField(
            model_name='routeweather',
            name='wind_gust',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4, verbose_name='Порыв ветра'),
        ),
    ]