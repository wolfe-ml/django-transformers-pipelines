"""
Utilities for django inference
"""
from django.conf import settings
from transformers import pipeline
from django_transformers_pipelines.models import Predictor, Tag, Prediction
from datetime import datetime
from django.utils.timezone import make_aware


def get_pipeline():
    """Get the pipeline object from the django settings"""
    pipeline_conf = getattr(settings, "TRANSFORMERS_PIPELINE", None)
    return pipeline_conf


def get_or_create_tags(tags, prediction):
    """Handle getting or creating tags as needed"""

    for tag in tags:
        tag_obj, _ = Tag.objects.get_or_create(**tag)
        prediction.tags.add(tag_obj)


def load_predictor_pipeline(predictor: Predictor):
    """load the predictor's pipeline for inference"""
    try:
        return pipeline(**predictor.parameters)
    except:
        raise Exception(f"Improperly configured predictor pipeline: {predictor.id}")


def run_predictor_pipeline(predictor: Predictor, data):
    """Run the predictor's pipeline inference on the input data"""
    predictor_pipeline = load_predictor_pipeline(predictor)

    try:
        pred_start = make_aware(datetime.now())
        prediction = predictor_pipeline(data)
        pred_end = make_aware(datetime.now())
    except:
        raise Exception("Encountered error while running pipeline")

    try:
        return Prediction.objects.create(
            predictor=predictor,
            input_data=data,
            prediction=prediction,
            request_time=pred_start,
            prediction_latency=pred_end,
        )
    except:
        raise Exception(
            "Encountered error while inserting prediction into the database"
        )
