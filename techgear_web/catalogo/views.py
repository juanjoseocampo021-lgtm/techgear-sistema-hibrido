import requests

from django.conf import settings
from django.shortcuts import render


def productos(request):
    """
    Obtiene el catálogo de productos desde la API FastAPI
    y lo envía al template de Django.
    """

    productos_data = []
    error_api = None

    try:
        respuesta = requests.get(
            f"{settings.API_URL}/productos/",
            timeout=10,
        )

        respuesta.raise_for_status()

        productos_data = respuesta.json()

    except requests.RequestException:
        error_api = (
            "No fue posible obtener los productos "
            "desde la API."
        )

    return render(
        request,
        "catalogo/productos.html",
        {
            "productos": productos_data,
            "error_api": error_api,
        },
    )