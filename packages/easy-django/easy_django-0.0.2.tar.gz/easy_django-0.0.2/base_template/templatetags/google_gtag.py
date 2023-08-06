from django import template
from django.core.exceptions import ObjectDoesNotExist
from ..models import DjangoAnalyticalServices

register = template.Library()


@register.inclusion_tag('base_template/template_tags/google_gtag.html')
def google_gtag():
    try:
        GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = DjangoAnalyticalServices.objects.get(service='GOOGLE_ANALYTICS_GTAG_PROPERTY_ID')
    except ObjectDoesNotExist:
        GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = None

    return {"GOOGLE_ANALYTICS_GTAG_PROPERTY_ID": GOOGLE_ANALYTICS_GTAG_PROPERTY_ID}