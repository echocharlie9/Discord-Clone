from django.urls import path
from . import views

urlpatterns = [
    path('getRecentMessages', views.GetNRecentMessages.as_view())
]