=================================
Capitulo 1: Introducción a Django
=================================

Este libro es sobre **Django**, un framework de desarrollo Web que ahorra
tiempo y hace que el desarrollo Web sea divertido. Utilizando Django puedes
crear y mantener aplicaciones Web de alta calidad con un mínimo esfuerzo.

En el mejor de los casos, el desarrollo Web es un acto entretenido y creativo;
en el peor, puede ser una molestia repetitiva y frustrante. Django te permite
enfocarte en la parte creativa -- la parte divertida de tus aplicaciones Web
al mismo tiempo que mitiga el esfuerzo de las partes repetitivas. De esta
forma, provee un alto nivel de abstracción de patrones comunes en el desarrollo
Web, atajos para tareas frecuentes de programación y convenciones claras sobre
cómo solucionar problemas. Al mismo tiempo, Django intenta no entrometerse,
dejándote trabajar fuera del ámbito del framework según sea necesario.

El objetivo de este libro es convertirte en un experto de Django. El enfoque
es doble.

* Primero, explicamos en profundidad lo que hace Django, y cómo crear
  aplicaciones Web con él.

* Segundo, discutiremos conceptos de alto nivel cuando se considere apropiado,
  contestando la pregunta ¿Cómo puedo aplicar estas herramientas de forma
  efectiva en mis propios proyectos?

Al leer este libro, aprenderás las habilidades necesarias para desarrollar
sitios Web conectados a una base de datos, poderosos,  de forma rápida, con
código limpio y de fácil mantenimiento.

En este capítulo presentamos  una visión general sobre Django.

Un poco de historia
===================

Al comienzo de internet, los desarrolladores Web escribían cada una de las
páginas a mano. Actualizar un sitio significaba editar HTML; un "rediseño"
implicaba rehacer cada una de las páginas, una a la vez.

Como los sitios Web crecieron y se hicieron más ambiciosos, rápidamente se hizo
evidente  que esta situación era tediosa, consumía tiempo y al final era
insostenible.  Un grupo de emprendedores del *NCSA* (Centro Nacional de
Aplicaciones para Supercomputadoras, donde se desarrollo el  Mosaic; el primer
navegador Web gráfico) solucionó este problema permitiendo que el servidor Web
invocara programas externos capaces de generar HTML dinámicamente.
Ellos llamaron a este protocolo "Puerta de Enlace Común", o CGI [1]_, y esto
cambió internet para siempre.

Ahora es difícil imaginar la revelación que CGI debe haber sido: en vez de
tratar con páginas HTML como simples archivos del disco, CGI te permite pensar
en páginas como recursos generados dinámicamente bajo demanda. El desarrollo de
CGI hace pensar en la primera generación de página Web dinámicas.

Sin embargo, CGI tiene sus problemas: los scripts CGI necesitan contener gran
cantidad de código repetitivo que los hace difícil de reutilizar, así como
complicados de entender y escribir para los desarrolladores novatos.

PHP solucionó varios de estos problemas y tomó al mundo por sorpresa --ahora es,
por lejos, la herramienta más popular usada para crear sitios Web dinámicos,
y decenas de lenguajes y entornos similares (ASP, JSP, etc.) siguieron de cerca
el diseño de PHP. La mayor innovación de PHP es que es fácil de usar: el código
PHP es simple de embeber en un HTML plano; la curva de aprendizaje para algunos
que recién conocen HTML es extremadamente llana.

Pero PHP tiene sus propios problemas; por su facilidad de uso,  alienta a la
producción de código mal hecho. Lo que es peor, PHP hace poco para proteger a
los programadores en cuanto a vulnerabilidades de seguridad, por lo que muchos
desarrolladores de PHP se encontraron con que tenían que aprender sobre
seguridad cuando ya era demasiado tarde.

Estas y otras frustraciones similares, condujeron directamente al desarrollo de
los actuales frameworks de desarrollo Web de **"tercera generación"**.
Estos frameworks  ``Django`` y ``Ruby on Rails`` -- parecen ser muy populares
en estos días -- reconocen que la importancia de la Web se ha intensificado en
los últimos tiempos. Con esta nueva explosión del desarrollo Web comienza otro
incremento en la ambición; se espera que los desarrolladores Web hagan más y más
cada día.

