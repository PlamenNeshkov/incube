web: newrelic-admin run-program gunicorn --pythonpath="$PWD/incube" wsgi:application
worker: python incube/manage.py rqworker default