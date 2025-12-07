from django import forms
from django.core.exceptions import ValidationError
from .models import Producto, Categoria
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CustomUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']
        #añadir alias a los campos, mediante labels
        labels = {
            'username':'Nombre de Usuario',
            'email':'Email',
            'password1':'Contraseña',
            'password2':'Repetir Contraseña'
        }
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'username': {
                'required':'Este campo es obligatorio'
            }
        }
            
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        #ocultar los mensajes de error
        for f in self.fields:
            self.fields[f].help_text = None


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['titulo', 'descripcion', 'precio', 'categoria', 'foto']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Nombre',
            'descripcion': 'Descripcion',
            'precio': 'Precio',
            'foto': 'Imagen',
        }

    # Validación personalizada para el campo 'precio'
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio < 0:
            raise ValidationError('El precio no puede ser negativo.')
        return precio
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurar que stock nunca se muestre ni se permita editar
        if 'stock' in self.fields:
            self.fields['stock'].widget = forms.HiddenInput()
