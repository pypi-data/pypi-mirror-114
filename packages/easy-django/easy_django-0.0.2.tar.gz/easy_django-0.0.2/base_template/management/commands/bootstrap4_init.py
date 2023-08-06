from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.utils import OperationalError

from ...models import HTMLHeadLink, HTMLBodyScript


class Command(BaseCommand):
    help = '\tInstalling bootstrap 4.6 in html head and body'

    def handle(self, *args, **options):
        self._init()

    def _init(self):
        try:
            HTMLHeadLink.objects.create(label="Bootstrap 4.6 CSS", content='<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css" integrity="sha384-B0vP5xmATw1+K9KRQjQERJvTumQW0nPEzvF6L/Z6nronJ3oUOFUFpCjEUQouq2+l" crossorigin="anonymous">')
            print("HTML Head link to Bootstrap 4.6 CSS inserted")
        except:
            print("HTML Head link to Bootstrap 4.6 CSS already exists")

        try:
            HTMLBodyScript.objects.create(
                label="Bootstrap 4.6 jquery-3.5.1.slim.min.js"
                , content='<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>'
                , order=100
            )
            print('HTML Body script Bootstrap 4.6 jquery-3.5.1.slim.min.js inserted')
        except:
            print('HTML Body script Bootstrap 4.6 jquery-3.5.1.slim.min.js already exists')

        try:
            HTMLBodyScript.objects.create(
                label="Bootstrap 4.6 popper.min.js"
                , content='<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>'
                , order=200
            )
            print('HTML Body script Bootstrap 4.6 popper.min.js inserted')
        except:
            print('HTML Body script Bootstrap 4.6 popper.min.js already exists')

        try:
            HTMLBodyScript.objects.create(
                label="Bootstrap 4.6 bootstrap.min.js"
                , content='<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.min.js" integrity="sha384-+YQ4JLhjyBLPDQt//I+STsc9iw4uQqACwlvpslubQzn4u2UU2UFM80nGisd026JF" crossorigin="anonymous"></script>'
                , order=300
            )
            print('HTML Body script Bootstrap 4.6 bootstrap.min.js inserted')
        except:
            print('HTML Body script Bootstrap 4.6 bootstrap.min.js already exists')