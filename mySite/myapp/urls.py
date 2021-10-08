
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('<str:api_key>',views.key),
]
