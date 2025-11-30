from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    ci = models.CharField(max_length=20, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'alumno'
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=200)
    salario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        managed = False
        db_table = 'profesor'
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_promedio_calificacion(self):
        """Calcula el promedio de calificaciones del profesor"""
        from django.db.models import Avg
        promedio = self.resenas.aggregate(Avg('calificacion'))
        return round(promedio['calificacion__avg'] or 0, 2)
    
    def get_total_resenas(self):
        """Retorna el número total de reseñas"""
        return self.resenas.count()

class Materia(models.Model):
    id_materia = models.AutoField(primary_key=True)
    nombre_materia = models.CharField(max_length=200)
    sigla = models.CharField(max_length=20)
    duracion = models.IntegerField(
        help_text="Duración en horas",
        validators=[MinValueValidator(1)]
    )
    precio = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # ForeignKey 
    id_profesor = models.ForeignKey(
        Profesor, 
        on_delete=models.CASCADE, 
        db_column='id_profesor',
        related_name='materias'
    )
    
    class Meta:
        managed = False
        db_table = 'materia'
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['nombre_materia']
    
    def __str__(self):
        return f"{self.nombre_materia} ({self.sigla})"
    
    def get_nombre_con_profesor(self):
        return f"{self.nombre_materia} - Prof. {self.id_profesor.get_nombre_completo()}"


class ReservaClase(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Cancelada', 'Cancelada'),
        ('Completada', 'Completada'),
    ]
    
    id_reserva = models.AutoField(primary_key=True)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=50, 
        choices=ESTADO_CHOICES,
        default='Pendiente'
    )
    requerimientos = models.TextField(blank=True, null=True)
    
    # ForeignKeys mejoradas con related_name
    id_alumno = models.ForeignKey(
        Alumno, 
        on_delete=models.CASCADE, 
        db_column='id_alumno',
        related_name='reservas'
    )
    id_profesor = models.ForeignKey(
        Profesor, 
        on_delete=models.CASCADE, 
        db_column='id_profesor',
        related_name='reservas'
    )
    id_materia = models.ForeignKey(
        Materia, 
        on_delete=models.CASCADE, 
        db_column='id_materia',
        related_name='reservas'
    )
    
    class Meta:
        managed = False
        db_table = 'reserva_clase'
        verbose_name = 'Reserva de Clase'
        verbose_name_plural = 'Reservas de Clases'
        ordering = ['-fecha_reserva']
    
    def __str__(self):
        return f"Reserva #{self.id_reserva} - {self.id_alumno.get_nombre_completo()} - {self.estado}"
    
    def get_descripcion_completa(self):
        return f"{self.id_alumno.get_nombre_completo()} reservó {self.id_materia.nombre_materia} con {self.id_profesor.get_nombre_completo()}"
    
    def esta_pendiente(self):
        return self.estado == 'Pendiente'
    
    def esta_confirmada(self):
        return self.estado == 'Confirmada'


class Resena(models.Model):
    id_resena = models.AutoField(primary_key=True)
    
    # ForeignKeys mejoradas con related_name
    id_profesor = models.ForeignKey(
        Profesor, 
        on_delete=models.CASCADE, 
        db_column='id_profesor', 
        related_name='resenas'
    )
    id_alumno = models.ForeignKey(
        Alumno, 
        on_delete=models.CASCADE, 
        db_column='id_alumno',
        related_name='resenas'
    )
    
    calificacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Calificación de 1 a 5 estrellas"
    )
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'resena'
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        ordering = ['-fecha']
        # Evitar que un alumno haga múltiples reseñas al mismo profesor
        unique_together = [['id_profesor', 'id_alumno']]
    
    def __str__(self):
        return f"Reseña de {self.id_alumno.get_nombre_completo()} para {self.id_profesor.get_nombre_completo()} - {self.calificacion}★"
    
    def get_estrellas(self):
        """Retorna las estrellas en formato visual"""
        return "★" * self.calificacion + "☆" * (5 - self.calificacion)