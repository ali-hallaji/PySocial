# Python Import
from pymongo import ASCENDING

# Django Import
from django.shortcuts import render

# PySocial Import
from core import cursor


def home(request):
    kwargs = {}
    news = cursor.home.find_one({'kind': 'news'})
    what = cursor.home.find_one({'kind': 'what'})
    roadmap = cursor.home.find({'kind': 'roadmap'}).sort('order', ASCENDING)

    if news:
        kwargs['news'] = news['news']

    if what:
        kwargs['what'] = what['body']

    if roadmap:
        kwargs['roadmap'] = list(roadmap)

    return render(request, 'home.html', kwargs)


def under_construction(request):
    return render(request, 'under_construction.html')
