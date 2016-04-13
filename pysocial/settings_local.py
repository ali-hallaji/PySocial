from settings import BASE_DIR

# Authetication url
LOGIN_URL = '/users/login'
# LOGIN_REDIRECT_URL = '/'  # Disable For staying and redirect to last page


# Captcha options
CAPTCHA_FONT_SIZE = 40
CAPTCHA_FOREGROUND_COLOR = '#666'
CAPTCHA_BACKGROUND_COLOR = '#ffffff'


# Ckeditor Configuration
CKEDITOR_JQUERY_URL = BASE_DIR + '/static/main/js/jquery-2.2.2.min.js'
CKEDITOR_UPLOAD_PATH = BASE_DIR + "/media/ckeditor/uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 350,
        'width': 800,
    },
}


# Customize Authentication
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email'
        ],
        'AUTH_PARAMS': {
            'access_type': 'online'
        }
    },
    'linkedin': {
        'SCOPE': ['r_emailaddress'],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            'picture-url',
            'public-profile-url'
        ]
    },
    'facebook': {
            'METHOD': 'oauth2',
            'SCOPE': ['email', 'public_profile', 'user_friends'],
            # 'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'FIELDS': [
                'id',
                'email',
                'name',
                'first_name',
                'last_name',
                'verified',
                'locale',
                'timezone',
                'link',
                'picture',
                'gender',
                'updated_time'
            ],
            'EXCHANGE_TOKEN': True,
            'VERIFIED_EMAIL': True,
            'VERSION': 'v2.4'
    }
}

ACCOUNT_ADAPTER = 'users.social_adapter.SocialAdapter'
ACCOUNT_USERNAME_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_UNIQUE_EMAIL = True

