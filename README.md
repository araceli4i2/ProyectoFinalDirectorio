## Proyecto Final: Directorio de profesores
### ProgramacionWeb III inf-133
## 📋 Tabla de Contenidos

1. [Integrantes](#-Integrantes)
2. [Acerca del Proyecto](#-acerca-del-proyecto)
3. [Estructura](#-estructura-del-proyecto)
4. [Instalación y Configuración](#-instalación-y-configuración)
5. [Uso y Ejecución](#-uso-y-ejecución)


</br>
## 🙋‍♂️ Integrantes
</br>
Arze Cachi Kevin Fabrizio         C.I. : 78785809<br>
Duran Alipaz Deysly Beatriz         C.I. : 64388344<br>
Herrera Bonilla Thaime Helen         C.I. : 72053905<br>
Raquel Araceli Serrano Mamani         C.I. : 9250244<br>
Zamora Paredes Amilcar Brandon         C.I. : 14793345<br>

<br>
## Acerca del Proyecto
## 🌲 Estructura
<br>

````
ª   README.md
ª   
+---directorio_profesores
ª   ª   manage.py
ª   ª   requirements.txt
ª   ª   
ª   +---directorio_profesores
ª   ª   ª   asgi.py
ª   ª   ª   settings.py
ª   ª   ª   urls.py
ª   ª   ª   wsgi.py
ª   ª   ª   __init__.py
ª   ª   ª   
ª   ª   +---__pycache__
ª   ª           
ª   +---reservas
ª       ª   admin.py
ª       ª   apps.py
ª       ª   models.py
ª       ª   tests.py
ª       ª   views.py
ª       ª   __init__.py
ª       ª   
ª       +---migrations     
ª       +---__pycache__
ª               
+---env
````
<br>
## 🌲 Instalación y Configuración
</br>

*1.- Clonar Repositorio* (Recomendacióm: clonalo en una carpeta vacia) </br>
git clone https://github.com/araceli4i2/ProyectoFinalDirectorio.git </br>
*2.- Entronno Virtual*</br>
python -m venv env</br>
.\env\Scripts\activate</br>
*3.- Instalación de Dependencias* <br> 
pip install -r requirements.txt</br>

<br>
## 🎲 Uso y Ejecución
</br>
1.- Migraciones </br>
python manage.py makemigrations</br>
python manage.py migrate</br>

2.- Iniciar el servidor</br>
py manage.py runserver</br>




