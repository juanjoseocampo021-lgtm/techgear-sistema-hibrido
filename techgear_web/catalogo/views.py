import os
import requests
from django.shortcuts import render


def productos(request):

    api_url = os.getenv("API_URL", "http://127.0.0.1:8000")

    respuesta = requests.get(f"{api_url}/productos/")

    productos = respuesta.json()

    return render(
        request,
        "catalogo/productos.html",
        {"productos": productos}
    )