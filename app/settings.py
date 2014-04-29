"""
Django settings for lgt project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import app.conf as conf
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bfni$e*y89wryr-mknd@9876szj6^*607n-h9jl*6hv3#gzarn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'games',
    'frontend',
    'pipeline',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # ...
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    # ...
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__) , 'templates').replace('\\', '/')
)

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': conf.DATABASE_NAME,                      # Or path to database file if using sqlite3.
        'USER': conf.DATABASE_USER,                      # Not used with sqlite3.
        'PASSWORD': conf.DATABASE_PASSWORD,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static').replace('\\', '/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join( (os.path.dirname(__file__)), 'static').replace('\\','/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

LOGIN_REDIRECT_URL = '/games/'
# ================== PIPELINE =================

PIPELINE_COMPILERS = (
    'pipeline_browserify.compiler.BrowserifyCompiler',
)

#STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

PIPELINE_BROWSERIFY_ARGUMENTS = '-t reactify'

PIPELINE_JS = {
    'browserify': {
        'source_filenames' : (
            'js/app.browserify.js',
        ),
        'output_filename': 'js/browserified.js',
    },
}

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None