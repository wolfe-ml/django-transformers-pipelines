"""
App registration for django_transformers_pipelines
"""
from django.apps import AppConfig


class DjangoTransformersPipelinesConfig(AppConfig):
    """App config for django transformers pipelines

    This config enforces a TRANSFORMERS_PIPELINE django setting to be configured
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_transformers_pipelines"
