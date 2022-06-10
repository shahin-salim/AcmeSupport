from django.shortcuts import render
from rest_framework import viewsets
from .models import Departments
from .serializer import DepartmentsSerializer
# Create your views here.

# crud of the departmeent model


class DepartmentView(viewsets.ModelViewSet):
    serializer_class = DepartmentsSerializer
    queryset = Departments.objects.all()
