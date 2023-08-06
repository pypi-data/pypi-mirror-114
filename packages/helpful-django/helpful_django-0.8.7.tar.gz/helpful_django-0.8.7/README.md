Helpful Django Apps
=====

This python package implements some very helpful web applications for the django framework.

Quick start
-----------

1. Add the app you want to use to your INSTALLED_APPS setting like this:
    ```
    INSTALLED_APPS = [
        ...
        'helpful_django.some_name',
    ]
   ``

2. Include the polls URLconf in your project urls.py like this::

   path('some_name/', include('some_name.urls')),

3. Run ``python manage.py migrate`` to create the required models.
