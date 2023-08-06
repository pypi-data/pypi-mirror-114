from ..models import Favicon


def get_favicons():
    favicons_objects = Favicon.objects.all()
    favicons = []
    for item in favicons_objects:
        obj = {}
        obj['desktop'] = get_favicon_desktop(item)
        obj['android'] = get_favicon_android(item)
        obj['ios'] = get_favicon_ios(item)
        obj['macos'] = get_favicon_macos(item)
        obj['windows'] = get_favicon_windows(item)
        obj['favicon'] = item

        favicons.append(obj)

    return favicons


def get_favicon_desktop(favicon: Favicon):
    list = []
    # Десктоп
    obj = {}

    obj['type'] = 'image/x-icon'
    obj['sizes'] = '512x512'
    obj['rel'] = 'shortcut icon'
    obj['url'] = favicon.get_absolute_url_size(512)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = 'image/png'
    obj['sizes'] = '16x16'
    obj['rel'] = 'icon'
    obj['url'] = favicon.get_absolute_url_size(16)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = 'image/png'
    obj['sizes'] = '32x32'
    obj['rel'] = 'icon'
    obj['url'] = favicon.get_absolute_url_size(32)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = 'image/png'
    obj['sizes'] = '96x96'
    obj['rel'] = 'icon'
    obj['url'] = favicon.get_absolute_url_size(96)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = 'image/png'
    obj['sizes'] = '120x120'
    obj['rel'] = 'icon'
    obj['url'] = favicon.get_absolute_url_size(120)
    list.append(obj.copy())
    obj.clear()

    return list


def get_favicon_android(favicon: Favicon):
    list = []
    obj = {}
    obj['type'] = 'image/png'
    obj['sizes'] = '192x192'
    obj['rel'] = 'icon'
    obj['url'] = favicon.get_absolute_url_size(192)
    list.append(obj.copy())
    obj.clear()

    return list


def get_favicon_ios(favicon: Favicon):
    list = []
    obj = {}

    obj['type'] = None
    obj['sizes'] = '57x57'
    obj['rel'] = 'apple-touch-icon'
    obj['url'] = favicon.get_absolute_url_size(57)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = None
    obj['sizes'] = '60x60'
    obj['rel'] = 'apple-touch-icon'
    obj['url'] = favicon.get_absolute_url_size(60)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = None
    obj['sizes'] = '72x72'
    obj['rel'] = 'apple-touch-icon'
    obj['url'] = favicon.get_absolute_url_size(72)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = None
    obj['sizes'] = '76x76'
    obj['rel'] = 'apple-touch-icon'
    obj['url'] = favicon.get_absolute_url_size(76)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = None
    obj['sizes'] = '114x114'
    obj['rel'] = 'apple-touch-icon'
    obj['url'] = favicon.get_absolute_url_size(114)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = None
    obj['sizes'] = '120x120'
    obj['rel'] = 'apple-touch-icon'
    obj['url'] = favicon.get_absolute_url_size(120)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = None
    obj['sizes'] = '144x144'
    obj['rel'] = 'apple-touch-icon'
    obj['url'] = favicon.get_absolute_url_size(144)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = None
    obj['sizes'] = '152x152'
    obj['rel'] = 'apple-touch-icon'
    obj['url'] = favicon.get_absolute_url_size(152)
    list.append(obj.copy())
    obj.clear()

    obj['type'] = None
    obj['sizes'] = '180x180'
    obj['rel'] = 'apple-touch-icon'
    obj['url'] = favicon.get_absolute_url_size(180)
    list.append(obj.copy())
    obj.clear()

    return list


def get_favicon_macos(favicon: Favicon):
    list = []
    obj = {}

    obj['color'] = favicon.tile_color
    obj['rel'] = 'mask-icon'
    obj['url'] = favicon.get_absolute_url_size(512)
    list.append(obj.copy())
    obj.clear()

    return list


def get_favicon_windows(favicon: Favicon):
    list = []
    obj = {}

    obj['name'] = 'msapplication-square70x70logo'
    obj['content'] = favicon.get_absolute_url_size(70)
    list.append(obj.copy())
    obj.clear()

    obj['name'] = 'msapplication-square150x150logo'
    obj['content'] = favicon.get_absolute_url_size(150)
    list.append(obj.copy())
    obj.clear()

    obj['name'] = 'msapplication-wide310x150logo'
    obj['content'] = favicon.get_absolute_url_size(310)
    list.append(obj.copy())
    obj.clear()

    obj['name'] = 'msapplication-square310x310logo'
    obj['content'] = favicon.get_absolute_url_size(310)
    list.append(obj.copy())
    obj.clear()

    obj['name'] = 'msapplication-TileImage'
    obj['content'] = favicon.get_absolute_url_size(144)
    list.append(obj.copy())
    obj.clear()


    return list





































