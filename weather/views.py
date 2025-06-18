
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from weather.forms import TemperatureForms

from .models import Temperature
from .services import add_temperature_monitoring, stop_scheduler


def home_weather(request):
    if request.method == 'POST':
        form = TemperatureForms(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            place = form.clean_place()
            max_temp = form.cleaned_data['max_temperature']
            interval = form.clean_interval()
            lat, lon = form.get_coordinates()

            add_temperature_monitoring({
                'email': email,
                'place': place,
                'lat': lat,
                'lon': lon,
                'max_temp': max_temp,
                'interval_minutes': interval
            })

            return redirect('weather:history')
    else:
        form = TemperatureForms()

    context = {'form': form}

    return render(request, 'weather/index.html', context)


def history_weather(request: HttpRequest) -> HttpResponse:
    temperatures = []
    email_search = None

    if request.method == 'GET' and request.GET.get('email'):
        email_search = request.GET.get('email').strip()

        if email_search:
            temperatures = Temperature.objects.filter(
                email__icontains=email_search
            ).order_by('-created_at')

            if not temperatures.exists():
                messages.warning(request, 'No register found for this email.')
        else:
            messages.warning(request, 'Please enter an email to search.')

    context = {
        'title': 'History in Weather',
        'temperatures': temperatures,
        'email_search': email_search,
    }

    return render(request, 'weather/history.html', context)

def stop_monitoring(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            if stop_scheduler(email):
                messages.success(request, f'Monitoring stopped for: {email}')
            else:
                messages.warning(request, f'No monitoring found for: {email}')
        else:
            messages.error(request, 'Email not provided.')

    return redirect('weather:history')