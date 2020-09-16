# Programa control mantenimiento

# SETUP
```bash
cd C:\Users\EQ01\Documents\Github\maintenance_crm
conda activate django
python manage.py runserver 0.0.0.0:8000
```
# TODOs:
- Quitar Area de los customers (Esta en grupos)
- La parte de actualizar el status solo el admin lo puede hacer (Momentaneo)
- Exportar a excel tambien la url del archivo (video, imagen, etc)
- Agregar descripcion y ultima modificación a cada.
- Agregar assigned to
- Modelo de Imagenes
  - ForeignKey Orden
  - Imagen (URL)
  - media_data/imagenes/%Y/%m/%d/nombre.png
  - Opcionales:
    - Bajarle resolución
    - Hashear (Cambiar nombre y evitar colisiones)
- Añadirlo al form de Actualizar y al de Crear.
- Modelo de videos
  - ForeignKey Orden
  - Imagen (URL)
  - media_data/imagenes/%Y/%m/%d/nombre.png
  - Opcionales:
    - Bajarle resolución
    - Hashear (Cambiar nombre y evitar colisiones)
- Añadirlo al form de Actualizar y al de Crear.
- https://stackoverflow.com/questions/60754900/connectionreseterror-while-playing-a-video-file-over-django-with-filefield-and

# Usuario
## Admin
- admin: farmaplast2020
- q12345678 psql
- Al iniciar Postgres. Hay q crear los grupos:
  - mantenimiento
  - produccion
  - admin

## Actualizar con CSS
Ctrl + F5

# Otros
- producción1: ejemplo1
- mantenimiento1: ejemplo1
- producción2: ejemplo2
- mantenimiento2: ejemplo2

## Nomenclatura:
- Customer: Persona de producción que puede poner ordenes
- Equipment: Maquina,Equipo o molde
- Order: Ordenes de mantenimiento

## Comandos Django
url/admin

### Create Admin
 ```bash
 python manage.py createsuperuser
 ```

### Ejecución del programa
 ```bash
 python manage.py runserver
 ```

### Actualizar base de datos
 Cada vez que se quiere adicionar algo a lo que el cliente debe suplir o en cuanto a temas en los modelos se debe utilizar el comando para actualizar el servidor:
 ```bash
 python manage.py makemigrations
 python manage.py migrate
 # special case python manage.py migrate --run-syncdb
 ```
 Para resetear se borra todos los .py menos el `__init__.py`

### Guardado de imagenes
Las imagenes son guardadas de acuerdo al `settings.py` 

### Models
Los modelos internos son los siguientes
- Customer: 
   - Se refiere a todas las personas que usan la aplicación (Los de producción)
   - Los attributos son los siguientes:
     - user: ID del customer
     - name: Nombre del customer
     - phone: Celular del customer
     - email: Email
     - profile_pic
     - date_created
- Representative: 
   - Se refiere a todas las personas que usan la aplicación (Los de producción)
   - Los attributos son los siguientes:
     - user: ID del customer
     - name: Nombre del customer
     - phone: Celular del customer
     - email: Email
     - profile_pic
     - date_created
- Equipment:
  - Se refiere a todos los equipos q hay molde/maquina
  - Los attributos son:
    - name
    - category: Categoria Molde o Maquina
    - description:
    - date_created:
    - tags: (TagsEquipment)
- Order:
  - Se refiere a todos los equipos q hay molde/maquina
  - Los attributos son:
    - customer: Quin puso la orden
    - equipo: Que maquina es
    - date_created:
    - status: En revisión, Abierta, Cerrada
    - order_tags: (TagsEquipment)


## Esquema
1. Seleccionar Modulo de Producción o Mantenimiento
2. Ingresar usuario de acuerdo a producción o mantenimiento

### Producción
1. Seleccionar equipo de una lista desplegable (Total 20 equipos aprox). 
2. De acuerdo al equipo seleccionado (Molde o Maquina). Se abre una interfaz para ingresar:
   1. Solicitud de mantenimiento
      - Formulario con:
        - Molde o Maquina
        - Consecutivo #
        - Fecha de Solicitud
        - Descripción del daño
        - Prioridad
        - Adjuntar fotos y/o videos
        - Usuario que reporta el daño
        - Estado de Solicitud (Abierta)
   2. Ficha tecnica equipo (Cargar tabla de base datos) En este momento esta en Excel.

### Mantenimiento
1. Consulta por maquina y/o molde
   - Ultimas solicitudes de mantenimiento (Historial) de la maquina o molde
   - Ficha tecnica (la misma para producción y mantenimiento)
2. Ordenes abiertas (Lista con breve descripción y fecha, ordenar por prioridad)
   - Se abre una orden
     - Leer descripción de producción
     - Procedimiento realizado
       - Descripción
       - Clasificación del daño (Definir tipos de daños: Ej Molde, refrigeración, lubricación, etc)
       - Repuestos usados
       - Estado de la orden (Abierta, Revisada, Cerrada)
       - Fecha y Hora de cierra de orden
       - Nombre de persona de producción a la que entrega equipo.

