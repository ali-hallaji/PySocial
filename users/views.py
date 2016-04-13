# -*- coding: utf-8 -*-
# Python import
import logging

from pymongo.errors import DuplicateKeyError

# Django Import
from allauth.account.signals import user_logged_in
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms import RegisterUsersForm

# PySocial Import
from core import cursor
from core.mail_functions import welcome_mail
from pysocial import settings

logger = logging.getLogger(__name__)


def login(request):
    referer = request.META.get('HTTP_REFERER', '').rstrip('/')

    if 'next' in request.GET:

        if 'logout' in request.GET['next']:
            redirect_url = '/'
        else:
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

        if 'logout' in request.GET['next']:
            redirect_url = '/'
        else:
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

                try:
                    user = User.objects.create_user(
                        username=data['username'],
                        password=data['password1'],
                        email=data['email'],
                    )
                    user.save()

                except IntegrityError:
                    cursor.users.remove({'username': data['username']})
                    kwargs['duplicate_username'] = True

                    return render(request, 'users/register.html', kwargs)

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

    if 'logout' in url:
        url = '/'

    auth.logout(request)

    return HttpResponseRedirect(url)


@receiver(user_logged_in)
def social_auth_handler(request, user, sociallogin=None, **kwargs):
    '''
    When a social account is created or login successfully and this
    signal is received, django-allauth passes in the sociallogin param,
    giving access to metadata on the remote account, e.g.:

    sociallogin.account.provider  # e.g. 'twitter'
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']

    See the socialaccount_socialaccount table for more
    in the 'extra_data' field.
    '''

    doc = user.__dict__

    try:
        del doc['_state']
        del doc['_emailaddress_cache']
    except:
        pass

    sl = sociallogin

    doc['last_login'] = doc['last_login'].replace(tzinfo=None)
    doc['date_joined'] = doc['date_joined'].replace(tzinfo=None)
    doc['social_name'] = sl.account.provider
    doc['social_auth'] = True
    doc['groups_name'] = [
        'Member',
    ]

    if sl:
        # Extract first / last names from social nets and store on User record
        if sl.account.provider == 'twitter':
            name = sl.account.extra_data['name']
            doc['first_name'] = name.split()[0]
            doc['last_name'] = name.split()[1]
            doc['picture'] = sl.account.extra_data['profile_image_url']

        if sl.account.provider == 'facebook':
            doc['first_name'] = sl.account.extra_data['first_name']
            doc['last_name'] = sl.account.extra_data['last_name']
            doc['email'] = sl.account.extra_data['email']

        if sl.account.provider == 'google':
            doc['first_name'] = sl.account.extra_data['given_name']
            doc['last_name'] = sl.account.extra_data['family_name']
            doc['email'] = sl.account.extra_data['email']
            doc['picture'] = sl.account.extra_data['picture']
            doc['social_url'] = sl.account.extra_data['link']

        if sl.account.provider == 'linkedin':
            doc['first_name'] = sl.account.extra_data['first-name']
            doc['last_name'] = sl.account.extra_data['last-name']
            doc['email'] = sl.account.extra_data['email-address']
            doc['social_url'] = sl.account.extra_data['public-profile-url']
            doc['picture'] = sl.account.extra_data['picture-url']

        if sl.account.provider == 'github':
            name = sl.account.extra_data['name']
            doc['first_name'] = name.split()[0]
            doc['last_name'] = name.split()[1]
            doc['email'] = sl.account.extra_data['email']
            doc['social_url'] = sl.account.extra_data['url']
            doc['picture'] = sl.account.extra_data['avatar_url']

    if user.is_authenticated():
        criteria = {'username': doc['username']}
        update_data = {'$set': doc}
        update = cursor.users.update_one(
            criteria,
            update_data,
            upsert=True
        )

        if update.raw_result.get('updatedExisting', None):
            logger.debug("User: {0}, Data: {1}".format(doc['username'], doc))
        else:
            msg = "User authenticate faild! "
            msg += "User: {0}, Data: {1}".format(doc['username'], doc)
            logger.warning(msg)

