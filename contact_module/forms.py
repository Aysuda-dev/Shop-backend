from  django import forms
from .models import ContactUs



class ContactUstForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('title', 'email',"full_name", 'message')
        widgets = {
            "full_name":forms.TextInput(attrs={'class':'form-control'}),
            "email":forms.EmailInput(attrs={'class':'form-control'}),
            "title":forms.TextInput(attrs={'class':'form-control'}),
            "message":forms.Textarea(attrs={
                'class':'form-control',
                'rows':1,
                'id':'message',
            }),

        }
        labels = {
            'full_name':"نام و نام خانوادگی",
            'email':"ایمیل",
            'message':'نظر شما',
            'title':'موضوع'

        }

