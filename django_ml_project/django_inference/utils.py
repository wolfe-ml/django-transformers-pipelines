"""
Utilities for django inference
"""
from django.conf import settings
from django_inference.pipelines.core import Pipeline
from transformers import pipeline


def get_pipeline() -> Pipeline:
    """Get the pipeline object from the django settings"""
    pipeline_conf = getattr(settings, "PIPELINE", None)
    return pipeline(**pipeline_conf)
