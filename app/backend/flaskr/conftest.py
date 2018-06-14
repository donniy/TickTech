import os
import pytest
import tempfile
from flaskr import create_app
from flaskr.database import get_db, init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    print("db_path: {}".format(db_path))
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path + '.db',
    })

    db = get_db()
    # Create database and load test data
    # Create a new session for every test.
    with app.app_context():
        init_db()
        yield app
        db.session.remove()
        db.drop_all()

    # Close the db data.
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()
