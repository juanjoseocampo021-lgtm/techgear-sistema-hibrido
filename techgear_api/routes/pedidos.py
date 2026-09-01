from fastapi import APIRouter, HTTPException
from bson import ObjectId

from techgear_api.database import pedidos_collection, productos_collection
from techgear_api.models.pedido import Pedido, PedidoActualizacion


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

    # -----------------------------------------------------
    # Validar productos y stock
    # -----------------------------------------------------
    for producto in pedido_dict["productos"]:

        producto_id = producto["producto_id"]
        cantidad = producto["cantidad"]

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

        # Validar stock disponible
        stock_actual = producto_existente.get("stock", 0)

        if cantidad > stock_actual:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Stock insuficiente para el producto "
                    f"'{producto_existente.get('nombre', producto_id)}'. "
                    f"Stock disponible: {stock_actual}"
                )
            )

    # -----------------------------------------------------
    # Descontar stock
    # -----------------------------------------------------
    for producto in pedido_dict["productos"]:

        producto_id = producto["producto_id"]
        cantidad = producto["cantidad"]

        resultado_stock = await productos_collection.update_one(
            {
                "_id": ObjectId(producto_id),
                "stock": {"$gte": cantidad}
            },
            {
                "$inc": {
                    "stock": -cantidad
                }
            }
        )

        if resultado_stock.modified_count == 0:
            raise HTTPException(
                status_code=400,
                detail=(
                    "No fue posible actualizar el stock. "
                    "Es posible que el stock haya cambiado."
                )
            )

    # -----------------------------------------------------
    # Guardar pedido
    # -----------------------------------------------------
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


# ---------------------------------------------------------
# PATCH - Actualizar estado del pedido
# ---------------------------------------------------------
@router.patch("/{pedido_id}")
async def actualizar_pedido(
    pedido_id: str,
    actualizacion: PedidoActualizacion
):

    # Validar ID
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(
            status_code=400,
            detail="ID de pedido no válido"
        )

    # Verificar que exista el pedido
    pedido_existente = await pedidos_collection.find_one(
        {"_id": ObjectId(pedido_id)}
    )

    if pedido_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    # Actualizar solamente el estado
    resultado = await pedidos_collection.update_one(
        {"_id": ObjectId(pedido_id)},
        {
            "$set": {
                "estado": actualizacion.estado
            }
        }
    )

    if resultado.modified_count == 0:
        raise HTTPException(
            status_code=400,
            detail="No fue posible actualizar el pedido"
        )

    # Recuperar pedido actualizado
    pedido_actualizado = await pedidos_collection.find_one(
        {"_id": ObjectId(pedido_id)}
    )

    pedido_actualizado["id"] = str(pedido_actualizado["_id"])
    del pedido_actualizado["_id"]

    return pedido_actualizado


# ---------------------------------------------------------
# DELETE - Eliminar pedido
# ---------------------------------------------------------
@router.delete("/{pedido_id}")
async def eliminar_pedido(pedido_id: str):

    # Validar ID
    if not ObjectId.is_valid(pedido_id):
        raise HTTPException(
            status_code=400,
            detail="ID de pedido no válido"
        )

    # Buscar pedido
    pedido_existente = await pedidos_collection.find_one(
        {"_id": ObjectId(pedido_id)}
    )

    if pedido_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    # -----------------------------------------------------
    # Restaurar stock de los productos del pedido
    # -----------------------------------------------------
    for producto in pedido_existente.get("productos", []):

        producto_id = producto.get("producto_id")
        cantidad = producto.get("cantidad", 0)

        if not ObjectId.is_valid(producto_id):
            continue

        if cantidad <= 0:
            continue

        await productos_collection.update_one(
            {"_id": ObjectId(producto_id)},
            {
                "$inc": {
                    "stock": cantidad
                }
            }
        )

    # -----------------------------------------------------
    # Eliminar pedido
    # -----------------------------------------------------
    resultado = await pedidos_collection.delete_one(
        {"_id": ObjectId(pedido_id)}
    )

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="No fue posible eliminar el pedido"
        )

    return {
        "mensaje": "Pedido eliminado correctamente",
        "pedido_id": pedido_id
    }