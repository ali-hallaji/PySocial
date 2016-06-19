# Python Import
import os
import re

from pymongo import ASCENDING
from pymongo import DESCENDING

# Django Import
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# PySocial Import
from core import cursor
from core.func_tools import handle_uploaded_file
from pysocial.settings import BASE_DIR


def show_forum(request):
    return render(request, 'forum/show_forum.html')