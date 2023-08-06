import io

import qrcode
import qrcode.image.svg
from django_otp import user_has_device
from django_otp.plugins.otp_totp.models import TOTPDevice

from django.shortcuts import redirect, render

from zweifach.forms import SetupForm, VerifyForm


def verify(request):
    """Verify second auth factor."""
    if request.method == "POST":
        form = VerifyForm(request.POST, request=request)
        if form.is_valid():
            return redirect(request.GET.get("next", "/"))
    else:
        form = VerifyForm(request=request)
    return render(request, "zweifach/verify.html", {'form': form})


def setup(request):
    """Setup two factor auth for user."""
    if user_has_device(request.user):
        raise NotImplementedError("already configured!")

    # create TOTP device
    device = TOTPDevice.objects.get_or_create(
        user=request.user,
        confirmed=False,
        defaults={"name": "auto-generated device"},
    )[0]

    # display QR-Code (provided as base64 string, so we don't need any url configuration)
    qr_code = io.BytesIO()
    img = qrcode.make(
        device.config_url, image_factory=qrcode.image.svg.SvgImage
    )
    img.save(qr_code)

    # display form
    if request.method == "POST":
        form = SetupForm(request.POST, request=request, device=device)
        # setup is done, if the entered code is valid
        if form.is_valid():
            return redirect(request.GET.get("next", "/"))
    else:
        form = SetupForm(request=request, device=device)

    return render(
        request,
        "zweifach/setup.html",
        {
            'form': form,
            'qrcode': qr_code.getvalue().decode("utf-8"),
            'device': device,
        },
    )
