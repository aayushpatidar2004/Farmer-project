from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.recommendation_view, name='index'),
]
