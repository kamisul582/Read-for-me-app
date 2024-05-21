from django.urls import path
from . import views
from .views import speech_api, translate_api

app_name = 'app'

urlpatterns = [
   
    path('api/upload/', views.UploadFileAPI.as_view(), name='api-upload-file'),
    path('api/speech/', speech_api, name='speech_api'),
    path('api/translate/', translate_api, name='translate_api'),
]
