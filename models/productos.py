from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Productos(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del producto"
    )

    nombre_producto: str = Field(
        description="Nombre del producto",
        max_length=150,
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9' ()-]+$"
    )

    descripcion_producto: Optional[str] = Field(
        description="Descripción del producto",
        max_length=300,
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9.,' ()-]+$",
        default=None
    )

    precio_unitario: float = Field(
        description="Precio unitario del producto"
    )

    activo: Optional[bool] = Field(
        default=True,
        description="Estado activo"
    )

    id_categoria: int = Field(
        description="ID de categoría (FK)"
    )
