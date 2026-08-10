from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class RegisterForm(forms.Form):
    email = forms.EmailField(
        label=_('ایمیل'),
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator()

        ]
    )

    password = forms.CharField(
        label=_('کلمه عبور '),
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label=_('تکرار کلمه عبور '),
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password

        raise ValidationError(_('کلمه عبور و تکرار کلمه عبور مغایرت دارند.'))


class LoginForm(forms.Form):
    email = forms.EmailField(
        label=_('ایمیل'),
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator()
        ]
    )

    password = forms.CharField(
        label=_('کلمه عبور '),
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label=_('ایمیل'),
        widget=forms.EmailInput(),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator()
        ]
    )



class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label=_('کلمه عبور '),
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label=_('تکرار کلمه عبور '),
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password

        raise ValidationError(_('کلمه عبور و تکرار کلمه عبور مغایرت دارند.'))

