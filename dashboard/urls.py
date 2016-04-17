# Django import
from django.conf.urls import url

# PySocial import
from views import content


urlpatterns = [
    url(
        r'^content/(?P<dashboard>[\w\d]+)/(?P<_id>[\w\d]+)/$',
        content,
        name="content"
    ),
]
