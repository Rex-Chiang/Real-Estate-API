import pytest
from RealEstateApp.models import UserProfile, UserToken
from RealEstateApp.utils import auth

pytestmark = pytest.mark.django_db

class TestModel:
    def test_UserProfile(self):
        assert UserProfile.objects.count() == 6

    def test_UserProfile_create(self):
        UserProfile.objects.create_user(username = "test", password = "test123", email = "test@test.com")
        assert UserProfile.objects.count() == 7

    def test_UserProfile_retrieve(self):
        obj = UserProfile.objects.filter(username = "user1").first()
        assert obj.user_level == 1

    def test_UserToken(self):
        assert UserToken.objects.count() == 5

    def test_UserToken_create(self):
        user = UserProfile.objects.filter(username = "user1").first()
        token = auth.md5("user1")
        UserToken.objects.update_or_create(user = user, defaults = {"token": token})
        obj = UserToken.objects.filter(user_id = 1).first()
        assert obj.token == token

    def test_UserToken_retrieve(self):
        obj = UserToken.objects.filter(user_id = 1).first()
        assert obj.token == "f02483cf5de6856dbe391f1b977ae341"