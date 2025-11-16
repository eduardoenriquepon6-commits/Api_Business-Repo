import json
import logging

from fastapi import HTTPException

from models.categoria import Categoria
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_one_ctg( id: int ) -> Categoria:

    selectscript = """
        SELECT [id]
            ,[nombre_categoria]
        FROM [ventas_directas].[categorias]
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
            raise HTTPException(status_code=404, detail=f"categoria no encontrada")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error en la base de datos: { str(e) }")

async def get_all_ctg() -> list[Categoria]:

    selectscript = """
        SELECT [id]
            ,[nombre_categoria]
        FROM [ventas_directas].[categorias]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")

async def create_category( categoria: Categoria ) -> Categoria:

    sqlscript: str = """
        INSERT INTO [ventas_directas].[categorias] ([nombre_categoria])
        VALUES (?);
    """

    params = [
        categoria.nombre_categoria
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json( sqlscript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")

    sqlfind: str = """
        SELECT [id]
            ,[nombre_categoria]
        FROM [ventas_directas].[categorias]
        WHERE nombre_categoria = ?;
    """

    params = [categoria.nombre_categoria]

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
    
async def update_ctg( categoria: Categoria ) -> Categoria:

    dict = categoria.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [ventas_directas].[categorias]
        SET {variables}
        WHERE [id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( categoria.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")
    sqlfind: str = """
        SELECT [id]
            ,[nombre_categoria]
        FROM [ventas_directas].[categorias]
        WHERE id = ?;
    """

    params = [categoria.id]

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