Django fue desarrollado para satisfacer esas nuevas ambiciones. Django te permite
construir en profundidad, de forma dinámica, sitios interesantes en un tiempo
extremadamente corto. Django está diseñado para hacer foco en la diversión, en
las partes interesantes de tu trabajo, al mismo tiempo que alivia el dolor de
las partes repetitivas. Al hacerlo, proporciona abstracciones de alto nivel a
patrones comunes del desarrollo Web, agrega atajos para tareas frecuentes de
programación y claras convenciones sobre cómo resolver problemas. Al mismo
tiempo, intenta mantenerse fuera de tu camino, dejando que trabajes fuera del
alcance del framework cuando sea necesario. Escribimos este libro porque creemos
firmemente que Django mejora el desarrollo Web. Está diseñado para poner
rápidamente en movimiento tu propio proyecto de Django, en última instancia
aprenderás todo lo que necesites saber para producir un diseño, desarrollo y
despliegue de sitios satisfactorios y de los cuales te sientas orgulloso.

Estamos extremadamente interesados en la retroalimentación. La versión online de
este libro te permite dejar un comentario en cualquier parte del libro y
discutir con otros lectores. Hacemos cuanto podemos para leer todos los
comentarios posteados allí y responder tantos como nos sea posible. Si prefieres
utilizar correo electrónico, por favor envíanos unas líneas (en inglés) a
feedback@djangobook.com. De cualquier modo, ¡nos encantaría escucharte! Nos
alegra que estés aquí, y esperamos que encuentres a Django tan emocionante,
divertido y útil como nosotros.


¿Qué es un Framework Web?
=========================

Django es un miembro importante de una nueva generación de **frameworks Web**.
*¿Pero qué significa este término exactamente?*

Para contestar esa pregunta, consideremos el diseño de una aplicación Web
escrita  en Python, *sin usar* un framework. A lo largo del libro,  trataremos
de aprovechar la forma básica de mostrarte como  empezar a trabajar, *si usar*
atajos, con la esperanza de que reconozcas lo útil que son los atajos. El valor
de conocer como se hacen las cosas, sin usar atajos, es que  estos no siempre
están disponibles. Y una de las cosas mas importantes que debes conocer, es
*porque* se  trabaja de forma que seas un  mejor desarrollador Web.

Una de las formas mas simples y directas para construir una aplicación Web
desde cero en python, es usando el estándar Common Gateway Interface (CGI),
una  técnica muy popular para escribir aplicaciones Web alrededor del año 1998.
Esta es una explicación de alto nivel sobre como trabaja. Solo  crea un script
Python, que produzca HTML, guarda el script en el servidor Web con la
extensión .cgi y visita la pagina con un navegador Web. Eso ¡Eso todo!

Por ejemplo, aquí hay un  sencillo script CGI, escrito en Python, que muestra
los diez últimos  libros  publicados  recientemente en una base de datos.
No te preocupes por los detalles de la  sintaxis; solo observa las cosas
básicas que hace:

.. code-block:: python

    #!/usr/bin/env python

    import MySQLdb

    print "Content-Type: text/html\n"
    print "<html><head><title>Libros</title></head>"
    print "<body>"
    print "<h1>Libros</h1>"
    print "<ul>"

    connection = MySQLdb.connect(user='yo', passwd='dejamentrar', db='books.db')
    cursor = connection.cursor()
    cursor.execute("SELECT nombre FROM libros ORDER BY fecha DESC LIMIT 10")

    for row in cursor.fetchall():
        print "<li>%s</li>" % row[0]

    print "</ul>"
    print "</body></html>"

    connection.close()

Este código es sencillo  de entender. Primero imprime una línea de
“Content-Type”, seguido de una línea en blanco, tal como requiere CGI. Imprime
el HTML introductorio, se conecta a la base de datos y ejecuta una consulta
que obtiene los diez libros más recientes, de una tabla llamada libros. Hace un
bucle sobre esos libros y genera una lista HTML desordenada. Finalmente imprime
el código para cerrar el HTML y cierra la conexión con la base de datos.

