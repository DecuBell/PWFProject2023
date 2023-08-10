from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

UserModel = get_user_model()


def validate_only_numbers(value):
    if not value.isdigit():
        raise ValidationError('Only numbers (digits) are allowed.')


class Ads(models.Model):
    BUY = 'Buy'
    SELL = 'Sell'

    CATEGORIES = [(cat, cat) for cat in (BUY, SELL)]

    TITLE_MAX_LENGTH = 50
    BODY_MAX_LENGTH = 500
    PHONE_MIN_LENGTH = 10

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        blank=False,
        null=False
    )

    body = models.TextField(
        max_length=BODY_MAX_LENGTH,
        blank=False,
        null=False
    )

    category = models.CharField(
        max_length=max(len(cat) for (cat, x) in CATEGORIES),
        choices=CATEGORIES,
    )

    phone_number = models.CharField(
        validators=[
            validators.MinLengthValidator(PHONE_MIN_LENGTH),
            validate_only_numbers
        ],
        max_length=10,
        blank=True,
        null=True,
    )

    publish_date = models.DateField(
        auto_now_add=True,
    )

    expiration_date = models.DateField(
        default=timezone.now() + timezone.timedelta(days=7),
        blank=False,
        null=False
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
