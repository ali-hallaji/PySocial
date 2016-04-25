# Python Import
from pymongo import ASCENDING
from pymongo import DESCENDING

# Django Import
from django.shortcuts import render

# PySocial Import
from core import cursor
from core.func_tools import path_pic_box
from settings import last_lesson_qty as llq


def home(request):
    kwargs = {}

    # Get data from DB
    news = cursor.home.find_one({'kind': 'news'})
    what = cursor.home.find_one({'kind': 'what'})
    roadmap = cursor.home.find({'kind': 'roadmap'}).sort('order', ASCENDING)
    boxs = cursor.box.find().sort('order', ASCENDING)
    last_lesson = list(cursor.lessons.find({}, {'body': 0}).sort(
        'created',
        DESCENDING
    ).limit(llq))

    if news:
        kwargs['news'] = news['body']

    if what:
        kwargs['what'] = what['body']

    if roadmap:
        kwargs['roadmap'] = list(roadmap)

    if boxs:
        kwargs['boxs'] = list(boxs)

    if last_lesson:
        id_list = []

        for doc in last_lesson:
            id_list.append(doc['content_id'])

        content = cursor.contents.find({'_id': {'$in': id_list}})
        final_last_content = []

        for doc in last_lesson:
            doc['picture'] = path_pic_box(str(doc['box_id']))

            for doc2 in content:
                if doc['content_id'] == doc2['_id']:
                    doc['description'] = doc2['description']
                    doc['content_title'] = doc2['title']
                    doc['parent'] = doc2['parent']
                    doc['box_name_en'] = doc['parent'].split('|')[0]

            final_last_content.append(doc)

        kwargs['last_lesson'] = final_last_content

    return render(request, 'home.html', kwargs)


def under_construction(request):
    return render(request, 'under_construction.html')
