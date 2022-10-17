from django.contrib import admin
from django_transformers_pipelines.models import Prediction, Predictor, Tag


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Prediction._meta.fields]


@admin.register(Predictor)
class PredictorAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
