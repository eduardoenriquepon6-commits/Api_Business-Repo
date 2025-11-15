from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class DetallePedido(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del detalle"
    )

    id_orden: int = Field(
        description="ID de la orden (FK)"
    )

    id_productos: int = Field(
        description="ID del producto (FK)"
    )

    cantidad: int = Field(
        description="Cantidad de productos comprados"
    )

    precio_unitario: float = Field(
        description="Precio unitario"
    )

    subtotal: Optional[float] = Field(
        description="Subtotal calculado automáticamente",
        default=None
    )
