from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from user_service.app.db import engine
from user_service.app.models import User
from pydantic import BaseModel


class UserSearchDTO(BaseModel):
  id: Optional[int]
  username: Optional[str] = None
  email: Optional[str] = None
  is_active: Optional[bool] = True #need to convert str to bool
  is_cat: Optional[bool] = None

class UserDTO(BaseModel):
  username: str
  email: str
  password: str
  is_cat: bool

  def to_dao(self):
    return User(name=self.username, email=self.email, password_hash=self.password, is_a_cat=self.is_cat)


class UserService:
  def __init__(self):
        session = sessionmaker(bind=engine)
        self.session = session()

  def create_user(self, user: User):
    self.session.add(user)
    self.session.commit()

  def get_users(self):
    users = self.session.query(User).all()
    return users

  def search_user(self, search_params: UserSearchDTO):
    if search_params.id is not None:
      return self.get_user_by_id(search_params.id)

    if search_params.username is None:
      search_params.username = "*"
    if search_params.email is None:
      search_params.email = "*"
    if search_params.is_active is None:
      search_params.is_active = True

    query = text("select * from users where username = :username and "
             "email = :email and is_active = :is_active")
    params = {"username":search_params.username, "email":search_params.email, "is_active":search_params.is_active}

    users = self.session.execute(query, params).fetchall()
    return users


  def get_user_by_id(self, user_id: int):
    user = self.session.query(User).filter(User.id == user_id).first()
    return user

  def get_user_by_name(self, name: str):
    user = self.session.query(User).filter(User.name == name).first()
    return user

