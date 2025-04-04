from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser


class UserManager(BaseUserManager):
    def create(self, username, password, **extra_fields):
        user = self.model(username=username.lower(), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **extra_fields):
        return self.create(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, db_index=True, unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"User({self.username})"
