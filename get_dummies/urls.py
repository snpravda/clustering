
from django.urls import path
from .views import *

urlpatterns = [
    path('', GetuDummies.as_view())
]