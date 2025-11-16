import json
import logging

from fastapi import HTTPException

from models.productos import Productos
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_product( producto: Productos ) -> Productos:

    sqlscript: str = """
        INSERT INTO [ventas_directas].[productos] ([nombre_producto], [descripcion_producto], [precio_unitario], [activo])
        VALUES (?, ?, ?, ?);
    """

    params = [
        producto.nombre_producto
        , producto.descripcion_producto
        , producto.precio_unitario
        , producto.activo
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
            ,[precio_unitario]
            ,[activo]
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