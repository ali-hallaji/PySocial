# Python Import
import os


def handle_uploaded_file(path, _file):
    path_without_file = '/'.join(path.split('/')[:-1])

    if not os.path.exists(path_without_file):
        os.makedirs(path_without_file)

    with open(path, 'wb+') as destination:
        for chunk in _file.chunks():
            destination.write(chunk)


def find_pic_by_id(name, path):
    list_pic = os.listdir(path)

    for pic in list_pic:
        if name in pic:
            return pic

    else:
        return False
