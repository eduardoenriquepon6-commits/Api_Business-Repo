from fastapi import APIRouter, HTTPException, Request, status
from models.Detalle_pedido import DetallePedido

router = APIRouter(prefix = "/detalle_pedido")
