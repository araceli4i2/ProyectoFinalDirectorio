from django.urls import path
from . import views

#app_name = 'reservas'

urlpatterns = [
	path('', views.home, name='home'),
    path('buscar/', views.buscar, name='buscar'),
    
    # URLs de profesores
    path('profesores/', views.listar_profesores, name='listar_profesores'),
    path('profesores/<int:id_profesor>/', views.detalle_profesor, name='detalle_profesor'),
    path('profesores/crear/', views.crear_profesor, name='crear_profesor'),
    path('profesores/editar/<int:id_profesor>/', views.editar_profesor, name='editar_profesor'),
    path('profesores/eliminar/<int:id_profesor>/', views.eliminar_profesor, name='eliminar_profesor'),
    
]
