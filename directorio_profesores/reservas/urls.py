from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('buscar/', views.buscar, name='buscar'),
    
    # URLs de profesores
    path('profesores/', views.listar_profesores, name='listar_profesores'),
    path('profesores/<int:id_profesor>/', views.detalle_profesor, name='detalle_profesor'),
    path('profesores/crear/', views.crear_profesor, name='crear_profesor'),
    path('profesores/editar/<int:id_profesor>/', views.editar_profesor, name='editar_profesor'),
    path('profesores/eliminar/<int:id_profesor>/', views.eliminar_profesor, name='eliminar_profesor'),

    # URLs de materias
    path('materias/', views.listar_materias, name='listar_materias'),
    path('materias/crear/', views.crear_materia, name='crear_materia'),
    path('materias/<int:id_materia>/', views.detalle_materia, name='detalle_materia'),
    path('materias/editar/<int:id_materia>/', views.editar_materia, name='editar_materia'),
    path('materias/eliminar/<int:id_materia>/', views.eliminar_materia, name='eliminar_materia'),


]