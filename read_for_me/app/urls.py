from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
   
    path('api/upload/', views.UploadFileAPI.as_view(), name='api-upload-file'),
]
