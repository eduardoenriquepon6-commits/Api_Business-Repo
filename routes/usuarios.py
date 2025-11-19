from fastapi import APIRouter, HTTPException, Request, status
from models.usuarios import Usuarios
from controllers.usuarios import (
    create_user,
    update_user,
    get_all_u,
    get_one_u,
    delete_user
)

router = APIRouter(prefix = "/usuarios")

@router.get( "/" , tags=["Usuarios"], status_code=status.HTTP_200_OK)
async def get_all_users():
    result = await get_all_u()
    return result

@router.get("/{id}", tags=["Usuarios"], status_code=status.HTTP_200_OK)
async def get_one_user( id: int ):
    result: Usuarios =  await get_one_u(id)
    return result

@router.post( "/" , tags = ["Usuarios"], status_code=status.HTTP_201_CREATED)
async def create_new_user(usuario_data: Usuarios):
    result = await create_user(usuario_data)
    return result

@router.put("/{id}", tags=["Usuarios"], status_code=status.HTTP_201_CREATED)
async def update_user_information( usuario_data: Usuarios , id: int ):
    usuario_data.id = id
    result = await update_user(usuario_data)
    return result

@router.delete("/{id}", tags=["Usuarios"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user( id: int ):
    status: str =  await delete_user(id)
    return status