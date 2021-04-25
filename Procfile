release: python manage.py migrate
web: gunicorn fakecsv_generator.wsgi --log-file -
worker: celery worker --app=fakecsv_generator