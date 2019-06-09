#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

__version__ = '0.1'
__author__ = 'Alice Ferrazzi'
__license__ = 'GNU GPLv2+'

from flask import Flask
from flask_restful import Api
import multiprocessing
import argparse
from .resources import AgentInfo, dispatcher


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--jobs', type=int,
                        default=multiprocessing.cpu_count(),
                        help='Specify the number of make jobs')

    parser.add_argument('-H', '--host', type=str,
                        default='0.0.0.0',
                        help='Specify the host')

    parser.add_argument('-P', '--port', type=int,
                        default='5000',
                        help='Specify the port')

    parser.add_argument('-T', '--threaded', action='store_true',
                        help='Enable threading')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debugging')

    return parser.parse_args()


def create_app(cmdline_args):
    """
    Create server application
    RESTful api version 1.0
    """

    app = Flask(__name__, static_url_path="")
    api = Api(app)

    api.add_resource(AgentInfo.AgentAPI, '/elivepatch/api/',
                     endpoint='root')

    # get agento information
    api.add_resource(AgentInfo.AgentAPI, '/elivepatch/api/v1.0/agent',
                     endpoint='agent')

    # where to retrieve the live patch when ready
    api.add_resource(dispatcher.SendLivePatch,
                     '/elivepatch/api/v1.0/send_livepatch',
                     endpoint='send_livepatch')

    # where to receive the config file
    api.add_resource(dispatcher.GetFiles, '/elivepatch/api/v1.0/get_files',
                     endpoint='config',
                     resource_class_kwargs={'cmdline_args': cmdline_args})
    return app


def run():
    cmdline_args = parse_args()
    app = create_app(cmdline_args)
    app.run(debug=cmdline_args.debug,
            host=cmdline_args.host, port=cmdline_args.port,
            threaded=cmdline_args.threaded)


if __name__ == '__main__':
    run()
