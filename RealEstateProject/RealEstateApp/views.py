from RealEstateApp.models import UserProfile, UserToken
from RealEstateApp.serializers import UserProfileSerializer
from RealEstateApp.utils import auth, database
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class RegisterView(views.APIView):
    # Skip the authentication when user register
    authentication_classes = []

    def post(self, request):

        serializer = UserProfileSerializer(data = request.data)

        if serializer.is_valid():
            # User who fill both phone and living_area fields will become level 3
            if request.data.get("phone") and request.data.get("living_area"):
                serializer.save(user_level = 3)
            # User who fill phone field will become level 2
            elif request.data.get("phone"):
                serializer.save(user_level = 2)
            # Other users will be level 1
            else:
                serializer.save(user_level = 1)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class TokenView(views.APIView):
    # Skip the authentication when user get the token key
    authentication_classes = []

    def post(self, request):

        name = request.data.get("username")
        pwd = request.data.get("password")
        user = UserProfile.objects.filter(username = name, password = pwd).first()

        if not user:
            return Response("Wrong User Name or Password !", status = status.HTTP_400_BAD_REQUEST)

        try:
            # Use user name to generate token key
            token = auth.md5(name)
            UserToken.objects.update_or_create(user = user, defaults = {"token": token})
        except Exception as msg:
            return Response({"message":str(msg)}, status = status.HTTP_400_BAD_REQUEST)

        return Response({"message":"Get Token Successfully!", "token":token}, status = status.HTTP_201_CREATED)

class RealEstateDataView(views.APIView, PageNumberPagination):
    # This line can be remove since authentication is in global setting
    authentication_classes = [auth.Authentication,]

    def get(self, request):
        # Use user level to distinguish the data amount that user can get
        if request.user.user_level == 3:
            limit = "30"
        elif request.user.user_level == 2:
            limit = "20"
        else:
            limit = "10"

        try:
            # Default to use data in Taoyuan
            command = "SELECT * FROM real_estate_taoyuan LIMIT " + limit + ";"
            external_db = database.ControlExternalDB()
            data = external_db.query(command)

        except Exception as msg:
            return Response({"message": str(msg)}, status=status.HTTP_400_BAD_REQUEST)

        # Paginate the data
        page = self.paginate_queryset(data, request)

        if not page:
            return Response({"message": "Data Not Found !"}, status=status.HTTP_404_NOT_FOUND)

        return self.get_paginated_response(page)

class RealEstateAreaDataView(views.APIView, PageNumberPagination):
    # Set the permission for this view
    # Only the user that user level greater than 1 can visit this view
    permission_classes = [auth.AdvancedSearch,]

    def get(self, request):
        try:
            area = request.query_params.get("area")
            # Default to use data in Taoyuan
            if not area:
                area = "taoyuan"

            command = "SELECT * FROM real_estate_" + area.lower() + " LIMIT 10;"
            external_db = database.ControlExternalDB()
            data = external_db.query(command)

        except Exception as msg:
            return Response({"message": str(msg)}, status=status.HTTP_400_BAD_REQUEST)

        page = self.paginate_queryset(data, request)

        if not page:
            return Response({"message": "Data Not Found !"}, status=status.HTTP_404_NOT_FOUND)

        return self.get_paginated_response(page)