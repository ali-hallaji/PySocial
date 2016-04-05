# Django import
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# PySocial import
from core import cursor
from forms import HomeForm


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
