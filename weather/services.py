import atexit
from csv import Error
from http import HTTPStatus

import openmeteo_requests
import requests
import requests_cache
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
from django.core.mail import send_mail
from retry_requests import retry

from .models import Temperature


def get_temperature(lat: float, lon: float):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        'latitude': lat,
        'longitude': lon,
        'daily': 'weather_code',
        'timezone': 'America/Sao_Paulo',
        'forecast_days': 1,
        'current': 'temperature_2m',
        'hourly': '',
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()

    return int(current_temperature_2m)


def get_coordinates(place_name: str):
    url = 'https://nominatim.openstreetmap.org/search'
    headers = {'User-Agent': 'weather-app'}
    params = {'q': place_name, 'format': 'jsonv2', 'limit': 1}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == HTTPStatus.OK:
        results = response.json()
        try:
            lat = float(results[0]['lat'])
            lon = float(results[0]['lon'])
            return lat, lon
        except Error:
            raise Exception(Error)
    else:
        raise Exception('Error when searching coordinates.')


def send_temperature_alert(email, place, current_temp, max_temp):
    try:
        subject = f'Temperature Alert - {place}'

        message = (
            f'The current temperature in {place} is {current_temp}°C, and you\'ve set the limit to {max_temp}°C.'
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return True

    except Exception as e:
        return e


scheduler = BackgroundScheduler()
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


def stop_scheduler(job_id: str):
    if scheduler and scheduler.get_job(job_id):
        scheduler.remove_job(job_id)
        return True
    return False


def add_temperature_monitoring(items: dict):
    job_id = f"{items['email']}"

    if scheduler.get_job(job_id):
        return

    scheduler.add_job(
        func=check_temperature,
        trigger=IntervalTrigger(minutes=items['interval_minutes']),
        args=(
            [items['email'],
             items['place'],
             items['lat'],
             items['lon'],
             items['max_temp']]),
        id=job_id,
        max_instances=1,
        misfire_grace_time=30
    )

    return job_id


def check_temperature(email, place, lat, lon, max_temp):
    try:
        temperature = get_temperature(lat, lon)

        if temperature >= max_temp:
            Temperature.objects.create(
                email=email,
                place=place,
                temperature=temperature,
            )
            print(f'Temperature: {temperature}°C')
            send_temperature_alert(email, place, temperature, max_temp)
    except Exception as e:
        print(f'Erro: {str(e)}')
