from sqlalchemy.orm import sessionmaker

Session: sessionmaker


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
