import uvicorn 
from fastapi import FastAPI
from routes.usuarios import router as router_usuarios
from routes.categoria import router as router_categoria
from routes.productos import router as router_productos

app = FastAPI()

app.include_router(router_usuarios)

app.include_router(router_categoria)

app.include_router(router_productos)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")