from RealEstateApp.models import UserProfile
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["username", "password", "user_level", "email", "phone", "living_area"]
        extra_kwargs = {
            "email": {"required": True},
            "phone": {"required": False},
            "living_area": {"required": False},
            "password": {"write_only": True},}