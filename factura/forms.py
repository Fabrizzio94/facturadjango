from django import forms
from django.core.validators import RegexValidator, MinLengthValidator
from .models import Producto
class FacturaFormulario(forms.Form):
    numeric = RegexValidator(r'^[0-9]*$', 'Campo de solo numeros')
    onlyLetters = RegexValidator(r'^[0-9a-zA-Z]*$', 'Ingrese datos validos')
    cedula = forms.CharField(label="Cédula", required=True, max_length=10, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese Cédula',
            'pattern': r'^[0-9]*$'
        }
    ))
    nom_cliente = forms.CharField(label="Nombre", required=True, validators=[onlyLetters], widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Nombre'
        }
    ))
    direccion = forms.CharField(label="Dirección", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'ejem: Calle norte entre avenida'
        }
    ))
    telefono = forms.CharField(label="Telefono", widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'ejem: 0992333226'
        }
    ))

    class Meta:
        pass
class FacturaForm(forms.ModelForm):
    pass