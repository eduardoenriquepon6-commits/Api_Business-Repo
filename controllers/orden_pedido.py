import json
from fastapi import HTTPException
from models.orden_pedido import OrdenPedido
from models.stock import Stock
from utils.database import execute_query_json

# ==============================
# ORDEN PEDIDO CRUD
# ==============================

async def get_one(id: int) -> OrdenPedido:
    query = """
        SELECT o.id,
               o.id_usuario,
               u.nombre_completo as usuario_nombre,
               o.fecha_orden,
               o.estado_pago,
               o.metodo_pago
        FROM ventas_directas.Orden_pedido o
        INNER JOIN ventas_directas.usuarios u ON o.id_usuario = u.id
        WHERE o.id = ?;
    """
    try:
        result = await execute_query_json(query, params=[id])
        data = json.loads(result)
        if len(data) == 0:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        return data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_all() -> list[OrdenPedido]:
    query = """
        SELECT o.id,
               o.id_usuario,
               u.nombre_completo as usuario_nombre,
               o.fecha_orden,
               o.estado_pago,
               o.metodo_pago
        FROM ventas_directas.Orden_pedido o
        INNER JOIN ventas_directas.usuarios u ON o.id_usuario = u.id;
    """
    try:
        result = await execute_query_json(query)
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def create_orden(orden: OrdenPedido) -> OrdenPedido:
    insert_query = """
        INSERT INTO ventas_directas.Orden_pedido (id_usuario, estado_pago, metodo_pago)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?);
    """
    params = [orden.id_usuario, orden.estado_pago, orden.metodo_pago]
    try:
        insert_result = await execute_query_json(insert_query, params=params, needs_commit=True)
        inserted_id = json.loads(insert_result)[0]["id"]
        return await get_one(inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_orden(orden: OrdenPedido) -> OrdenPedido:
    fields = orden.model_dump(exclude_none=True)
    keys = [k for k in fields.keys() if k != "id"]
    variables = " = ?, ".join(keys) + " = ?"
    update_query = f"""
        UPDATE ventas_directas.Orden_pedido
        SET {variables}
        WHERE id = ?;
    """
    params = [fields[k] for k in keys] + [orden.id]
    try:
        await execute_query_json(update_query, params=params, needs_commit=True)
        return await get_one(orden.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_orden(id: int) -> str:
    delete_query = "DELETE FROM ventas_directas.Orden_pedido WHERE id = ?;"
    try:
        await execute_query_json(delete_query, params=[id], needs_commit=True)
        return "Orden eliminada"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# ==============================
# DETALLE PEDIDO CRUD
# ==============================

async def get_all_detalle(orden_id: int) -> list[Stock]:
    query = """
        SELECT d.id,
               d.id_orden,
               d.id_producto,
               p.nombre_producto,
               d.cantidad,
               d.precio_unitario,
               d.subtotal
        FROM ventas_directas.Detalle_pedido d
        INNER JOIN ventas_directas.productos p ON d.id_producto = p.id
        WHERE d.id_orden = ?;
    """
    try:
        result = await execute_query_json(query, params=[orden_id])
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_one_detalle(orden_id: int, detalle_id: int) -> Stock:
    query = """
        SELECT d.id,
               d.id_orden,
               d.id_producto,
               p.nombre_producto,
               d.cantidad,
               d.precio_unitario,
               d.subtotal
        FROM ventas_directas.Detalle_pedido d
        INNER JOIN ventas_directas.productos p ON d.id_producto = p.id
        WHERE d.id = ? AND d.id_orden = ?;
    """
    try:
        result = await execute_query_json(query, params=[detalle_id, orden_id])
        data = json.loads(result)
        if len(data) == 0:
            raise HTTPException(status_code=404, detail="Detalle no encontrado")
        return data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def add_detalle(orden_id: int, detalle: Stock) -> Stock:
    # Validar stock
    stock_query = "SELECT cantidad FROM ventas_directas.stock WHERE id_producto = ?;"
    stock_result = await execute_query_json(stock_query, params=[detalle.id_producto])
    stock_data = json.loads(stock_result)
    if len(stock_data) == 0 or stock_data[0]["cantidad"] < detalle.cantidad:
        raise HTTPException(status_code=400, detail="No hay stock suficiente")

    insert_query = """
        INSERT INTO ventas_directas.Detalle_pedido (id_orden, id_producto, cantidad, precio_unitario)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?);
    """
    params = [orden_id, detalle.id_producto, detalle.cantidad, detalle.precio_unitario]
    try:
        insert_result = await execute_query_json(insert_query, params=params, needs_commit=True)
        new_id = json.loads(insert_result)[0]["id"]
        return await get_one_detalle(orden_id, new_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_detalle_info(detalle: Stock, orden_id: int) -> Stock:
    # Obtener detalle actual de la base de datos
    current = await get_one_detalle(orden_id, detalle.id)

    # Usar los valores enviados o mantener los actuales
    cantidad = detalle.cantidad if detalle.cantidad is not None else current["cantidad"]
    precio_unitario = detalle.precio_unitario if detalle.precio_unitario is not None else current["precio_unitario"]
    subtotal = cantidad * precio_unitario  # recalcular subtotal automáticamente

    update_query = """
        UPDATE ventas_directas.Detalle_pedido
        SET cantidad = ?, precio_unitario = ?
        WHERE id = ?;
    """
    params = [cantidad, precio_unitario, detalle.id]

    try:
        await execute_query_json(update_query, params=params, needs_commit=True)
        # devolver el detalle actualizado
        return await get_one_detalle(orden_id, detalle.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def remove_detalle(orden_id: int, detalle_id: int) -> str:
    delete_query = "DELETE FROM ventas_directas.Detalle_pedido WHERE id = ? AND id_orden = ?;"
    try:
        await execute_query_json(delete_query, params=[detalle_id, orden_id], needs_commit=True)
        return "Detalle eliminado"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")