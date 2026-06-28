from  django import forms
from django.core import validators
from django.core.exceptions import ValidationError

from account_module.models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',"email", 'avatar', 'address' ,'about_user')
        widgets = {
            "first_name":forms.TextInput(attrs={'class':'form-control'}),
            "last_name":forms.TextInput(attrs={'class':'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "avatar": forms.FileInput(attrs={'class': 'form-control'}),
            "address":forms.Textarea(attrs={
                'class':'form-control',
                'rows':2,

            }), "about_user":forms.Textarea(attrs={
                'class':'form-control',
                'rows':6,

            }),

        }
        labels = {
            'first_name':"نام",
            'last_name':"نام خانوادگی",
            'email':"ایمیل",
            'address':'آدرس',
            'avatar':'پروفایل',
            'about_user':'درباره شخص'

        }




class ChangePasswordForm(forms.Form):
    current_user=forms.CharField(
        label='کلمه عبور فعلی ',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label='کلمه عبور جدید ',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    confirm_password = forms.CharField(
        label='تکرار کلمه عبور جدید ',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند.')
