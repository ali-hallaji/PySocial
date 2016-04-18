# Python Import

# Django Import

# PySocial Import
from core import cursor
from core.func_tools import avatar_maker


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

        user = avatar_maker(user)

    else:
        user = None

    return {'user_data': user}
