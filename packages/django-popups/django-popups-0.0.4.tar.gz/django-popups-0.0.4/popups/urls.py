from django.urls import path
from . import views

app_name = 'popups'

urlpatterns = [
    path('', views.test, name='test'),
]
