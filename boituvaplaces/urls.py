from django.urls import path

from .views import buscar_proximidades

urlpatterns = [
    path("", buscar_proximidades, name="index"),
    path("buscar/", buscar_proximidades, name="buscar_proximidades"),
]
