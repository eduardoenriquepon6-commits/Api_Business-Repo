import json
import logging

from fastapi import HTTPException

from models.stock import Stock
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_one_stck( id: int ) -> Stock:

    selectscript = """
        SELECT [id]
            ,[id_producto]
            ,[cantidad_disponible]
        FROM [ventas_directas].[stock]
        WHERE id = ?
    """

    params = [id]
    result_dict=[]
    try:
        result = await execute_query_json(selectscript, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail=f"Producto no encontrado")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error en la base de datos: { str(e) }")

async def get_all_stocks() -> list[Stock]:

    selectscript = """
        SELECT [id]
            ,[id_producto]
            ,[cantidad_disponible]
        FROM [ventas_directas].[stock]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")
    
async def create_stock( stock: Stock ) -> Stock:

    sqlscript: str = """
        INSERT INTO [ventas_directas].[stock] ([id_producto], [cantidad_disponible])
        VALUES (?, ?);
    """

    params = [
        stock.id_producto,
        stock.cantidad_disponible
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json( sqlscript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")

    sqlfind: str = """
        SELECT [id]
            ,[id_producto]
            ,[cantidad_disponible]
        FROM [ventas_directas].[stock]
        WHERE id_producto = ?;
    """

    params = [stock.id_producto]

    result_dict=[]
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")

async def update_stock( stock: Stock ) -> Stock:

    dict = stock.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [ventas_directas].[stock]
        SET {variables}
        WHERE [id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( stock.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")
    sqlfind: str = """
        SELECT [id]
            ,[id_producto]
            ,[cantidad_disponible]
        FROM [ventas_directas].[stock]
        WHERE id = ?;
    """

    params = [stock.id]

    result_dict=[]
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")
    
    
async def delete_stock( id: int ) -> str:

    deletescript = """
        DELETE FROM [ventas_directas].[stock]
        WHERE [id] = ?;
    """

    params = [id];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")