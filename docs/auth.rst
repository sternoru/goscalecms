4. Authorization and registration
====================

You can use any auth app for django but if you want a quick and easy setup with GoScale you're in luck - we support django-allauth_ ! Which is one of the most convenient apps to handle all of your user account needs.
We also added a few template tags and utils for it to make it easier to use.

.. _django-allauth: https://github.com/pennersr/django-allauth

4.1. Installation
---------------------

Just follow the tutorial from django-allauth_ README. Here's a brief summary:

Install django the requirements::

    pip install django-allauth django-avatar
    ./manage.py syncdb avatar

settings.py::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        "django.core.context_processors.request",
        ...
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",
        ...
    )

    AUTHENTICATION_BACKENDS = (
        ...
        # Needed to login by username in Django admin, regardless of `allauth`
        "django.contrib.auth.backends.ModelBackend",

        # `allauth` specific authentication methods, such as login by e-mail
        "allauth.account.auth_backends.AuthenticationBackend",
        ...
    )

    INSTALLED_APPS = (
        ...
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        # ... include the providers you want to enable:
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.github',
        'allauth.socialaccount.providers.linkedin',
        'allauth.socialaccount.providers.openid',
        'allauth.socialaccount.providers.persona',
        'allauth.socialaccount.providers.soundcloud',
        'allauth.socialaccount.providers.stackexchange',
        'allauth.socialaccount.providers.twitter',
        'allauth.socialaccount.providers.weibo',
        ...
    )

urls.py::

    urlpatterns = patterns('',
        ...
        (r'^accounts/', include('allauth.urls')),
        (r'^goscale/', include('goscale.urls')),
        ...
    )

Example settings (consult the docs for more customizaton)::

    LOGIN_REDIRECT_URL = '/'
    ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
    ACCOUNT_EMAIL_VERIFICATION = 'optional'
    SOCIALACCOUNT_PROVIDERS = {
        'google': {
            'SCOPE': [
                'https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'
            ],
            'AUTH_PARAMS': { 'access_type': 'online' }
        }
    }

Make sure to create social apps in the admin for all the providers you choose.

4.2. Usage
---------------------

You can use it as is the way intended by django-allauth_ . Or you can use GoScale combined Sign In / Sign Up view::

    {% load url from future %}
    {% load i18n %}
    {% load account %}

    <a href="{% url 'goscale_account_signup' %}" rel="next">{% trans "Log in" %} / {% trans "Register" %}</a>

We also already have a template tag that handles the whole "User bar"::

    {% load goscale_tags %}

    {% goscale_user %}