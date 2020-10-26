import os
import pytest
import tempfile

from project import create_app
from flask_migrate import upgrade


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""

    db_fd, db_path = tempfile.mkstemp()

    # create the app with common test config
    app = create_app({
		"SQLALCHEMY_DATABASE_URI": "sqlite:///%s" % db_path,
		"SECRET_KEY": "test_key"
    })

    with app.app_context():
        upgrade()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
