""" gunicorn wsgi server configuration. """

from os import environ

bind = '0.0.0.0:' + environ.get('PORT', '8000')
max_requests = 1000
worker_class = 'gevent'
workers = 1
