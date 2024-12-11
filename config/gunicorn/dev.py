"""Gunicorn *dev* config file"""

from pathlib import Path

def create_file(filepath):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()

project_name = "healthops"
wsgi_app = f"{project_name}.wsgi:application"

# The granularity of Error log outputs
loglevel = "debug"

# The number of worker processes for handling requests
workers = 2

# The socket to bind
bind = "127.0.0.1:8001"

reload = True

# Write access and error info to /var/log
log_file = f".logs/staging.log"
create_file(log_file)

accesslog = errorlog = log_file

# Redirect stdout/stderr to log file
capture_output = True

# Daemonize the Gunicorn process (detach & enter background)
daemon = False
