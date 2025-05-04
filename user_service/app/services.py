from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from pyxtension.streams import stream
from user_service.app.db import engine
from user_service.app.models import User
from pydantic import BaseModel
from typing import Dict


class UserSearchDTO(BaseModel):
  id: Optional[int] = None
  username: Optional[str] = None
  email: Optional[str] = None
  is_active: Optional[str] = "true" #need to convert str to bool
  is_cat: Optional[str] = None


class UserDTO(BaseModel):
  username: str
  email: str
  password: str
  is_active: Optional[bool] = True
  is_cat: bool

  def to_dao(self):
    return User(name=self.username, email=self.email, password_hash=self.password, is_a_cat=self.is_cat)


class UserResponse:
  id: int
  username: str
  email: str
  is_active: bool
  is_a_cat: bool

  def __init__(self, dao: User):
    self.id = dao.id
    self.username = dao.name
    self.email = dao.email
    self.is_active = dao.is_active
    self.is_a_cat = dao.is_a_cat


class UserService:
  def __init__(self):
        session = sessionmaker(bind=engine)
        self.session = session()

  def create_user(self, user: User):
    self.session.add(user)
    self.session.commit()

  def get_users(self):
    users = self.session.query(User).all()
    return stream(users).map(lambda u: UserResponse(u)).to_list()

  def search_user(self, search_params: UserSearchDTO):
    if search_params.id is not None:
      return self.get_user_by_id(search_params.id)

    query = ["select * from users where 1==1 "]
    if search_params.username is not None:
      query.append(" name == :username ")
    if search_params.email is not None:
      query.append(" email == :email ")
    if search_params.is_active is not None:
      query.append(" is_active == :is_active ")

    query_full = "and".join(query)
    params = {"username":search_params.username, "email":search_params.email, "is_active":bool(search_params.is_active)}

    users = self.session.execute(text(query_full), params).fetchall()
    return stream(users).map(lambda u: UserResponse(u)).to_list()


  def get_user_by_id(self, user_id: int):
    user = self.session.query(User).filter(User.id == user_id).first()
    return user

  def get_user_by_name(self, name: str):
    user = self.session.query(User).filter(User.name == name).first()
    return user

