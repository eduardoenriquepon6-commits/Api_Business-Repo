from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Productos(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del producto"
    )

    nombre_producto: Optional[str] = Field(
        description="Nombre del producto",
        max_length=150,
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9' ()-]+$",
        examples=["Optimus Lima-Limon", "Base de Maquillaje"],
        default = None
    )

    descripcion_producto: Optional[str] = Field(
        description="Descripción del producto",
        max_length=300,
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9.,' ()-]+$",
        examples=["Suplemento vitamínico sabor lima-limón", "Base líquida para maquillaje de larga duración"],
        default=None
    )

    activo: Optional[bool] = Field(
        default=True,
        description="Estado activo",
        examples=[True, False]
    )

    id_categoria: Optional[int] = Field(
        description="ID de categoría (FK)",
        default = None
    )
