import pytest
from flask_migrate import downgrade, upgrade
from project import create_app
from project.infra.tokenizer import Tokenizer
from testing.postgresql import PostgresqlFactory

Postgresql = PostgresqlFactory(cache_initialized_db=True)

@pytest.fixture
def app():
    postgresql = Postgresql()

    app = create_app({
        "DATABASE_URL": postgresql.url(),
        "SQLALCHEMY_DATABASE_URI": postgresql.url(),
        "SECRET_KEY": "test_key",
        "REQUIRE_API_KEY": False
    })

    with app.app_context():
        upgrade()

    yield app

    postgresql.stop()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def tokenizer(app):
    return Tokenizer(app.config['SECRET_KEY'])

def pytest_sessionfinish(session, exitstatus):
    Postgresql.clear_cache()
