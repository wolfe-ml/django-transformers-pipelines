# File sets up the django environment, used by other scripts that need to
# execute in django land
import os
import django
from django.conf import settings
from django.core.management import call_command
import sys

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "django_transformers_pipelines")
)


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
        INSTALLED_APPS=("django_transformers_pipelines",),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )
    django.setup()


if __name__ == "__main__":
    command = "shell"
    if len(sys.argv[1:]) > 0:
        command = " ".join(sys.argv[1:])

    print("booting django...")
    boot_django()
    print("Done booting django!")

    print(f"Running command: '{command}'...")
    call_command(command)
    print(f"Finished running command: '{command}'")
