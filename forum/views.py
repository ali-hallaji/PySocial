# Python Import

# Django Import
from django.shortcuts import render

# PySocial Import
from core import cursor


def show_forum(request):
    kwargs = {}
    kwargs['forum'] = list(cursor.forum.find())
    return render(request, 'forum/show_forum.html', kwargs)


def show_thread(request, _id):
    kwargs = {}
    criteria = {
        '_id': object(_id)
    }
    kwargs['thread'] = list(cursor.thread.find(criteria))
    return render(request, 'forum/show_thread.html', kwargs)
