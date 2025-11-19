from fastapi import APIRouter, status
from models.orden_pedido import OrdenPedido
from models.stock import Stock
from controllers.orden_pedido import (
    get_one as get_one_orden,
    get_all as get_all_ordenes,
    create_orden,
    update_orden,
    delete_orden,
    get_all_detalle,
    get_one_detalle,
    add_detalle,
    update_detalle_info,
    remove_detalle
)

router = APIRouter(prefix="/orden_pedido")

# ==============================
# ORDEN PEDIDO CRUD
# ==============================

@router.get("/", tags=["OrdenPedido"], status_code=status.HTTP_200_OK)
async def list_orders():
    result = await get_all_ordenes()
    return result

@router.get("/{id}", tags=["OrdenPedido"], status_code=status.HTTP_200_OK)
async def obtain_order(id: int):
    orden: OrdenPedido = await get_one_orden(id)
    return orden

@router.post("/", tags=["OrdenPedido"], status_code=status.HTTP_201_CREATED)
async def create_new_order(orden_data: OrdenPedido):
    result = await create_orden(orden_data)
    return result

@router.put("/{id}", tags=["OrdenPedido"], status_code=status.HTTP_201_CREATED)
async def update_order(id: int, orden_data: OrdenPedido):
    orden_data.id = id
    result = await update_orden(orden_data)
    return result

@router.delete("/{id}", tags=["OrdenPedido"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(id: int):
    result: str = await delete_orden(id)
    return result

# ==============================
# DETALLE PEDIDO CRUD (relación con productos)
# ==============================

@router.get("/{id}/detalle", tags=["DetallePedido"], status_code=status.HTTP_200_OK)
async def get_order_details(id: int):
    result = await get_all_detalle(id)
    return result

@router.get("/{id}/detalle/{detalle_id}", tags=["DetallePedido"], status_code=status.HTTP_200_OK)
async def get_one_detail(id: int, detalle_id: int):
    result = await get_one_detalle(id, detalle_id)
    return result

@router.post("/{id}/detalle", tags=["DetallePedido"], status_code=status.HTTP_201_CREATED)
async def add_order_detail(id: int, detalle_data: Stock):
    # detalle_data.id_producto → FK con productos
    result = await add_detalle(id, detalle_data)
    return result

@router.put("/{id}/detalle/{detalle_id}", tags=["DetallePedido"], status_code=status.HTTP_201_CREATED)
async def update_order_detail(id: int, detalle_id: int, detalle_data: Stock):
    detalle_data.id = detalle_id
    result = await update_detalle_info(detalle_data, orden_id=id)
    return result

@router.delete("/{id}/detalle/{detalle_id}", tags=["DetallePedido"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_detail(id: int, detalle_id: int):
    result: str = await remove_detalle(id, detalle_id)
    return result