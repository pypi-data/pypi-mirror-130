Zweifach
========

Zweifach (german for "two times") is an app to make integration of django-otp a bit more biased.

Integration of two factor auth is enforced by a middleware which will ensure two things:

- make sure a user who is required to enable 2FA for its account will be redirected to the setup-view until setup is done.
- make sure a user who has 2FA enabled will be redirected to verify-view for token input after login until verified.


Quickstart
----------

- Install packages by running 'pip install zweifach django-otp qrcode'
- Add 'zweifach' to INSTALLED_APPS.
- Add 'zweifach.middleware.ZweifachMiddleware' to MIDDLEWARE, *after* AuthenticationMiddleware.
- Inlcude 'zweifach.urls' somewhere in your url-config.
- Configure django-otp as described further down below


Settings
--------

settings.ZWEIFACH_AUTH_REQUIRED

    default: []

    A list of checks which determine, if a user needs 2FA to use its account.

    examaple::

        ZWEIFACH_AUTH_REQUIRED = [
            lambda user: user.is_staff,  # all staff unsers must use two factor auth
            lambda user: '2fa' in user.groups.values_list("name", flat=True),  # all users in group '2fa' must use two factor auth
        ]


settings.ZWEIFACH_URL_EXCLUDES

    default: []

    A list of url which are always accessible without 2FA.
    Verify and Setup views are always excluded as well as settings.LOGIN_URL and the admin login view, if admin is enabled.

    example::

        ZWEIFACH_URL_EXCLUDES = [
            '/imprint/',
            '/faq/how-to-setup-2fa/',
        ]

Note: If a url is accessible without login, it can of course still be viewed without any 2FA interaction.


Notes about django-otp configuration
------------------------------------

A compatible installation of django-otp should be setup as follows:

Add to INSTALLED_APPS::

    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',

Add to MIDDLEWARE (between AuthenticationMiddleware and ZweifachMiddleware)::

    'django_otp.middleware.OTPMiddleware'

Configure issuer::

    OTP_TOTP_ISSUER = 'MyProject'


Usage
-----

To generate static recovery tokens (also useful for first login on freshly installed systems) use::

    ./manage.py addstatictoken <username>


Development
-----------

Ensure basic code style with::

    tox

Build package with::

    python3 -m build

Upload package to PyPI::

    python3 -m twine upload dist/zweifach-x.x.x*
