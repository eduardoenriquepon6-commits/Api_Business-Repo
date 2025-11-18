import json
import logging

from fastapi import HTTPException

from models.productos import Productos
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_one_p( id: int ) -> Productos:

    selectscript = """
        SELECT [id]
            ,[nombre_producto]
            ,[descripcion_producto]
            ,[activo]
            ,[id_categoria]
        FROM [ventas_directas].[productos]
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
            raise HTTPException(status_code=404, detail=f"producto no encontrado")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error en la base de datos: { str(e) }")


async def get_all_p() -> list[Productos]:

    selectscript = """
        SELECT [id]
            ,[nombre_producto]
            ,[descripcion_producto]
            ,[activo]
            ,[id_categoria]
        FROM [ventas_directas].[productos]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")

async def create_product( producto: Productos ) -> Productos:

    sqlscript: str = """
        INSERT INTO [ventas_directas].[productos] ([nombre_producto], [descripcion_producto], [activo], [id_categoria])
        VALUES (?, ?, ?, ?);
    """

    params = [
        producto.nombre_producto
        , producto.descripcion_producto
        , producto.activo
        , producto.id_categoria
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json( sqlscript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")

    sqlfind: str = """
        SELECT [id]
            ,[nombre_producto]
            ,[descripcion_producto]
            ,[activo]
            ,[id_categoria]
        FROM [ventas_directas].[productos]
        WHERE nombre_producto = ?;
    """

    params = [producto.nombre_producto]

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
    
async def update_product( producto: Productos ) -> Productos:

    dict = producto.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [ventas_directas].[productos]
        SET {variables}
        WHERE [id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( producto.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")
    sqlfind: str = """
        SELECT [id]
            ,[nombre_producto]
            ,[descripcion_producto]
            ,[activo]
            ,[id_categoria]
        FROM [ventas_directas].[productos]
        WHERE id = ?;
    """

    params = [producto.id]

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
    
async def delete_product( id: int ) -> str:

    deletescript = """
        DELETE FROM [ventas_directas].[productos]
        WHERE [id] = ?;
    """

    params = [id];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")