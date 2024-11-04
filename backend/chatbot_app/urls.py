from django.conf import settings
from django.urls import include, path
from django.contrib import admin
# from home import models

from .models import *
from .views import *


urlpatterns = [
    path('webhook/', webhook, name='webhook'),
]
    
    
    
    
    
    
    
