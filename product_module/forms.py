from  django import forms
from .models import ProductComment
from django.utils.translation import gettext_lazy as _



class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['message']
        widgets = {
            "message":forms.Textarea(attrs={
                'class':'form-control',
                'rows':1,
                'id':'message',
            }),

        }
        labels = {
            'message':_('نظر شما'),

        }

