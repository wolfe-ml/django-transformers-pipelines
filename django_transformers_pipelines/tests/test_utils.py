"""
Test django utils
"""
from unittest import mock
from django.test import TestCase
from django_transformers_pipelines.tests.factories import (
    PredictionFactory,
    PredictorFactory,
)
from django_transformers_pipelines.utils import (
    get_or_create_tags,
    get_pipeline,
    load_predictor_pipeline,
)


def mock_pipeline(**kwargs):
    """Mock pipeline for testing"""
    if not kwargs:
        raise Exception
    return dict(**kwargs)


class UtilsTest(TestCase):
    """Tests for the utils of DTP"""

    def test_get_pipeline(self):
        """Test getting the pipeline"""
        example_pipeline = {"test": "test-params"}
        with self.settings(TRANSFORMERS_PIPELINE=example_pipeline):
            pipeline = get_pipeline()
            self.assertEqual(pipeline, example_pipeline)

    def test_get_or_create_tags(self):
        """Test get or create tags"""

        pred = PredictionFactory()
        tags = [
            {"name": "tag1"},
            {"name": "tag2"},
            {"name": "tag1"},
        ]

        get_or_create_tags(tags, pred)
        tag_names = [tag.name for tag in pred.tags.all()]
        self.assertEqual(len(tag_names), 2)
        for tag in tags:
            self.assertIn(tag["name"], tag_names)

    def test_load_predictor_pipeline(self):
        """Test load_predictor_pipeline util"""
        with mock.patch("transformers.pipeline", return_value=mock_pipeline):
            pred = PredictorFactory(parameters={"fake": "test"})
            load_predictor_pipeline(pred)

            pred = PredictorFactory(parameters="test")
            load_predictor_pipeline(pred)

            pred = PredictorFactory(parameters=[])
            self.assertRaises(Exception, load_predictor_pipeline, pred)
