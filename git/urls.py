from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('user/<str:username>/', gituser, name="gituser"),
]