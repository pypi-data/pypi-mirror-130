from django_otp import user_has_device

from django.conf import settings
from django.shortcuts import redirect
from django.template.defaultfilters import urlencode
from django.urls import reverse


def two_factor_auth_required(user):
    """Check if 'user' must enable 2FA."""
    for check in getattr(settings, 'ZWEIFACH_AUTH_REQUIRED', []):
        if check(user):
            return True
    return False


def two_factor_auth_configured(user):
    """Check if 'user' has 2FA enabled."""
    if user.is_authenticated:
        return user_has_device(user)
    return False


def excluded_urls():
    """Return a list of URLs which are accessible without verifying the second factor."""
    default_excludes = [reverse('zweifach_verify'), reverse('zweifach_setup')]
    if 'django.contrib.admin' in settings.INSTALLED_APPS:
        default_excludes.append(reverse('admin:login'))
    if settings.LOGIN_URL:
        default_excludes.append(settings.LOGIN_URL)

    return getattr(settings, 'ZWEIFACH_URL_EXCLUDES', []) + default_excludes


class ZweifachMiddleware:
    """
    - Enforce 2FA, if user has it configured.
    - Enforce 2FA-Setup, if user is required to use it.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_urls = excluded_urls()

    def __call__(self, request):

        if request.path not in self.excluded_urls:

            if two_factor_auth_required(
                request.user
            ) and not two_factor_auth_configured(request.user):
                return redirect(
                    reverse('zweifach_setup')
                    + f'?next={urlencode(request.get_full_path())}'
                )

            if (
                two_factor_auth_configured(request.user)
                and not request.user.is_verified()
            ):
                return redirect(
                    reverse('zweifach_verify')
                    + f'?next={urlencode(request.get_full_path())}'
                )

        return self.get_response(request)
