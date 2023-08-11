from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible


UserModel = get_user_model()


@deconstructible
class MaxImageSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        filesize = value.file.size
        if filesize > self.__megabytes_to_bytes(self.max_size):
            raise ValidationError(f'Image maximum allowed size ({self.max_size} MB) exceeded!')

    @staticmethod
    def __megabytes_to_bytes(value):
        return value * 1024 * 1024


def get_sentinel_user():
    #
    # profile_data = {
    #     'first_name': 'John',
    #     'last_name': 'Doe',
    #     'profile_description': 'This is a default user profile',
    #     'profile_picture': 'https://img.freepik.com/free-icon/user_318-804790.jpg'
    # }
    # # user = UserModel.objects.create_user_with_profile(email='default@zapital.bg', password='password', profile_data=profile_data)

    return get_user_model().objects.get_or_create(email='default@zapital.bg')[0]


class Article(models.Model):
    GENERAL_CRIME = 'General crimes'
    GOOD_NEWS = 'Good news'
    POLITICS = 'Politics'
    LOCAL_NEWS = 'Local News'
    STREET_REPORTERS = 'Street reporters'

    CATEGORIES = [(cat, cat) for cat in (GENERAL_CRIME, GOOD_NEWS, POLITICS, LOCAL_NEWS, STREET_REPORTERS)]

    TITLE_MAX_LENGTH = 150
    BODY_MAX_LENGTH = 2000

    HEADER_IMAGE_DIR = 'images/'
    HEADER_IMAGE_MAX_SIZE = 5

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

    publish_date = models.DateField(
        auto_now_add=True,
    )

    update_date = models.DateField(
        auto_now=True,
    )

    header_image = models.ImageField(
        upload_to=HEADER_IMAGE_DIR,
        null=True,
        blank=True,
        default='images/img_1_horizontal.jpg',
        validators=(
            MaxImageSizeValidator(HEADER_IMAGE_MAX_SIZE),
        )
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.SET(get_sentinel_user),
    )

    def __str__(self):
        return f"{self.title} {self.publish_date}"
