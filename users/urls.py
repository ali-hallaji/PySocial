# Django import
from django.conf.urls import url

# PySocial import
from views import registration


urlpatterns = [
    url(r'^register/$', registration, name="register"),
]
