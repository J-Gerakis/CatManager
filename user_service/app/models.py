from sqlalchemy import Column, Integer, String, Boolean
from user_service.app.db import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_a_cat = Column(Boolean, nullable=False)


Base.metadata.create_all(engine)