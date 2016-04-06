# -*- coding: utf-8 -*-
# Python import
from pymongo.errors import DuplicateKeyError

# Django Import
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import RegisterUsersForm

# PySocial Import
from core import cursor
from core.mail_functions import welcome_mail
from pysocial import settings


def login(request):
    referer = request.META.get('HTTP_REFERER', '').rstrip('/')

    if 'next' in request.GET:
        redirect_url = request.GET['next']

    elif referer and not referer.endswith(settings.LOGIN_URL):
        redirect_url = referer

    else:
        redirect_url = '/'

    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect_url)

    elif request.method == 'GET':
        return render(
            request,
            'users/login.html',
            {'redirect_url': redirect_url}
        )

    elif request.method == 'POST':
        user = auth.authenticate(
            username=request.POST.get('username', '').lower(),
            password=request.POST.get('password', '')
        )

        if user:
            ignore_url = ['logout', 'login']

            for item in ignore_url:
                if item in redirect_url:
                    redirect_url = '/'

            auth.login(request, user)

            return HttpResponseRedirect(
                request.POST.get('redirect_url', redirect_url)
            )

        else:
            return render(request, 'users/login.html', {
                'msg': 'نام کاربری یا گذرواژه را اشتباه وارد کرده اید!'
            })


def registration(request):
    kwargs = {}

    if 'next' in request.GET:
        redirect_url = request.GET['next']
    else:
        redirect_url = '/'

    if request.method == 'POST':
        kwargs['form'] = RegisterUsersForm(request.POST)

        if kwargs['form'].is_valid():  # All validation rules pass
            data = kwargs['form'].cleaned_data
            data['username'] = data['username'].lower()

            doc = {}
            doc['username'] = data['username']
            doc['groups_name'] = [
                'Member',
            ]

            try:
                result = cursor.users.insert(doc)

            except DuplicateKeyError:
                kwargs['duplicate_username'] = True
                return render(request, 'users/register.html', kwargs)

            if result:

                user = User.objects.create_user(
                    username=data['username'],
                    password=data['password1'],
                    email=data['email'],
                )
                user.save()

                criteria = {'username': data['username']}

                user_data = user.__dict__
                del user_data['_state']
                user_data['real_password'] = data['password1']

                update_data = {'$set': user_data}

                update = cursor.users.update_one(criteria, update_data)

                if update.raw_result.get('updatedExisting', None):

                    try:
                        welcome_mail([data['email'], ])
                    except:
                        pass

                    user = auth.authenticate(
                        username=data['username'],
                        password=data['password1'],
                        email=data['email']
                    )
                    auth.login(request, user)

                    return HttpResponseRedirect(
                        request.POST.get('redirect_url', redirect_url)
                    )

    else:
        kwargs['form'] = RegisterUsersForm()

    return render(request, 'users/register.html', kwargs)


@login_required
def logout(request):

    try:
        url = request.get_full_path().split('next=')[1]

    except:
        url = request.get_full_path()

    auth.logout(request)

    return HttpResponseRedirect(url)
