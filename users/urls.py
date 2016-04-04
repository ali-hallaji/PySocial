# Django import
from django.conf.urls import url

# PySocial import
from views import login
from views import logout
from views import registration


urlpatterns = [
    url(r'^register/$', registration, name="register"),
    url(r'^login', login, name='login'),
    url(r'^logout', logout, name='logout'),
]
