from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Navbar, NavbarItem, NavbarItemChild, SVG_html, Offcanvas, OffcanvasItem, OffcanvasItemChild


@register(Navbar)
class NavbarAdmin(admin.ModelAdmin):
    pass


@register(NavbarItem)
class NavbarItemAdmin(admin.ModelAdmin):
    pass


@register(NavbarItemChild)
class NavbarItemChildAdmin(admin.ModelAdmin):
    pass


@register(SVG_html)
class SVG_htmlAdmin(admin.ModelAdmin):
    pass


@register(Offcanvas)
class OffcanvasAdmin(admin.ModelAdmin):
    pass


@register(OffcanvasItem)
class OffcanvasItemAdmin(admin.ModelAdmin):
    pass


@register(OffcanvasItemChild)
class OffcanvasItemChildAdmin(admin.ModelAdmin):
    pass

