#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) 2017, Alice Ferrazzi <alice.ferrazzi@gmail.com>
# Distributed under the terms of the GNU General Public License v2 or later

from flask_restful import Resource, reqparse, fields, marshal

agent_fields = {
    'module': fields.String,
    'version': fields.String,
}


def agentinfo(module=None):
    """
    :rtype: object
    """
    agents = []
    agent = {
        'id': 1,
        'module': 'elivepatch',
        'version' : '0.01',
    }
    agents.append(agent)
    return agents

agents = agentinfo()


class AgentAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('module', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('version', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        super(AgentAPI, self).__init__()

    def get(self):
        return {'agent': [marshal(host, agent_fields) for host in agents]}

    def post(self):
        args = self.reqparse.parse_args()
        host = {
            'id': agents[-1]['id'] + 1,
            'module': args['module'],
            'version': args['version'],
        }
        agents.append(host)
        return {'agent': marshal(host, agent_fields)}, 201
