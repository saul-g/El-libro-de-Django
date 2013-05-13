============
Introducción
============

Al comienzo de internet, los desarrolladores web escribían cada una de las páginas
a mano. Actualizar un sitio significaba editar HTML; un "rediseño" implicaba
rehacer cada una de las páginas, una por vez.

Como los sitios web crecieron y se hicieron más ambiciosos, rápidamente se hizo
obvio que esta situación era tediosa, consumía tiempo y al final era insostenible.
Un grupo de emprendedores del **NCSA** (Centro Nacional de Aplicaciones para
Supercomputadoras, donde Mosaic, el primer navegador web gráfico, fue desarrollado)
solucionó este problema permitiendo que el servidor web invocara programas externos
capaces de generar HTML dinámicamente. Ellos llamaron a este protocolo
Puerta de Enlace Común, o CGI [1]_, y esto cambió la web para siempre.

Ahora es duro imaginar la revelación que CGI debe haber sido: en vez de tratar
con páginas HTML como simples archivos del disco, CGI te permite pensar en páginas
como recursos generados dinámicamente bajo demanda. El desarrollo de CGI hace
pensar en la primera generación de página web dinámicas.

Sin embargo, CGI tiene sus problemas: los scripts CGI necesitan contener gran
cantidad de código repetitivo que los hace difícil de reutilizar, así como
complicados de entender y escribir para los desarrolladores novatos.

PHP solucionó varios de estos problemas y tomó al mundo por sorpresa --ahora es,
por lejos, la herramienta más popular usada para crear sitios web dinámicos,
y decenas de lenguajes y entornos similares (ASP, JSP, etc.) siguieron de cerca
el diseño de PHP. La mayor innovación de PHP es que es fácil de usar: el código
PHP es simple de embeber en un HTML plano; la curva de aprendizaje para algunos
que recién conocen HTML es extremadamente llana.

Pero PHP tiene sus propios problemas; por su facilidad de uso alienta a la producción
de código mal hecho. Lo que es peor, PHP hace poco para proteger a los programadores
en cuanto a vulnerabilidades de seguridad, por lo que muchos desarrolladores de PHP
se encontraron con que tenían que aprender sobre seguridad cuando ya era
demasiado tarde.

Estas y otras frustraciones similares, condujeron directamente al desarrollo de los actuales
frameworks de desarrollo web de **"tercera generación"**. Estos frameworks -- ``Django``
y ``Ruby on Rails`` parecen ser muy populares en estos días -- reconocen que la importancia
de la web se ha intensificado en los últimos tiempos. Con esta nueva explosión del
desarrollo web comienza otro incremento en la ambición; se espera que los
desarrolladores web hagan más y más cada día.

Django fue inventado para satisfacer esas nuevas ambiciones. Django te permite
construir en profundidad, de forma dinámica, sitios interesantes en un tiempo
extremadamente corto. Django está diseñado para hacer foco en la diversión, en
las partes interesantes de tu trabajo, al mismo tiempo que alivia el dolor de las
partes repetitivas. Al hacerlo, proporciona abstracciones de alto nivel de patrones
comunes del desarrollo web, atajos para tareas frecuentes de programación y claras
convenciones sobre cómo resolver problemas. Al mismo tiempo, Django intenta
mantenerse fuera de tu camino, dejando que trabajes fuera del alcance del framework cuando
es necesario. Escribimos este libro porque creemos firmemente que Django mejora el
desarrollo web. Está diseñado para poner rápidamente en movimiento tu
propio proyecto de Django, en última instancia aprenderás todo lo que necesites
saber para producir un diseño, desarrollo y despliegue de sitios satisfactorios y
de los cuales te sientas orgulloso.

Estamos extremadamente interesados en la retroalimentación. La versión online de
este libro te permite dejar un comentario en cualquier parte del libro y discutir
con otros lectores. Hacemos cuanto podemos para leer todos los comentarios
posteados allí y responder tantos como sea posible. Si prefieres utilizar correo
electrónico, por favor envíanos unas líneas (en inglés) a feedback@djangobook.com.
De cualquier modo, ¡nos encantaría escucharte! Nos alegra que estés aquí, y
esperamos que encuentres a Django tan emocionante, divertido y útil como nosotros.

.. [1] \N. del T.: Common Gateway Interface
