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

    # Create database and load test data
    with app.app_context():
        init_db()
        #get_db().executescript(_data_sql)
    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()
