from django.contrib import admin

from newsapp.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'author', 'publish_date', )
    list_filter = ('publish_date', )
