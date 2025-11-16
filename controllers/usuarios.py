# En controllers manejamos la lógica de negocio, como vamos a recibir las entradas y como vamos a interactuar con nuestro modelo de datos

import json
import logging

from fastapi import HTTPException
from models.usuarios import Usuarios
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def delete_user( id: int ) -> str:

    deletescript = """
        DELETE FROM [ventas_directas].[usuarios]
        WHERE [id] = ?;
    """

    params = [id];

    try:
        await execute_query_json(deletescript, params=params, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

async def get_one_u( id: int ) -> Usuarios:

    selectscript = """
        SELECT [id]
            ,[nombre_completo]
            ,[telefono]
            ,[correo]
            ,[fecha_registro]
        FROM [ventas_directas].[usuarios]
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
            raise HTTPException(status_code=404, detail=f"usuario no encontrado")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error en la base de datos: { str(e) }")

async def get_all_u() -> list[Usuarios]:

    selectscript = """
        SELECT [id]
            ,[nombre_completo]
            ,[telefono]
            ,[correo]
            ,[fecha_registro]
        FROM [ventas_directas].[usuarios]
    """

    result_dict=[]
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")

async def create_user( usuario: Usuarios ) -> Usuarios:

    sqlscript: str = """
        INSERT INTO [ventas_directas].[usuarios] ([nombre_completo], [telefono], [correo])
        VALUES (?, ?, ?);
    """

    params = [
        usuario.nombre_completo
        , usuario.telefono
        , usuario.correo
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json( sqlscript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")

    sqlfind: str = """
        SELECT [id]
            ,[nombre_completo]
            ,[telefono]
            ,[correo]
            ,[fecha_registro]
        FROM [ventas_directas].[usuarios]
        WHERE correo = ?;
    """

    params = [usuario.correo]

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

async def update_user( usuario: Usuarios ) -> Usuarios:

    dict = usuario.model_dump(exclude_none=True)

    keys = [ k for k in  dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [ventas_directas].[usuarios]
        SET {variables}
        WHERE [id] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( usuario.id )

    update_result = None
    try:
        update_result = await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: { str(e) }")
    sqlfind: str = """
        SELECT [id]
            ,[nombre_completo]
            ,[telefono]
            ,[correo]
            ,[fecha_registro]
        FROM [ventas_directas].[usuarios]
        WHERE id = ?;
    """

    params = [usuario.id]

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

