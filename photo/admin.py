from django.contrib import admin

# Register your models here.
from photo.models import Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'photo', 'created', 'text', 'updated']
    list_filter = ['author', 'created', 'updated']
    search_fields = ['text', 'updated']
    raw_id_fields = ['author']
    ordering = ['-updated', '-created']

admin.site.register(Photo, PhotoAdmin)
