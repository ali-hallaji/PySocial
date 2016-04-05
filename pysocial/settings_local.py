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
