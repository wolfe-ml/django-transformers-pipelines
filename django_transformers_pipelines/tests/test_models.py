from django.test import TestCase
from django_transformers_pipelines.models import Tag, Prediction, Predictor
from django_transformers_pipelines.tests.factories import (
    PredictionFactory,
    PredictorFactory,
    TagFactory,
)
from django_transformers_pipelines.utils import get_or_create_tags


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
