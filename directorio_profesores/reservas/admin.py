from django.contrib import admin
from .models import Alumno, Profesor, Materia, ReservaClase, Resena

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ['id_profesor', 'nombre', 'apellido', 'especialidad', 'salario']
    search_fields = ['nombre', 'apellido', 'especialidad']

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['id_alumno', 'nombre', 'apellido', 'ci', 'fecha_registro']
    search_fields = ['nombre', 'apellido', 'ci']

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['id_materia', 'nombre_materia', 'sigla', 'duracion', 'precio', 'id_profesor']
    list_filter = ['id_profesor']

@admin.register(ReservaClase)
class ReservaClaseAdmin(admin.ModelAdmin):
    list_display = ['id_reserva', 'fecha_reserva', 'estado', 'id_alumno', 'id_profesor', 'id_materia']
    list_filter = ['estado', 'fecha_reserva']

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ['id_resena', 'id_profesor', 'id_alumno', 'calificacion', 'fecha']
    list_filter = ['calificacion', 'fecha']
    search_fields = ['id_profesor__nombre', 'id_alumno__nombre', 'comentario']
