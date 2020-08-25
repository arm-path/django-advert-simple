from django.contrib import admin
from .models import Advert


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.site_header = "Администрирование сайта"
admin.site.site_title = "Адимнистрирование сайта"
