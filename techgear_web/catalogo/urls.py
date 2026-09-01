from django.urls import path

from . import views


urlpatterns = [
    # Catálogo
    path(
        "",
        views.productos,
        name="productos",
    ),

    # Checkout
    path(
        "checkout/<str:producto_id>/",
        views.checkout,
        name="checkout",
    ),

    # Pedidos públicos
    path(
        "pedidos/",
        views.pedidos,
        name="pedidos",
    ),

    # ========================================================
    # PANEL ADMINISTRATIVO PERSONALIZADO
    # ========================================================

    path(
        "admin-panel/",
        views.admin_panel,
        name="admin_panel",
    ),

    # Crear producto
    path(
        "admin-panel/productos/crear/",
        views.admin_producto_crear,
        name="admin_producto_crear",
    ),

    # Editar producto
    path(
        "admin-panel/productos/<str:producto_id>/editar/",
        views.admin_producto_editar,
        name="admin_producto_editar",
    ),

    # Eliminar producto
    path(
        "admin-panel/productos/<str:producto_id>/eliminar/",
        views.admin_producto_eliminar,
        name="admin_producto_eliminar",
    ),

    # Actualizar estado pedido
    path(
        "admin-panel/pedidos/<str:pedido_id>/actualizar/",
        views.admin_pedido_actualizar,
        name="admin_pedido_actualizar",
    ),

    # Eliminar pedido
    path(
        "admin-panel/pedidos/<str:pedido_id>/eliminar/",
        views.admin_pedido_eliminar,
        name="admin_pedido_eliminar",
    ),
]