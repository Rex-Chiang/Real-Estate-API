from RealEstateApp.models import UserProfile
from RealEstateApp.serializers import UserProfileSerializer
from rest_framework.response import Response
from rest_framework import views, viewsets
from rest_framework import status

class RegisterView(views.APIView):
    def post(self, request):

        serializer = UserProfileSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)