# Django import
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

# PySocial import
import settings

from views import home
from views import search
# from views import under_construction


urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls')),
    url(r'^forum/', include('forum.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^robots\.txt', include('robots.urls')),
    url(r'^search/$', search, name='search'),
    url(r'', include('webmaster_verification.urls')),
    url(r'^$', home, name="home"),
    # url(
    #     r'^$',
    #     under_construction,
    #     name="under_construction"
    # )
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)