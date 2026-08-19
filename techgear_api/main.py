from fastapi import FastAPI
from techgear_api.routes.productos import router as productos_router
from techgear_api.routes.pedidos import router as pedidos_router


app = FastAPI(
    title="TechGear API",
    description="API REST para el catálogo de productos y pedidos de TechGear",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "mensaje": "TechGear API funcionando"
    }


app.include_router(productos_router)
app.include_router(pedidos_router)