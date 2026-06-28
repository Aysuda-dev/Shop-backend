from django.shortcuts import render
from .forms import ContactUstForm
from django.views.generic import CreateView
# Create your views here.

class ContactUsView(CreateView):
    form_class = ContactUstForm
    template_name = 'contact_module/contact_us.html'

    success_url = '/contact-us/'