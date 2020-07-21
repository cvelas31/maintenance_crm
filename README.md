# Programa control mantenimiento

# Usuario
## Admin
- admin: farmaplast2020

# Otros
- producción1: ejemplo1
- mantenimiento1: ejemplo1

## Nomenclatura:
- Customer: Persona de producción que puede poner ordenes
- Equipment: Maquina,Equipo o molde
- Order: Ordenes de mantenimiento 

## Comandos Django
url/admin

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

### Models
Add class to models and in the 



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


caes70551987

usuarios
admin
