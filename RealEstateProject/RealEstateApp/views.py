from RealEstateApp.models import UserProfile, UserToken
from RealEstateApp.serializers import UserProfileSerializer
from RealEstateApp.utils import auth, database
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class RegisterView(views.APIView):

    authentication_classes = []

    def post(self, request):

        serializer = UserProfileSerializer(data = request.data)

        if serializer.is_valid():
            if request.data.get("phone") and request.data.get("living_area"):
                serializer.save(user_level = 3)
            elif request.data.get("phone"):
                serializer.save(user_level = 2)
            else:
                serializer.save(user_level = 1)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TokenView(views.APIView):

    authentication_classes = []

    def post(self, request):

        name = request.data.get("username")
        pwd = request.data.get("password")
        user = UserProfile.objects.filter(username = name, password = pwd).first()

        if not user:
            return Response("Wrong User Name or Password !", status = status.HTTP_400_BAD_REQUEST)

        try:
            token = auth.md5(name)
            UserToken.objects.update_or_create(user = user, defaults = {"token": token})
        except Exception as msg:
            return Response({"message":str(msg)}, status = status.HTTP_400_BAD_REQUEST)

        return Response({"message":"Get Token Successfully!", "token":token}, status = status.HTTP_201_CREATED)

class RealEstateDataView(views.APIView, PageNumberPagination):

    authentication_classes = [auth.Authentication,]

    def get(self, request):
        if request.user.user_level == 3:
            limit = "30"
        elif request.user.user_level == 2:
            limit = "20"
        else:
            limit = "10"

        try:
            command = "SELECT * FROM real_estate_taoyuan LIMIT " + limit + ";"
            external_db = database.ControlExternalDB()
            data = external_db.query(command)

        except Exception as msg:
            return Response({"message": str(msg)}, status=status.HTTP_400_BAD_REQUEST)

        page = self.paginate_queryset(data, request)

        if not page:
            return Response({"message": "Data Not Found !"}, status=status.HTTP_404_NOT_FOUND)

        return self.get_paginated_response(page)