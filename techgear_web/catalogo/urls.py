from django.urls import path

from . import views


urlpatterns = [
    path("", views.productos, name="productos"),
    path(
        "checkout/<str:producto_id>/",
        views.checkout,
        name="checkout",
    ),
    path(
        "pedidos/",
        views.pedidos,
        name="pedidos",
    ),
]