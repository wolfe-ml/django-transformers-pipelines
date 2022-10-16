"""
Views for the inference app
"""
from datetime import datetime

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_inference.models import Prediction, Predictor, Tag
from django_inference.serializers import (
    PredictionSerializer,
    PredictorSerializer,
    TagSerializer,
)
from django_inference.utils import get_pipeline
from django.core import serializers


class PredictorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Predictor serializer"""

    serializer_class = PredictorSerializer
    queryset = Predictor.objects.all()


class TagViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Tag view set"""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class PredictionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Viewset for ML Inference"""

    serializer_class = PredictionSerializer
    queryset = Prediction.objects.all()
    pipeline = get_pipeline()

    def get_queryset(self):
        """Retrieve predictions"""

        queryset = self.queryset

        tags = self.request.query_params.get("tags")
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        return queryset.order_by("-id").distinct()

    @action(detail=False, methods=["post"])
    def inference(self, request):
        """Run inference on the pipeline"""

        data = request.data.pop("data", [])
        # tags = request.data.pop("tags", [])
        t0 = datetime.now()
        prediction = self.pipeline(data)
        print(prediction)
        t1 = datetime.now()

        Prediction.objects.create(
            predictor=None,
            # tags=tags,
            input_data=data,
            prediction=prediction,
            request_time=t0,
            prediction_latency=t1,
        )
        # serializer = self.get_serializer()
        return Response(prediction, status=status.HTTP_400_BAD_REQUEST)
