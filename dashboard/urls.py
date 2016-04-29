# Django import
from django.conf.urls import url

# PySocial import
from views import content
from views import lesson
from views import no_publish


urlpatterns = [
    url(
        r'^content/(?P<dashboard>[a-zA-Z\s]*)/(?P<_id>[\w\d]+)/$',
        content,
        name="content"
    ),
    url(
        r'^lesson/(?P<dashboard>[a-zA-Z\s]*)/(?P<_id>[\w\d]+)/$',
        lesson,
        name="lesson"
    ),
    url(r'^lesson/no_publish/$', no_publish, name='no_publish'),
]
