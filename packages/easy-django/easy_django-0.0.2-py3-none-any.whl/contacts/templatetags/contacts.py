from django import template
from ..service.get_contacts import get_contacts

register = template.Library()


@register.inclusion_tag('contacts/contacts.html')
def show_contacts():
    contacts = get_contacts()

    return {"contacts": contacts}