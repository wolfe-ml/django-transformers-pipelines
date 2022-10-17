# File sets up the django environment, used by other scripts that need to
# execute in django land
import os
import django
from django.conf import settings
from django.core.management import call_command
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "django_inference"))


def boot_django():
    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=("django_inference",),
        TIME_ZONE="UTC",
        USE_TZ=True,
        TRANSFORMERS_PIPELINE={
            "task": "text-generation",
        },
    )
    django.setup()


if __name__ == "__main__":
    command = "shell"
    if len(sys.argv[1:]) > 0:
        command = sys.argv[1:]

    call_command(command)
