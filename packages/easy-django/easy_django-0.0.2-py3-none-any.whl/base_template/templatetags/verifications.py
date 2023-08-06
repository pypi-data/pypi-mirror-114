from django import template
from ..service.get_verifications import get_verifications

register = template.Library()


@register.inclusion_tag('base_template/template_tags/verifications.html')
def verifications():
    verifications = get_verifications()
    return {"verifications": verifications}