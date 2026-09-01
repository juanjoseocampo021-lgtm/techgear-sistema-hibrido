import requests

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import PedidoForm, ProductoForm


def obtener_detalle_error(response):
    """
    Obtiene un mensaje entendible cuando FastAPI devuelve un error.
    """
    if response is None:
        return None

    try:
        data = response.json()
    except ValueError:
        return None

    detalle = data.get("detail")

    if isinstance(detalle, str):
        return detalle

    if isinstance(detalle, list):
        mensajes = []

        for error in detalle:
            if isinstance(error, dict):
                mensaje = error.get("msg")

                if mensaje:
                    mensajes.append(str(mensaje))

        if mensajes:
            return " ".join(mensajes)

    if detalle:
        return str(detalle)

    return None


# ============================================================
# CATÁLOGO
# ============================================================

def productos(request):
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
        error_api = "No fue posible obtener los productos desde la API."

    return render(
        request,
        "catalogo/productos.html",
        {
            "productos": productos_data,
            "error_api": error_api,
            "api_url": settings.API_URL,
        },
    )


# ============================================================
# CHECKOUT / CREACIÓN DE PEDIDOS
# ============================================================

def checkout(request, producto_id):
    try:
        response = requests.get(
            f"{settings.API_URL}/productos/{producto_id}",
            timeout=10,
        )

        response.raise_for_status()
        producto = response.json()

    except requests.RequestException:
        messages.error(
            request,
            "No fue posible obtener la información del producto.",
        )

        return redirect("productos")

    if request.method == "POST":
        form = PedidoForm(request.POST)

        if form.is_valid():
            cantidad = form.cleaned_data["cantidad"]

            pedido = {
                "cliente": {
                    "nombre": form.cleaned_data["nombre"],
                    "identificacion": form.cleaned_data["identificacion"],
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

                detalle = obtener_detalle_error(exc.response)

                if detalle:
                    error = detalle

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


# ============================================================
# PEDIDOS
# ============================================================

def pedidos(request):
    pedidos_data = []
    error_api = None

    try:
        response = requests.get(
            f"{settings.API_URL}/pedidos/",
            timeout=10,
        )

        response.raise_for_status()
        pedidos_data = response.json()

    except requests.RequestException:
        error_api = "No fue posible obtener los pedidos desde la API."

    return render(
        request,
        "catalogo/pedidos.html",
        {
            "pedidos": pedidos_data,
            "error_api": error_api,
        },
    )


# ============================================================
# PANEL ADMINISTRATIVO PERSONALIZADO
# ============================================================

def admin_panel(request):
    productos_data = []
    pedidos_data = []

    error_productos = None
    error_pedidos = None

    # -----------------------------
    # Obtener productos
    # -----------------------------
    try:
        response_productos = requests.get(
            f"{settings.API_URL}/productos/",
            timeout=10,
        )

        response_productos.raise_for_status()
        productos_data = response_productos.json()

    except requests.RequestException:
        error_productos = (
            "No fue posible obtener los productos desde la API."
        )

    # -----------------------------
    # Obtener pedidos
    # -----------------------------
    try:
        response_pedidos = requests.get(
            f"{settings.API_URL}/pedidos/",
            timeout=10,
        )

        response_pedidos.raise_for_status()
        pedidos_data = response_pedidos.json()

    except requests.RequestException:
        error_pedidos = (
            "No fue posible obtener los pedidos desde la API."
        )

    return render(
        request,
        "catalogo/admin_panel.html",
        {
            "productos": productos_data,
            "pedidos": pedidos_data,
            "error_productos": error_productos,
            "error_pedidos": error_pedidos,
        },
    )


# ============================================================
# CREAR PRODUCTO
# ============================================================

def admin_producto_crear(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)

        if form.is_valid():
            producto = {
                "nombre": form.cleaned_data["nombre"],
                "descripcion": form.cleaned_data["descripcion"],
                "precio": float(form.cleaned_data["precio"]),
                "stock": form.cleaned_data["stock"],
                "categoria": form.cleaned_data["categoria"],
            }

            try:
                response = requests.post(
                    f"{settings.API_URL}/productos/",
                    json=producto,
                    timeout=10,
                )

                response.raise_for_status()

                messages.success(
                    request,
                    "Producto creado correctamente.",
                )

                return redirect("admin_panel")

            except requests.RequestException as exc:
                error = "No fue posible crear el producto mediante la API."

                detalle = obtener_detalle_error(exc.response)

                if detalle:
                    error = detalle

                form.add_error(None, error)

    else:
        form = ProductoForm()

    return render(
        request,
        "catalogo/producto_form.html",
        {
            "form": form,
            "titulo": "Crear producto",
            "accion": "Crear producto",
        },
    )


# ============================================================
# EDITAR PRODUCTO
# ============================================================

def admin_producto_editar(request, producto_id):
    try:
        response = requests.get(
            f"{settings.API_URL}/productos/{producto_id}",
            timeout=10,
        )

        response.raise_for_status()
        producto = response.json()

    except requests.RequestException:
        messages.error(
            request,
            "No fue posible obtener el producto.",
        )

        return redirect("admin_panel")

    if request.method == "POST":
        form = ProductoForm(request.POST)

        if form.is_valid():
            producto_actualizado = {
                "nombre": form.cleaned_data["nombre"],
                "descripcion": form.cleaned_data["descripcion"],
                "precio": float(form.cleaned_data["precio"]),
                "stock": form.cleaned_data["stock"],
                "categoria": form.cleaned_data["categoria"],
            }

            try:
                response = requests.put(
                    f"{settings.API_URL}/productos/{producto_id}",
                    json=producto_actualizado,
                    timeout=10,
                )

                response.raise_for_status()

                messages.success(
                    request,
                    "Producto actualizado correctamente.",
                )

                return redirect("admin_panel")

            except requests.RequestException as exc:
                error = "No fue posible actualizar el producto."

                detalle = obtener_detalle_error(exc.response)

                if detalle:
                    error = detalle

                form.add_error(None, error)

    else:
        form = ProductoForm(
            initial={
                "nombre": producto.get("nombre", ""),
                "descripcion": producto.get("descripcion", ""),
                "precio": producto.get("precio", ""),
                "stock": producto.get("stock", 0),
                "categoria": producto.get("categoria", ""),
            }
        )

    return render(
        request,
        "catalogo/producto_form.html",
        {
            "form": form,
            "titulo": "Editar producto",
            "accion": "Guardar cambios",
            "producto": producto,
        },
    )


# ============================================================
# ELIMINAR PRODUCTO
# ============================================================

def admin_producto_eliminar(request, producto_id):
    if request.method != "POST":
        return redirect("admin_panel")

    try:
        response = requests.delete(
            f"{settings.API_URL}/productos/{producto_id}",
            timeout=10,
        )

        response.raise_for_status()

        messages.success(
            request,
            "Producto eliminado correctamente.",
        )

    except requests.RequestException as exc:
        error = "No fue posible eliminar el producto."

        detalle = obtener_detalle_error(exc.response)

        if detalle:
            error = detalle

        messages.error(request, error)

    return redirect("admin_panel")


# ============================================================
# ACTUALIZAR ESTADO DEL PEDIDO
# ============================================================

def admin_pedido_actualizar(request, pedido_id):
    if request.method != "POST":
        return redirect("admin_panel")

    estado = request.POST.get("estado", "").strip()

    estados_validos = {
        "pendiente",
        "procesando",
        "enviado",
        "entregado",
        "cancelado",
    }

    if estado not in estados_validos:
        messages.error(
            request,
            "El estado seleccionado no es válido.",
        )

        return redirect("admin_panel")

    try:
        response = requests.patch(
            f"{settings.API_URL}/pedidos/{pedido_id}",
            json={
                "estado": estado,
            },
            timeout=10,
        )

        response.raise_for_status()

        messages.success(
            request,
            "Estado del pedido actualizado correctamente.",
        )

    except requests.RequestException as exc:
        error = "No fue posible actualizar el pedido."

        detalle = obtener_detalle_error(exc.response)

        if detalle:
            error = detalle

        messages.error(request, error)

    return redirect("admin_panel")


# ============================================================
# ELIMINAR PEDIDO
# ============================================================

def admin_pedido_eliminar(request, pedido_id):
    if request.method != "POST":
        return redirect("admin_panel")

    try:
        response = requests.delete(
            f"{settings.API_URL}/pedidos/{pedido_id}",
            timeout=10,
        )

        response.raise_for_status()

        messages.success(
            request,
            "Pedido eliminado correctamente.",
        )

    except requests.RequestException as exc:
        error = "No fue posible eliminar el pedido."

        detalle = obtener_detalle_error(exc.response)

        if detalle:
            error = detalle

        messages.error(request, error)

    return redirect("admin_panel")