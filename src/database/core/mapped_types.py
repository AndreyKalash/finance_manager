import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import mapped_column

UUID_PK = Annotated[
    uuid.UUID, mapped_column(UUID, primary_key=True, default=uuid.uuid4)
]

CREATED_AT = Annotated[datetime, mapped_column(DateTime, default=datetime.now)]
UPDATED_AT = Annotated[
    datetime, mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
]
