from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
]
