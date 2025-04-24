import pytest
from app import create_app
from app.models import Base, engine, db_session
from sqlalchemy.orm import close_all_sessions

@pytest.fixture(scope="function")
def test_client():
    app = create_app(testing=True)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    with app.test_client() as client:
        yield client

    # Cleanup
    db_session.remove()
    close_all_sessions()
    Base.metadata.drop_all(bind=engine)
