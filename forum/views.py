# Python Import

# Django Import
from django.shortcuts import render

# PySocial Import
from core import cursor


def show_forum(request):
    kwargs = {}
    kwargs['forum'] = list(cursor.forum.find())
    return render(request, 'forum/show_forum.html', kwargs)
