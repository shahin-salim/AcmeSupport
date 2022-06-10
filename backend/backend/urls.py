"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from department.views import DepartmentView
from accounts.views import UserView

department_route = DefaultRouter()
department_route.register(r'', DepartmentView, basename='')

user_route = DefaultRouter()
user_route.register(r'', UserView, basename='')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('department/', include(department_route.urls)),
    path('accounts/', include(user_route.urls)),
    path('login/', include("accounts.urls")),
    path('tickets/', include("user_tickets.urls")),
]