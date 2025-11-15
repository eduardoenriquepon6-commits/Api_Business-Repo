from fastapi import APIRouter, HTTPException, Request
from models.usuarios import Usuarios
from controllers.usuarios import (
    create_user,
    update_user
)

router = APIRouter(prefix = "/usuarios")

@router.post( "/" , tags = ["Usuarios"])
async def create_new_user(usuario_data: Usuarios):
    result = await create_user(usuario_data)
    return result

@router.put("/{id}", tags=["Usuarios"])
async def update_user_information( usuario_data: Usuarios , id: int ):
    usuario_data.id = id
    result = await update_user(usuario_data)
    return result