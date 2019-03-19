from factory import create_app
import pytest
from extensions import db


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_schema()

    # Insert user data
    # user1 = User(email='patkennedy79@gmail.com', plaintext_password='FlaskIsAwesome')
    # user2 = User(email='kennedyfamilyrecipes@gmail.com', plaintext_password='PaSsWoRd')
    # db.session.add(user1)
    # db.session.add(user2)

    # Commit the changes for the users
    # db.session.commit()

    yield db  # this is where the testing happens!

    db.drop_all()
