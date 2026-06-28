from  django import forms
from .models import ProductComment



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
            'message':'نظر شما',

        }

