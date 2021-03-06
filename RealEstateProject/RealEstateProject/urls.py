"""RealEstateProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.documentation import include_docs_urls
from RealEstateApp.views import RegisterView, TokenView, RealEstateDataView, RealEstateAreaDataView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Skip the authentication when user visit API document
    path(r'api/doc/', include_docs_urls(title = "Real Estate API Document", authentication_classes = [])),
    path(r'api/register/', RegisterView.as_view(), name = "register"),
    path(r'api/token/', TokenView.as_view(), name = "token"),
    path(r'api/real_estate_data/', RealEstateDataView.as_view(), name = "data"),
    path(r'api/real_estate_area_data/', RealEstateAreaDataView.as_view(), name = "area_data"),
]
