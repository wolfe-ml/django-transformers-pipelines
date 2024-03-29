django-transformers-pipelines
===============
![Deployment Status](https://github.com/wolfe-ml/django-transformers-pipelines/actions/workflows/deploy.yml/badge.svg)

This is still in development and has not yet been released

This is a python package housing a django app to allow for a simple interface to facilitate
ML model inference and storage of prediction results in the associated django DB.

Installable App
---------------

This app provides an api interaction for a transformers `pipeline`, and a `Prediction` table
to keep track of inference made by the specified pipeline.

This app can be installed and used in your django project by:

    $ pip install django-transformers-pipelines


Edit your `settings.py` file to include `'django_transformers_pipelines'` in the `INSTALLED_APPS`
listing.

    INSTALLED_APPS = [
        ...

        'django_transformers_pipelines',
    ]

Add the parameter `TRANSFORMERS_PIPELINE` to your `settings.py`. This parameter will house all the
desired key word arguments to instantiate your pipeline.

    TRANSFORMERS_PIPELINE = {
        ...
    }

For example a simple `text generation pipeline <https://huggingface.co/docs/transformers/task_summary#text-generation>`_ can be started up with the following setting:

    TRANSFORMERS_PIPELINE = {
        "task": "text-generation",
    }

Edit your project `urls.py` file to import the URLs:


    from django_transformers_pipelines.routers import pipeline_router

    ...

    url_patterns = [
        ...

        path("api/", include(pipeline_router.urls)),
    ]


Finally, make migrations for all apps, or add the specific app to your database:

    $ ./manage.py makemigrations django_transformers_pipelines


Docs & Source
-------------

* Helpful Django app deployment article: https://realpython.com/installable-django-app/
* Huggingface: https://huggingface.co/
* Existing huggingface pipelines: https://huggingface.co/docs/transformers/task_summary
