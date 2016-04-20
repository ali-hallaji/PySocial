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
    criteria = {'box_id': ObjectId(_id)}
    contents = list(cursor.contents.find(criteria))
    kwargs['len_contents'] = len(contents)

    distinct_parent = []

    for content in contents:
        if content.get('parent', None):
            if content['parent'] not in distinct_parent:
                distinct_parent.append(content['parent'])

    kwargs['parents'] = []

    for parent in distinct_parent:
        criteria = {
            'settings_type': 'Parents',
            'parent_name': {'$regex': parent}
        }
        desc = cursor.settings.find_one(criteria)

        if not desc:
            continue
        else:
            desc = desc['description']

        title = parent.split('|')[1]

        countent_list = []
        for content in contents:
            if content['parent'] == parent:
                countent_list.append(content)

        kwargs['parents'].append((parent, desc, title, countent_list))

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
    kwargs['lesson'] = cursor.lessons.find_one({'content_id': ObjectId(_id)})

    criteria = {'_id': kwargs['lesson']['user_id']}
    kwargs['author'] = avatar_maker(cursor.users.find_one(criteria))

    criteria = {'_id': kwargs['lesson']['content_id']}
    kwargs['content'] = cursor.contents.find_one(criteria)

    kwargs['box_name_en'] = kwargs['content']['parent'].split('|')[0]
    kwargs['box_name_fa'] = kwargs['content']['parent'].split('|')[1]

    return render(request, 'dashboard/lesson.html', kwargs)
