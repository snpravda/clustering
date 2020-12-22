
from django.urls import path
from .views import *

urlpatterns = [
    path('', GetDummies.as_view())
]