from django_transformers_pipelines.views import (
    PredictionViewSet,
    PredictorViewSet,
    TagViewSet,
)
from rest_framework.routers import DefaultRouter


pipeline_router = DefaultRouter()
pipeline_router.register("predictions", PredictionViewSet)
pipeline_router.register("predictors", PredictorViewSet)
pipeline_router.register("tags", TagViewSet)
