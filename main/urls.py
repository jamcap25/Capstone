# main/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('diagnosis/', views.diagnosis, name='diagnosis'),
    path('history/', views.history, name='history'),
    path('predict_diagnosis/', views.predict_diagnosis, name='predict_diagnosis'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)