from pydantic import BaseModel, Field
from typing import List, Optional


class ProductoPedido(BaseModel):
    producto_id: str
    cantidad: int = Field(..., gt=0)


class Pedido(BaseModel):
    id: Optional[str] = None
    cliente: str
    productos: List[ProductoPedido]
    total: float = Field(..., gt=0)
    estado: str = "pendiente"