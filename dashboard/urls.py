# Django import
from django.conf.urls import url

# PySocial import
from views import content
from views import lesson


urlpatterns = [
    url(
        r'^content/(?P<dashboard>[a-zA-Z\s]*)/(?P<_id>[\w\d]+)/$',
        content,
        name="content"
    ),
    url(
        r'^lesson/(?P<dashboard>[\w\d]+)/(?P<_id>[\w\d]+)/$',
        lesson,
        name="lesson"
    ),
]
