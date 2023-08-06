from .models import Price


def get_price_list():
    price = Price.objects.filter(status='ACTIVE')
    return price