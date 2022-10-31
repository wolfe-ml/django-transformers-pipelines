"""
Views for the inference app
"""
from rest_framework import mixins, viewsets

from django_transformers_pipelines.models import Prediction, Predictor, Tag
from django_transformers_pipelines.serializers import (
    PredictionSerializer,
    PredictorSerializer,
    TagSerializer,
)

from rest_framework import filters


class PredictorViewSet(viewsets.ModelViewSet):
    """Predictor serializer"""

    serializer_class = PredictorSerializer
    queryset = Predictor.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    """Tag view set"""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class PredictionViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    """Viewset for ML Inference"""

    serializer_class = PredictionSerializer
    queryset = Prediction.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["tags__name", "predictor__name"]
