# Programa control mantenimiento

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