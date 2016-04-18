# Python Import
import logging
import os

from bson.objectid import ObjectId

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
from core.acl_general_funcs import has_perm_view
from core.func_tools import find_pic_by_id
from core.func_tools import handle_uploaded_file
from forms import BoxForm
from forms import GroupForm
from forms import HomeForm
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

    return render(request, 'manager/edit_home.html', kwargs)


@login_required
@has_perm_view()
def edit_home(request, _id):
    kwargs = {}
    criteria = {'_id': ObjectId(_id)}
    home = cursor.home.find_one(criteria)

    if not home:
        kwargs['not_exists'] = True
        return render(request, 'manager/edit_home.html', kwargs)

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

    return render(request, 'manager/edit_home.html', kwargs)


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

    return render(request, 'manager/define_group.html', kwargs)


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
        return render(request, 'manager/define_group.html', kwargs)

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

    return render(request, 'manager/define_group.html', kwargs)


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

    return render(request, 'manager/add_box.html', kwargs)


@login_required
@has_perm_view()
def box_list(request):
    kwargs = {}

    kwargs['boxs'] = list(cursor.box.find())

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
        return render(request, 'manager/add_box.html', kwargs)

    if request.method == 'POST':
        kwargs['form'] = BoxForm(request.POST, request.FILES)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            box_pic = data.pop('box_pic')

            result = cursor.box.update_one(criteria, {'$set': data})

            if result.raw_result.get('updatedExisting', None):
                if box_pic:
                    path = BASE_DIR
                    _format = os.path.splitext(request.FILES['box_pic'].name)
                    path += '/media/dashboard/box/{0}'.format(_id)
                    path += '{0}'.format(_format[1])
                    print path

                    handle_uploaded_file(path, request.FILES['box_pic'])

                return HttpResponseRedirect('/manager/box_list')

    else:
        kwargs['form'] = BoxForm(box)

    return render(request, 'manager/add_box.html', kwargs)
