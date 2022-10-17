"""
Serializers for the django inference models
"""
from rest_framework import serializers
from django_inference.models import Predictor, Prediction, Tag


class PredictorSerializer(serializers.ModelSerializer):
    """Serializer for predictors"""

    class Meta:
        model = Predictor
        fields = ["id", "name", "version", "parameters"]
        read_only_fields = ["id"]


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags"""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class PredictionSerializer(serializers.ModelSerializer):
    """Serializer for predictions"""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Prediction
        fields = [
            "id",
            "tags",
            "input_data",
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

    def _get_or_create_tags(self, tags, prediction):
        """Handle getting or creating tags as needed"""

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(**tag)
            prediction.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a prediction in the db"""

        tags = validated_data.pop("tags", [])
        prediction = Prediction.objects.create(**validated_data)
        self._get_or_create_tags(tags, prediction)
        return prediction

    def update(self, instance, validated_data):
        """Update a prediction"""

        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
