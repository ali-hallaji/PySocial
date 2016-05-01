# Python Import
import re
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


def avatar_maker(user):

    if user and not user.get('social_auth', None):
        path = BASE_DIR + '/media/avatars/'
        file_name = find_pic_by_id(str(user['_id']), path)

        if file_name:
            path += file_name
            path = '/media' + path.split('media')[1]
            user['picture'] = path

        else:
            user['picture'] = '/media/avatars/default.png'

    else:
        if user and not user.get('picture', None):
            user['picture'] = '/media/avatars/default.png'

    return user


def list_of_seq_unique_by_key(seq, key):
    # Remove everything with a duplicate value for key 'key'
    seen = set()
    seen_add = seen.add
    result = [x for x in seq if x[key] not in seen and not seen_add(x[key])]

    return result


def truncate_word(text, n):
    return ' '.join(cleanhtml(text).split()[:n])


def truncate_val_dict(_list, n):

    new_list = []

    for _dict in _list:

        for k, v in _dict.items():

            if isinstance(v, unicode) or isinstance(v, str):
                _dict[k] = truncate_word(v, n)

        new_list.append(_dict)

    return new_list


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
