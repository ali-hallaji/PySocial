# Python Import
import datetime
import logging
import os

from bson.objectid import ObjectId
from pymongo import ASCENDING
from pymongo import DESCENDING

# Django import
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# PySocial import
from core import cursor
from core.acl_general_funcs import get_all_view_names
from core.date_utils import gregorian_to_jalali
from core.acl_general_funcs import has_perm_view
from core.func_tools import find_pic_by_id
from core.func_tools import handle_uploaded_file
from forms import BoxForm
from forms import ContentForm
from forms import ForumForm
from forms import GroupForm
from forms import HomeForm
from forms import LessonForm
from forms import ParentForm
from forms import UserForm
from pysocial.settings import BASE_DIR

logger = logging.getLogger(__name__)


@login_required
@has_perm_view()
def add_home(request):
    kwargs = {}

    if request.method == 'POST':
        kwargs['form'] = HomeForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data

            result = cursor.home.insert(data)

            if result:
                return HttpResponseRedirect('/manager/home_list')

    else:

        kwargs['form'] = HomeForm()

    return render(request, 'manager/home.html', kwargs)


@login_required
@has_perm_view()
def edit_home(request, _id):
    kwargs = {}
    criteria = {'_id': ObjectId(_id)}
    home = cursor.home.find_one(criteria)

    if not home:
        kwargs['not_exists'] = True
        return render(request, 'manager/home.html', kwargs)

    if request.method == 'POST':
        kwargs['form'] = HomeForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data

            update = cursor.home.update_one(
                {'_id': home['_id']},
                {'$set': data}
            )

            if update.raw_result.get('updatedExisting', None):
                return HttpResponseRedirect('/manager/home_list')

    else:

        kwargs['form'] = HomeForm(home)

    return render(request, 'manager/home.html', kwargs)


@login_required
@has_perm_view()
def home_list(request):
    kwargs = {}
    kwargs['data'] = list(cursor.home.find())

    return render(request, 'manager/home_list.html', kwargs)


@login_required
@has_perm_view()
def define_group(request):
    kwargs = {}
    all_views = get_all_view_names()

    if request.method == 'POST':
        kwargs['form'] = GroupForm(request.POST, views_name=all_views)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data

            result = cursor.acl_group.insert(data)

            if result:
                return HttpResponseRedirect('/manager/group_list')

            else:
                kwargs['error'] = {
                    'errors': {
                        'insert error': 'insert was not successful'
                    }
                }

        else:
            kwargs['error'] = {'errors': kwargs['form'].errors}

    else:
        kwargs['form'] = GroupForm(views_name=all_views)

    return render(request, 'manager/group.html', kwargs)


@login_required
@has_perm_view()
def group_list(request):
    kwargs = {}
    kwargs['data'] = list(cursor.acl_group.find())

    return render(request, 'manager/group_list.html', kwargs)


@login_required
@has_perm_view()
def edit_group(request, _id):
    kwargs = {}

    criteria = {'_id': ObjectId(_id)}
    group = cursor.acl_group.find_one(criteria)

    if not group:
        kwargs['not_exists'] = True
        return render(request, 'manager/group.html', kwargs)

    all_views = get_all_view_names()

    if request.POST:
        kwargs['form'] = GroupForm(request.POST, views_name=all_views)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            update = cursor.acl_group.find_one_and_replace(criteria, data)

            if update:
                criteria = {'groups_name': {'$in': [group['group_name']]}}
                _update = {'$set': {'groups_name.$': data['group_name']}}
                users_update = cursor.users.update_many(criteria, _update)

                msg = 'All users group name modified. result: '
                msg += '{0}'.format(users_update.raw_result)
                logger.debug(msg)

                return HttpResponseRedirect('/manager/group_list')

        else:
            kwargs['error'] = {'errors': kwargs['form'].errors}

    else:
        kwargs['form'] = GroupForm(group, views_name=all_views)

    return render(request, 'manager/group.html', kwargs)


@login_required
@csrf_exempt
@require_POST
@has_perm_view()
def delete_group(request, _id):
    remove = cursor.acl_group.delete_one({'_id': ObjectId(_id)})
    return JsonResponse(remove, safe=False)


