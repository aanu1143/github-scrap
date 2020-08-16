from django.contrib import admin
from django.urls import path, include
from git import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('git.urls')),
]
