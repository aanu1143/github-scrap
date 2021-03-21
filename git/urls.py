from django.urls import path
from .views import index, gituser, repos, about


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('user/<str:username>', gituser, name="gituser"),
    path('user/<str:username>/repositories', repos, name="repos"),
]