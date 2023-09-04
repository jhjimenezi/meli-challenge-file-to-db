# MELI Challenge - Ejericicio teorico

## Procesos, hilos y corrutinas
1. Un caso en el que usarías procesos para resolver un problema y por qué.
Lo usaría para procesar gran cantidad de datos que no necesiten una relación entre ellos mismos, dado que se puede paralelizar y transformar los datos de manera independiente, un ejemplo es como funciona Apache Spark. Otro caso de uso es cuando una aplicación tiene picos de tráfico en los cuales se puede escalar para incrementar el rendimiento de la aplicación.

2. Un caso en el que usarías hilos para resolver un problema y por qué.
Lo usaría para orquestar tareas dentro de una aplicación que tiene una relación entre sí pero que su ejecución no depende entre ellos, esto ayudaría a que no se tenga que esperar a que cada proceso termine para ejecutar el siguiente, pero si se tiene que esperar a que todos los hilos terminen para que la aplicación termine, esto haría que la aplicación sea más rápida.

3. Un caso en el que usarías corrutinas para resolver un problema y por qué.
Lo usaría para cuando una aplicación tiene que leer o llamar un servicio externo, y podría procesarlo inmediatamente, en vez de esperar hacer todos los llamados y procesarlos al mismo tiempo.

## Optimización de recursos del sistema operativo

1. Si tuvieras 1.000.000 de elementos y tuvieras que consultar para cada uno de
ellos información en una API HTTP. ¿Cómo lo harías? Explicar.

Lo haría usando las estrategias que usé en el challenge de código, tomando partida de los procesos para ejecutar varios set de datos al mismo tiempo, también usaría hilos para ejecutar llamadas en paralelo a las apis para tener concurrencia en estas y no bloquear, y corrutinas para ir procesando los datos inmediatamente sin cargar al sistema con todo al mismo tiempo. El sistema de caché también lo usaría para evitar hacer llamados innecesarios a las apis.

## Análisis de complejidad

1. Dados 4 algoritmos A, B, C y D que cumplen la misma funcionalidad.

Tomaría el D - O(n log n), dado que una complejidad logarítmica sería mucho menor que las demás propuestas. 

2. Asume que dispones de dos bases de datos para utilizar en diferentes
problemas a resolver. La primera llamada AlfaDB tiene una complejidad de O(1)
en consulta y O(n2) en escritura. La segunda llamada BetaDB que tiene una
complejidad de O(log n) tanto para consulta, como para escritura. ¿Describe en
forma sucinta, qué casos de uso podrías atacar con cada una?

Usaría AlfaDB para casos donde la escritura no sea tan frecuente, pero la consulta de los datos necesita ser eficiente.

Usaría BetaDB para casos donde los datos crecen rápidamente y hay modificaciones o inserciones constantes, que necesitan ser consultadas con frecuencia, como un sistema altamente transaccional.

