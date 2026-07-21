import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop_backend.settings")
django.setup()

from django.core.management import call_command

with open("data.json", "w", encoding="utf-8") as f:
    call_command(
        "dumpdata",
        exclude=["contenttypes", "auth.permission"],
        stdout=f,
    )

print("Done!")