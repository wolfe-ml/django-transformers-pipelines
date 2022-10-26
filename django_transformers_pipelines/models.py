"""
Models for inference
"""
from django.db import models


class Predictor(models.Model):
    """Predictor model"""

    name = models.CharField(max_length=255)
    version = models.IntegerField()
    parameters = models.JSONField()


class Tag(models.Model):
    """Tag for filtering predictions"""

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.name)


class Prediction(models.Model):
    """Prediction model"""

    predictor = models.ForeignKey(
        "Predictor",
        on_delete=models.PROTECT,
        related_name="predictions",
    )
    tags = models.ManyToManyField("Tag", related_name="predictions")

    input_data = models.JSONField()
    prediction = models.JSONField()

    request_time = models.DateTimeField()
    prediction_latency = models.DateTimeField()
    response_time = models.DateTimeField(auto_now=True)
