from django.urls import path
from . import views


url_patterns = [
    path('image/build', views.build_image),
]