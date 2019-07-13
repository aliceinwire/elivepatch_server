import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from elivepatch_server import create_app
import pytest
from flask_restful import Api as api
from flask_testing import TestCase


@pytest.fixture
def app():
    app = create_app("testing")
    return app
