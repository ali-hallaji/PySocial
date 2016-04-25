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

        all_content = list(cursor.contents.find({'_id': {'$in': id_list}}))
        final_last_content = []

        for doc in last_lesson:

            for doc2 in all_content:
                if doc['content_id'] == doc2['_id']:
                    new_doc = {}
                    new_doc['_id'] = doc['_id']
                    new_doc['picture'] = path_pic_box(str(doc2['box_id']))
                    new_doc['description'] = doc2['description']
                    new_doc['content_title'] = doc2['title']
                    new_doc['box_name_en'] = doc2['parent'].split('|')[0]
                    new_doc['box_name_fa'] = doc2['parent'].split('|')[1]
                    new_doc['parent'] = doc2['parent']

                    final_last_content.append(new_doc)

        kwargs['last_lesson'] = final_last_content

    return render(request, 'home.html', kwargs)


def under_construction(request):
    return render(request, 'under_construction.html')
