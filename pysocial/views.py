# Python Import
import re

from pymongo import ASCENDING
from pymongo import DESCENDING

# Django Import
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# PySocial Import
from core import cursor
from core.func_tools import path_pic_box
from core.json_utils import MongoJsonResponse
from settings import last_lesson_qty
from settings import search_limit_count


def home(request):
    kwargs = {}

    # Get data from DB
    news = cursor.home.find_one({'kind': 'news'})
    what = cursor.home.find_one({'kind': 'what'})
    roadmap = cursor.home.find({'kind': 'roadmap'}).sort('order', ASCENDING)
    boxs = cursor.box.find().sort('order', ASCENDING)
    last_lesson = list(cursor.lessons.find(
            {'published': True},
            {'body': 0}
        ).sort(
            'created',
            DESCENDING
        ).limit(last_lesson_qty)
    )

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
                    new_doc['content_id'] = doc['content_id']

                    final_last_content.append(new_doc)

        kwargs['last_lesson'] = final_last_content

    return render(request, 'home.html', kwargs)


@require_POST
@csrf_exempt
def search(request):
    kwargs = {}
    search = request.POST.get('search', None)

    if search:
        search = re.compile(search, re.IGNORECASE)
        user_criteria = {
            '$or': [
                {'username': search},
                {'first_name': search},
                {'last_name': search}
            ]
        }
        user_projection = {
            'username': 1,
            'first_name': 1,
            'last_name': 1
        }
        kwargs['users'] = list(cursor.users.find(
                user_criteria,
                user_projection
            ).limit(
                search_limit_count
            )
        )

        box_criteria = {
            '$or': [
                {'title': search},
                {'title_fa': search},
                {'description': search}
            ]
        }
        kwargs['boxs'] = list(cursor.box.find(box_criteria).limit(
            search_limit_count
        ))

        content_criteria = {
            '$or': [
                {'title': search},
                {'description': search}
            ]
        }
        content_projection = {
            'description': 1,
            'box_id': 1
        }
        kwargs['contents'] = list(cursor.contents.find(
                content_criteria,
                content_projection
            ).limit(
                search_limit_count
            )
        )

        lesson_criteria = {
            'body': search
        }
        lesson_projection = {
            'content_id': 1,
            'body': 1,
            'box_id': 1
        }
        kwargs['lessons'] = list(cursor.lessons.find(
                lesson_criteria,
                lesson_projection
            ).limit(
                search_limit_count
            )
        )

    return MongoJsonResponse(kwargs)


def under_construction(request):
    return render(request, 'under_construction.html')
