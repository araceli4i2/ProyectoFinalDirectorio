# forms.py
from django import forms
from .models import Profesor, Alumno, Materia

class ProfesorForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre'
        })
    )
    apellido = forms.CharField(
        label="Apellido",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido'
        })
    )
    especialidad = forms.CharField(
        label="Especialidad",
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Matemáticas, Física, etc.'
        })
    )
    salario = forms.DecimalField(
        label="Salario",
        required=True,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        })
    )


class AlumnoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del alumno'
        })
    )
    apellido = forms.CharField(
        label="Apellido",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el apellido del alumno'
        })
    )
    ci = forms.CharField(
        label="CI (Carnet de Identidad)",
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el CI'
        })
    )

class MateriaForm(forms.Form):
    nombre_materia = forms.CharField(max_length=200)
    sigla = forms.CharField(max_length=20)
    duracion = forms.IntegerField(min_value=1)
    precio = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    id_profesor = forms.ModelChoiceField(
        queryset=Profesor.objects.all(),
        empty_label="Seleccione un profesor"
    )
    sigla = forms.CharField(
        label="Sigla",
        required=True,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: MAT101'
        })
    )
    duracion = forms.IntegerField(
        label="Duración (horas)",
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de horas'
        })
    )
    precio = forms.DecimalField(
        label="Precio",
        required=True,
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0.00',
            'step': '0.01'
        })
    )
    id_profesor = forms.ChoiceField(
        label="Profesor",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Llenar el dropdown de profesores
        profesores = Profesor.objects.all().order_by('apellido', 'nombre')
        self.fields['id_profesor'].choices = [('', 'Seleccione un profesor')] + [
            (p.id_profesor, f"{p.apellido}, {p.nombre} - {p.especialidad}") 
            for p in profesores
        ]

    #def __init__(self, *args, **kwargs):
     #   super().__init__(*args, **kwargs)
        # Llenar el dropdown de profesores
      #  self.fields['id_profesor'].choices = [
       #     (p.id_profesor, f"{p.nombre} {p.apellido}") 
        #    for p in Profesor.objects.all()
       # ]

