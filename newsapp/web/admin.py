from django.contrib import admin
from newsapp.web.models import Ads


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date', 'expiration_date', )
    list_filter = ('publish_date', )
