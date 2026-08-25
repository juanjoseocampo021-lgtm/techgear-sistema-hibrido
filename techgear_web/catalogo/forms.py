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