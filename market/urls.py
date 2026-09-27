from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.market_list_view, name='list'),
    path('add/', views.market_add_view, name='add'),
    path('<int:pk>/edit/', views.market_edit_view, name='edit'),
    path('<int:pk>/delete/', views.market_delete_view, name='delete'),
]
