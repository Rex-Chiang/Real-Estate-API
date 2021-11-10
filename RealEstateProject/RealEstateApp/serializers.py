from RealEstateApp.models import UserProfile
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["username", "password", "user_level", "email", "phone", "living_area"]
        # Set phone and living_area fields to unrequired, but will upgrade user level if user fill
        # Set password field to write-only
        extra_kwargs = {
            "phone": {"required": False},
            "living_area": {"required": False},
            "password": {"write_only": True},}