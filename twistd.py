"""Twisted application definition module.

The twisted application framework provides a simple interface
(service.Application) to run your code taking care of initialisation
tasks such as running a reactor.

Applications are run using the `twistd` CLI that comes bundled with Twisted
installations. So it should be enough to run it with:
$ /path/to/twistd --python twistd.py --nodaemon

Note: you'll have to specify the full path to twistd (even if you're using
a virtual environment).

The --nodaemon flag prevents daemonisation, but if you have the daemon running
you can terminate it using `kill $(cat twistd.pid)`.

The Application itself is just a container for Services that handle your specific
application logic (web servers, SSH clients, etc.).
"""

import logging

# if '.' is not added to PYTHONPATH,
# twistd won't do it for you so you'll get import errors.
import sys

sys.path.append(".")

from twisted.application import internet, service
from twisted.python import log
from twisted.web import server

from src.services import CCTVLoggerRunner, CCTVLoggerServer

TIME_INTERVAL = 5

logging.basicConfig(level=logging.INFO)

top_service = service.MultiService()

# service to take logs
cctv_logger_runner = CCTVLoggerRunner()
cctv_logger_service = internet.TimerService(
    step=TIME_INTERVAL, callable=cctv_logger_runner.run
)
cctv_logger_service.setServiceParent(top_service)

# service to listen for connections
cctv_logger_server = server.Site(CCTVLoggerServer())
tcp_service = internet.TCPServer(8080, cctv_logger_server)
tcp_service.setServiceParent(top_service)

application = service.Application("cctv_logger")
top_service.setServiceParent(application)
