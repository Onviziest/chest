import pytest

from app.models import Model
from app import configured_app


@pytest.fixture(scope='session')
def client():
    app = configured_app()
    app.debug = True
    context = app.app_context()
    context.push()

    testing_client = app.test_client()
    yield testing_client

    context.pop()


@pytest.fixture(scope='session', autouse=True)
def register_db_session():
    app = configured_app()
    app.debug = True
    context = app.app_context()
    context.push()

    Model.register_session()
    yield

    context.pop()
