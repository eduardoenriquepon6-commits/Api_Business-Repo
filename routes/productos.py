from fastapi import APIRouter, HTTPException, Request, status
from models.productos import Productos
from controllers.productos import (
    create_product,
    get_all_p,
    get_one_p,
    delete_product,
    update_product,
)

router = APIRouter(prefix = "/productos")

@router.get( "/" , tags=["Productos"])
async def get_all_products():
    result = await get_all_p()
    return result

@router.get("/{id}", tags=["Productos"])
async def get_one_product( id: int ):
    result: Productos = await get_one_p(id)
    return result

@router.post( "/" , tags = ["Productos"])
async def create_new_product(producto_data: Productos):
    result = await create_product(producto_data)
    return result

@router.put("/{id}", tags=["Productos"])
async def update_product_information( producto_data: Productos , id: int ):
    producto_data.id = id
    result = await update_product(producto_data)
    return result

@router.delete("/{id}", tags=["Productos"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_product( id: int ):
    status: str =  await delete_product(id)
    return status
