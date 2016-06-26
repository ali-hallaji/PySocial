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
        'forum_id': object(_id)
    }
    kwargs['thread'] = list(cursor.thread.find(criteria))
    return render(request, 'forum/show_thread.html', kwargs)


def show_posts(request, _id):
    kwargs = {}
    criteria = {
        'thread_id': object(_id)
    }
    kwargs['posts'] = list(cursor.post.find(criteria))
    return render(request, 'forum/show_posts.html', kwargs)


def show_post(request, _id):
    kwargs = {}
    criteria = {
        '_id': object(_id)
    }
    kwargs['post'] = cursor.post.find_one(criteria)
    return render(request, 'forum/show_post.html', kwargs)
