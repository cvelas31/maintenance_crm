# Programa control mantenimiento

# SETUP
```bash
cd C:\Users\EQ01\Documents\Github\maintenance_crm
conda activate django
python manage.py runserver 0.0.0.0:8000
```

# Database Backup and Loaddata
TODO: This is not working properly to load data from nothing.
- Findings:
  - Cuando uno crea un supeeruser sale el issue de los grupos, de q tienen q existir desde antes
  - Con el issue de los customer, vemos q el id ya estaba incrementado y no empezaba desde 1. Habria q resetearlo completamente o como hacemos para q el Postgres quede con la data original y sus keys.
- Hyphotesis:
  - Order data
  - Foreign Key problems as table doesn't already exist
  - Use other libraries to dump and load data in a better format (https://github.com/davedash/django-fixture-magic)
  - In the original computer it worked but we only changed a single model. insert all models may have some additional issues.
  - Probar si subiendo todo a Postgres desde un CSV podria funcionar haciendo un INSERT en BATCH.

Dump data may be coded in ANSI, convert it to UTF-8 in Notepad.

- To dump database without auth permisson and without contenttypes 
```bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
```
- To dump data on natural way
```bash
python manage.py dumpdata --natural
```
- To load data: Ensure that coding is in utf-8. Convert if necessary.
```bash
python manage.py loaddata db.json
```


# TODOs:
- En admin mostrar las ordenes cerradas con la fecha de cerrado, o añadirle una pestaña en la fecha de la ultima actualización.
- Mostrar un id de cada orden
- Usuario Taller, que solo vea las ot q tengan tag taller si es posible.
- Usuarios de mantenimiento tengan la opción de buscar las ordenes como lo hace el admin. pero no de eliminar
- Dias ultima modificación (Cerrada)
- Asignar a una persona (ver si solo esa persoan la puede ver o q)
- BackUp - De la base de datos de postgres
- 
- Servidor usando docker, gunicorn y nginx para manejo de cargas
- La parte de actualizar el status solo el admin lo puede hacer (Momentaneo)
- Letra más grande en general
- Script para poder hacer analitica de las ordenes
- Agregar quien hizo ultima modificación y cuando a cada orden en tabla.
- Agregar ID de la orden para poderlo ver y hacerle tracking más fácil
- Modelo de Imagenes
  - Opcionales:
    - Bajarle resolución
- Modelo de videos
    - Bajarle resolución

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

