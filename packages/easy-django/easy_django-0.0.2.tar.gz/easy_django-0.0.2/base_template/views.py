from django.shortcuts import render


def test(request, exception=None, template='base_template/base.html'):
    context = {}
    return render(request, template_name='base_template/base.html', context=context)