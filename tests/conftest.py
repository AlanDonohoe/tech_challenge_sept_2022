import pytest

from app.main import flask_app as fa


@pytest.fixture()
def app():
    fa.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup goes here

    yield fa

    # clean up goes here


@pytest.fixture()
def flask_client(app):
    return app.test_client()
