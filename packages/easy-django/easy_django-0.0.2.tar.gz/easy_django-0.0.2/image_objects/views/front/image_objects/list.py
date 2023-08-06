from django.shortcuts import render
from django.views import View

from ....service.search_image_objects import search_image_objects
from ....service.get_images import get_images_by_image_object_id
from ....permissions import get_perms_dict
from ....util import get_config


class ListImageObjects(View):
    template = 'image_objects/list.html'

    def get(self, request,  *args, **kwargs):
        self.request = request
        context = {}

        self.config = get_config()
        self._set_title()
        self._set_keywords()
        self._set_request_parametrs()
        self._set_query_set()

        context['config'] = self.config
        context['title'] = self.title
        context.update(get_perms_dict(request))
        context['list_image_objects'] = self.list_image_objects
        context['search_string'] = self.string
        context['last_days'] = self.last_days
        context['keywords'] = self.html_keywords

        return render(
            request
            , template_name=self.template
            , context=context
        )

    def _set_title(self):
        self.title = self.config['titles']['list_image_objects_title']

    def _set_keywords(self):
        project_keywords = self.config['keywords']
        self.html_keywords = f'<meta name="keywords" content="{project_keywords}"/>'

    def _set_request_parametrs(self):
        try:
            self.string = self.request.GET["search_string"]
        except:
            self.string = ''

        try:
            last_days = self.request.GET["last_days"]
            if last_days == "" or last_days == 0 or last_days is None:
                self.last_days = 737938
            else:
                self.last_days = int(last_days)
        except:
            self.last_days = self.config['default_last_days']

    def _set_query_set(self):
        image_objects = search_image_objects(last_days=self.last_days, string=self.string, quantity=30)
        _list_image_objects = image_objects

        self.list_image_objects = []

        for item in _list_image_objects:
            images = get_images_by_image_object_id(image_object_id=item.pk, status='ACTIVE')
            image_object = {
                'image_object': item
                , 'images': images
            }
            self.list_image_objects.append(image_object)



