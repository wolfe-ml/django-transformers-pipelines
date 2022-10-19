"""
Views for the inference app
"""
import logging
from datetime import datetime

from django.http import JsonResponse
from django.utils.timezone import make_aware
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action

from django_transformers_pipelines.models import Prediction, Predictor, Tag
from django_transformers_pipelines.serializers import (
    PredictionSerializer,
    PredictorSerializer,
    TagSerializer,
)
from django_transformers_pipelines.utils import get_or_create_tags, get_pipeline


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
    logger = logging.Logger(__name__)

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
        tags = request.data.pop("tags", [])

        self.logger.info("starting prediction...")
        pred_start = make_aware(datetime.now())
        prediction = self.pipeline(data)
        pred_end = make_aware(datetime.now())
        self.logger.info("Completed prediction")

        self.logger.info("Saving prediction...")
        output = self.queryset.create(
            input_data=data,
            prediction=prediction,
            request_time=pred_start,
            prediction_latency=pred_end,
        )
        get_or_create_tags(tags, output)
        self.logger.info("Done saving prediction")
        serializer = self.get_serializer(output)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
