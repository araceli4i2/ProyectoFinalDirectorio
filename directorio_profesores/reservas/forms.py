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



class ReservaClaseForm(forms.Form):
    id_alumno = forms.ChoiceField(
        label="Alumno",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    id_materia = forms.ChoiceField(
        label="Materia",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    requerimientos = forms.CharField(
        label="Requerimientos",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Describe tus requerimientos o necesidades especiales',
            'rows': 4
        })
    )
    def __init__(self, *args, **kwargs):
        profesor_id = kwargs.pop('profesor_id', None)
        super().__init__(*args, **kwargs)
        
        # Llenar el dropdown de alumnos
        alumnos = Alumno.objects.all().order_by('apellido', 'nombre')
        self.fields['id_alumno'].choices = [('', 'Seleccione un alumno')] + [
            (a.id_alumno, f"{a.apellido}, {a.nombre} - CI: {a.ci}") 
            for a in alumnos
        ]
        
        # Llenar el dropdown de materias filtradas por profesor
        if profesor_id:
            materias = Materia.objects.filter(id_profesor_id=profesor_id).order_by('nombre_materia')
            if materias.exists():
                self.fields['id_materia'].choices = [('', 'Seleccione una materia')] + [
                    (m.id_materia, f"{m.nombre_materia} ({m.sigla}) - Bs. {m.precio}") 
                    for m in materias
                ]
            else:
                self.fields['id_materia'].choices = [('', '⚠️ Este profesor no tiene materias asignadas')]
        else:
            materias = Materia.objects.all().order_by('nombre_materia')
            self.fields['id_materia'].choices = [('', 'Seleccione una materia')] + [
                (m.id_materia, f"{m.nombre_materia} ({m.sigla}) - Bs. {m.precio}") 
                for m in materias
            ]
    
    #def __init__(self, *args, **kwargs):
     #   profesor_id = kwargs.pop('profesor_id', None)
      #  super().__init__(*args, **kwargs)
        
        # Llenar el dropdown de alumnos
       # self.fields['id_alumno'].choices = [('', 'Seleccione un alumno')] + [
        #    (a.id_alumno, f"{a.nombre} {a.apellido}") 
          #  for a in Alumno.objects.all()
        #]
        
        # Llenar el dropdown de materias filtradas por profesor
        #if profesor_id:
         #   materias = Materia.objects.filter(id_profesor_id=profesor_id)
          #  self.fields['id_materia'].choices = [('', 'Seleccione una materia')] + [
           #     (m.id_materia, f"{m.nombre_materia} - {m.sigla}") 
            #    for m in materias
            #]
        #else:
         #   self.fields['id_materia'].choices = [('', 'Seleccione una materia')] + [
          #      (m.id_materia, f"{m.nombre_materia} - {m.sigla}") 
           #     for m in Materia.objects.all()
            #]

class ResenaForm(forms.Form):
    id_alumno = forms.ChoiceField(
        label="Alumno",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    calificacion = forms.IntegerField(
        label="Calificación",
        required=True,
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calificación de 1 a 5',
            'min': '1',
            'max': '5'
        })
    )
    comentario = forms.CharField(
        label="Comentario",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe tu opinión sobre el profesor',
            'rows': 4
        })
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Llenar el dropdown de alumnos
        self.fields['id_alumno'].choices = [
            (a.id_alumno, f"{a.nombre} {a.apellido}") 
            for a in Alumno.objects.all()
        ]


class BusquedaForm(forms.Form):
    q = forms.CharField(
        label="Buscar",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar profesor por nombre, apellido o especialidad'
        })
    )
    materia = forms.CharField(
        label="Materia",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filtrar por materia'
        })
    )