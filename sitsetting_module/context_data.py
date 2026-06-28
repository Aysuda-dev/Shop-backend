from .models import Sitsetting


def site_setting(request):
    sit_setting:Sitsetting = Sitsetting.objects.filter(is_active=True).first()
    context = {
        "site_setting": sit_setting
    }

    return context
