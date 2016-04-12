# Python Import
import logging

# Django Import
from allauth.account.signals import user_logged_in
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def social_auth_handler(request, user, sociallogin=None, **kwargs):
    '''
    When a social account is created or login successfully and this
    signal is received, django-allauth passes in the sociallogin param,
    giving access to metadata on the remote account, e.g.:

    sociallogin.account.provider  # e.g. 'twitter'
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']

    See the socialaccount_socialaccount table for more
    in the 'extra_data' field.
    '''

    logger.info("#########################################")
    logger.info(sociallogin.account.extra_data)
    logger.info("#########################################")

    if sociallogin:
        # Extract first / last names from social nets and store on User record
        if sociallogin.account.provider == 'twitter':
            name = sociallogin.account.extra_data['name']
            first_name = name.split()[0]
            last_name = name.split()[1]
            email = sociallogin.account.extra_data['email']

        if sociallogin.account.provider == 'facebook':
            first_name = sociallogin.account.extra_data['first_name']
            last_name = sociallogin.account.extra_data['last_name']
            email = sociallogin.account.extra_data['email']

        if sociallogin.account.provider == 'google':
            first_name = sociallogin.account.extra_data['given_name']
            last_name = sociallogin.account.extra_data['family_name']
            email = sociallogin.account.extra_data['email']

