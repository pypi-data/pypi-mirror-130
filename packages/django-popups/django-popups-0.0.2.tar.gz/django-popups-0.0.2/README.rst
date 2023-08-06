django-popups
==========

django-popups is a Django app to use for demiansoft. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
------------

1. Add "popups" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'popups',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('popups/', include('popups.urls')),

3. Run ``python manage.py migrate`` to create the popups models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a popups (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/popups/ to test the app.
