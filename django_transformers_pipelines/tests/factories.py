"""Factories to make models for tests"""
import factory
from faker import Faker
from django_transformers_pipelines.models import Prediction, Predictor, Tag

faker = Faker()


class PredictorFactory(factory.django.DjangoModelFactory):
    """Predictor factory"""

    name = faker.name()
    version = faker.random_int()
    parameters = dict()

    class Meta:
        """Meta params for predictor factory"""

        model = Predictor


class TagFactory(factory.django.DjangoModelFactory):
    """Tag factory"""

    name = faker.name()

    class Meta:
        """Meta params for tag factory"""

        model = Tag


class PredictionFactory(factory.django.DjangoModelFactory):
    """Prediction factory"""

    class Meta:
        """Meta params for prediction factory"""

        model = Prediction

    predictor = factory.SubFactory(PredictorFactory)
    input_data = faker.json(data_columns={"data": ["sentence"]}, num_rows=1)
    prediction = faker.json(data_columns={"data": ["sentence"]}, num_rows=1)
    request_time = faker.date_time()
    prediction_latency = faker.date_time()

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        """function to add tags on creation"""
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)
