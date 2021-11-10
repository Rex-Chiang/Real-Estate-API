from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    user_level = models.IntegerField(default = 1)
    email = models.EmailField(unique=True, max_length=50, verbose_name="Email")
    # Use null=True and blank=True to cover the null value in the situation that field need to be unique
    phone = models.CharField(unique = True, null=True, blank=True, max_length = 10, verbose_name = "Phone")
    living_area = models.CharField(max_length = 50, verbose_name = "Living Area")
    date_joined = models.DateTimeField(default = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"), verbose_name = "Joined Date")

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = verbose_name
        db_table = "UserProfile"

    def __str__(self):
        return self.username

class UserToken(models.Model):
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    token = models.CharField(max_length = 100)
    updated_time = models.DateTimeField(auto_now = True, verbose_name="Updated Time")

    class Meta:
        verbose_name = "User Token"
        verbose_name_plural = verbose_name
        db_table = "UserToken"

    def __str__(self):
        return self.token