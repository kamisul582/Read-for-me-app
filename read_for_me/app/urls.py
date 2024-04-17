from django.urls import path
from . import views
app_name = 'app'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('file-upload/', views.upload_file, name='upload_file'),
]