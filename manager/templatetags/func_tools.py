# Python Import
import os

# Django Import
from django import template

# PySocial Import
from pysocial.settings import BASE_DIR


register = template.Library()


@register.filter("mongo_id")
def mongo_id(value):
    return str(value['_id'])


@register.filter("box_exist_file")
def box_exist_file(value):
    path = BASE_DIR
    path += '/media/dashboard/box/{0}.jpg'.format(value)

    if os.path.exists(path):
        return 'True'
    else:
        return 'False'
