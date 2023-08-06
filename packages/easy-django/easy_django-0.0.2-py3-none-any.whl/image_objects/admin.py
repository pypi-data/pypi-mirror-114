from django.contrib import admin
from .models import ImageObject, Image
from django.contrib.admin.decorators import register


@register(ImageObject)
class ImageObjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'tags' ,'user', 'status',)
    list_filter = ('status', 'date', 'user', )
    search_fields = ('description', 'tags', 'title',)


@register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'image_object', 'uploaded_at', 'image',)
    list_filter = ('tag', 'status',)
    search_fields = ('title', 'tag', )
