from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

from .database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    requirements = Column(String, nullable=False)
    link = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('unis.id', ondelete="CASCADE"), nullable=False)

    owner = relationship("Uni")


class Uni(Base):
    __tablename__ = "unis"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    img = Column(String, nullable=False)
    color = Column(String, nullable=False, server_default=text('white'))
    text_color = Column(String, nullable=False, server_default=text('black'))
    nickname = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    password = Column(String(), nullable=False)





