from fastapi import APIRouter, HTTPException
from bson import ObjectId

from techgear_api.database import productos_collection
from techgear_api.models.producto import Producto


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


# ---------------------------------------------------------
# GET - Obtener todos los productos
# ---------------------------------------------------------
@router.get("/")
async def obtener_productos():

    productos = []

    async for producto in productos_collection.find():

        producto["id"] = str(producto["_id"])
        del producto["_id"]

        productos.append(producto)

    return productos


# ---------------------------------------------------------
# GET - Obtener un producto por ID
# ---------------------------------------------------------
@router.get("/{producto_id}")
async def obtener_producto(producto_id: str):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="ID de producto no válido"
        )

    producto = await productos_collection.find_one(
        {"_id": ObjectId(producto_id)}
    )

    if producto is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto["id"] = str(producto["_id"])
    del producto["_id"]

    return producto


# ---------------------------------------------------------
# POST - Crear producto
# ---------------------------------------------------------
@router.post("/")
async def crear_producto(producto: Producto):

    producto_dict = producto.model_dump(exclude={"id"})

    result = await productos_collection.insert_one(producto_dict)

    producto_creado = await productos_collection.find_one(
        {"_id": result.inserted_id}
    )

    if producto_creado is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudo recuperar el producto creado"
        )

    producto_creado["id"] = str(producto_creado["_id"])
    del producto_creado["_id"]

    return producto_creado


# ---------------------------------------------------------
# PUT - Actualizar producto
# ---------------------------------------------------------
@router.put("/{producto_id}")
async def actualizar_producto(
    producto_id: str,
    producto: Producto
):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="ID de producto no válido"
        )

    producto_dict = producto.model_dump(exclude={"id"})

    resultado = await productos_collection.update_one(
        {"_id": ObjectId(producto_id)},
        {"$set": producto_dict}
    )

    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    producto_actualizado = await productos_collection.find_one(
        {"_id": ObjectId(producto_id)}
    )

    producto_actualizado["id"] = str(producto_actualizado["_id"])
    del producto_actualizado["_id"]

    return producto_actualizado


# ---------------------------------------------------------
# DELETE - Eliminar producto
# ---------------------------------------------------------
@router.delete("/{producto_id}")
async def eliminar_producto(producto_id: str):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="ID de producto no válido"
        )

    resultado = await productos_collection.delete_one(
        {"_id": ObjectId(producto_id)}
    )

    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {
        "mensaje": "Producto eliminado correctamente",
        "id": producto_id
    }