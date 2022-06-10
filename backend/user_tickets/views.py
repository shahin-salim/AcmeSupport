import json
import jwt
import requests
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from accounts.decorator import is_user_is_authenticated
import ast

from user_tickets.models import UserWithRequestId


class TicketView(APIView):

    BASE_URL = "https://sample4365.zendesk.com/"
    email = 'shahinsalim82@gmail.com'
    password = '!@@shahinS123'
    api_token = 'UfWqWQDiPxvrPb9jP6ams19nUA2ZFXrrALB4wEmB'
    headers = {'content-type': 'application/json'}

    def get_request_url(self, user):
        ins = UserWithRequestId.objects.get(user_id__id=user.id)
        print(ins, "===========================")
        URL = f"/api/v2/users/{ins.request_id}/tickets/requested"
        if ins.user_id.role == "admin":
            URL = "api/v2/tickets.json"
        return self.BASE_URL + URL

    @is_user_is_authenticated
    def get(self, request, user):

        response = requests.get(
            self.get_request_url(user),
            auth=(
                'shahinsalim82@gmail.com',
                '!@@shahinS123'
            ))

        s = response.json()
        return Response(s, status=status.HTTP_200_OK)

    @is_user_is_authenticated
    def post(self, request, user_ins):

        print(request.data)

        arr = ["subject", "description", "priority"]

        for i in arr:
            if i not in request.data and not request.data[i]:
                return Response(
                    {"error": f'{i} not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        print(request.data["priority"], " *******")
        data = {
            "ticket": {
                "comment": {
                    "body":  request.data["description"],
                },
                "priority": request.data["priority"],
                "subject": request.data["subject"],
                "requester": {
                    "locale_id": user_ins.id,
                    "name": user_ins.name,
                    "email": user_ins.email or user_ins.phone_number
                },
            }
        }

        ticket = json.dumps(data)

        user = "shahinsalim82@gmail.com" + '/token'
        api_token = 'UfWqWQDiPxvrPb9jP6ams19nUA2ZFXrrALB4wEmB'
        url = 'https://sample4365.zendesk.com/api/v2/tickets'
        headers = {'content-type': 'application/json'}

        response = requests.post(
            url,
            data=ticket,
            auth=(user, api_token),
            headers=headers
        )
        res_json = response.json()

        print(res_json)

        UserWithRequestId.objects.update_or_create(
            user_id=user_ins,
            request_id=res_json["ticket"]["requester_id"]
        )

        return Response(res_json, status=status.HTTP_200_OK)

    @is_user_is_authenticated
    def delete(self, request, user):

        id = int(request.GET["id"])
        print(type(id), " %%%%%%%%%%%%%%%%%%%%%%%%%%")

        print(self.BASE_URL + f"api/v2/tickets/{int(id)}")

        user = "shahinsalim82@gmail.com" + '/token'
        api_token = 'UfWqWQDiPxvrPb9jP6ams19nUA2ZFXrrALB4wEmB'
        url = f'https://sample4365.zendesk.com/api/v2/tickets/{id}'
        headers = {'content-type': 'application/json'}

        response = requests.delete(
            url,
            auth=(user, api_token),
            headers=headers
        )

        return Response({}, status=status.HTTP_200_OK)