"""
Admin registration for pipeline models
"""
from django.contrib import admin
from django_transformers_pipelines.models import Prediction, Predictor, Tag


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    """Admin registration of prediction model"""

    readonly_fields = [field.name for field in Prediction._meta.fields]


@admin.register(Predictor)
class PredictorAdmin(admin.ModelAdmin):
    """Admin registration of predictor model"""


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin registration of tag model"""