@login_required
@csrf_exempt
@require_POST
@has_perm_view()
def delete_user(request, username):
    kwargs = {}
    user = get_object_or_404(User, username=username)
    kwargs['django_remove'] = user.delete()
    mongodb_remove = cursor.users.delete_one({'username': username})
    kwargs['mongodb_remove'] = mongodb_remove.raw_result

    return JsonResponse(kwargs, safe=False)


@login_required
@has_perm_view()
def user_list(request):
    kwargs = {}
    projection = {
        'username': 1,
        'groups_name': 1,
        'first_name': 1,
        'last_name': 1
    }
    kwargs['users'] = list(cursor.users.find({}, projection))

    return render(request, 'manager/user_list.html', kwargs)


@login_required
@has_perm_view()
def edit_user(request, _id):
    kwargs = {}
    criteria = {'_id': ObjectId(_id)}
    user = cursor.users.find_one(criteria)

    if not user:
        kwargs['not_exists'] = True
        return render(request, 'manager/edit_username.html', kwargs)

    django_user = get_object_or_404(User, username=user['username'])

    if request.method == 'POST':
        kwargs['form'] = UserForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            password1 = data['password1']
            password2 = data['password2']

            if password1 and password2 and password1 != password2:
                msg = "Passwords don't match"
                kwargs['errors'] = {'Password mismatch!': msg}
                kwargs['form'] = UserForm()
                return render(request, 'acl/add_user.html', kwargs)

            else:
                if 'password1' in data and not data['password1']:
                    del data['password1']
                if 'password2' in data and not data['password2']:
                    del data['password2']

            if 'password1' in data:
                real_password = data['password1']
                django_user.set_password(real_password)

            else:
                real_password = None

            django_user.username = data['username']
            django_user.last_name = data['last_name']
            django_user.first_name = data['first_name']
            django_user.email = data['email']
            django_user.save()

            if real_password:
                data['password'] = django_user.password
                del data['password1']
                del data['password2']

            update = cursor.users.update_one(criteria, {'$set': data})

            if update.raw_result.get('updatedExisting', None):
                return HttpResponseRedirect('/manager/user_list')

    else:
        kwargs['form'] = UserForm(user)

    return render(request, 'manager/edit_username.html', kwargs)


@login_required
@has_perm_view()
def add_box(request):
    kwargs = {}

    if request.method == 'POST':
        kwargs['form'] = BoxForm(request.POST, request.FILES)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            box_pic = data.pop('box_pic')

            result = cursor.box.insert(data)

            if result:
                if box_pic:
                    path = BASE_DIR
                    _format = os.path.splitext(request.FILES['box_pic'].name)
                    path += '/media/dashboard/box/{0}'.format(str(result))
                    path += '{0}'.format(_format[1])

                    handle_uploaded_file(path, request.FILES['box_pic'])

                return HttpResponseRedirect('/manager/box_list')

    else:
        kwargs['form'] = BoxForm()

    return render(request, 'manager/box.html', kwargs)


@login_required
@has_perm_view()
def box_list(request):
    kwargs = {}
    projection = {'pk': 0, 'cssfile_lessons': 0, 'cssfile': 0}
    kwargs['boxs'] = list(cursor.box.find({}, projection))

    return render(request, 'manager/box_list.html', kwargs)


@login_required
@csrf_exempt
@require_POST
@has_perm_view()
def delete_box(request, _id):
    kwargs = {}

    mongodb_remove = cursor.box.delete_one({'_id': ObjectId(_id)})
    kwargs['mongodb_remove'] = mongodb_remove.raw_result

    path = BASE_DIR
    path += '/media/dashboard/box/'
    path_file = find_pic_by_id(_id, path)

    if os.path.exists(path_file):
        os.remove(path_file)

    return JsonResponse(kwargs, safe=False)


