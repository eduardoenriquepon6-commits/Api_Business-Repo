import uvicorn 
from fastapi import FastAPI
from routes.usuarios import router as router_usuarios
from routes.categoria import router as router_categoria
from routes.productos import router as router_productos
from routes.stock import router as router_stock
from routes.detalle_pedido import router as router_detalle_pedido
from routes.orden_pedido import router as router_orden_pedido

app = FastAPI()

app.include_router(router_usuarios)

app.include_router(router_categoria)

app.include_router(router_productos)

app.include_router(router_stock)

app.include_router(router_detalle_pedido)

app.include_router(router_orden_pedido)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")