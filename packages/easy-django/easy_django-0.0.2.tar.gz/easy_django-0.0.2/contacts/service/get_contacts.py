from ..models import Contact


def get_contacts():
    contacts = Contact.objects.filter(status='ACTIVE').order_by('order')
    return contacts