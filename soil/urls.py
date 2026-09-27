from django.urls import path
from . import views

app_name = 'soil'

urlpatterns = [
    path('', views.soil_list_view, name='list'),
    path('add/', views.soil_add_view, name='add'),
    path('<int:pk>/', views.soil_detail_view, name='detail'),
    path('<int:pk>/edit/', views.soil_edit_view, name='edit'),
    path('<int:pk>/delete/', views.soil_delete_view, name='delete'),
]
