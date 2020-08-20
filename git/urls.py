from django.urls import path
from .views import index, gituser, repos


urlpatterns = [
    path('', index, name='index'),
    path('user/<str:username>/', gituser, name="gituser"),
    path('user/<str:username>/repositories/', repos, name="repos"),
]