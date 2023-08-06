from django import template
from django.core.exceptions import ObjectDoesNotExist
from ..models import DjangoAnalyticalServices

register = template.Library()


@register.inclusion_tag('base_template/template_tags/yandex_metrika.html')
def yandex_metrika():
    try:
        YANDEX_METRIKA_COUNTER_ID = DjangoAnalyticalServices.objects.get(service='YANDEX_METRIKA_COUNTER_ID')
    except ObjectDoesNotExist:
        YANDEX_METRIKA_COUNTER_ID = None

    return {"YANDEX_METRIKA_COUNTER_ID": YANDEX_METRIKA_COUNTER_ID}