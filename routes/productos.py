from fastapi import APIRouter, HTTPException, Request, status
from models.productos import Productos
from controllers.productos import (
    create_product,
)

router = APIRouter(prefix = "/productos")

@router.post( "/" , tags = ["Productos"])
async def create_new_product(producto_data: Productos):
    result = await create_product(producto_data)
    return result