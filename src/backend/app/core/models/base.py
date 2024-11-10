from pydantic import ConfigDict
from sqlmodel import SQLModel, Field

class Base(SQLModel):
    __abstract__ = True  # Ensures SQLModel doesn't create a table for this base class

    # Apply the metadata convention for SQLModel if required
    metadata = SQLModel.metadata
