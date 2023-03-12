from __future__ import annotations

import uuid
from copy import deepcopy
from typing import Any, Dict

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.connection import Base


class Answer(Base):
    __tablename__ = "answer"

    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True, unique=True)
    question_guid = Column(UUID(as_uuid=True), ForeignKey("question.guid"), index=True)
    question = relationship("Question", back_populates="answers", lazy="joined", uselist=False)

    text = Column(String, nullable=False)
    sub_text = Column(String, nullable=True)
    is_correct = Column(Integer, nullable=False)

    is_deleted = Column(Integer, default=0)

    created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    updated_by = Column(UUID(as_uuid=True), nullable=False)

    @property
    def to_api_dict(self) -> Dict[str, Any]:
        api_dict = deepcopy(self.__dict__)

        api_dict.pop('guid')
        api_dict.pop('is_deleted')

        api_dict['id'] = str(self.guid)

        return api_dict
