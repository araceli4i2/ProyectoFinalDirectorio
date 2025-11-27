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

# ============= BÚSQUEDA =============

def buscar(request):
    form = BusquedaForm(request.GET)
    profesores = Profesor.objects.all()
    materias = Materia.objects.all()
    query = ''
    materia_filter = ''
    
    if form.is_valid():
        query = form.cleaned_data.get('q', '')
        materia_filter = form.cleaned_data.get('materia', '')
        
        if query:
            # Buscar en nombre, apellido o especialidad del profesor
            profesores = profesores.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(especialidad__icontains=query)
            )
        
        if materia_filter:
            # Filtrar profesores que enseñan una materia específica
            profesores = profesores.filter(
                materias__nombre_materia__icontains=materia_filter
            ).distinct()
    
    # Agregar promedio de calificación a cada profesor
    for profesor in profesores:
        profesor.promedio = profesor.get_promedio_calificacion()
    
    return render(request, 'reservas/buscar.html', {
        'form': form,
        'profesores': profesores,
        'materias': materias,
        'query': query,
        'materia_filter': materia_filter,
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

# ============= VISTAS DE ALUMNOS =============

def listar_alumnos(request):
    try:
        alumnos = Alumno.objects.all()
        return render(request, 'reservas/lista_alumnos.html', {
            'alumnos': alumnos
        })
    except Exception as e:
        messages.error(request, f'Error al listar alumnos: {str(e)}')
        return render(request, 'reservas/lista_alumnos.html', {
            'alumnos': []
        })

def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            try:
                Alumno.objects.create(
                    nombre=form.cleaned_data['nombre'],
                    apellido=form.cleaned_data['apellido'],
                    ci=form.cleaned_data['ci']
                )
                messages.success(request, 'Alumno creado exitosamente.')
                return redirect('listar_alumnos')
            except Exception as e:
                messages.error(request, f'Error al crear alumno: {str(e)}')
    else:
        form = AlumnoForm()
    
    return render(request, 'reservas/crear_alumno.html', {'form': form})

def editar_alumno(request, id_alumno):
    alumno = get_object_or_404(Alumno, id_alumno=id_alumno)
    
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            try:
                alumno.nombre = form.cleaned_data['nombre']
                alumno.apellido = form.cleaned_data['apellido']
                alumno.ci = form.cleaned_data['ci']
                alumno.save()
                messages.success(request, 'Alumno actualizado exitosamente.')
                return redirect('listar_alumnos')
            except Exception as e:
                messages.error(request, f'Error al actualizar alumno: {str(e)}')
    else:
        form = AlumnoForm(initial={
            'nombre': alumno.nombre,
            'apellido': alumno.apellido,
            'ci': alumno.ci,
        })
    
    return render(request, 'reservas/editar_alumno.html', {
        'form': form,
        'alumno': alumno
    })

def eliminar_alumno(request, id_alumno):
    alumno = get_object_or_404(Alumno, id_alumno=id_alumno)
    
    if request.method == 'POST':
        try:
            nombre_completo = alumno.get_nombre_completo()
            alumno.delete()
            messages.success(request, f'Alumno {nombre_completo} eliminado exitosamente.')
            return redirect('listar_alumnos')
        except Exception as e:
            messages.error(request, f'Error al eliminar alumno: {str(e)}')
            return redirect('listar_alumnos')
    
    return render(request, 'reservas/confirmar_eliminar_alumno.html', {
        'alumno': alumno
    })

# ============= VISTAS DE MATERIAS =============

def listar_materias(request):
    materias = Materia.objects.all().select_related('id_profesor')

    query = request.GET.get('q', '')
    prof = request.GET.get('profesor', '')

    if query:
        materias = materias.filter(
            Q(nombre_materia__icontains=query) |
            Q(sigla__icontains=query)
        )

    if prof:
        materias = materias.filter(id_profesor__id_profesor=prof)

    profesores = Profesor.objects.all()

    return render(request, 'reservas/lista_materias.html', {
        'materias': materias,
        'profesores': profesores,
        'query': query,
        'prof': prof,
    })


def detalle_materia(request, id_materia):
    materia = get_object_or_404(Materia, id_materia=id_materia)
    profesor = materia.id_profesor
    reservas = materia.reservas.all()

    return render(request, 'reservas/detalle_materia.html', {
        'materia': materia,
        'profesor': profesor,
        'reservas': reservas
    })


def crear_materia(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            try:
                profesor = get_object_or_404(Profesor, id_profesor=form.cleaned_data['id_profesor'])
                Materia.objects.create(
                    nombre_materia=form.cleaned_data['nombre_materia'],
                    sigla=form.cleaned_data['sigla'],
                    duracion=form.cleaned_data['duracion'],
                    precio=form.cleaned_data['precio'],
                    id_profesor=profesor
                )
                messages.success(request, 'Materia creada exitosamente.')
                return redirect('listar_materias')
            except Exception as e:
                messages.error(request, f'Error al crear materia: {str(e)}')
    else:
        form = MateriaForm()
    
    return render(request, 'reservas/crear_materia.html', {'form': form})

def editar_materia(request, id_materia):
    materia = get_object_or_404(Materia, id_materia=id_materia)
    
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            try:
                profesor = get_object_or_404(Profesor, id_profesor=form.cleaned_data['id_profesor'])
                materia.nombre_materia = form.cleaned_data['nombre_materia']
                materia.sigla = form.cleaned_data['sigla']
                materia.duracion = form.cleaned_data['duracion']
                materia.precio = form.cleaned_data['precio']
                materia.id_profesor = profesor
                materia.save()
                messages.success(request, 'Materia actualizada exitosamente.')
                return redirect('listar_materias')
            except Exception as e:
                messages.error(request, f'Error al actualizar materia: {str(e)}')
    else:
        form = MateriaForm(initial={
            'nombre_materia': materia.nombre_materia,
            'sigla': materia.sigla,
            'duracion': materia.duracion,
            'precio': materia.precio,
            'id_profesor': materia.id_profesor.id_profesor,
        })
    
    return render(request, 'reservas/editar_materia.html', {
        'form': form,
        'materia': materia
    })

def eliminar_materia(request, id_materia):
    materia = get_object_or_404(Materia, id_materia=id_materia)
    
    if request.method == 'POST':
        try:
            nombre_materia = materia.nombre_materia
            materia.delete()
            messages.success(request, f'Materia {nombre_materia} eliminada exitosamente.')
            return redirect('listar_materias')
        except Exception as e:
            messages.error(request, f'Error al eliminar materia: {str(e)}')
            return redirect('listar_materias')
    
    return render(request, 'reservas/confirmar_eliminar_materia.html', {
        'materia': materia
    })
