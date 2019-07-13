from elivepatch_server import create_app
import pytest
from flask_restful import Api as api
from conftest import app
import unittest


class TestIntegrations(unittest.TestCase):
    def cmdline_args(object):
        debug = True
        host = "0.0.0.0"
        port = "5000"
        threaded = True

    def setUp(self):
        cmdline = self.cmdline_args()
        self.app = create_app(cmdline)
        self.app = self.app.test_client()

    def test_not_found(self):
        response = self.app.get("/")
        assert response.status_code == 404

    def test_found(self):
        response = self.app.get("/elivepatch/api/")
        assert response.status_code == 200
