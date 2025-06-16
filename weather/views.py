from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_weather(request: HttpRequest) -> HttpResponse:
    return render(request, 'weather/index.html')


def history_weather(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'History in Weather',
    }
    return render(request, 'weather/history.html', context)