Con una página única y poco dinámica como esta, el enfoque desde cero no es
necesariamente malo. Por un lado, este código es sencillo de comprender
-- incluso un desarrollador novato puede leer estas 16 líneas de Python y
entender todo lo que hace el script, de principio a fin. No hay más nada
que  aprender; no hay más código para leer. También es sencillo de utilizar:
sólo guarda este código en un archivo llamado ``ultimoslibros.cgi``,  sube ese
archivo a un servidor Web y visita esa página con un navegador.

Sin embargo a medida que una aplicación Web crece más allá de lo trivial, este
enfoque se desmorona y te enfrentas a una serie de problemas:

* *¿Qué sucede cuando múltiples páginas necesitan conectarse a la base de
  datos?* Seguro que ese código de conexión a la base de datos no debería
  estar duplicado en cada uno de los scripts CGI, así que la forma pragmática
  de hacerlo sería refactorizarlo en una función compartida.

* *¿Debería un desarrollador realmente tener que preocuparse por imprimir la
  línea de “Content-Type” y acordarse de cerrar la conexión con la base de
  datos?*  Este tipo de código repetitivo reduce la productividad del
  programador e introduce la oportunidad para que se cometan errores. Estas
  tareas de configuración y cierre estarían mejor manejadas por una
  infraestructura común.

* *¿Qué sucede cuando este código es reutilizado en múltiples entornos, cada
  uno con una base de datos y contraseñas diferentes?* En ese punto, se vuelve
  esencial alguna configuración específica del entorno.

* *¿Qué sucede cuando un diseñador Web que no tiene experiencia programando en
  Python desea rediseñar la página?* Lo ideal sería que la lógica de la página
  -- la búsqueda de libros en la base de datos – esté separada del código HTML
  de la página, de modo que el diseñador pueda hacer modificaciones sin
  afectar la búsqueda.

Precisamente estos son los problemas que un framework Web intenta resolver. Un
framework Web provee una infraestructura de programación para tus
aplicaciones, para que puedas concentrarte en escribir código limpio y de
fácil mantenimiento sin tener que reinventar la rueda.  En resumidas cuentas,
eso es lo que hace Django.

El patrón de diseño MVC
=======================

Comencemos con un ejemplo rápido,  que demuestra la diferencia entre el
enfoque anterior y el empleado al usar un framework Web. Así es como se podría
escribir el código CGI anterior usando Django:

.. snippet::
   :filename: models.py

   from django.db import models
   '''Las tablas de la base de datos'''

   class Libro(models.Model):
       nombre = models.CharField(maxlength=50)
       fecha = models.DateField()

.. snippet::
   :filename: views.py

   from django.shortcuts import render_to_response
   from models import Libro

   def ultimos_libros(request):
       '''La parte lógica'''

       lista_libros = Libro.objects.order_by('-fecha')[:10]
       return render_to_response('ultimos-libros.html', {'lista_libros': lista_libros})

.. snippet::
   :filename: urls.py

   from django.conf.urls import url
   import views

   # La configuración URL
   urlpatterns = [
       url(r'^ultimos_libros/$', views.ultimos_libros),
    ]

