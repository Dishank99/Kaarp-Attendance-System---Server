from django.urls import path
from .views import *

urlpatterns = [
   path('validate/', ValidateUser.as_view()),
   path('requests/', UserRequests.as_view()),
]