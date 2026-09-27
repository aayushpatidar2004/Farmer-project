from django.urls import path
from . import views

app_name = 'diseases'

urlpatterns = [
    path('', views.disease_list_view, name='list'),
    path('<int:pk>/', views.disease_detail_view, name='detail'),
]
