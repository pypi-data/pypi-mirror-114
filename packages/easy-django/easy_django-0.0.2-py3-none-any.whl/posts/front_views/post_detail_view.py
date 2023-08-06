from django.shortcuts import render
from django.views import View
from ..models import Posts
from ..util import get_config


class PostDetailView(View):
    template_name = 'posts/post_detail.html'

    def get(self, request, post_id, *args, **kwargs):
        self.post_id = post_id
        self._set_config()
        self._set_query_set()
        self._set_title()
        self._set_keywords()
        self._set_description()

        context = {
            'post_detail': self.post,
            'title': self.title,
            'config': self.config,
            'keywords': self.html_keywords,
            'description': self.html_description
        }

        return render(
            request,
            template_name=self.template_name,
            context=context
        )

    def _set_config(self):
        self.config = get_config()

    def _set_query_set(self):
        try:
            self.post = Posts.objects.get(pk=self.post_id)
        except:
            self.post = None

    def _set_title(self):
        try:
            self.title = self.post.post_header
        except:
            self.title = ''

    def _set_keywords(self):

        project_keywords = self.config['keywords']
        try:
            post_keywords = self.post.post_header
        except:
            post_keywords = ''
        self.html_keywords = f'<meta name="keywords" content="{project_keywords},{post_keywords}"/>'

    def _set_description(self):
        try:
            self.html_description = f'<meta name="description" content="{self.post.post_content_preview}" />'
        except:
            self.html_description = f'<meta name="description" content=" "/>'


