from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class DjangoInferenceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_transformers_pipelines"

    def ready(self):

        if not hasattr(settings, "TRANSFORMERS_PIPELINE"):
            raise ImproperlyConfigured(
                "You must specify a TRANSFORMERS_PIPELINE object in your settings"
            )
