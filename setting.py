import os

BASE_DIR=os.path.abspath(os.path.dirname(__file__))

STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

DATABASES = {
    'default': {
        'ENGINE': '/instance/flaskr.sqlite',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}