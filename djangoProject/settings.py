"""
Django settings for djangoProject project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = ''
MEDIA_URL = ''

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7s=g$3k(n6=w8k8f=#z@yxn4l1t79z9h=93b(=z(m=6%1c=6qj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'ckeditor',
    'django_quill',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_static_jquery',
    'crispy_forms',
    'crispy_bootstrap5',
    'home',
    'base',
    'problemBase',
    'account',
    'notifications',
]

AUTH_USER_MODEL = 'base.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'base.context_processors.load_categories',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'EUhCPTNHtfMniM94HStU',
        'HOST': 'containers-us-west-8.railway.app',
        'PORT': '6869',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Crispy forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'static/base'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CKEditor UI and plugins configuration
CKEDITOR_CONFIGS = {
    'default': {
        # Toolbar configuration
        # name - Toolbar name
        # items - The buttons enabled in the toolbar
        'toolbar_DefaultToolbarConfig': [
            {
                'name': 'basicstyles',
                'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                          'Superscript', ],
            },
            {
                'name': 'clipboard',
                'items': ['Undo', 'Redo', ],
            },
            {
                'name': 'paragraph',
                'items': ['NumberedList', 'BulletedList', 'Outdent', 'Indent',
                          'HorizontalRule', 'JustifyLeft', 'JustifyCenter',
                          'JustifyRight', 'JustifyBlock', ],
            },
            {
                'name': 'format',
                'items': ['Format', ],
            },
            {
                'name': 'extra',
                'items': ['Link', 'Unlink', 'Blockquote', 'Image', 'Table',
                          'CodeSnippet', 'Mathjax', 'Embed', ],
            },
            {
                'name': 'source',
                'items': ['Maximize', 'Source', ],
            },
        ],

        # This hides the default title provided by CKEditor
        'title': False,

        # Use this toolbar
        'toolbar': 'DefaultToolbarConfig',

        # Which tags to allow in format tab
        'format_tags': 'p;h1;h2',

        # Remove these dialog tabs (semicolon separated dialog:tab)
        'removeDialogTabs': ';'.join([
            'image:advanced',
            'image:Link',
            'link:upload',
            'table:advanced',
            'tableProperties:advanced',
        ]),
        'linkShowTargetTab': False,
        'linkShowAdvancedTab': False,

        # CKEditor height and width settings
        'height': '250px',
        'width': 'auto',
        'forcePasteAsPlainText ': True,

        # Class used inside span to render mathematical formulae using latex
        'mathJaxClass': 'mathjax-latex',

        # Mathjax library link to be used to render mathematical formulae
        'mathJaxLib': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS_SVG',

        # Tab = 4 spaces inside the editor
        'tabSpaces': 4,

        # Extra plugins to be used in the editor
        'extraPlugins': ','.join([
            # 'devtools',  # Shows a tooltip in dialog boxes for developers
            'mathjax',  # Used to render mathematical formulae
            'codesnippet',  # Used to add code snippets
            'image2',  # Loads new and better image dialog
            'embed',  # Used for embedding media (YouTube/Slideshare etc)
            'tableresize',  # Used to allow resizing of columns in tables
        ]),
    }
}
