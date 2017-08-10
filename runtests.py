#!/usr/bin/env python
import sys
import django
from django.core.management import execute_from_command_line
from django.conf import settings
from os import path

# Give feedback on used versions
sys.stderr.write('Using Python version {0} from {1}\n'.format(sys.version[:5], sys.executable))
sys.stderr.write('Using Django version {0} from {1}\n'.format(
    django.get_version(),
    path.dirname(path.abspath(django.__file__)))
)

if not settings.configured:
    module_root = path.dirname(path.realpath(__file__))

    settings.configure(
        DEBUG=False,  # will be False anyway by DjangoTestRunner.
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SITE_ID=1,
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sites',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.messages',
            'fluent_contents',
            'fluent_contents.tests.testapp',
            'fluentcms_googlemaps',
            'geoposition',
            'django_wysiwyg',
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': (),
                'OPTIONS': {
                    'loaders': (
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ),
                    'context_processors': (
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.request',
                        'django.template.context_processors.static',
                        'django.contrib.auth.context_processors.auth',
                    ),
                },
            },
        ],
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ),
        FLUENT_CONTENTS_CACHE_OUTPUT=False,
        TEST_RUNNER='django.test.runner.DiscoverRunner',
        ROOT_URLCONF='fluentcms_googlemaps.tests.urls',
        STATIC_URL='/static/',
        GEOPOSITION_GOOGLE_MAPS_API_KEY=None,
    )

DEFAULT_TEST_APPS = [
    'fluentcms_googlemaps',
]


def runtests():
    other_args = list(filter(lambda arg: arg.startswith('-'), sys.argv[1:]))
    test_apps = list(filter(lambda arg: not arg.startswith('-'), sys.argv[1:])) or DEFAULT_TEST_APPS
    argv = sys.argv[:1] + ['test', '--traceback'] + other_args + test_apps
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
