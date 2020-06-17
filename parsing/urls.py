from django.urls import path
from .views import ListPhone

urlpatterns = [
    path('',ListPhone.as_view()),
]