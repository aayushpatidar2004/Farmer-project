from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('crops/', include('crops.urls', namespace='crops')),
    path('weather/', include('weather.urls', namespace='weather')),
    path('soil/', include('soil.urls', namespace='soil')),
    path('recommendations/', include('recommendations.urls', namespace='recommendations')),
    path('diseases/', include('diseases.urls', namespace='diseases')),
    path('market/', include('market.urls', namespace='market')),
    path('api/', include('api.urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'config.views.error_403'
handler404 = 'config.views.error_404'
handler500 = 'config.views.error_500'
