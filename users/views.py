import datetime
from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponseRedirect

from pysocial import settings
from forms import RegisterUsersForm
from core import cursor


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
            auth.login(request, user)

            return HttpResponseRedirect(
                request.POST.get('redirect_url', redirect_url)
            )

        else:
            return render(request, 'users/login.html', {
                'msg': 'نام کاربری یا گذرواژه را اشتباه وارد کرده اید!'
            })


def user_register(request):
    if 'next' in request.GET:
        redirect_url = request.GET['next']
    else:
        redirect_url = '/'

    result = {}
    if request.method == 'POST':  # If the form has been submitted...
        form = RegisterUsersForm(request.POST)
        if form.is_valid():  # All validation rules pass
            data = form.cleaned_data
            doc = {}
            doc['username'] = data['username']
            doc["is_active"] = True
            doc["is_superuser"] = False
            doc["is_staff"] = False
            doc['email'] = data['email']
            doc['date_joined'] = datetime.datetime.now()

            result = cursor.users.insert(doc)

            if result:

                user = auth.authenticate(
                    username=data['username'],
                    password=data['password'],
                )
                auth.login(request, user)

                return HttpResponseRedirect(
                    request.POST.get('redirect_url', redirect_url)
                )
    else:
        result['form'] = RegisterUsersForm()

    return render(request, 'users/register.html', result)
