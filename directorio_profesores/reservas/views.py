from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.contrib import messages
from .models import Profesor, Materia, Alumno, ReservaClase, Resena
from .forms import (
    ProfesorForm, AlumnoForm, MateriaForm, 
    ReservaClaseForm, ResenaForm, BusquedaForm
)

# ============= VISTA PRINCIPAL/HOME =============

def home(request):
    try:
        total_profesores = Profesor.objects.count()
        total_materias = Materia.objects.count()
        total_reservas = ReservaClase.objects.count()
        total_alumnos = Alumno.objects.count()
        
        # Profesores mejor calificados
        profesores_destacados = Profesor.objects.all()[:5]
        for profesor in profesores_destacados:
            profesor.promedio = profesor.get_promedio_calificacion()
        
        return render(request, 'reservas/home.html', {
            'total_profesores': total_profesores,
            'total_materias': total_materias,
            'total_reservas': total_reservas,
            'total_alumnos': total_alumnos,
            'profesores_destacados': profesores_destacados,
        })
    except Exception as e:
        messages.error(request, f'Error al cargar la página principal: {str(e)}')
        return render(request, 'reservas/home.html', {
            'total_profesores': 0,
            'total_materias': 0,
            'total_reservas': 0,
            'total_alumnos': 0,
        })
