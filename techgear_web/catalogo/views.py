import requests

from django.conf import settings
from django.shortcuts import render


def productos(request):

    respuesta = requests.get(
        f"{settings.API_URL}/productos/"
    )

    productos = respuesta.json()

    return render(
        request,
        "catalogo/productos.html",
        {"productos": productos}
    )