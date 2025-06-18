from django.urls import path

from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.home_weather, name='home'),
    path('history/', views.history_weather, name='history'),
    path('stop-monitoring/',
         views.stop_monitoring,
         name='stop_monitoring'
        ),
]
