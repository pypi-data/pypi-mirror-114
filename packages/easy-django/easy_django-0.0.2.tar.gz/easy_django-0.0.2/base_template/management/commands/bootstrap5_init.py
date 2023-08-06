from django.core.management.base import BaseCommand
from ...models import HTMLHeadLink, HTMLBodyScript


class Command(BaseCommand):
    help = '\tInstalling bootstrap 5.0 in html head and body'

    def handle(self, *args, **options):
        self._init()

    def _init(self):
        try:
            HTMLHeadLink.objects.create(label="Bootstrap 5.0 CSS", content='<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">')
            print("HTML Head link to Bootstrap 5.0 CSS inserted")
        except:
            print("HTML Head link to Bootstrap 5.0 CSS already exists")

        try:
            HTMLBodyScript.objects.create(
                label="Bootstrap 5.0 popperjs/core@2.9.2/dist/umd/popper.min.js"
                , content='<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>'
                , order=100
            )
            print('HTML Body script Bootstrap 5.0 popperjs/core@2.9.2/dist/umd/popper.min.js inserted')
        except:
            print('HTML Body script Bootstrap 5.0 popperjs/core@2.9.2/dist/umd/popper.min.js already exists')

        try:
            HTMLBodyScript.objects.create(
                label="Bootstrap 5.0 bootstrap@5.0.2/dist/js/bootstrap.min.js"
                , content='<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>'
                , order=200
            )
            print('HTML Body script Bootstrap 5.0 bootstrap@5.0.2/dist/js/bootstrap.min.js inserted')
        except:
            print('HTML Body script Bootstrap 5.0 bootstrap@5.0.2/dist/js/bootstrap.min.js already exists')