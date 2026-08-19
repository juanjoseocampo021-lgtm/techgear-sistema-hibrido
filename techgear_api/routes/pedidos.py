from fastapi import APIRouter, HTTPException
from bson import ObjectId

from techgear_api.database import pedidos_collection, productos_collection
from techgear_api.models.pedido import Pedido


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


# ---------------------------------------------------------
# GET - Obtener todos los pedidos
# ---------------------------------------------------------
@router.get("/")
async def obtener_pedidos():

    pedidos = []

    async for pedido in pedidos_collection.find():

        pedido["id"] = str(pedido["_id"])
        del pedido["_id"]

        pedidos.append(pedido)

    return pedidos


# ---------------------------------------------------------
# GET - Obtener pedido por ID
# ---------------------------------------------------------
@router.get("/{pedido_id}")
async def obtener_pedido(pedido_id: str):

    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(
            status_code=400,
            detail="ID de pedido no válido"
        )

    pedido = await pedidos_collection.find_one(
        {"_id": ObjectId(pedido_id)}
    )

    if pedido is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    pedido["id"] = str(pedido["_id"])
    del pedido["_id"]

    return pedido


# ---------------------------------------------------------
# POST - Crear pedido
# ---------------------------------------------------------
@router.post("/")
async def crear_pedido(pedido: Pedido):

    pedido_dict = pedido.model_dump(exclude={"id"})

    # Validar que los productos existan
    for producto in pedido_dict["productos"]:

        producto_id = producto["producto_id"]

        # Validar formato del ID
        if not ObjectId.is_valid(producto_id):
            raise HTTPException(
                status_code=400,
                detail=f"ID de producto no válido: {producto_id}"
            )

        # Buscar producto en MongoDB
        producto_existente = await productos_collection.find_one(
            {"_id": ObjectId(producto_id)}
        )

        if producto_existente is None:
            raise HTTPException(
                status_code=404,
                detail=f"Producto no encontrado: {producto_id}"
            )

    # Guardar pedido
    resultado = await pedidos_collection.insert_one(pedido_dict)

    # Recuperar pedido creado
    pedido_creado = await pedidos_collection.find_one(
        {"_id": resultado.inserted_id}
    )

    if pedido_creado is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudo recuperar el pedido creado"
        )

    # Convertir ObjectId a string
    pedido_creado["id"] = str(pedido_creado["_id"])
    del pedido_creado["_id"]

    return pedido_creado