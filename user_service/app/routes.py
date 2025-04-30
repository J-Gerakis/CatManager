from fastapi import APIRouter
from user_service.app.services import UserService, UserDTO, UserSearchDTO
router = APIRouter()

user_service = UserService()


@router.get("/users/", tags=["users"])
async def read_users():
  return user_service.get_users()


@router.get("/users/search", tags=["users"])
async def search(search_params: UserSearchDTO):
  #do some value check here in the future
  return user_service.search_user(search_params)


@router.post("/users/new", tags=["users"])
async def create_user(dto: UserDTO):
  user_service.create_user(dto.to_dao())
  return {"message": "User created"}

