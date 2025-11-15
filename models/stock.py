from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Stock(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del registro de stock"
    )

    id_productos: int = Field(
        description="ID del producto (FK)"
    )

    cantidad_disponible: Optional[int] = Field(
        description="Unidades disponibles",
        default=0
    )