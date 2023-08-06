from django.db import models
from django.conf import settings

CSS_FRAMEWORKS = [
    ('BS4', 'Bootstrap 4')
    , ('BS5', 'Bootstrap 5')
]

NAVBAR_POSITION = [
    ('top', 'top')
    , ('bottom', 'bottom')
]

NAVBAR_UL_POSITION = [
    ('mx-auto', 'center')
    , ('me-auto', 'left')
    , ('ms-auto', 'right')
]

NAVBAR_EXPAND = [
    (' ', 'None')
    , ('-sm', 'sm')
    , ('-md', 'md')
    , ('-lg', 'lg')
    , ('-xl', 'xl')
    , ('-xxl', 'xxl')
]

NAVBAR_BG = [
    (' ', 'None')
    , ('bg-primary', 'Primary')
    , ('bg-secondary', 'Secondary')
    , ('bg-success', 'Success')
    , ('bg-warning', 'Warning')
    , ('bg-info', 'Info')
    , ('bg-light', 'Light')
    , ('bg-dark', 'Dark')
    , ('bg-white', 'White')
]

NAVBAR_STYLE = [
    (' ', 'None')
    , ('navbar-dark', 'Dark')
    , ('navbar-light', 'Light')
]

NAVBAR_ITEM_TYPE = [
    ('btn', 'Button')
    , ('nav-link', 'Link')
]

NAVBAR_ITEM_TYPE_STYLE = [
    (' ', 'None')
    , ('btn-primary', 'Primary')
    , ('btn-secondary', 'Secondary')
    , ('btn-success', 'Success')
    , ('btn-warning', 'Warning')
    , ('btn-info', 'Info')
    , ('btn-light', 'Light')
    , ('btn-dark', 'Dark')
    , ('btn-white', 'White')
]

OFFCANVAS_PLACEMENT = [
    ('offcanvas-start', 'left')
    , ('offcanvas-end', 'right')
    , ('offcanvas-top', 'top')
    , ('offcanvas-bottom', 'bottom')
]

OFFCANVAS_BTN_STYLE = [
    (' ', 'None')
    , ('btn-primary', 'Primary')
    , ('btn-secondary', 'Secondary')
    , ('btn-success', 'Success')
    , ('btn-warning', 'Warning')
    , ('btn-info', 'Info')
    , ('btn-light', 'Light')
    , ('btn-dark', 'Dark')
    , ('btn-white', 'White')
]


class SVG_html(models.Model):
    label = models.CharField(
        null=False
        , default="My SVG html"
        , verbose_name="Label for SVG html"
        , max_length=50
    )

    content = models.TextField(
        null=False
        , default="SVG"
        , verbose_name="SVG html"
        , max_length=4096
    )

    def __str__(self):
        return f'{self.label}'

    class Meta:
        verbose_name = 'SVG'
        verbose_name_plural = 'SVG'


class Navbar(models.Model):
    label = models.CharField(
        null=False
        , default="My navbar"
        , verbose_name="Label for navbar"
        , max_length=50
    )

    css_framework = models.CharField(
        choices=CSS_FRAMEWORKS
        , null=False
        , default="BS5"
        , verbose_name="CSS framework"
        , max_length=100
    )

    position = models.CharField(
        choices=NAVBAR_POSITION
        , null=False
        , default="top"
        , verbose_name="Navbar position (fixed top/fixed bottom)"
        , max_length=100
    )

    ul_position = models.CharField(
        choices=NAVBAR_UL_POSITION
        , null=False
        , default="mx-auto"
        , verbose_name="Navbar position (left/center/right)"
        , max_length=100
    )

    navbar_expand = models.CharField(
        choices=NAVBAR_EXPAND
        , null=False
        , default=" "
        , verbose_name="Navbar expand"
        , max_length=100
    )

    navbar_bg = models.CharField(
        choices=NAVBAR_BG
        , null=False
        , default=" "
        , verbose_name="Navbar background"
        , max_length=100
    )

    navbar_style = models.CharField(
        choices=NAVBAR_STYLE
        , null=False
        , default=" "
        , verbose_name="Navbar style"
        , max_length=100
    )

    nav_extraclass = models.CharField(
        null=False
        , default="my-navbar-nav-class"
        , verbose_name="Nav class for customisation"
        , max_length=512
    )

    ul_extraclass = models.CharField(
        null=False
        , default="my-navbar-ul-class"
        , verbose_name="Ul class for customisation"
        , max_length=512
    )

    svg_toggler_icon = models.ForeignKey(
        'SVG_html'
        , on_delete=models.PROTECT
        , verbose_name="toggler icon from SVG html model"
        , null=True
        , blank=True
    )

    is_collapsed = models.BooleanField(
        default=False
        , verbose_name="Is collapsed navbar"
    )

    is_enabled = models.BooleanField(
        default=True
        , verbose_name="Is use this navbar"
    )

    @property
    def get_items(self):
        return NavbarItem.objects.filter(is_enabled=True, navbar__pk=self.pk).order_by('order')

    def __str__(self):
        return f'{self.label} {self.css_framework} {self.position} is collapsed: {self.is_collapsed} is enabled {self.is_enabled}'


