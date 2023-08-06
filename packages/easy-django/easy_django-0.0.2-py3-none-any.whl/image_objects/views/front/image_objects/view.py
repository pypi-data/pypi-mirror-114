from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404

from ....models import ImageObject
from ....service.get_images import get_images_by_image_object_id
from ....permissions import get_perms_dict
from ....util import get_config


class ViewImageObject(View):
    template = 'image_objects/view.html'
    image_object_does_not_exists_template = 'image_objects/_/add_image_object.html'

    def get(self, request, image_object_id, *args, **kwargs):

        self.image_object_id = image_object_id
        self._set_config()
        self._set_query_set()
        self._set_title()
        self._set_keywords()
        self._set_description()

        context = {}
        context['config'] = self.config
        context.update(get_perms_dict(request))
        context['image_object'] = self.image_object
        context['images'] = self.images
        context['title'] = self.title
        context['keywords'] = self.html_keywords
        context['description'] = self.html_description

        return render(
            request
            , template_name=self.template
            , context=context
        )

    def _set_config(self):
        self.config = get_config()

    def _set_title(self):
        self.title = self.image_object.title

    def _set_keywords(self):
        project_keywords = self.config['keywords']
        image_object_keywords = self.image_object.tags
        self.html_keywords = f'<meta name="keywords" content="{project_keywords}, {image_object_keywords}"/>'

    def _set_query_set(self):
        # self.image_object = ImageObject.objects.get(pk=self.image_object_id)
        self.image_object = get_object_or_404(ImageObject, pk=self.image_object_id)
        self.images = get_images_by_image_object_id(self.image_object_id, 'ACTIVE')

    def _set_description(self):
        self.html_description = f'<meta name="description" content="{self.image_object.title}. {self.image_object.tags}" />'


