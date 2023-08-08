from django.contrib import admin

from newsapp.articles.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ('publish_date', )
    list_display = ('title', 'category', 'publish_date', 'user', )
    search_fields = ('title', )
    list_filter = ('category', 'publish_date', 'user', )
    admin.site.site_title = 'Custom Project Admin Title'
    admin.site.site_header = 'Custom Project Admin'
