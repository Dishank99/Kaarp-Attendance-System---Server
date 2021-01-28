from django.urls import path
from .views import *

urlpatterns = [
    path('daily/', DailyRecord.as_view()),
]