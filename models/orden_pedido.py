from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re
from datetime import datetime

class OrdenPedido(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID de la orden"
    )

    id_usuarios: int = Field(
        description="ID del usuario (FK)"
    )

    fecha_orden: Optional[datetime] = Field(
        default=None,
        description="Fecha de la orden"
    )

    total: float = Field(
        description="Total de la orden"
    )

    estado_pago: Optional[str] = Field(
        default="Pendiente",
        description="Estado del pago",
        max_length=50,
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$"
    )

    metodo_pago: Optional[str] = Field(
        default=None,
        description="Método de pago",
        max_length=50,
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+$"
    )