from .app import app, host, remote_port, app_port
from tornado import wsgi, httpserver, ioloop, autoreload
from bokeh.server.server import Server
from bokeh.command.util import build_single_handler_applications
import os


def run_bokeh_server(bok_io_loop):
    files = ['whoseline_vis/plot.py']
    args = {k: None for k in files}

    apps = build_single_handler_applications(files, args)

    kwargs = {
        'io_loop': bok_io_loop,
        # 'redirect_root': True,
        # 'num_procs': 1,
        # 'sign_sessions': False,
        # 'host':['%s:%d' % (host,app_port),'%s:%d' % (host,bokeh_port)],
        # 'port': bokeh_port,
        # 'use_index': True,
        'allow_websocket_origin': ['%s:%d' % (host, remote_port)]
    }
    srv = Server(apps, **kwargs)


def start():
    # initialize the tornado server
    http_server = httpserver.HTTPServer(
        wsgi.WSGIContainer(app)
    )
    http_server.listen(app_port)
    io_loop = ioloop.IOLoop.instance()
    autoreload.start(io_loop)

    # add the io_loop to the bokeh server
    run_bokeh_server(io_loop)
    print('Starting the server on http://{}:{}/'.format(host, app_port))

    # run the bokeh server
    io_loop.start()