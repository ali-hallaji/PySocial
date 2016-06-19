# Django import
from django.conf.urls import url

# PySocial import
from views import show_forum


urlpatterns = [
    url(r'^show_forum/$', show_forum, name='show_forum'),
]