class NavbarItem(models.Model):
    label = models.CharField(
        null=False
        , default="My navbar item"
        , verbose_name="Label for navbar item"
        , max_length=50
    )

    url = models.CharField(
        verbose_name="Url"
        , default="#"
        , null=False
        , max_length=1024

    )

    navbar = models.ForeignKey(
        'Navbar'
        , on_delete=models.CASCADE
        , verbose_name="Navbar"
        , related_name="items"
    )

    order = models.IntegerField(
        unique=True
        , default=1
        , null=False
        , verbose_name="Ordering in navbar"
        ,
    )

    type = models.CharField(
        choices=NAVBAR_ITEM_TYPE
        , null=False
        , default='link'
        , max_length=100
    )

    btn_style = models.CharField(
        choices=NAVBAR_ITEM_TYPE_STYLE
        , null=True
        , blank=True
        , default='btn-primary'
        , max_length=100
        , verbose_name="Button style (if type button)"
    )

    svg_html = models.ForeignKey(
        "SVG_html"
        , on_delete=models.PROTECT
        , related_name="navbar_items"
        , blank=True
        , null=True
    )

    offcanvas = models.ForeignKey(
        'base_navbar.Offcanvas'
        , on_delete=models.PROTECT
        , null=True
        , blank=True
    )

    is_enabled = models.BooleanField(
        default=True
        , verbose_name="Is use this navbar item"
    )

    # extraclasses

    def __str__(self):
        return f'{self.label} {self.type} {self.order} {self.url} is enabled {self.is_enabled}'

    @property
    def get_children(self):
        # return NavbarItemChild.objects.filter(is_enabled=True, navbar_item__pk=self.pk).order_by('order')
        children = NavbarItemChild.objects.filter(is_enabled=True, navbar_item__pk=self.pk).order_by('order')
        if len(children) > 0:
            return children
        else:
            return None


class NavbarItemChild(models.Model):
    label = models.CharField(
        null=False
        , default="My navbar item"
        , verbose_name="Label for navbar item"
        , max_length=50
    )

    url = models.CharField(
        verbose_name="Url"
        , default="#"
        , null=False
        , max_length=1024

    )

    navbar_item = models.ForeignKey(
        'NavbarItem'
        , on_delete=models.CASCADE
        , verbose_name="Navbar item"
        , related_name="items"
    )

    order = models.IntegerField(
        unique=True
        , default=1
        , null=False
        , verbose_name="Ordering in navbar item"
        ,
    )

    svg_html = models.ForeignKey(
        "SVG_html"
        , on_delete=models.PROTECT
        , related_name="navbar_child_items"
        , blank=True
        , null=True
    )

    is_enabled = models.BooleanField(
        default=True
        , verbose_name="Is use this navbar item child"
    )

    # extraclasses

    def __str__(self):
        return f'{self.label} {self.order} {self.url} is enabled {self.is_enabled}'


