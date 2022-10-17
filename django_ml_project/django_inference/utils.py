"""
Utilities for django inference
"""
from django.conf import settings
from transformers import pipeline
from django_inference.models import Tag


def get_pipeline():
    """Get the pipeline object from the django settings"""
    pipeline_conf = getattr(settings, "TRANSFORMERS_PIPELINE", None)
    return pipeline(**pipeline_conf)


def get_or_create_tags(tags, prediction):
    """Handle getting or creating tags as needed"""

    for tag in tags:
        tag_obj, created = Tag.objects.get_or_create(**tag)
        prediction.tags.add(tag_obj)
