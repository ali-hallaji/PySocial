# Django Import
from django.shortcuts import render

# PySocial Import
from core import cursor


def home(request):
    kwargs = {}
    news = cursor.home.find_one({'_type': 'news'})

    if news:
        kwargs['news'] = news['news']

    return render(request, 'home.html', kwargs)


def under_construction(request):
    return render(request, 'under_construction.html')
