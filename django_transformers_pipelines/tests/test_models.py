"""Tests for the Django models"""
from django.test import TestCase
from django_transformers_pipelines.models import Tag, Prediction, Predictor
from django_transformers_pipelines.serializers import (
    TagSerializer,
    PredictionSerializer,
)
from django_transformers_pipelines.tests.factories import (
    PredictionFactory,
    PredictorFactory,
    TagFactory,
)
from django_transformers_pipelines.utils import get_or_create_tags
from unittest import mock


def mock_pipeline(data):
    return {}


class ModelTests(TestCase):
    """Tests for django_transformers_pipelines models"""

    def test_create_tag(self):
        """Test creating a tag is successful"""
        tag = TagFactory.create()

        self.assertEqual(str(tag), tag.name)
        self.assertIn(tag, Tag.objects.all())

    def test_create_predictor(self):
        """Test creating a predictor is successful"""

        predictor = PredictorFactory.create()

        self.assertIn(predictor, Predictor.objects.all())

    def test_create_prediction(self):
        """Test creating a prediction is successful"""

        prediction = PredictionFactory.create()

        self.assertIn(prediction, Prediction.objects.all())

    def test_create_prediction_with_tags(self):
        """Test creating a prediction is successful"""
        tags = [
            {"name": "Tag1"},
            {"name": "Tag2"},
            {"name": "Tag3"},
        ]
        prediction = PredictionFactory.create()
        get_or_create_tags(tags, prediction)

        self.assertIn(prediction, Prediction.objects.all())
        all_tags = [str(tag) for tag in Tag.objects.all()]
        for tag in tags:
            self.assertIn(tag["name"], all_tags)


class SerializerTests(TestCase):
    """Tests for the serializer classes"""

    def test_tag_serializer(self):
        """Test the tag serializer"""
        tag = TagFactory()
        serializer = TagSerializer(tag)
        self.assertEqual(serializer.data["name"], tag.name)

    def test_tag_deserialize(self):
        """Test the tag deserializer"""
        serializer = TagSerializer(data={"name": "test"})
        self.assertTrue(serializer.is_valid())
        tag = serializer.save()
        self.assertIn(tag, Tag.objects.all())

    def test_prediction_serializer(self):
        """Test the prediction serializer"""
        prediction = PredictionFactory()
        serializer = PredictionSerializer(prediction)
        self.assertEqual(serializer.data["id"], prediction.id)

    def test_prediction_deserialize(self):
        """Test the prediction deserializer"""
        with mock.patch(
            "django_transformers_pipelines.utils.load_predictor_pipeline",
            return_value=mock_pipeline,
        ):
            predictor = PredictorFactory()
            serializer = PredictionSerializer(
                data={
                    "predictor": predictor.id,
                    "input_data": "test data",
                    "tags": [],
                }
            )
            self.assertTrue(serializer.is_valid())
            s_prediction = serializer.save()
            self.assertIn(s_prediction, Prediction.objects.all())
