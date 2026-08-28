import requests

from django.conf import settings
from django.shortcuts import redirect, render

from .forms import PedidoForm


def productos(request):
    """
    Obtiene los productos desde FastAPI y los muestra
    en el catálogo de Django.
    """

    productos_data = []
    error_api = None

    try:
        response = requests.get(
            f"{settings.API_URL}/productos/",
            timeout=10,
        )
        response.raise_for_status()
        productos_data = response.json()

    except requests.RequestException:
        error_api = (
            "No fue posible obtener los productos desde la API."
        )

    return render(
        request,
        "catalogo/productos.html",
        {
            "productos": productos_data,
            "error_api": error_api,
        },
    )


def checkout(request, producto_id):
    """
    Muestra el formulario de pedido para un producto
    y registra el pedido mediante FastAPI.
    """

    try:
        response = requests.get(
            f"{settings.API_URL}/productos/{producto_id}",
            timeout=10,
        )
        response.raise_for_status()
        producto = response.json()

    except requests.RequestException:
        return redirect("productos")

    if request.method == "POST":
        form = PedidoForm(request.POST)

        if form.is_valid():
            cantidad = form.cleaned_data["cantidad"]

            pedido = {
                "cliente": {
                    "nombre": form.cleaned_data["nombre"],
                    "identificacion": form.cleaned_data[
                        "identificacion"
                    ],
                    "telefono": form.cleaned_data["telefono"],
                },
                "productos": [
                    {
                        "producto_id": producto_id,
                        "cantidad": cantidad,
                    }
                ],
                "total": producto["precio"] * cantidad,
                "estado": "pendiente",
            }

            try:
                response = requests.post(
                    f"{settings.API_URL}/pedidos/",
                    json=pedido,
                    timeout=10,
                )
                response.raise_for_status()

                return render(
                    request,
                    "catalogo/checkout.html",
                    {
                        "producto": producto,
                        "form": PedidoForm(),
                        "mensaje": "Pedido registrado correctamente.",
                    },
                )

            except requests.RequestException as exc:
                error = (
                    "No fue posible registrar el pedido. "
                    "Verifica que la API esté disponible."
                )

                if exc.response is not None:
                    try:
                        detalle = exc.response.json().get("detail")
                        if detalle:
                            error = detalle
                    except ValueError:
                        pass

                return render(
                    request,
                    "catalogo/checkout.html",
                    {
                        "producto": producto,
                        "form": form,
                        "error": error,
                    },
                )

    else:
        form = PedidoForm()

    return render(
        request,
        "catalogo/checkout.html",
        {
            "producto": producto,
            "form": form,
        },
    )
def pedidos(request):
    """
    Obtiene los pedidos registrados desde FastAPI
    y los muestra en el portal Django.
    """

    pedidos_data = []
    error_api = None

    try:
        respuesta = requests.get(
            f"{settings.API_URL}/pedidos/",
            timeout=10,
        )

        respuesta.raise_for_status()

        pedidos_data = respuesta.json()

    except requests.RequestException:
        error_api = (
            "No fue posible obtener los pedidos "
            "desde la API."
        )

    return render(
        request,
        "catalogo/pedidos.html",
        {
            "pedidos": pedidos_data,
            "error_api": error_api,
        },
    )