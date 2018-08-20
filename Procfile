release: python manage.py migrate
web: newrelic-admin run-program gunicorn -c config/gunicorn.conf.py control-ofelia.wsgi