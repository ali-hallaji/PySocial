# Django import
from django.conf.urls import url

# PySocial import
from views import edit_home


urlpatterns = [
    url(r'^edit_home/$', edit_home, name="edit_home"),
]
