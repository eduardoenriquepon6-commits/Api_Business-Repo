import uvicorn 
from typing import Union
from fastapi import FastAPI
from utils.database import execute_query_json
import json

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Customer!"}

@app.get("/users")
async def get_all_users():
    sqlscript = """
        SELECT [id]
            ,[nombre_completo]
            ,[telefono]
            ,[correo]
            ,[fecha_registro]
        FROM [ventas_directas].[usuarios]
    """
    result = await execute_query_json(sqlscript)
    result_dict = json.loads(result)

    return result_dict

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")