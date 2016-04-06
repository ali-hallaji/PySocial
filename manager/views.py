# Python Import
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
from forms import GroupForm
from forms import HomeForm
from forms import UserForm


@login_required
def edit_home(request):
    kwargs = {}

    if request.method == 'POST':
        kwargs['form'] = HomeForm(request.POST)

    else:
        news = cursor.home.find_one({'_type': 'news'})
        body = cursor.home.find_one({'_type': 'body'})
        data = {}

        if news:
            data['news'] = news['news']
        else:
            data['news'] = None

        if body:
            data['body'] = body['body']
        else:
            data['body'] = None

        kwargs['form'] = HomeForm(data)

    return render(request, 'manager/edit_home.html', kwargs)


@login_required
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
def group_list(request):
    kwargs = {}
    kwargs['data'] = list(cursor.acl_group.find())

    return render(request, 'manager/group_list.html', kwargs)


@login_required
def edit_group(request, _id):
    kwargs = {}

    criteria = {'_id': ObjectId(_id)}
    group = cursor.acl_group.find_one(criteria)
    all_views = get_all_view_names()

    if request.POST:
        kwargs['form'] = GroupForm(request.POST, views_name=all_views)

        if kwargs['form'].is_valid():
            data = kwargs['form'].cleaned_data
            update = cursor.acl_group.find_one_and_replace(criteria, data)

            if update:
                criteria = {'groups_name': {'$in': [group['group_name']]}}
                _update = {'$set': {'groups_name.$': data['group_name']}}
                cursor.users.update_many(criteria, _update)
                return HttpResponseRedirect('/manager/group_list')

        else:
            kwargs['error'] = {'errors': kwargs['form'].errors}

    else:
        kwargs['form'] = GroupForm(group, views_name=all_views)

    return render(request, 'manager/define_group.html', kwargs)


@login_required
@csrf_exempt
@require_POST
def delete_group(request, _id):
    remove = cursor.acl_group.delete_one({'_id': ObjectId(_id)})
    return JsonResponse(remove, safe=False)


@login_required
@csrf_exempt
@require_POST
def delete_user(request, username):
    kwargs = {}
    user = get_object_or_404(User, username=username)
    kwargs['django_remove'] = user.delete()
    mongodb_remove = cursor.users.delete_one({'username': username})
    kwargs['mongodb_remove'] = mongodb_remove.raw_result

    return JsonResponse(kwargs, safe=False)


@login_required
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
def edit_username(request, _id):
    kwargs = {}
    user = cursor.users.find_one({'_id': ObjectId(_id)})

    groups_name = []
    for item in user['groups_name']:
        groups_name.append((item, item))

    user['groups_name'] = groups_name

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
                django_user.set_password(data['password1'])

            django_user.username = data['username']
            django_user.last_name = data['last_name']
            django_user.first_name = data['first_name']
            django_user.email = data['email']
            django_user.save()

            return HttpResponseRedirect('/manager/user_list')

    else:
        kwargs['form'] = UserForm(user)

    return render(request, 'manager/edit_username.html', kwargs)