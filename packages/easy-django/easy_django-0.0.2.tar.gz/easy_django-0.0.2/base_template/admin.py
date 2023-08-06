from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import HTMLHeadLink, HTMLHeadMeta, HTMLBodyScript, DjangoAnalyticalServices, Favicon, CSS, Verifications, BaseTemplateCacheTime, Font


@register(HTMLHeadLink)
class HTMLHeadLinkAdmin(admin.ModelAdmin):
    list_display = ('label', 'content','order',)
    search_fields = ('label', 'content',)
    ordering = ('order',)


@register(HTMLHeadMeta)
class HTMLHeadMetaAdmin(admin.ModelAdmin):
    list_display = ('label', 'content','order',)
    search_fields = ('label', 'content',)
    ordering = ('order',)


@register(HTMLBodyScript)
class HTMLBodyScriptAdmin(admin.ModelAdmin):
    list_display = ('label', 'content','order',)
    search_fields = ('label', 'content',)
    ordering = ('order',)


@register(DjangoAnalyticalServices)
class DjangoAnalyticalServicesAdmin(admin.ModelAdmin):
    list_display = ('service', 'value',)
    search_fields = ('service', 'value',)


@register(Favicon)
class FaviconAdmin(admin.ModelAdmin):
    list_display = ('label', 'favicon', 'tile_color', 'app_name', 'theme_color',)
    search_fields = ('label', 'favicon', 'tile_color', 'app_name', 'theme_color',)


@register(CSS)
class FaviconAdmin(admin.ModelAdmin):
    list_display = ('label', 'content', )
    search_fields = ('label', 'content', )


@register(Verifications)
class VerificationsAdmin(admin.ModelAdmin):
    list_display = ('service', 'value',)
    search_fields = ('service', 'value',)


@register(BaseTemplateCacheTime)
class BaseTemplateCacheTimeAdmin(admin.ModelAdmin):
    list_display = ('base_template_part', 'seconds',)
    search_fields = ('base_template_part', 'seconds',)


@register(Font)
class FontAdmin(admin.ModelAdmin):
    list_display = ('label', 'content',)
    search_fields = ('label', 'content',)

