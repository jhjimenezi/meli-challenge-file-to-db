# MELI Challenge - Exportando datos de un archivo a la base de datos

Este proyecto comprende una aplicacion de la cual hace parte dos componentes los cuales sirven para leer un archivo csv y cargarlo en base de datos.

## Stack tecnologico
1. Docker Compose
2. Python 3.10
3. Apache Kafka
4. MySQL
5. Redis

## Como correr la aplicacion

### Prerrequisitos

1. Docker instalado
2. Python 3.10

### Pasos
Para ejecutar esta aplicacion es necesario los siguientes pasos:

1. Clonar el repositorio: ``` git clone https://github.com/jhjimenezi/meli-challenge-file-to-db.git```
2. Navegar a la carpeta raiz del proyecto y ejecutar: ```make start```
3. Una vez los contenedores esten disponibles: ejecutar ```curl -X POST http://127.0.0.1:5001/file/{nombre_archivo} ``` - esto leera el archivo precargado en el contenedor ubicado en <a href="https://github.com/jhjimenezi/meli-challenge-file-to-db/tree/master/read-file-app/resources/files">esta ruta</a>

***Para proposito de prueba se puede ejecutar el endpoint con el siguiente archivo ```http://127.0.0.1:5001/file/technical_challenge_data.csv```

### Consideraciones

La aplicacion esta configurada para una escalabilidad de 10 contenedores, en dado caso que sean necesarion incrementar o disminuir se debe cambiar las particiones del topico de Kafka y las replicas en los siguientes lugares:

1. <a href="https://github.com/jhjimenezi/meli-challenge-file-to-db/blob/master/docker-compose.yml#L79">Particiones del topico de kafka</a>
2. <a href="https://github.com/jhjimenezi/meli-challenge-file-to-db/blob/master/docker-compose.yml#L152">Replicas del contenedor</a>

Las razones de estas configuraciones seran explicada en la seccion de arquitectura

## Arquitectura

### Features faltantes

Debido a disponibilidad de tiempo no fue posible desarrollar las siguientes features y los siguientes requerimientos no funcionales:

1. Proveer un mecanismo que al colocar el archivo a procesar en un repositorio compartido, en donde sea permitido el acceso para el usuario final, se pueda capturar el evento y lanzar el proceso de carga de datos.
    #### Workaround
    Para este caso se utilizo un archivo precargado en el contenedor de la aplicacion, el cual se encuentra en <a href="https://github.com/jhjimenezi/meli-challenge-file-to-db/tree/master/read-file-app/resources/files">esta ruta</a>

2. Permitir que la carga de archivo sea asincrona, asi el endpoint no espera que el archivo se termine de leer y evitar asi la generacion de un timeout.

3. La arquitectura de aplicacion fue basada en un sistema de capas, las cuales no fueron desacopladas, esto hace que extensibilidad de la aplicacion se vea afectada, por ejemplo  agregar nuevos tipos de archivos o formatos. Esto se puede solucionar con el patron de diseño Strategy y Dependecy Inversion Principle.

4. Proveer un mecanismo de logging eficiente, en vez de usar print statements.

5. Uso de un linter para el codigo, asi como la mejora de nombramiento de variables y metodos.

6. Usar GraalVM para optimizar tamano de los contenedores y el tiempo de inicio de las aplicaciones, asi como el uso innecesario de recursos fisicos.

### Arquitectura propuesta

La arquitectura propuesta para la solucion dada los requerimientos no funcionales de escalabilidad y desempeno fue basada en Apache Kafka, Redis, MySQL y el uso de contenedores con Docker y Docker Compose.

![Project Image](/documentation/General_Schema.jpg)

#### Decisiones de Arquitectura

1. Usar libreria pandas para la lectura del archivo, la cual habilita el feature de chunks, que permite leer el archivo por batches y asi evitar el uso de memoria innecesario y en el caso de que sea un archivo muy grande, evitar que el proceso se caiga por falta de memoria.

![Project Image](/documentation/read_file_app.jpg)

2. Usar docker compose para la orquestacion de los contenedores, esto permite que la aplicacion sea facilmente escalable y portable

3. Usar Apache Kafka como broker de mensajes, esto permite que la aplicacion encargada de procesar los llamados a la API pueda ser escalada, partiendo del uso de las particiones, replicas y grupos de consumidores, lo cual habilita que si hay un tamano considerable de datos, se puedan procesar de manera paralela y asi evitar un cuello de botella en el procesamiento de los datos, incrementando el numero de consumidores y aplicaciones que procesan los mismos.

##### Particiones Vs Consumidores
En el caso de que no sea una cantidad considerable de datos, se puede usar un numero menor de consumidores o replicas que particiones configuradas en el topico de kafka, sera procesada los datos asi:

![Project Image](/documentation/Partitions_Consumers.png)

En el caso de que sea una cantidad considerable de datos, se puede usar el mismo numero de consumidores o replicas que particiones configuradas en el topico de kafka (Se pueden definir mas replicas de la aplicacion que particiones pero estas no recibiran mensajes), sera procesada la data asi:

![Project Image](/documentation/Partitions_Consumers2.png)

4. Usar Redis como cache, esto para reducir el llamada a las APIs de MELI, ya que algunos de los datos como los currencies, las categorias y los nicknames no cambian constantemente. Esto permite que la aplicacion sea mas eficiente y rapida, validando que los datos esten en REDIS antes de ir a buscarlos a las APIs de MELI, lo cual es mas demorado.

![Project Image](/documentation/proccess_file_app.jpg)

5. Usar MySQL como base de datos, esto para almacenar los datos de manera persistente y haciendo uso del query de upsert para evitar la duplicidad de datos.


