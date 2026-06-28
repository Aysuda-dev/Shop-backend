from django.shortcuts import render
from django.views.generic import TemplateView
from sitsetting_module.models import Sitsetting

# Create your views here.


class AboutView(TemplateView):
    template_name = 'aboutus_module/aboutus.html'

    # def get_context_data(self, **kwargs):
    #     context = super(AboutView, self).get_context_data(**kwargs)
    #     sit_setting:Sitsetting = Sitsetting.objects.filter(is_active=True).first()
    #     context['sit_setting'] = sit_setting
    #
    #     return context

