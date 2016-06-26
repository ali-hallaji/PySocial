# Django import
from django.conf.urls import url

# PySocial import
from views import show_forum
from views import show_post
from views import show_posts
from views import show_thread


urlpatterns = [
    url(r'^$', show_forum, name='show_forum'),
    url(r'^show_post/(?P<_id>[\w\d]+)/$', show_post, name='show_post'),
    url(r'^show_thread/(?P<_id>[\w\d]+)/$', show_thread, name='show_thread'),
    url(r'^show_posts/(?P<_id>[\w\d]+)/$', show_posts, name='show_posts'),
]
