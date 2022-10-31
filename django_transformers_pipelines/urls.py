from django_transformers_pipelines.views import (
    PredictionViewSet,
    PredictorViewSet,
    TagViewSet,
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"predictions", PredictionViewSet, basename="predictions")
router.register(r"predictors", PredictorViewSet, basename="predictors")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = router.urls
