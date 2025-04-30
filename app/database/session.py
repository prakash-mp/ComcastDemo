from typing import Any, Generator, Tuple

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.dependencies.config import settings

SQLALCHEMY_DATABASE_URL = (
    # f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_SERVER}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# MYSQL Series
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def generate_sa_model_attrs(
    model: "Base",
) -> Generator[Tuple[str, Any], None, None]:
    """
    Generate key value pairs for all non-internal SQLAlchemy attributes on a Base class.

    Args:
        model: the SQLAlchemy model

    Yields:
        A key value pair for each attribute on the model
    """
    excluded_attrs = ("_sa_class_manager", "_sa_instance_state", "_sa_registry")

    for key, value in vars(model).items():
        # Filter private and SQLAlchemy related attributes
        if not key.startswith("_") and not any(
            hasattr(value, attr) for attr in excluded_attrs
        ):
            yield key, value


class BaseWithRepresentation:
    """
    Base class for the SQLAlchemy declarative base that defines a string representation.
    """

    def __repr__(self) -> str:
        attributes = ", ".join(
            (f"{key}={value}" for key, value in generate_sa_model_attrs(self))
        )
        return f"{self.__class__.__name__}({attributes})"


Base = declarative_base(cls=BaseWithRepresentation)
