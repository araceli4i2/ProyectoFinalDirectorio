from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.contrib import messages
from .models import Profesor, Materia, Alumno, ReservaClase, Resena
from .forms import (
    ProfesorForm # AlumnoForm, MateriaForm, 
    #ReservaClaseForm, ResenaForm, BusquedaForm
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

# ============= VISTAS DE PROFESORES =============

def listar_profesores(request):
    try:
        profesores = Profesor.objects.all()
        
        # Calcular promedio de calificaciones para cada profesor
        for profesor in profesores:
            profesor.promedio = profesor.get_promedio_calificacion()
            profesor.total_resenas = profesor.get_total_resenas()
        
        return render(request, 'reservas/lista_profesores.html', {
            'profesores': profesores
        })
    except Exception as e:
        messages.error(request, f'Error al listar profesores: {str(e)}')
        return render(request, 'reservas/lista_profesores.html', {
            'profesores': []
        })

def detalle_profesor(request, id_profesor):
    try:
        profesor = get_object_or_404(Profesor, id_profesor=id_profesor)
        materias = profesor.materias.all()  # Usando related_name
        resenas = profesor.resenas.all().order_by('-fecha')  # Usando related_name
        
        return render(request, 'reservas/detalle_profesor.html', {
            'profesor': profesor,
            'materias': materias,
            'resenas': resenas,
            'promedio_calificacion': profesor.get_promedio_calificacion(),
            'total_resenas': profesor.get_total_resenas(),
        })
    except Exception as e:
        messages.error(request, f'Error al cargar el profesor: {str(e)}')
        return redirect('listar_profesores')

def crear_profesor(request):
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            try:
                Profesor.objects.create(
                    nombre=form.cleaned_data['nombre'],
                    apellido=form.cleaned_data['apellido'],
                    especialidad=form.cleaned_data['especialidad'],
                    salario=form.cleaned_data['salario']
                )
                messages.success(request, 'Profesor creado exitosamente.')
                return redirect('listar_profesores')
            except Exception as e:
                messages.error(request, f'Error al crear profesor: {str(e)}')
    else:
        form = ProfesorForm()
    
    return render(request, 'reservas/crear_profesor.html', {'form': form})

def editar_profesor(request, id_profesor):
    profesor = get_object_or_404(Profesor, id_profesor=id_profesor)
    
    if request.method == 'POST':
        form = ProfesorForm(request.POST)
        if form.is_valid():
            try:
                profesor.nombre = form.cleaned_data['nombre']
                profesor.apellido = form.cleaned_data['apellido']
                profesor.especialidad = form.cleaned_data['especialidad']
                profesor.salario = form.cleaned_data['salario']
                profesor.save()
                messages.success(request, 'Profesor actualizado exitosamente.')
                return redirect('detalle_profesor', id_profesor=id_profesor)
            except Exception as e:
                messages.error(request, f'Error al actualizar profesor: {str(e)}')
    else:
        form = ProfesorForm(initial={
            'nombre': profesor.nombre,
            'apellido': profesor.apellido,
            'especialidad': profesor.especialidad,
            'salario': profesor.salario,
        })
    
    return render(request, 'reservas/editar_profesor.html', {
        'form': form,
        'profesor': profesor
    })

def eliminar_profesor(request, id_profesor):
    profesor = get_object_or_404(Profesor, id_profesor=id_profesor)
    
    if request.method == 'POST':
        try:
            nombre_completo = profesor.get_nombre_completo()
            profesor.delete()
            messages.success(request, f'Profesor {nombre_completo} eliminado exitosamente.')
            return redirect('listar_profesores')
        except Exception as e:
            messages.error(request, f'Error al eliminar profesor: {str(e)}')
            return redirect('detalle_profesor', id_profesor=id_profesor)
    
    return render(request, 'reservas/confirmar_eliminar.html', {
        'profesor': profesor
    })
