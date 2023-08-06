from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Posts


@register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = (
        'post_header'
        , 'post_date'
        , 'source'
        , 'status'
    )
    list_filter = (
        'status', 'post_date',
    )