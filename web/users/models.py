from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    def create(self, username, password, **extra_fields):
        user = self.model(username=username.lower(), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **extra_fields):
        return self.create(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.SlugField(max_length=16, db_index=True, unique=True)
    image = models.ImageField(
        upload_to="users/",
        default="users/default-image.png",
        blank=True,
    )
    display_name = models.CharField(max_length=48, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    website_links = ArrayField(models.URLField(), size=10, blank=True, default=list)
    last_login = None

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"User({self.username})"
