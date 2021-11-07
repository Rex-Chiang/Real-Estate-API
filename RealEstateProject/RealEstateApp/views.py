from RealEstateApp.models import UserProfile, UserToken
from RealEstateApp.serializers import UserProfileSerializer
from RealEstateApp.utils import auth
from django.conf import settings
from rest_framework.response import Response
from rest_framework import views, viewsets
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
import pymysql

class RegisterView(views.APIView):
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
    def post(self, request):

        name = request.data.get("username")
        pwd = request.data.get("password")
        user = UserProfile.objects.filter(username = name, password = pwd).first()

        if not user:
            return Response("Wrong User Name or Password !", status = status.HTTP_400_BAD_REQUEST)

        try:
            token = auth.md5(user)
            UserToken.objects.update_or_create(user = user, defaults = {"token": token})
        except Exception as msg:
            return Response({"message":str(msg)}, status = status.HTTP_400_BAD_REQUEST)

        return Response({"message":"Get Token Successfully!", "token":token}, status = status.HTTP_201_CREATED)

class RealEstateDataView(views.APIView, PageNumberPagination):

    authentication_classes = []

    def get(self, request):
        try:
            db = pymysql.connect(user = settings.DATABASES["real_estate_db"]["USER"],
                                 password = settings.DATABASES["real_estate_db"]["PASSWORD"],
                                 host = settings.DATABASES["real_estate_db"]["HOST"],
                                 port = int(settings.DATABASES["real_estate_db"]["PORT"]),
                                 db = settings.DATABASES["real_estate_db"]["NAME"],
                                 cursorclass = pymysql.cursors.DictCursor)
            cursor = db.cursor()
            cursor.execute("SELECT * FROM real_estate_taoyuan LIMIT 10;")
            data = cursor.fetchall()
            db.close()
        except Exception as msg:
            return Response({"message": str(msg)}, status=status.HTTP_400_BAD_REQUEST)

        page = self.paginate_queryset(data, request)

        if not page:
            return Response({"message": "Data Not Found !"}, status=status.HTTP_404_NOT_FOUND)

        return self.get_paginated_response(page)

