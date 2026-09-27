from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    path('', views.crop_list_view, name='list'),
    path('add/', views.crop_add_view, name='add'),
    path('<int:pk>/', views.crop_detail_view, name='detail'),
    path('<int:pk>/edit/', views.crop_edit_view, name='edit'),
    path('<int:pk>/delete/', views.crop_delete_view, name='delete'),
    path('<int:crop_pk>/upload-image/', views.upload_image_view, name='upload_image'),
    path('image/<int:pk>/delete/', views.delete_image_view, name='delete_image'),
    path('my-images/', views.my_images_view, name='my_images'),
]
