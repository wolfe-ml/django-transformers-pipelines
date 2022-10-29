"""
Test django utils
"""
from django.test import TestCase

from django_transformers_pipelines.utils import get_pipeline


class UtilsTest(TestCase):
    def test_get_pipeline(self):
        """Test getting the pipeline"""
        example_pipeline = {"test": "test-params"}
        with self.settings(TRANSFORMERS_PIPELINE=example_pipeline):
            pipeline = get_pipeline()
            self.assertEqual(pipeline, example_pipeline)

    def test_get_or_create_tags(self):
        """Test get or create tags"""