.. snippet:: html+django
   :filename: ultimos-libros.html

   {# La plantilla #}
   <html><head><title>Libros</title></head>
   <body>
   <h1>Libros</h1>
   <ul>
       {% for libro in lista_libros %}
           <li>{{ libro.nombre }}</li>
       {% endfor %}
   </ul>
   </body></html>

No es todavía necesario preocuparse por los detalles sobre cómo funciona esto
-- tan sólo queremos que te acostumbres al diseño general. Lo que hay que
notar principalmente en este ejemplo,  son las *cuestiones de separación*:

* El archivo ``models.py``  contiene una descripción de la tabla de la base de
  datos, como una clase Python. A esto se lo llama el *modelo*. Usando esta
  clase se pueden crear, buscar, actualizar y borrar entradas de tu base de
  datos usando solo código Python  en lugar de escribir declaraciones SQL
  repetitivas.

* El archivo ``views.py`` contiene la lógica de la página, en la función
  ``ultimos_libros()`` . A esta función se la denomina *vista*.

* El archivo ``urls.py`` especifica qué vista es llamada según el patrón URL.
  En este caso, la URL ``/ultimos_libros/``  será manejada por la función
  ``ultimos_libros()``. En otras  palabras, si el nombre de nuestro dominio  es
  example.com, cualquier visita a la URL http://example.com/ultimos_libros/
  llamara a   la función ``ultimos_libros()``.

* El archivo ``ultimos_libros.html`` es una plantilla HTML especial, que
  describe el diseño de la página. Usa el lenguaje de plantillas de Django, con
  declaraciones básicas y lógicas por ejemplo: ``{% for libro in lista_libros %}``.

Tomadas en su conjunto, estas piezas se aproximan al patrón de diseño
Modelo-Vista-Controlador (MVC). Dicho de manera más fácil, MVC define una forma
de desarrollar software en la que el código para definir y acceder a los datos
(el modelo) está separado del pedido lógico de asignación de ruta
(el controlador), que a su vez está separado de la interfaz del usuario
(la vista).

Una ventaja clave de este enfoque es que los componentes tienen un *acoplamiento
débil*  entre sí. Eso significa que cada pieza de la aplicación Web que funciona
sobre Django tiene un único propósito clave, que puede ser modificado
independientemente sin afectar las otras piezas. Por ejemplo, un desarrollador
puede cambiar la URL de cierta parte de la aplicación sin afectar la
implementación subyacente. Un diseñador puede cambiar el HTML de una página sin
tener que tocar el código Python que la renderiza. Un administrador de base de
datos puede renombrar una tabla de la base de datos y especificar el cambio en
un único lugar, en lugar de tener que buscar y reemplazar en varios archivos.

En este libro, cada componente tiene su propio capítulo. Por ejemplo,
el :doc:`capitulo 3<chapter03>` trata sobre las vistas, el
:doc:`capitulo 4<chapter04>` sobre las plantillas  y el
:doc:`capitulo 5<chapter05>` sobre los modelos.

La historia de Django
=====================

Antes de empezar a escribir código, deberíamos tomarnos un momento para explicar
la historia de Django. Y para mostrar como se hacen las cosas *sin* usar atajos,
esto nos ayudara a entenderlos mejor. Es útil entender *por qué* se creó el
framework, ya que el conocimiento de la historia pone en contexto la razón por
la cual Django trabaja de la forma en que lo hace.

Si has estado creando aplicaciones Web por un tiempo, probablemente estés
familiarizado con los problemas del ejemplo CGI presentado con anterioridad.
El camino clásico de un desarrollador Web es algo como esto:

#. Escribir una aplicación Web desde cero.
#. Escribir otra aplicación Web desde cero.
#. Darse cuenta de que la aplicación del paso, 1 tiene muchas cosas en común
   con la aplicación del paso 2.
#. Refactorizar el código para que la aplicación 1,  comparta código con la
   aplicación 2.
#. Repetir los pasos 2-4 varias veces.
#. Darse cuenta de que acabamos de inventar un framework.

Así es precisamente como surgio Django.

Django nació naturalmente de aplicaciones de la vida real escritas por un equipo
de desarrolladores Web en Lawrence, Kansas. Nació en el otoño boreal de 2003,
cuando los programadores Web del diario *Lawrence Journal-World*,
Adrian Holovaty y Simon Willison, comenzaron a usar Python para crear sus
aplicaciones.

El equipo de The World Online, responsable de la producción y mantenimiento de
varios sitios locales de noticias, prosperaban en un entorno de desarrollo
dictado por las fechas límite del periodismo. Para los sitios --incluidos
LJWorld.com, Lawrence.com y KUsports.com los periodistas (y los directivos)
exigían que se agregaran nuevas características y que aplicaciones enteras se
crearan a una velocidad vertiginosa, a menudo con sólo días u horas de preaviso.
Es así que Adrian y Simon desarrollaron por necesidad un framework de desarrollo
Web que les ahorrara tiempo -- era la única forma en que podían crear
aplicaciones mantenibles en tan poco tiempo.

En el verano de 2005, luego de haber desarrollado este framework hasta el punto
en que estaba haciendo funcionar la mayoría de los sitios de World Online, el
equipo de World Online, que ahora incluía a Jacob Kaplan-Moss, decidió liberar
el framework como software de código abierto. Lo liberaron en julio de 2005 y
lo llamaron Django, por el guitarrista de jazz "Django Reinhardt".

Hoy en día, Django es un proyecto estable y maduro,  de código abierto con
cientos de miles de colaboradores y usuarios de todo el mundo. Dos de los
desarrolladores originales  de Worl Online ("Los benevolentes dictadores
vitalicios" Adrian y Jacob) siguen aportando una guía centralizada para el
crecimiento del framework, por lo que es mas un equipo de colaboración
comunitario.

Esta historia es relevante porque ayuda a explicar dos cuestiones clave. La
primera es el “punto dulce” de Django. Debido a que Django nació en un entorno
de noticias, ofrece varias características (en particular la interfaz
administrativa, tratada en el :doc:`capitulo 6<chapter06>` ,  que son
particularmente apropiadas para sitios de “contenido” -- sitios como eBay,
craigslist.org y washingtonpost.com que ofrecen información basada en bases de
datos. (De todas formas, no dejes que eso te quite las ganas a pesar de que
Django es particularmente bueno para desarrollar esa clase de sitios, eso no
significa que no sea una herramienta efectiva para crear cualquier tipo de sitio
Web dinámico. Existe una gran diferencia entre ser *particularmente efectivo*
para algo y *no ser particularmente efectivo* para otras cosas).

La segunda cuestión a resaltar es cómo los orígenes de Django le han dado forma
a la cultura de su comunidad de código abierto. Debido a que Django fue extraído
de código de la vida real, en lugar de ser un ejercicio académico o un producto
comercial, está especialmente enfocado en resolver problemas de desarrollo Web
con los que los desarrolladores de Django se han encontrado -- y con los que
continúan encontrándose. Como resultado de eso, Django es continuamente
mejorado. Los desarrolladores del framework tienen un alto grado de interés en
asegurarse de que Django les ahorre tiempo a los desarrolladores, produzca
aplicaciones que sean fáciles de mantener y rindan bajo mucha carga. Aunque
existen otras razones, los desarrolladores están motivados por sus propios
deseos egoístas de ahorrarse tiempo a ellos mismos y disfrutar de sus trabajos.

Cómo leer este libro
=====================

Al escribir este libro, tratamos de alcanzar un balance entre legibilidad y
referencia, con una tendencia a la legibilidad. Nuestro objetivo, como se
mencionó anteriormente, es hacerte un experto en Django, y creemos que la mejor
manera de enseñar es a través de la prosa y numerosos ejemplos, en vez de
proveer un exhaustivo pero inútil catálogo de las características de Django
(Como alguien dijo una vez, no puedes esperar enseñarle a alguien cómo hablar
simplemente enseñándole el alfabeto).

Con esto en mente, te recomendamos que leas los capítulos del 1 al 7 en orden.
Ellos forman los fundamentos básicos sobre la forma en que se usa Django; una
vez que los hayas leído, serás capaz de construir sitios Web que funcionen
sobre Django. Los capítulos 7 al 12, muestran característica avanzadas del
framework, los capítulos restantes, están enfocados en características
específicas de Django y  pueden ser leídos en cualquier orden.

Los apéndices son para referencia. Que  junto a la documentación libre disponible
en http://www.djangoproject.com/, son probablemente los documentos que tendrás
que leer de vez en  cuando,  para recordar la sintaxis o buscar un resumen
rápido de lo que hacen ciertas partes de Django, no explicadas aquí.

Conocimientos de programación requeridos
----------------------------------------

Los lectores de este libro deben comprender las bases de la programación
orientada a objetos e imperativa: estructuras de control  (por ejemplo: ``if``,
``while``, ``for``)), estructuras de datos (listas, hashes/diccionarios),
variables, clases y objetos.

La experiencia en desarrollo Web es, como podrás esperar, muy útil, pero no es
requisito para leer este libro. A lo largo del mismo, tratamos de promover las
mejores prácticas en desarrollo Web para los lectores a los que les falta este
tipo de experiencia.

Conocimientos de Python requeridos
----------------------------------

En esencia, Django es sencillamente una colección de bibliotecas escritas en el
lenguaje de programación Python. Para desarrollar un sitio usando Django
escribes código Python que utiliza esas bibliotecas. Aprender Django, entonces,
es sólo cuestión de aprender a programar en Python y comprender cómo funcionan
las bibliotecas de Django.

Si tienes experiencia programando en Python, no deberías tener problema en
meterte de lleno. En conjunto, el código Django no produce “magia negra”
(es decir, trucos de programación cuya implementación es difícil de explicar o
entender). Para ti, aprender Django será sólo cuestión de aprender las
convenciones y APIs de Django.

Si no tienes experiencia programando en Python, te espera una grata sorpresa.
Es fácil de aprender y muy divertido de usar. A pesar de que este libro no
incluye un tutorial completo de Python, sí hace hincapié en las características
y funcionalidades de Python cuando se considera apropiado, particularmente
cuando el código no cobra sentido de inmediato. Aún así, recomendamos leer el
tutorial oficial de Python, disponible en
http://pyspanishdoc.sourceforge.net/tut/tut.html o su versión más reciente en
inglés en http://docs.python.org/tut/. También recomendamos el libro libre y
gratuito de Mark Pilgrim *Inmersión en Python*, disponible en
http://es.diveintopython.org/ y publicado en inglés en papel por Apress.

Version requerida de Django
---------------------------

Este libro cubre la version 2.0

El equipo de  desarrolladores de Django, trata en la medida de lo posible de
mantener compatibilidad con versiones anteriores,  sin embargo ocasionalmente,
se  introducen algunos  cambios drásticos e incompatibles con versiones
anteriores. En cada lanzamiento estos cambios son cubiertos en las notas del
lanzamiento, que se pueden encontrar en:
https://docs.djangoproject.com/en/dev/releases/2.X

Nuevas características de Django
--------------------------------

Tal como mencionamos  anteriormente, Django es mejorado con frecuencia, y
probablemente tendrá un gran número de nuevas -- e incluso esenciales
características para cuando este libro sea publicado. Por ese motivo, nuestro
objetivo como autores de este libro es doble:

* Asegurarnos que este libro sea “a prueba de tiempo” tanto como nos sea
  posible, para que cualquier cosa que leas aquí todavía sea relevante en
  futuras versiones de Django.

* Actualizar este libro continuamente en el sitio Web en inglés,
  http://www.djangobook.com/, para que puedas acceder a la mejor y más reciente
  documentación tan pronto como la escribamos.

Si quieres implementar con Django algo que no está explicado en este libro,
revisa la versión más reciente de este libro en el
`sitio Web <http://github.com/saulgm/djangobook.com>`_  y también revisa
la documentación oficial de Django, para obtener detalles mas completos.

Obtener  ayuda
--------------

Para obtener  ayuda con cualquier aspecto de Django -- desde instalación y
diseño de aplicaciones, hasta diseño de bases de datos e implementaciones
siéntete libre de hacer preguntas online.

En la lista de correo de usuarios de Django (en inglés) se juntan miles de
usuarios para preguntar y responder dudas. Suscríbete gratuitamente en
http://www.djangoproject.com/r/django-users.

El canal de IRC de Django donde los usuarios de Django se juntan a chatear y se
ayudan unos a otros en tiempo real. Únete a la diversión en #django (inglés) o
#django-es (español) en la red de IRC Freenode.

¿Qué sigue?
-----------

A continuación, en el :doc:`capitulo 2<chapter02>` utilizaremos Django,
explicaremos su instalación y la configuración inicial.

.. [1] \N. del T.: Common Gateway Interface

.. OK

