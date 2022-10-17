from datetime import datetime
from django.test import TestCase
from django_inference.models import Tag, Prediction, Predictor
from django_inference.utils import get_or_create_tags


class ModelTests(TestCase):
    """Tests for django_inference models"""

    def test_create_tag(self):
        """Test creating a tag is successful"""
        tag = Tag.objects.create(name="Tag1")

        self.assertEqual(str(tag), tag.name)
        self.assertIn(tag, Tag.objects.all())

    def test_create_prediction(self):
        """Test creating a prediction is successful"""

        prediction = Prediction.objects.create(
            input_data="test input",
            prediction="test prediction",
            request_time=datetime.now(),
            prediction_latency=datetime.now(),
        )

        self.assertIn(prediction, Prediction.objects.all())

    def test_create_prediction_with_tags(self):
        """Test creating a prediction is successful"""
        tags = [
            {"name": "Tag1"},
            {"name": "Tag2"},
            {"name": "Tag3"},
        ]
        prediction = Prediction.objects.create(
            input_data="test input",
            prediction="test prediction",
            request_time=datetime.now(),
            prediction_latency=datetime.now(),
        )
        get_or_create_tags(tags, prediction)

        self.assertIn(prediction, Prediction.objects.all())
