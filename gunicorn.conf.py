# # Gunicorn configuration file
# import multiprocessing

# max_requests = 1000
# max_requests_jitter = 50

# log_file = "-"

# bind = "0.0.0.0:3100"

# worker_class = "uvicorn.workers.UvicornWorker"
# workers = (multiprocessing.cpu_count() * 2) + 1

#5:02 - 36924
import os
574



workers = int(os.environ.get('GUNICORN_PROCESSES', '8'))

threads = int(os.environ.get('GUNICORN_THREADS', '16'))

# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:5100')
#gunicorn --config gunicorn.conf.py server:app


forwarded_allow_ips = '*'

secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }