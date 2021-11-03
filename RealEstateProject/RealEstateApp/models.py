from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    user_level_choices = ((1, "Level 1"), (2, "Level 2"), (3, "Level 3"),)
    user_level = models.IntegerField(choices = user_level_choices)
    phone = models.CharField(max_length = 10, verbose_name = "Phone")
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