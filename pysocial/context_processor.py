# Python Import

# Django Import

# PySocial Import
from core import cursor
from core.func_tools import find_pic_by_id
from pysocial.settings import BASE_DIR


def get_user_data(request):

    if request.user.is_authenticated():
        criteria = {
            'username': request.user.username
        }
        projection = {
            'username': 1,
            'first_name': 1,
            'last_name': 1,
            'last_login': 1,
            'groups_name': 1,
            'email': 1,
            'date_joined': 1
        }
        user = cursor.users.find_one(criteria, projection)

        if not user.get('social_auth', None):
            path = BASE_DIR + '/media/avatars/'
            file_name = find_pic_by_id(str(user['_id']), path)

            if file_name:
                path += file_name
                path = '/media' + path.split('media')[1]
                user['picture'] = path

            else:
                user['picture'] = '/media/avatars/default.png'

        else:
            if not user.get('picture', None):
                user['picture'] = '/media/avatars/default.png'

    else:
        user = None

    return {'user_data': user}
