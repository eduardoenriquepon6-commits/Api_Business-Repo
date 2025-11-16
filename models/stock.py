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

    cantidad_disponible: Optional[int] = Field(
        description="Unidades disponibles",
        examples=[100, 250, 500],
        default=0
    )