# Python Import
from bson.objectid import ObjectId

# Django Import
from django.shortcuts import render

# PySocial Import
from core import cursor


def content(request, dashboard, _id):
    kwargs = {}
    kwargs['contents'] = cursor.contents.find({'box_id': ObjectId(_id)})
    return render(request, 'dashboard/content.html', kwargs)


def lesson(request, dashboard, _id):
    kwargs = {}
    kwargs['lesson'] = cursor.lessons.find_one({'_id': ObjectId(_id)})
    return render(request, 'dashboard/lesson.html', kwargs)
