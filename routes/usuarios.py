from fastapi import APIRouter, HTTPException, Request
from models.usuarios import Usuarios
from controllers.usuarios import (
    create_user
)

router = APIRouter(prefix = "/usuarios")

@router.post( "/" , tags = ["Usuarios"])
async def create_new_user(usuario_data: Usuarios):
    result = await create_user(usuario_data)
    return result