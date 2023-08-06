from django.shortcuts import render
from django.views import View

from .service import get_price_list
from .util import get_config


class PriceList(View):
    template = 'price/price_list.html'
    title = 'Price'

    def get(self, request,  *args, **kwargs):

        context = {}
        config = get_config()
        self.title = config['price_list_title']

        context['config'] = config
        context['title'] = self.title
        context['list_price'] = get_price_list()

        return render(
            request
            , template_name=self.template
            , context=context
        )