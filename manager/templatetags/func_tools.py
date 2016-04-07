# Python Import
import os

# Django Import
from django import template

# PySocial Import
from core.func_tools import find_pic_by_id
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


@register.filter("get_path_pic_box")
def get_path_pic_box(value):

    if isinstance(value, dict):
        _id = str(value['_id'])
    elif isinstance(value, str):
        _id = value
    elif isinstance(value, unicode):
        _id = value

    path = BASE_DIR + '/media/dashboard/box/'
    file_name = find_pic_by_id(_id, path)

    if file_name:
        path += file_name
        path = '/media' + path.split('media')[1]

    else:
        path = '/static/main/img/default.png'

    return path
