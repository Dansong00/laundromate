from app.core.models import Base
from app.core.database.session import engine

# Import models to register them with SQLAlchemy's Base metadata
from app.core.models.user import User  # noqa: F401


def create_all_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_all_tables()
