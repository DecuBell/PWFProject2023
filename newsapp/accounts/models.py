from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model


class UserAuthManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class UserAuth(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = 'email'

    objects = UserAuthManager()

    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )


UserModel = get_user_model()


def validate_only_alphabetical(value):
    for char in value:
        if not char.isalpha():
            raise ValidationError('Only letters allowed')
    return True


class Profile(models.Model):
    FIRST_NAME_MIN_LENGTH = 2
    FIRST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_alphabetical,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_alphabetical,
        )
    )

    email = models.EmailField(
        unique=True,
    )

    profile_picture = models.URLField(
        null=True,
        blank=True,
    )

    creation_date = models.DateTimeField(
        auto_now_add=True,
    )

    profile_description = models.TextField(
        null=True,
        blank=True,
        max_length=255
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.email

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
