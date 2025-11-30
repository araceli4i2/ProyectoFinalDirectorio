# 📚 Proyecto Final: Directorio de Profesores

### ProgramacionWeb III INF-133

---

## 📋 Tabla de Contenidos

1. [Integrantes](#integrantes)
2. [Acerca del Proyecto](#acerca-del-proyecto)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Uso y Ejecución](#uso-y-ejecución)



## Integrantes

Este proyecto fue desarrollado por:

* **Arze Cachi Kevin Fabrizio** — C.I.: 10017630
* **Duran Alipaz Deysly Beatriz** — C.I.: 13502101 
* **Herrera Bonilla Thaime Helen** — C.I.: 12394581
* **Raquel Araceli Serrano Mamani** — C.I.: 9250244
* **Zamora Paredes Amilcar Brandon** — C.I.: 14793345



## Acerca del Proyecto




### Estructura del Proyecto

La estructura de directorios principal es la siguiente:
```branch
📦directorio_profesores
 ┣ 📂directorio_profesores
 ┃ ┣ 📂__pycache__
 ┃ ┣ 📜asgi.py
 ┃ ┣ 📜settings.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜wsgi.py
 ┃ ┗ 📜__init__.py
 ┃
 ┣ 📂reservas
 ┃ ┣ 📂migrations
 ┃ ┣ 📂Templates
 ┃ ┃ ┣ 📂reservas
 ┃ ┃ ┃ ┣ 📜403.html
 ┃ ┃ ┃ ┣ 📜agregar_resena.html
 ┃ ┃ ┃ ┣ 📜buscar.html
 ┃ ┃ ┃ ┣ 📜confirmar_eliminar.html
 ┃ ┃ ┃ ┣ 📜crear_profesor.html
 ┃ ┃ ┃ ┣ 📜detalle_materia.html
 ┃ ┃ ┃ ┣ 📜detalle_profesor.html
 ┃ ┃ ┃ ┣ 📜editar_profesor.html
 ┃ ┃ ┃ ┣ 📜home.html
 ┃ ┃ ┃ ┣ 📜lista_materias.html
 ┃ ┃ ┃ ┣ 📜lista_profesores.html
 ┃ ┃ ┃ ┣ 📜login.html
 ┃ ┃ ┃ ┣ 📜mis_reservas.html
 ┃ ┃ ┃ ┣ 📜registro.html
 ┃ ┃ ┃ ┗ 📜solicitar_clase.html
 ┃ ┃ ┗ 📜base.html
 ┃ ┃
 ┃ ┣ 📂__pycache__
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜forms.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┗ 📜manage.py
````

### Instalación y Configuración

Sigue estos pasos para poder clonar el proyecto:

### Clonar el Repositorio

```bash
git clone https://github.com/araceli4i2/ProyectoFinalDirectorio.git
cd ProyectoFinalDirectorio
````

## Uso y Ejecución
### 1. Base de Datos y Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```
### 2. Iniciar el Servidor
```bash
python manage.py runserver
```





