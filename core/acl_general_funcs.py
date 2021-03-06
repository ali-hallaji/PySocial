# Python Import
from functools import wraps

# Django Import
from django.core.urlresolvers import RegexURLPattern
from django.core.urlresolvers import RegexURLResolver
from django.shortcuts import render

# PySocial Import
from pysocial import settings
from users.func_tools import super_user
from core import cursor


def has_perm_view(in_view=None):

    def real_func(method):

        @wraps(method)
        def permission(*args, **kwargs):

            param = {}
            views_list = []
            username = args[0].user.username

            if username not in super_user:

                criteria = {
                    'username': username
                }
                projection = {
                    'groups_name': 1
                }
                groups_name = cursor.users.find_one(criteria, projection)

                for group in groups_name['groups_name']:
                    criteria = {'group_name': group}
                    projection = {'views': 1}
                    views = cursor.acl_group.find_one(criteria)['views']
                    views_list.extend(views)

                if method.func_name in views_list:

                    return method(*args, **kwargs)
                    # if in_view:
                    #     return True
                    # else:
                    #     return method(*args, **kwargs)

                else:
                    # if in_view:
                    #     return False
                    msg = "Forbidden: You don't have permission to access for"
                    msg += " {0}".format(method.func_name)
                    param['msg'] = msg

                    return render(
                        args[0],
                        'users/not_permit_views.html',
                        param
                    )

            else:
                return method(*args, **kwargs)

        return permission

    return real_func


def get_all_view_names(urlpatterns=None):
    """
        Getting list of all the views in a Django application:
        To get the list of all the views present in a Django application,
        we will use the get_all_view_names() function defined above.

        We will first import all the urlpatterns of the application and
        pass this list to the get_all_view_names() function.


        Example for each app:
        1- import urlpatterns of the app:
            from my_app.urls import urlpatterns as my_app_urlpatterns

        2- call the function with app's urlpatterns as the argument:
            my_app_views = get_all_view_names(my_app_urlpatterns)
    """

    ignore_list = [
        'app_index',
        'add_view',
        'check',
        'index',
        'shortcut',
        'render_panel',
        'password_reset_confirm',
        'public',
        'user_change_password',
        'history_view',
        'permission',
        'serve',
        'password_reset_complete',
        'password_reset_done',
        'logout',
        'sql_profile',
        'delete_view',
        'template_source',
        'change_view',
        'password_reset',
        'counter',
        'i18n_javascript',
        'changelist_view',
        'sql_select',
        'password_change_done',
        'login',
        'view',
        'sql_explain',
        'ImageUploadView',
        'RedirectView',
        'browse',
        'captcha_audio',
        'captcha_image',
        'captcha_refresh',
        'password_change'
    ]

    add_to_list = []

    if not urlpatterns:
        global views_name
        # maintain a global list
        views_name = []
        # import root_urlconf module
        root_urlconf = __import__(settings.ROOT_URLCONF)
        # project's urlpatterns
        urlpatterns = root_urlconf.urls.urlpatterns

    for pattern in urlpatterns:
        if isinstance(pattern, RegexURLResolver):
            # call this function recursively
            get_all_view_names(pattern.url_patterns)

        elif isinstance(pattern, RegexURLPattern):
            # get the view name
            view_name = pattern.callback.func_name
            # add the view to the global list
            views_name.append(view_name)

    final_views = list(set(views_name))

    for item in ignore_list:
        try:
            final_views.remove(item)

        except ValueError:
            pass

    for item in add_to_list:
        final_views.append(item)

    return sorted(final_views)
