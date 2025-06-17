import time

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from weather.forms import TemperatureForms

from .models import Temperature
from .services import add_temperature_monitoring, get_temperature


def home_weather(request):
    if request.method == 'POST':
        form = TemperatureForms(request.POST)
        if form.is_valid():
            one_day = 86400

            email = form.cleaned_data['email']
            place = form.clean_place()
            max_temp = form.cleaned_data['max_temperature']
            interval = form.clean_interval()
            lat, lon = form.get_coordinates()

            add_temperature_monitoring(
                email=email,
                place=place, 
                lat=lat,
                lon=lon,
                max_temp=max_temp,
                interval_minutes=interval
            )

            return redirect('weather:history')
    else:
        form = TemperatureForms()

    context = {'form': form}

    return render(request, 'weather/index.html', context)


def history_weather(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'History in Weather',
    }
    return render(request, 'weather/history.html', context)
