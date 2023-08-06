from django.shortcuts import render
from pprint import pprint as print
import time


def test(request):
    return render(request, 'base_navbar/test.html')
