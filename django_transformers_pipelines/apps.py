"""
App registration for django_transformers_pipelines
"""
from symbol import parameters
from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import warnings


class DjangoTransformersPipelinesConfig(AppConfig):
    """App config for django transformers pipelines

    This config enforces a TRANSFORMERS_PIPELINE django setting to be configured
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_transformers_pipelines"

    def ready(self):

        if not hasattr(settings, "TRANSFORMERS_PIPELINE"):
            warnings.warn(
                "No TRANSFORMERS_PIPELINE object specified in the django settings"
            )
