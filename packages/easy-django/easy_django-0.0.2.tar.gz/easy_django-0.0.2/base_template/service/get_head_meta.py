from ..models import HTMLHeadMeta


def get_head_meta():
    return HTMLHeadMeta.objects.all().order_by('order')