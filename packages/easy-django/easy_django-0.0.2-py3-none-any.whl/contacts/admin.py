from django.contrib import admin
from .models import Contact
from django.contrib.admin.decorators import register


@register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('contact_type', 'size', 'style', 'status', )
    list_filter = ('status', 'contact_type', )