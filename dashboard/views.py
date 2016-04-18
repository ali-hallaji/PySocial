# Python Import
from bson.objectid import ObjectId

# Django Import
from django.shortcuts import render

# PySocial Import
from core import cursor
from core.func_tools import path_pic_box


def content(request, dashboard, _id):
    kwargs = {}
    kwargs['contents'] = list(cursor.contents.find({'box_id': ObjectId(_id)}))
    kwargs['box'] = cursor.box.find_one({'title': dashboard})
    kwargs['box']['picture'] = path_pic_box(kwargs['box'])
    return render(request, 'dashboard/content.html', kwargs)


def lesson(request, dashboard, _id):
    kwargs = {}
    kwargs['lesson'] = cursor.lessons.find_one({'_id': ObjectId(_id)})
    return render(request, 'dashboard/lesson.html', kwargs)
