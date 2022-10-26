from factory.django import DjangoModelFactory
from django_transformers_pipelines.models import Prediction, Predictor, Tag
from faker import Faker
import factory

faker = Faker()


class PredictorFactory(DjangoModelFactory):
    """Predictor factory"""

    name = faker.name()
    version = faker.random_int()
    parameters = dict()

    class Meta:
        model = Predictor


class TagFactory(DjangoModelFactory):
    """Tag factory"""

    name = faker.name()

    class Meta:
        model = Tag


class PredictionFactory(DjangoModelFactory):
    """Prediction factory"""

    class Meta:
        model = Prediction

    predictor = factory.SubFactory(PredictorFactory)
    input_data = faker.json(data_columns={"data": ["sentence"]}, num_rows=1)
    prediction = faker.json(data_columns={"data": ["sentence"]}, num_rows=1)
    request_time = faker.date_time()
    prediction_latency = faker.date_time()

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of tags were passed in, use them
            for tag in extracted:
                self.tags.add(tag)
