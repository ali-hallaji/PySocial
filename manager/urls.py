# Django import
from django.conf.urls import url

# PySocial import
from views import define_group
from views import delete_group
from views import delete_user
from views import edit_group
from views import edit_home
from views import edit_username
from views import group_list
from views import user_list


urlpatterns = [
    url(r'^user_list/$', user_list, name="user_list"),
    url(r'^edit_home/$', edit_home, name="edit_home"),
    url(r'^define_group/$', define_group, name="define_group"),
    url(r'^group_list/$', group_list, name="group_list"),
    url(r'^edit_group/(?P<_id>[\w\d]+)/$', edit_group, name="edit_group"),
    url(
        r'^edit_username/(?P<_id>[\w\d]+)/$',
        edit_username,
        name="edit_username"
    ),
    url(
        r'^delete_group/(?P<_id>[\w\d]+)/$',
        delete_group,
        name="delete_group"
    ),
    url(
        r'^delete_user/(?P<username>[\w\d]+)/$',
        delete_user,
        name="delete_user"
    ),
]
