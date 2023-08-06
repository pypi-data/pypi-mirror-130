from django.conf import settings
from django.core.checks import Error, Tags, register


@register(Tags.compatibility)
def dependencies_check(app_configs, **kwargs):
    errors = []

    if "django_otp" not in settings.INSTALLED_APPS:
        errors.append(
            Error(
                "zweifach app requires django-otp to be installed.",
                id="zweifach.E001",
            )
        )

    if "django_otp.middleware.OTPMiddleware" not in settings.MIDDLEWARE:
        errors.append(
            Error(
                "zweifach app requires OTPMiddleware to be enabled.",
                id="zweifach.E002",
                hint="OTPMiddleware is included in django-otp package",
            )
        )
    return errors