@login_required
@has_perm_view()
def edit_box(request, _id):
    kwargs = {}

    kwargs['id'] = _id
    criteria = {'_id': ObjectId(_id)}
    box = cursor.box.find_one(criteria)

    if not box:
        kwargs['not_exists'] = True
        return render(request, 'manager/box.html', kwargs)

    if request.method == 'POST':
        kwargs['form'] = BoxForm(request.POST, request.FILES)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            box_pic = data.pop('box_pic')

            update = cursor.box.update_one(criteria, {'$set': data})

            if update.raw_result.get('updatedExisting', None):
                if box_pic:
                    path = BASE_DIR
                    _format = os.path.splitext(request.FILES['box_pic'].name)
                    path += '/media/dashboard/box/{0}'.format(_id)
                    path += '{0}'.format(_format[1])

                    handle_uploaded_file(path, request.FILES['box_pic'])

                return HttpResponseRedirect('/manager/box_list')

    else:
        kwargs['form'] = BoxForm(box)

    return render(request, 'manager/box.html', kwargs)


@login_required
@has_perm_view()
def add_content(request):
    kwargs = {}

    if request.method == 'POST':
        kwargs['form'] = ContentForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            result = cursor.contents.insert(data)

            if result:
                return HttpResponseRedirect('/manager/content_list')

    else:
        kwargs['form'] = ContentForm()

    return render(request, 'manager/content.html', kwargs)


@login_required
@has_perm_view()
def edit_content(request, _id):
    kwargs = {}

    criteria = {'_id': ObjectId(_id)}
    content = cursor.contents.find_one(criteria)

    if request.method == 'POST':
        kwargs['form'] = ContentForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            _update = {'$set': data}
            update = cursor.contents.update_one(criteria, _update)

            if update.raw_result.get('updatedExisting', None):
                return HttpResponseRedirect('/manager/content_list')

    else:
        kwargs['form'] = ContentForm(content)

    return render(request, 'manager/content.html', kwargs)


@login_required
@has_perm_view()
def content_list(request):
    kwargs = {}
    kwargs['contents'] = list(cursor.contents.find())

    return render(request, 'manager/content_list.html', kwargs)


@login_required
@has_perm_view()
def add_parent(request):
    kwargs = {}

    if request.method == 'POST':
        kwargs['form'] = ParentForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            data['settings_type'] = 'Parents'
            result = cursor.settings.insert(data)

            if result:
                return HttpResponseRedirect('/manager/parent_list')

    else:
        kwargs['form'] = ParentForm()

    return render(request, 'manager/parent.html', kwargs)


@login_required
@has_perm_view()
def edit_parent(request, _id):
    kwargs = {}

    criteria = {'_id': ObjectId(_id)}
    parent = cursor.settings.find_one(criteria)

    if not parent:
        kwargs['not_exists'] = True
        return render(request, 'manager/parent.html', kwargs)

    if request.method == 'POST':
        kwargs['form'] = ParentForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            data['settings_type'] = 'Parents'
            _update = {'$set': data}
            update = cursor.settings.update_one(criteria, _update)

            if update.raw_result.get('updatedExisting', None):
                return HttpResponseRedirect('/manager/parent_list')

    else:
        kwargs['form'] = ParentForm(parent)

    return render(request, 'manager/parent.html', kwargs)


@login_required
@has_perm_view()
def parent_list(request):
    kwargs = {}
    kwargs['parents'] = list(
        cursor.settings.find({'settings_type': 'Parents'})
    )

    return render(request, 'manager/parent_list.html', kwargs)


@login_required
@has_perm_view()
def home_manager(request):
    return render(request, 'manager/home_manager.html')


@login_required
@has_perm_view()
def add_forum(request):
    kwargs = {}
    if request.method == 'POST':
        kwargs['form'] = ForumForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            forum_pic = request.FILES.get('forum_pic', None)
            result = cursor.forum.insert(data)

            if result:
                if forum_pic:
                    path = BASE_DIR
                    _format = os.path.splitext(request.FILES['forum_pic'].name)
                    path += '/media/forum/{0}'.format(str(result))
                    path += '{0}'.format(_format[1])

                    handle_uploaded_file(path, request.FILES['forum_pic'])
                return HttpResponseRedirect('/manager/forum_list')

    else:
        kwargs['form'] = ForumForm()

    return render(request, 'manager/forum.html', kwargs)


@login_required
@has_perm_view()
def forum_list(request):
    kwargs = {}
    kwargs['forums'] = list(cursor.forum.find().sort('sort', ASCENDING))
    return render(request, 'manager/forum_list.html', kwargs)


