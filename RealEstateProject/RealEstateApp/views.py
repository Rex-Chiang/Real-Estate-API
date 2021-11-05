from RealEstateApp.models import UserProfile, UserToken
from RealEstateApp.serializers import UserProfileSerializer
from RealEstateApp.utils import auth
from rest_framework.response import Response
from rest_framework import views, viewsets
from rest_framework import status
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

class RealEstateDataView(views.APIView):

    authentication_classes = [auth.Authentication,]

    def get(self, request):

        db = pymysql.connect(user="root", password="1209", host="127.0.0.1", port=3306, db="real_estate", cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM real_estate_taoyuan LIMIT 3;")
        data = cursor.fetchall()
        db.close()

        return Response(data)

