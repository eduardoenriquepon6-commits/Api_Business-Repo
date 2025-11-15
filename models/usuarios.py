# models se definen las clases que están alineadas a las traducciones del modelo de datos

from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re
from datetime import datetime

class Usuarios(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID autoincrementable"
    )

    nombre_completo: str = Field(
        description="Nombre completo del Usuario",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Eduardo Enrique Ponce Palma"],
        default=None
    )

    telefono: Optional[str] = Field(
        description="Telefono del Usuario",
        pattern=r"^[0-9 +()-]{7,20}$",
        examples=["98765432"],
        default=None
    )

    correo: Optional[str] = Field(
        description="Correo electrónico del usuario",
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["eduardo@example.com"],
        default=None
    )

    fecha_registro: Optional[datetime] = Field(
        default=None,
        description="Fecha de registro generada automáticamente"
    )