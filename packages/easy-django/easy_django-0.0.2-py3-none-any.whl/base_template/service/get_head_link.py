from ..models import HTMLHeadLink


def get_head_links():
    return HTMLHeadLink.objects.all().order_by('order')