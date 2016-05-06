# Python Import
import os

# Django Import
from django import template

# PySocial Import
from core.func_tools import find_pic_by_id
from core.func_tools import path_pic_box
from core.date_utils import gregorian_to_jalali
from pysocial.settings import BASE_DIR


register = template.Library()


@register.filter("mongo_id")
def mongo_id(value, key=None):
    try:
        if not key:
            return str(value['_id'])

        else:
            return str(value[key])

    except:
        return value


@register.filter("box_exist_file")
def box_exist_file(value):
    path = BASE_DIR + '/media/dashboard/box/'
    file_name = find_pic_by_id(value, path)

    if file_name:
        path += file_name
        path = '/media' + path.split('media')[1]

    if os.path.exists(path):
        return 'True'
    else:
        return 'False'


@register.filter("get_path_pic_box")
def get_path_pic_box(value):

    return path_pic_box(value)


@register.filter("to_jalali")
def to_jalali(value):
    if value:
        return gregorian_to_jalali(value)
    else:
        return None
