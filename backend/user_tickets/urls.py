
from django.urls import path
from .import views


urlpatterns = [
    path('', views.TicketView.as_view(), name=''),
]