@login_required
@has_perm_view()
def edit_forum(request, _id):
    kwargs = {}
    criteria = {'_id': ObjectId(_id)}
    forum = cursor.forum.find_one(criteria)

    if not forum:
        kwargs['not_exists'] = True
        return render(request, 'manager/forum.html', kwargs)

    if request.method == 'POST':
        kwargs['form'] = ForumForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            forum_pic = request.FILES.get('forum_pic', None)
            update = cursor.forum.update_one(criteria, {'$set': data})

            if update.raw_result.get('updatedExisting', None):
                if forum_pic:
                    path = BASE_DIR
                    _format = os.path.splitext(request.FILES['forum_pic'].name)
                    path += '/media/forum/{0}'.format(_id)
                    path += '{0}'.format(_format[1])
                    handle_uploaded_file(path, request.FILES['forum_pic'])

                return HttpResponseRedirect('/manager/forum_list')

    else:
        kwargs['form'] = ForumForm(forum)

    return render(request, 'manager/forum.html', kwargs)


@login_required
@has_perm_view()
def add_lesson(request):
    kwargs = {}
    user_id = cursor.users.find_one({'username': request.user.username})
    if request.method == 'POST':
        kwargs['form'] = LessonForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            data['content_id'] = ObjectId(data['content_id'])
            data['box_id'] = ObjectId(data['box_id'])
            data['user_id'] = user_id['_id']
            data['created'] = datetime.datetime.now()
            result = cursor.lessons.insert(data)

            if result:
                return HttpResponseRedirect('/manager/lesson_list')

    else:
        kwargs['form'] = LessonForm()

    return render(request, 'manager/lesson.html', kwargs)


@login_required
@has_perm_view()
def lesson_list(request):
    kwargs = {}
    users = {}
    user = cursor.users.find({}, {'username': 1})
    for doc in user:
        users[doc['_id']] = doc['username']

    boxs = {}
    box = cursor.box.find({}, {'title': 1})
    for doc in box:
        boxs[doc['_id']] = doc['title']

    contents = {}
    content = cursor.contents.find({}, {'title': 1})
    for doc in content:
        contents[doc['_id']] = doc['title']

    kwargs['lessons'] = list(cursor.lessons.find().sort('created', DESCENDING))
    for doc in kwargs['lessons']:
        doc['user_id'] = users[doc['user_id']]
        doc['content_id'] = contents[doc['content_id']]
        doc['box_id'] = boxs[doc['box_id']]
        doc['created'] = gregorian_to_jalali(doc['created'])[:10]

    return render(request, 'manager/lesson_list.html', kwargs)


@login_required
@has_perm_view()
def edit_lesson(request, _id):
    kwargs = {}

    criteria = {'_id': ObjectId(_id)}
    lesson = cursor.lessons.find_one(criteria)

    if not lesson:
        kwargs['not_exists'] = True
        return render(request, 'manager/lesson.html', kwargs)

    user_id = cursor.users.find_one({'username': request.user.username})
    if request.method == 'POST':
        kwargs['form'] = LessonForm(request.POST)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            data['content_id'] = ObjectId(data['content_id'])
            data['box_id'] = ObjectId(data['box_id'])
            data['user_id'] = user_id['_id']
            data['modified'] = datetime.datetime.now()
            update = cursor.lessons.update_one(criteria, {'$set': data})

            if update.raw_result.get('updatedExisting', None):
                return HttpResponseRedirect('/manager/lesson_list')

    else:
        kwargs['form'] = LessonForm(lesson)

    return render(request, 'manager/lesson.html', kwargs)


@login_required
@csrf_exempt
@require_POST
@has_perm_view()
def delete_lesson(request, _id):
    kwargs = {}

    mongodb_remove = cursor.lessons.delete_one({'_id': ObjectId(_id)})
    kwargs['mongodb_remove'] = mongodb_remove.raw_result

    return JsonResponse(kwargs, safe=False)


@login_required
@csrf_exempt
@require_POST
@has_perm_view()
def delete_parent(request, _id):
    kwargs = {}
    mongodb_remove = cursor.settings.delete_one({'_id': ObjectId(_id)})
    kwargs['mongodb_remove'] = mongodb_remove.raw_result

    return JsonResponse(kwargs, safe=False)
