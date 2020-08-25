from django.contrib import admin

from .models import Gallery, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ['title', ]


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'user']
    list_filter = ['user']
    prepopulated_fields = {'slug':('title',)}
