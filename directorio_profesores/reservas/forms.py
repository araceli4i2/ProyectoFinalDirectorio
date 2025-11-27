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