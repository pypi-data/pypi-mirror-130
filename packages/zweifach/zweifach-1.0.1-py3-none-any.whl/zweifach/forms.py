from django_otp import login, match_token, verify_token

from django import forms


class VerifyForm(forms.Form):
    code = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_code(self):
        device = match_token(self.request.user, self.cleaned_data["code"])
        if not device:
            raise forms.ValidationError("code did not validate")
        else:
            login(self.request, device)


class SetupForm(forms.Form):
    code = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.device = kwargs.pop("device")
        super().__init__(*args, **kwargs)

    def clean_code(self):
        device = verify_token(
            self.request.user,
            self.device.persistent_id,
            self.cleaned_data["code"],
        )
        if not device == self.device:
            raise forms.ValidationError("code did not validate")
        else:
            device.confirmed = True
            device.save(update_fields=("confirmed",))
            login(self.request, device)
