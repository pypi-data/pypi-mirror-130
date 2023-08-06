from django.urls import path
from . import views

app_name = 'popup'

urlpatterns = [
    path('', views.test, name='test'),
]
