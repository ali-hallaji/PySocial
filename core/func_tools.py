# Python Import
import os

# Django Import

# PySocial Import
from pysocial.settings import BASE_DIR


def handle_uploaded_file(path, _file):
    path_without_file = '/'.join(path.split('/')[:-1])

    if not os.path.exists(path_without_file):
        os.makedirs(path_without_file)

    with open(path, 'wb+') as destination:
        for chunk in _file.chunks():
            destination.write(chunk)


def find_pic_by_id(name, path):
    try:
        list_pic = os.listdir(path)

        for pic in list_pic:
            if name in pic:
                return pic

        else:
            return False

    except:
        return False


def path_pic_box(value):

    if isinstance(value, dict):
        _id = str(value['_id'])
    elif isinstance(value, str):
        _id = value
    elif isinstance(value, unicode):
        _id = value

    path = BASE_DIR + '/media/dashboard/box/'
    path_file = find_pic_by_id(_id, path)

    if path_file:
        path += path_file
        path = '/media' + path.split('media')[1]

    else:
        path = '/static/main/img/default.png'

    return path
