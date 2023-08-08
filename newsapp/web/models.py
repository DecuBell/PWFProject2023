from enum import Enum

from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models


# class Article(models.Model):
#     user = models.ForeignKey(UserModel)
