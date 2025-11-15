# En controllers manejamos la lógica de negocio, como vamos a recibir las entradas y como vamos a interactuar con nuestro modelo de datos

import json
import logging

from fastapi import HTTPException
from models.usuarios import Usuarios
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_user(usuario: Usuarios) -> Usuarios:

    sqlscript = """
        INSERT INTO [ventas_directas].[usuarios] ([nombre_completo], [telefono], [correo])
        VALUES (?, ?, ?);
    """

    params = [
        usuario.nombre_completo,
        usuario.telefono,
        usuario.correo
    ]

    insert_result = None

    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit = True) # Los inserts, updates y deletes necesitan commit, los selects no
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    
    sqlfind: str = """
        SELECT [id]
            ,[nombre_completo]
            ,[telefono]
            ,[correo]
            ,[fecha_registro]
        FROM [ventas_directas].[usuarios]
        WHERE correo = ?;
    """

    params = [Usuarios.correo]

    result_dict = []

    try:
        result = await execute_query_json(sqlfind, params = params)
        result_dict = json.loads(result)

        if len(result_dict) > 0:
            return result_dict[0]
        else: 
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    