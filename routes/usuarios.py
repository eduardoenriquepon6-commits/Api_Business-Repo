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

@router.get( "/" , tags=["Usuarios"])
async def get_all_users():
    result = await get_all_u()
    return result

@router.get("/{id}", tags=["Usuarios"])
async def get_one_user( id: int ):
    result: Usuarios =  await get_one_u(id)
    return result

@router.post( "/" , tags = ["Usuarios"])
async def create_new_user(usuario_data: Usuarios):
    result = await create_user(usuario_data)
    return result

@router.put("/{id}", tags=["Usuarios"])
async def update_user_information( usuario_data: Usuarios , id: int ):
    usuario_data.id = id
    result = await update_user(usuario_data)
    return result

@router.delete("/{id}", tags=["Usuarios"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_content( id: int ):
    status: str =  await delete_user(id)
    return status