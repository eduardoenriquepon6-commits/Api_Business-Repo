from fastapi import APIRouter, HTTPException, Request, status
from models.stock import Stock
from controllers.stock import (
    get_all_stocks,
    get_one_stck,
    create_stock,
    delete_stock,
    update_stock
)

router = APIRouter(prefix = "/stock")

@router.get( "/" , tags=["Stock"], status_code=status.HTTP_200_OK)
async def get_products_stock():
    result = await get_all_stocks()
    return result

@router.get("/{id}", tags=["Stock"], status_code=status.HTTP_200_OK)
async def get_one_stock( id: int ):
    result: Stock =  await get_one_stck(id)
    return result

@router.post( "/" , tags = ["Stock"], status_code=status.HTTP_201_CREATED)
async def create_new_stock(stock_data: Stock):
    result = await create_stock(stock_data)
    return result

@router.put("/{id}", tags=["Stock"], status_code=status.HTTP_200_OK)
async def update_stock_information( stock_data: Stock , id: int ):
    stock_data.id = id
    result = await update_stock(stock_data)
    return result

@router.delete("/{id}", tags=["Stock"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_stock( id: int ):
    status: str =  await delete_stock(id)
    return status