from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Categoria(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID de categoría"
    )

    nombre_categoria: str = Field(
        description="Nombre de la categoría",
        max_length=100,
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Suplementos", "Maquillaje", "Cosmeticos"]
    )