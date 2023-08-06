from django.shortcuts import render
from django.views import View
from ..service.search_posts import search_posts
from ..util import get_config


class PostsListView(View):
    template_name = 'posts/posts_list.html'

    def get(self, request, *args, **kwargs):
        """
            1. Присвоение запроса
            2. Получение конфигурации
            3. Получение ключевых слов
            4. Получение параметров запроса
            5. Получение заголовка страницы
            6. Получение объектов запроса
            7. Построение контекста
        """
        self.request = request
        self._set_config()
        self._set_keywords()
        self._set_request_params()
        self._set_title()
        self._set_query_set()


        context = {
            'empty': self.empty,
            'posts_list': self.posts,
            'last_days': self.last_days,
            'search_string': self.string,
            'config': self.config,
            'keywords': self.html_keywords,
            'title': self.config['posts_list_title']
        }

        return render(
            request,
            template_name=self.template_name,
            context=context
        )

    def _set_keywords(self):
        project_keywords = self.config['keywords']
        self.html_keywords = f'<meta name="keywords" content="{project_keywords}"/>'

    def _set_config(self):
        self.config = get_config()

    def _set_request_params(self):
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
        self.posts = search_posts(string=self.string, last_days=self.last_days)

        if len(self.posts) < 1:
            self.empty = True
        else:
            self.empty = False

    def _set_title(self):
        self.title = self.config['posts_list_title']

