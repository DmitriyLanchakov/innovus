# encoding: utf-8
import os
import sys


user = "www"
bind = "localhost:8080"
workers = 10
max_requests = 100
timeout = 300
keepalive = 15
preload_app = True
logfile = "/var/log/nginx.unicorn.log"
pidfile = "/var/run/tomskforum/tomskforum.pid"

rel = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

for path in ['../contrib', ]:
    abspath = rel(path)
    if abspath not in sys.path:
        sys.path.insert(0, path)
