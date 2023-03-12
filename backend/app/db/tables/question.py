from __future__ import annotations

import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.connection import Base


class Question(Base):
    __tablename__ = "question"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    test_guid = Column(UUID(as_uuid=True), ForeignKey("test.guid"), index=True)
    test = relationship("Test", back_populates="questions", lazy="joined", uselist=False)

    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    answers = relationship("Answer", back_populates="question", lazy="joined")

    is_deleted = Column(Integer, default=0)

    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_by = Column(UUID(as_uuid=True), nullable=False)
