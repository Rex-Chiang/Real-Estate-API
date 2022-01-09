import pytest
import json
from django.urls import reverse
from RealEstateApp.views import RegisterView, TokenView, RealEstateDataView, RealEstateAreaDataView

pytestmark = pytest.mark.django_db

class TestView:
    def test_RegisterView(self, rf):
        request = rf.post(reverse('register'), {"username":"test", "password":"test123", "email":"test@test.com"})
        response = RegisterView.as_view()(request)
        assert response.status_code == 201

    def test_TokenView(self, rf):
        request = rf.post(reverse('token'), {"username":"user1", "password":"111"})
        response = TokenView.as_view()(request)
        assert response.status_code == 201
        response.render()
        content = json.loads(response.content)
        assert content["message"] == "Get Token Successfully!"

    def test_RealEstateDataView(self, rf):
        request = rf.get(reverse('data'), {"token":"f02483cf5de6856dbe391f1b977ae341"})
        response = RealEstateDataView.as_view()(request)
        assert response.status_code == 200
        response.render()
        content = json.loads(response.content)
        assert content["count"] == 10

    def test_RealEstateAreaDataView(self, rf):
        request = rf.get(reverse('area_data'), {"token":"f02483cf5de6856dbe391f1b977ae341"})
        response = RealEstateAreaDataView.as_view()(request)
        assert response.status_code == 403
        request = rf.get(reverse('area_data'), {"token": "60bd7a2f1b5c659b1e12e1039337ad44"})
        response = RealEstateAreaDataView.as_view()(request)
        assert response.status_code == 200
        response.render()
        content = json.loads(response.content)
        assert content["count"] == 10
