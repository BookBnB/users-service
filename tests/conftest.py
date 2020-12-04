import pytest
from flask_migrate import upgrade
from testing.postgresql import PostgresqlFactory

from project import create_app
from flask_migrate import upgrade, downgrade
from project.db import db
from testing.postgresql import PostgresqlFactory

Postgresql = PostgresqlFactory(cache_initialized_db=True)

@pytest.fixture
def app():
    postgresql = Postgresql()

    app = create_app({
        "DATABASE_URL": postgresql.url(),
        "SQLALCHEMY_DATABASE_URI": postgresql.url(),
        "SECRET_KEY": "test_key"
    })

    with app.app_context():
        upgrade()

    yield app

    postgresql.stop()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def pytest_sessionfinish(session, exitstatus):
    Postgresql.clear_cache()
