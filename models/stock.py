from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Stock(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del registro de stock"
    )

    id_producto: Optional[int] = Field(
        description="ID del producto (FK)",
        default=None
    )

    cantidad: Optional[int] = Field(
        description="Unidades disponibles",
        examples=[3, 250, 500],
        default=None,
        ge=0
    )

    precio_unitario: Optional[float] = Field(
        description="Precio unitario del producto en stock",
        examples=[1200, 700, 900],
        default=None,
        ge=0.0
    )