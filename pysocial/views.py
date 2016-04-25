# Python Import
from pymongo import ASCENDING
from pymongo import DESCENDING

# Django Import
from django.shortcuts import render

# PySocial Import
from settings import last_lesson_qty
from core import cursor


def home(request):
    kwargs = {}

    # Get data from DB
    news = cursor.home.find_one({'kind': 'news'})
    what = cursor.home.find_one({'kind': 'what'})
    roadmap = cursor.home.find({'kind': 'roadmap'}).sort('order', ASCENDING)
    boxs = cursor.box.find().sort('order', ASCENDING)
    last_lesson = cursor.lessons.find().sort('created', DESCENDING)

    if news:
        kwargs['news'] = news['body']

    if what:
        kwargs['what'] = what['body']

    if roadmap:
        kwargs['roadmap'] = list(roadmap)

    if boxs:
        kwargs['boxs'] = list(boxs)

    if last_lesson:
        kwargs['last_lesson'] = list(last_lesson.limit(last_lesson_qty))

    return render(request, 'home.html', kwargs)


def under_construction(request):
    return render(request, 'under_construction.html')
