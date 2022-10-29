"""
Views for the inference app
"""

from django.http import JsonResponse
from rest_framework import mixins, status, viewsets, generics
from rest_framework.decorators import action

from django_transformers_pipelines.models import Prediction, Predictor, Tag
from django_transformers_pipelines.serializers import (
    PredictionSerializer,
    PredictorSerializer,
    TagSerializer,
)
from django_transformers_pipelines.utils import (
    get_or_create_tags,
    run_predictor_pipeline,
)
from rest_framework import filters


class PredictorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Predictor serializer"""

    serializer_class = PredictorSerializer
    queryset = Predictor.objects.all()

    @action(detail=True, methods=["post"])
    def inference(self, request, pk):
        """Run inference on the pipeline"""

        data = request.data.pop("data", [])
        tags = request.data.pop("tags", [])
        predictor = self.get_object()

        output = run_predictor_pipeline(predictor, data)
        get_or_create_tags(tags, output)

        serializer = PredictionSerializer(output)
        return JsonResponse(
            serializer.data,
            status=status.HTTP_200_OK,
            safe=False,
        )


class TagViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Tag view set"""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class PredictionViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Viewset for ML Inference"""

    serializer_class = PredictionSerializer
    queryset = Prediction.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["tags"]

    # def get_queryset(self):
    #     """Retrieve predictions"""

    #     queryset = self.queryset

    #     tags = self.request.query_params.get("tags")
    #     if tags:
    #         tag_ids = self._params_to_ints(tags)
    #         queryset = queryset.filter(tags__id__in=tag_ids)

    #     return queryset.order_by("-id").distinct()
