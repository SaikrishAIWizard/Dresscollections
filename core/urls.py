from django.urls import path
from .views import home, upload_dress

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_dress, name='upload_dress')
]
