from pydantic import BaseModel, Field
from typing import Optional


class Producto(BaseModel):
    id: Optional[str] = None
    nombre: str = Field(..., min_length=2)
    descripcion: str
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: str