from django import forms


class PedidoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre completo",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu nombre completo",
                "required": True,
            }
        ),
    )

    identificacion = forms.CharField(
        label="Número de identificación",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu identificación",
                "required": True,
            }
        ),
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu teléfono",
                "required": True,
            }
        ),
    )

    cantidad = forms.IntegerField(
        label="Cantidad",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "1",
                "required": True,
            }
        ),
    )


class ProductoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre del producto",
        min_length=2,
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Teclado mecánico",
                "required": True,
            }
        ),
    )

    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Descripción del producto",
                "rows": 4,
                "required": True,
            }
        ),
    )

    precio = forms.DecimalField(
        label="Precio",
        min_value=0.01,
        decimal_places=2,
        max_digits=12,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. 250000",
                "step": "0.01",
                "min": "0.01",
                "required": True,
            }
        ),
    )

    stock = forms.IntegerField(
        label="Stock",
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. 10",
                "min": "0",
                "required": True,
            }
        ),
    )

    categoria = forms.CharField(
        label="Categoría",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Periféricos",
                "required": True,
            }
        ),
    )