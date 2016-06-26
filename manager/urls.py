# Django import
from django.conf.urls import url

# PySocial import
from views import add_box
from views import add_content
from views import add_forum
from views import add_home
from views import add_lesson
from views import add_parent
from views import box_list
from views import content_list
from views import define_group
from views import delete_box
from views import delete_group
from views import delete_lesson
from views import delete_parent
from views import delete_user
from views import edit_box
from views import edit_content
from views import edit_forum
from views import edit_group
from views import edit_home
from views import edit_lesson
from views import edit_parent
from views import edit_user
from views import forum_list
from views import group_list
from views import home_list
from views import home_manager
from views import lesson_list
from views import parent_list
from views import user_list


urlpatterns = [
    url(r'^home/$', home_manager, name="home_manager"),
    url(r'^user_list/$', user_list, name="user_list"),
    url(r'^forum_list/$', forum_list, name='forum_list'),
    url(r'^home_list/$', home_list, name="home_list"),
    url(r'^box_list/$', box_list, name="box_list"),
    url(r'^parent_list/$', parent_list, name="parent_list"),
    url(r'^lesson_list/$', lesson_list, name="lesson_list"),
    url(r'^group_list/$', group_list, name="group_list"),
    url(r'^content_list/$', content_list, name="content_list"),
    url(r'^add_box/$', add_box, name="add_box"),
    url(r'^add_group/$', define_group, name="add_group"),
    url(r'^add_forum/$', add_forum, name='add_forum'),
    url(r'^add_content/$', add_content, name="add_content"),
    url(r'^add_home/$', add_home, name="add_home"),
    url(r'^add_parent/$', add_parent, name="add_parent"),
    url(r'^add_lesson/$', add_lesson, name="add_lesson"),
    url(r'^edit_group/(?P<_id>[\w\d]+)/$', edit_group, name="edit_group"),
    url(r'^edit_box/(?P<_id>[\w\d]+)/$', edit_box, name="edit_box"),
    url(r'^edit_home/(?P<_id>[\w\d]+)/$', edit_home, name="edit_home"),
    url(
        r'^edit_content/(?P<_id>[\w\d]+)/$',
        edit_content,
        name="edit_content"
    ),
    url(
        r'^edit_user/(?P<_id>[\w\d]+)/$',
        edit_user,
        name="edit_user"
    ),
    url(
        r'^edit_forum/(?P<_id>[\w\d]+)/$',
        edit_forum,
        name="edit_forum"
    ),
    url(
        r'^edit_lesson/(?P<_id>[\w\d]+)/$',
        edit_lesson,
        name="edit_lesson"
    ),
    url(
        r'^edit_parent/(?P<_id>[\w\d]+)/$',
        edit_parent,
        name="edit_parent"
    ),
    url(
        r'^delete_group/(?P<_id>[\w\d]+)/$',
        delete_group,
        name="delete_group"
    ),
    url(
        r'^delete_parent/(?P<_id>[\w\d]+)/$',
        delete_parent,
        name="delete_parent"
    ),
    url(
        r'^delete_lesson/(?P<_id>[\w\d]+)/$',
        delete_lesson,
        name="delete_lesson"
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
