# Django import
from django.conf.urls import url

# PySocial import
from views import add_box
from views import add_home
from views import box_list
from views import define_group
from views import delete_box
from views import delete_group
from views import delete_user
from views import edit_box
from views import edit_group
from views import edit_home
from views import edit_user
from views import group_list
from views import home_list
from views import user_list


urlpatterns = [
    url(r'^user_list/$', user_list, name="user_list"),
    url(r'^home_list/$', home_list, name="home_list"),
    url(r'^define_group/$', define_group, name="define_group"),
    url(r'^group_list/$', group_list, name="group_list"),
    url(r'^add_box/$', add_box, name="add_box"),
    url(r'^add_home/$', add_home, name="add_home"),
    url(r'^box_list/$', box_list, name="box_list"),
    url(r'^edit_group/(?P<_id>[\w\d]+)/$', edit_group, name="edit_group"),
    url(r'^edit_box/(?P<_id>[\w\d]+)/$', edit_box, name="edit_box"),
    url(r'^edit_home/(?P<_id>[\w\d]+)/$', edit_home, name="edit_home"),
    url(
        r'^edit_user/(?P<_id>[\w\d]+)/$',
        edit_user,
        name="edit_user"
    ),
    url(
        r'^delete_group/(?P<_id>[\w\d]+)/$',
        delete_group,
        name="delete_group"
    ),
    url(
        r'^delete_box/(?P<_id>[\w\d]+)/$',
        delete_box,
        name="delete_box"
    ),
    url(
        r'^delete_user/(?P<username>[a-zA-Z\s]*)/$',
        delete_user,
        name="delete_user"
    ),
]
