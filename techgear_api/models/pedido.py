from typing import List, Optional

from pydantic import BaseModel, Field


class ProductoPedido(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0)


class ClientePedido(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    identificacion: str = Field(..., min_length=5, max_length=30)
    telefono: str = Field(..., min_length=7, max_length=20)


class Pedido(BaseModel):
    id: Optional[str] = None
    cliente: ClientePedido
    productos: List[ProductoPedido]
    total: float = Field(..., gt=0)
    estado: str = "pendiente"