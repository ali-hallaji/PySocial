# project/users/adapter.py:
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class SocialAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        referer = request.META.get('HTTP_REFERER', '').rstrip('/')

        if 'next' in request.GET:
            redirect_url = request.GET['next']

        elif referer and not referer.endswith(settings.LOGIN_URL):
            redirect_url = referer

        else:
            redirect_url = '/'

        return redirect_url
