from fastapi import APIRouter, HTTPException, Request, status
from models.categoria import Categoria
from controllers.categoria import (
    create_category,
    get_all_ctg,
    get_one_ctg,
    update_ctg
)

router = APIRouter(prefix = "/categorias")

@router.get( "/" , tags=["Categorias"], status_code=status.HTTP_200_OK)
async def get_all_categories():
    result = await get_all_ctg()
    return result

@router.get("/{id}", tags=["Categorias"], status_code=status.HTTP_200_OK)
async def get_one_category( id: int ):
    result: Categoria =  await get_one_ctg(id)
    return result

@router.post( "/" , tags = ["Categorias"], status_code=status.HTTP_201_CREATED)
async def create_new_category(categoria_data: Categoria):
    result = await create_category(categoria_data)
    return result

@router.put("/{id}", tags=["Categorias"], status_code=status.HTTP_201_CREATED)
async def update_category_information( categoria_data: Categoria , id: int ):
    categoria_data.id = id
    result = await update_ctg(categoria_data)
    return result