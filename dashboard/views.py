# Python Import
from bson.objectid import ObjectId

# Django Import
from django.shortcuts import render

# PySocial Import
from core import cursor
from core.func_tools import path_pic_box
from core.func_tools import avatar_maker


def content(request, dashboard, _id):
    kwargs = {}

    # Get all users
    users = {}
    get_users = cursor.users.find(
        {
            'groups_name': {'$in': ['author']}
        },
        {
            '_id': 1,
            'username': 1,
            'last_name': 1,
            'first_name': 1,
            'social_auth': 1,
            'picture': 1
        }
    )

    for user in get_users:
        users[user['_id']] = user

    # Get all contents
    kwargs['contents'] = list(cursor.contents.find({'box_id': ObjectId(_id)}))

    # Get all boxs
    kwargs['box'] = cursor.box.find_one({'title': dashboard})

    # Set picture for box
    kwargs['box']['picture'] = path_pic_box(kwargs['box'])

    # Get all authors
    author_list = []
    authors = cursor.lessons.find(
        {
            'box_id': kwargs['box']['_id']
        },
        {
            'user_id': 1
        }
    )

    for author in authors:

        try:
            author_list.append(users[author['user_id']])

        except KeyError:
            continue

    # Get profile picture for author
    kwargs['authors'] = []

    for author in author_list:
        author = avatar_maker(author)

        if author not in kwargs['authors']:
            kwargs['authors'].append(author)

    return render(request, 'dashboard/content.html', kwargs)


def lesson(request, dashboard, _id):
    kwargs = {}
    kwargs['lesson'] = cursor.lessons.find_one({'_id': ObjectId(_id)})
    return render(request, 'dashboard/lesson.html', kwargs)
