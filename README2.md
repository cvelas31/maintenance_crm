# Instrucciones de manejo de los servidores y bases de datos
## Base: ## 
se debe activar el environment con django y estar en la carpeta madre que en este caso es eva1
1. Para inicializar los servidores el comando a utilizar es: 
```bash
python manage.py runserver
```

2. En la carpeta static estan guardados los bootstraps las imagenes y los codigos de javascript predeterminados

3. 

4. Cada vez que se quiere adicionar algo a lo que el cliente debe suplir o en cuanto a temas en los modelos se debe utilizar el comando para actualizar el servidor:
 ```bash
 python manage.py makemigrations
 python manage.py migrate
 ```

5. para filtrar customers y hacer querys se tiene que hacer desde el cmd y dentro del primer eva1 con el siguiente comando y luego importar todos los modelos y customers se usa:
```bash
python manage.py shell
```
```python
from accounts.models import *
customers=Customer.objects.all()
```
Ya para pedidos en especificos se puede seguir la siguiente guía
https://github.com/divanov11/crash-course-CRM/blob/Part-7-Database-Queries/crm1_v7_database_queries/accounts/queryDemos.py


6. Hay que instalar pillows para ue funcione el add on de la imagen