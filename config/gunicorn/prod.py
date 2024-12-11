
wsgi_app = "healthops.wsgi:application"

# The granularity of Error log outputs
loglevel = "debug"

# The number of worker processes for handling requests
workers = 2

# The socket to bind
bind = "0.0.0.0:8000"

# Daemonize the Gunicorn process (detach & enter background)
# daemon = True
