from fastapi import FastAPI

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