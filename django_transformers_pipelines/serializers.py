"""
Serializers for the django inference models
"""
from rest_framework import serializers
from django_transformers_pipelines.models import Predictor, Prediction, Tag
from django_transformers_pipelines.utils import (
    get_or_create_tags,
    run_predictor_pipeline,
)


class PredictorSerializer(serializers.ModelSerializer):
    """Serializer for predictors"""

    class Meta:
        """Predictor serializer meta class"""

        model = Predictor
        fields = ["id", "name", "version", "parameters"]
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""

    class Meta:
        """Tag serializer meta class"""

        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class PredictionSerializer(serializers.ModelSerializer):
    """Serializer for predictions"""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        """Prediction serializer meta class"""

        model = Prediction
        fields = [
            "id",
            "tags",
            "input_data",
            "predictor",
            "prediction",
            "request_time",
            "prediction_latency",
            "response_time",
        ]
        read_only_fields = [
            "id",
            "prediction",
            "request_time",
            "prediction_latency",
            "response_time",
        ]

    def create(self, validated_data):
        """Create a prediction in the db"""

        tags = validated_data.pop("tags", [])
        data = validated_data.pop("input_data", [])
        predictor = validated_data.pop("predictor", 1)

        prediction = run_predictor_pipeline(predictor, data)
        get_or_create_tags(tags, prediction)

        return prediction

    def update(self, instance, validated_data):
        """Update a prediction"""

        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.clear()
            get_or_create_tags(tags, instance)

        instance.save()
        return instance
