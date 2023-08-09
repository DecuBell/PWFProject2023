from django.contrib.auth import get_user_model
from django.db import models

from newsapp.accounts.models import Profile
from newsapp.articles.models import Article

UserModel = get_user_model()


class Comment(models.Model):
    MAX_COMMENT_LENGTH = 200

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(
        auto_now_add=True
    )
    comment_body = models.TextField(
        max_length=MAX_COMMENT_LENGTH
    )

    def ___str__(self):
        return f'Comment by {self.author.user.username} on {self.article.title}'
