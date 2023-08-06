from django.contrib import admin
from .models import Price
from django.contrib.admin.decorators import register


@register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', 'image', 'created_at', 'status', )
    list_filter = ('status', )
    search_fields = ('description', 'title', )