class Offcanvas(models.Model):
    label = models.CharField(
        null=False
        , default="My offcanvas"
        , verbose_name="Label for offcanvas"
        , max_length=50
    )

    placement = models.CharField(
        choices=OFFCANVAS_PLACEMENT
        , null=False
        , default="top"
        , verbose_name="Offcanvas placement"
        , max_length=100
    )

    text = models.TextField(
        null=True
        , blank=True
        , verbose_name="Text for offcanvas"
        , max_length=2048
    )

    extraclass = models.CharField(
        null=False
        , default="my-offcanvas-extra-class"
        , verbose_name="For customisation"
        , max_length=512
    )

    body_extraclass = models.CharField(
        null=False
        , default="my-offcanvas-body-extra-class"
        , verbose_name="For customisation"
        , max_length=512
    )

    header_extraclass = models.CharField(
        null=False
        , default="my-offcanvas-header-extra-class"
        , verbose_name="For customisation"
        , max_length=512
    )

    title_extraclass = models.CharField(
        null=False
        , default="my-offcanvas-title-extra-class"
        , verbose_name="For customisation"
        , max_length=512
    )

    def __str__(self):
        return f'{self.label}'

    @property
    def get_items(self):
        return OffcanvasItem.objects.filter(offcanvas__pk=self.pk, is_enabled=True).order_by('order')


class OffcanvasItem(models.Model):
    label = models.CharField(
        null=False
        , default="My offcanvas item"
        , verbose_name="Label for offcanvas item"
        , max_length=50
    )

    url = models.CharField(
        verbose_name="Url"
        , default="#"
        , null=False
        , max_length=1024

    )

    offcanvas = models.ForeignKey(
        'base_navbar.Offcanvas'
        , on_delete=models.CASCADE
        , verbose_name="Offcanvas"
        , related_name="items"
    )

    order = models.IntegerField(
        unique=True
        , default=1
        , null=False
        , verbose_name="Ordering in offcanvas"
        ,
    )

    extraclass = models.CharField(
        null=False
        , default="my-offcanvas-item-extra-class"
        , verbose_name="For customisation"
        , max_length=512
    )

    svg_html = models.ForeignKey(
        "SVG_html"
        , on_delete=models.PROTECT
        , related_name="offcanvas_items"
        , blank=True
        , null=True
    )

    btn_style = models.CharField(
        choices=OFFCANVAS_BTN_STYLE
        , null=True
        , blank=True
        , default='btn-primary'
        , max_length=100
        , verbose_name="Button style"
    )

    w = models.CharField(
        max_length=50
        , default="w-75"
        , null=False
        , verbose_name="Width"
    )

    is_enabled = models.BooleanField(
        default=True
        , verbose_name="Is use this offcanvas item"
    )

    def __str__(self):
        return f'{self.label}'

    @property
    def get_children(self):
        children = OffcanvasItemChild.objects.filter(is_enabled=True, offcanvas_item__pk=self.pk).order_by('order')
        if len(children) > 0:
            return children
        else:
            return None


class OffcanvasItemChild(models.Model):
    label = models.CharField(
        null=False
        , default="My offcanvas child item"
        , verbose_name="Label for offcanvas child item"
        , max_length=50
    )

    url = models.CharField(
        verbose_name="Url"
        , default="#"
        , null=False
        , max_length=1024

    )

    offcanvas_item = models.ForeignKey(
        'base_navbar.OffcanvasItem'
        , on_delete=models.CASCADE
        , verbose_name="Offcanvas item"
        , related_name="items"
    )

    order = models.IntegerField(
        unique=True
        , default=1
        , null=False
        , verbose_name="Ordering in offcanvas item"
        ,
    )

    svg_html = models.ForeignKey(
        "SVG_html"
        , on_delete=models.PROTECT
        , related_name="offcanvas_child_items"
        , blank=True
        , null=True
    )

    extraclass = models.CharField(
        null=False
        , default="my-offcanvas-item-child-extra-class"
        , verbose_name="For customisation"
        , max_length=512
    )

    w = models.CharField(
        max_length=50
        , default="w-75"
        , null=False
        , verbose_name="Width"
    )

    is_enabled = models.BooleanField(
        default=True
        , verbose_name="Is use this navbar item child"
    )

    def __str__(self):
        return f'{self.label}'
