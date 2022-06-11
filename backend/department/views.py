from django.shortcuts import render
from rest_framework import viewsets
from permission_class import AdminOnly
from .models import Departments
from .serializer import DepartmentsSerializer
from rest_framework.response import Response
from rest_framework import status
from accounts.models import CustomUser


class DepartmentView(viewsets.ModelViewSet):
    """crud of department . all the methods only accessed by admin"""

    serializer_class = DepartmentsSerializer
    queryset = Departments.objects.all()
    permission_classes = (AdminOnly,)

    # check department fk in user model
    def is_exist(self, pk):
        return CustomUser.objects.filter(department_fk__id=int(pk)).exists()

    def destroy(self, request, *args, **kwargs):
        if not self.is_exist(kwargs["pk"]):
            Departments.objects.get(id=int(kwargs["pk"])).delete()
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response(
            {"exist": "item alredy exist in another table"},
            status=status.HTTP_400_BAD_REQUEST
        )
