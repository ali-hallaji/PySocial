# Python Import
import re

from pymongo import ASCENDING
from pymongo import DESCENDING

# Django Import
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# PySocial Import
from core import cursor
from forms import ForumForm


def show_forum(request):
    kwargs = {}
    kwargs['forum'] = list(cursor.forum.find().sort('sort', ASCENDING))
    return render(request, 'forum/show_forum.html', kwargs)


@login_required
def add_forum(request):
    kwargs = {}

    if request.method == 'POST':
        kwargs['form'] = ForumForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data

    else:
        kwargs['form'] = ForumForm()

    return render(request, 'forum/forum.html', kwargs)
