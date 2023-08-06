from ..models import HTMLBodyScript


def get_body_scripts():
    return HTMLBodyScript.objects.all().order_by('order')