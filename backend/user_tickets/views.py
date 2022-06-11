import json
import jwt
import requests
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from accounts.decorator import is_user_is_authenticated
from user_tickets.models import UserWithRequestId
from backend.settings import EMAIL, API_TOKEN, PASSWORD


class TicketView(APIView):
    """ticket management"""

    BASE_URL = "https://sample4365.zendesk.com/"
    headers = {'content-type': 'application/json'}

    # get the user with correct url if user is admin url will change
    def get_request_url(self, user):
        try:
            ins = UserWithRequestId.objects.get(user_id__id=user.id)
            URL = f"/api/v2/users/{ins.request_id}/tickets/requested"
            if ins.user_id.role == "admin":
                URL = "api/v2/tickets.json"
            return self.BASE_URL + URL
        except:
            pass


    # get ticket details
    @is_user_is_authenticated
    def get(self, request, user):

        response = requests.get(
            self.get_request_url(user),
            auth=(
                EMAIL,
                PASSWORD
            ))

        s = response.json()
        return Response(s, status=status.HTTP_200_OK)


    # post for post the form for zendesk
    @is_user_is_authenticated
    def post(self, request, user_ins):

        arr = ["subject", "description", "priority"]

        for i in arr:
            if i not in request.data and not request.data[i]:
                return Response(
                    {"error": f'{i} not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # =============== data ===============

        data = {
            "ticket": {
                "subject":   request.data["subject"],
                "comment":   {"body": request.data["description"]},
                "requester": {"locale_id": user.id, "name": user_ins.name, "email": user_ins.email},
                "priority": request.data["priority"]
            }
        }

        ticket = json.dumps(data)

        user = EMAIL + '/token'
        url = 'https://sample4365.zendesk.com/api/v2/tickets'
        headers = {'content-type': 'application/json'}

        response = requests.post(
            url,
            data=ticket,
            auth=(user, API_TOKEN),
            headers=headers
        )
        res_json = response.json()

        try:

            is_in_model = UserWithRequestId.objects.filter(
                request_id=res_json["ticket"]["requester_id"]
            ).exists()

            print(is_in_model)

            if not is_in_model:
                UserWithRequestId.objects.create(
                    user_id=user_ins,
                    request_id=res_json["ticket"]["requester_id"]
                ).exists()

        except:
            pass

        return Response(res_json, status=status.HTTP_200_OK)

    @is_user_is_authenticated
    def delete(self, request, user):

        id = int(request.GET["id"])

        user = EMAIL + '/token'
        url = f'https://sample4365.zendesk.com/api/v2/tickets/{id}'
        headers = {'content-type': 'application/json'}

        response = requests.delete(
            url,
            auth=(user, API_TOKEN),
            headers=headers
        )

        return Response({}, status=status.HTTP_200_OK)
