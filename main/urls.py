from django.urls import path

from main.apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
    path('create/', ....as_view(), name='create'),
]