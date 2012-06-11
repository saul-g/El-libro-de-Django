=================================
Capítulo 1: Introducción a Django
=================================

Este libro es sobre Django, un framework de desarrollo Web que ahorra tiempo y
hace que el desarrollo Web sea divertido. Utilizando Django puedes crear y
mantener aplicaciones Web de alta calidad con un mínimo esfuerzo.

En el mejor de los casos, el desarrollo web es un acto entretenido y creativo;
en el peor, puede ser una molestia repetitiva y frustrante. Django te permite
enfocarte en la parte creativa -- la parte diverida de tus aplicaciones Web -- al mismo
tiempo que mitiga el esfuerzo de las partes repetitivas. De esta forma, provee
un alto nivel de abstracción de patrones comunes en el desarrollo Web, atajos
para tareas frecuentes de programación y convenciones claras sobre cómo
solucionar problemas. Al mismo tiempo, Django intenta no entrometerse, dejándote
trabajar fuera del ámbito del framework según sea necesario.

El objetivo de este libro es convertirte en un experto de Django. El enfoque es
doble. Primero, explicamos en profundidad lo que hace Django, y cómo crear
aplicaciones Web con él. Segundo, discutiremos conceptos de alto nivel cuando
se considere apropiado, contestando la pregunta "¿Cómo puedo aplicar estas
herramientas de forma efectiva en mis propios proyectos?" Al leer este libro,
aprenderás las habilidades necesarias para desarrollar sitios Web poderosos de
forma rápida, con código limpio y de fácil mantenimiento.

En este capítulo ofrecemos una visión general de Django.

¿Qué es un Framework Web?
=========================

Django es un miembro importante de una nueva generación de *frameworks Web*.
¿Y qué significa ese término exactamente?

Para contestar esa pregunta, consideremos el diseño de una aplicación Web
escrita usando el estándar Common Gateway Interface (CGI), una forma popular de
escribir aplicaciones Web alrededor del año 1998. En esa época, cuando escribías
una aplicación CGI, hacías todo por ti mismo -- el equivalente a hacer una torta
desde cero --. Por ejemplo, aquí hay un script CGI sencillo, escrito en Python,
que muestra los diez libros más recientemente publicados de una base de datos::

    #!/usr/bin/python

    import MySQLdb

    print "Content-Type: text/html"
    print
    print "<html><head><title>Libros</title></head>"
    print "<body>"
    print "<h1>Los ultimos 10 libros</h1>"
    print "<ul>"

    conexion = MySQLdb.connect(user='yo', passwd='dejame_entrar', db='mi_base')
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre FROM libros ORDER BY fecha_pub DESC LIMIT 10")
    for fila in cursor.fetchall():
        print "<li>%s</li>" % fila[0]

    print "</ul>"
    print "</body></html>"

    conexion.close()

Este código es fácil de entender. Primero imprime una línea de "Content-Type",
seguido de una línea en blanco, tal como requiere CGI. Imprime HTML introductorio,
se conecta a la base de datos y ejecuta una consulta que obtiene los diez
libros más recientes. Hace un bucle sobre esos libros y genera una lista HTML desordenada.
Finalmente imprime el código para cerrar el HTML y cierra la conexión con la base de datos.

Con una única página dinámica como esta, el enfoque desde cero no es necesariamente malo.
Por un lado, este código es sencillo de comprender -- incluso un desarrollador
novato puede leer estas 16 líneas de Python y entender todo lo que hace,
de principio a fin --. No hay más nada que aprender; no hay más código para leer.
También es sencillo de utilizar: tan sólo guarda este código en un archivo llamado
``ultimoslibros.cgi``, sube ese archivo a un servidor Web y visita esa página con un navegador.

Pero a medida que una aplicación Web crece más allá de lo trivial, este enfoque
se desmorona y te enfrentas a una serie de problemas:

* ¿Qué sucede cuando múltiples páginas necesitan conectarse a la base de datos?
  Seguro que ese código de conexión a la base de datos no debería estar duplicado
  en cada uno de los scripts CGI, así que la forma pragmática de hacerlo sería
  refactorizarlo en una función compartida.

* ¿Debería un desarrollador *realmente* tener que preocuparse por imprimir
  la línea de "Content-Type" y acordarse de cerrar la conexión con la base de datos?
  Este tipo de código repetitivo reduce la productividad del programador e
  introduce la oportunidad para que se cometan errores. Estas tareas de configuración y
  cierre estarían mejor manejadas por una infraestructura común.

* ¿Qué sucede cuando este código es reutilizado en múltiples entornos,
  cada uno con una base de datos y contraseñas diferentes? En ese punto,
  se vuelve esencial alguna configuración específica del entorno.

* ¿Qué sucede cuando un diseñador Web que no tiene experiencia programando
  en Python desea rediseñar la página? Lo ideal sería que la lógica de la página
  -- la búsqueda de libros en la base de datos -- esté separada del código HTML
  de la página, de modo que el diseñador pueda hacer modificaciones sin afectar
  la búsqueda.

Precisamente estos son los problemas que un framework Web intenta
resolver. Un framework Web provee una infraestructura de programación para tus
aplicaciones, para que puedas concentrarte en escribir código limpio y de fácil
mantenimiento sin tener que reinventar la rueda. En resumidas cuentas,
eso es lo que hace Django.

El patrón de diseño MVC
=======================

Comencemos con un rápido ejemplo que demuestra la diferencia entre el enfoque
anterior y el empleado al usar un framework Web. Así es como se podría escribir
el código CGI anterior usando Django:

.. code-block:: python

    # models.py (las tablas de la base de datos)

    from django.db import models

    class Book(models.Model):
        name = models.CharField(maxlength=50)
        pub_date = models.DateField()
        
.. code-block:: python

    # views.py (la parte lógica)

    from django.shortcuts import render_to_response
    from models import Book

    def latest_books(request):
        book_list = Book.objects.order_by('-pub_date')[:10]
        return render_to_response('latest_books.html', {'book_list': book_list})

.. code-block:: python

    # urls.py (la configuración URL)

    from django.conf.urls.defaults import *
    import views

    urlpatterns = patterns('',
        (r'latest/$', views.latest_books),
    )


.. code-block:: html

    # latest_books.html (la plantilla)

    <html><head><title>Books</title></head>
    <body>
    <h1>Books</h1>
    <ul>
    {% for book in book_list %}
    <li>{{ book.name }}</li>
    {% endfor %}
    </ul>
    </body></html>

Todavía no es necesario preocuparse por los detalles de *cómo* funciona esto --
tan sólo queremos que te acostumbres al diseño general --. Lo que hay que notar
principalmente en este caso son las *cuestiones de separación*:

* El archivo ``models.py`` contiene una descripción de la tabla de la base
  de datos, como una clase Python. A esto se lo llama el *modelo*. Usando esta
  clase se pueden crear, buscar, actualizar y borrar entradas de tu base de
  datos usando código Python sencillo en lugar de escribir declaraciones
  SQL repetitivas.

* El archivo ``views.py`` contiene la lógica de la página, en la función
  ``latest_books()``. A esta función se la denomina vista.

* El archivo ``urls.py`` especifica qué vista es llamada según el patrón URL.
  En este caso, la URL ``/latest/`` será manejada por la función
  ``latest_books()``.

* El archivo ``latest_books.html`` es una plantilla HTML que describe el
  diseño de la página.

Tomadas en su conjunto, estas piezas se aproximan al patrón de diseño 
Modelo-Vista-Controlador (MVC). Dicho de manera más fácil, MVC define una forma de
desarrollar software en la que el código para definir y acceder a los datos
(el modelo) está separado del pedido lógico de asignación de ruta (el controlador),
que a su vez está separado de la interfaz del usuario (la vista).

Una ventaja clave de este enfoque es que los componentes tienen un acoplamiento
débil (N. de T.: por *loosely coupled*) entre sí. Eso significa que cada pieza de la aplicación Web que 
funciona sobre Django tiene un único propósito clave, que puede ser
modificado independientemente sin afectar las otras piezas. Por ejemplo, un
desarrollador puede cambiar la URL de cierta parte de la aplicación sin afectar
la implementación subyacente. Un diseñador puede cambiar el HTML de una página
sin tener que tocar el código Python que la renderiza. Un administrador de base
de datos puede renombrar una tabla de la base de datos y especificar el cambio
en un único lugar, en lugar de tener que buscar y reemplazar en varios archivos.

En este libro, cada componente tiene su propio capítulo. Por ejemplo, el
:doc:`Capítulo 3<chapter03>` trata sobre las vistas, el :doc:`Capítulo 4<chapter04>` sobre las plantillas, y el
:doc:`Capítulo 5<chapter05>` sobre los modelos. El :doc:`Capítulo 5<chapter05>`  profundiza también en la
filosofía MVC de Django.

La historia de Django
=====================

Antes de continuar con más código, deberíamos tomarnos un momento para explicar
la historia de Django. Es útil entender por qué se creó el framework, ya que el
conocimiento de la historia pone en contexto la razón por la cual Django trabaja
de la forma en que lo hace.

Si has estado creando aplicaciones Web por un tiempo, probablemente estés
familiarizado con los problemas del ejemplo CGI presentado con anterioridad.
El camino clásico de un desarrollador Web es algo como esto:

1. Escribir una aplicación Web desde cero.
2. Escribir otra aplicación Web desde cero.
3. Darse cuenta de que la aplicación del paso 1 tiene muchas
   cosas en común con la aplicación del paso 2.
4. Refactorizar el código para que la aplicación 1 comparta código con la
   aplicación 2.
5. Repetir los pasos 2-4 varias veces.
6. Darse cuenta de que acabamos  de inventar un framework.

Así es precisamente como fue creado Django.

Django nació naturalmente de aplicaciones de la vida real escritas por un equipo
de desarrolladores Web en Lawrence, Kansas. Nació en el otoño boreal de 2003, cuando
los programadores Web del diario *Lawrence Journal-World*, Adrian Holovaty y
Simon Willison, comenzaron a usar Python para crear sus aplicaciones. El equipo
de The World Online, responsable de la producción y mantenimiento de varios sitios
locales de noticias, prosperaban en un entorno de desarrollo dictado por las
fechas límite del periodismo. Para los sitios -- incluidos LJWorld.com,
Lawrence.com y KUsports.com -- los periodistas (y los directivos) exigían que se
agregaran nuevas características y que aplicaciones enteras se crearan a una
velocidad vertiginosa, a menudo con sólo días u horas de preaviso. Es así que
Adrian y Simon desarrollaron por necesidad un framework de desarrollo Web que
les ahorrara tiempo -- era la única forma en que podían crear aplicaciones
mantenibles en tan poco tiempo -- .

En el verano boreal de 2005, luego de haber desarrollado este framework hasta
el punto en que estaba haciendo funcionar la mayoría de los sitios World Online,
el equipo de World Online, que ahora incluía a Jacob Kaplan-Moss, decidió
liberar el framework como software de código abierto. Lo liberaron en julio de
2005 y lo llamaron Django, por el guitarrista de jazz Django Reinhardt.

A pesar de que Django ahora es un proyecto de código abierto con colaboradores
por todo el mundo, los desarrolladores originales de World Online todavía
aportan una guía centralizada para el crecimiento del framework, y World Online
colabora con otros aspectos importantes tales como tiempo de trabajo, materiales
de marketing, y hosting/ancho de banda para el Web site del framework
(http://www.djangoproject.com/).

Esta historia es relevante porque ayuda a explicar dos cuestiones clave. La
primera es el "punto dulce" de Django. Debido a que Django nació en un entorno
de noticias, ofrece varias características (en particular la interfaz admin,
tratada en el :doc:`Capítulo 6<chapter06>` que son particularmente apropiadas para sitios de
"contenido" -- sitios como eBay, craigslist.org y washingtonpost.com que ofrecen
información basada en bases de datos --. (De todas formas, no dejes que eso te
quite las ganas -- a pesar de que Django es particularmente bueno para
desarrollar esa clase de sitios, eso no significa que no sea una herramienta
efectiva para crear cualquier tipo de sitio Web dinámico --. Existe una
diferencia entre ser *particularmente efectivo* para algo y *no ser efectivo*
para otras cosas).

La segunda cuestión a resaltar es cómo los orígenes de Django le han dado forma
a la cultura de su comunidad de código abierto. Debido a que Django fue extraído
de código de la vida real, en lugar de ser un ejercicio académico o un producto
comercial, está especialmente enfocado en resolver problemas de desarrollo Web
con los que los desarrolladores de Django se han encontrado -- y con los que
continúan encontrándose --. Como resultado de eso, Django es activamente mejorado
casi diariamente. Los desarrolladores del framework tienen un alto grado de
interés en asegurarse de que Django les ahorre tiempo a los desarrolladores,
produzca aplicaciones que son fáciles de mantener y rindan bajo mucha
carga. Aunque existan otras razones, los desarrolladores están motivados por
sus propios deseos egoístas de ahorrarse tiempo a ellos mismos y disfrutar de
sus trabajos. (Para decirlo sin vueltas, se comen su propia comida para perros).

Cómo leer este libro
====================

Al escribir este libro, tratamos de alcanzar un balance entre legibilidad y
referencia, con una tendencia a la legibilidad. Nuestro objetivo con este libro,
como se mencionó anteriormente, es hacerte un experto en Django, y creemos que
la mejor manera de enseñar es a través de la prosa y numerosos ejemplos, en vez
de proveer un exhaustivo pero inútil catálogo de las características de Django
(Como alguien dijo una vez, no puedes esperar enseñarle a alguien cómo hablar
simplemente enseñándole el alfabeto).

Con eso en mente, te recomendamos que leas los capítulos del 1 al 7 en orden.
Ellos forman los fundamentos de cómo se usa Django; una vez que los hayas leído,
serás capaz de construir sitios Web que funcionan sobre Django. Los capítulos
restantes, los cuales se enfocan en características específicas de Django,
pueden ser leídos en cualquier orden.

Los apéndices son para referencia. Ellos, junto con la documentación libre en
http://www.djangoproject.com/, son probablemente lo que releerás de vez en
cuando para recordar la sintaxis o buscar un resumen rápido de lo que hacen
ciertas partes de Django.

Conocimientos de programación requeridos
----------------------------------------

Los lectores de este libro deben comprender las bases de la programación
orientada a objetos e imperativa: estructuras de control
(``if``, ``while`` y ``for``), estructuras de datos (listas, hashes/diccionarios),
variables, clases y objetos.

La experiencia en desarrollo Web es, como podrás esperar, muy útil, pero no es
requisito para leer este libro. A lo largo del mismo, tratamos de promover las
mejores prácticas en desarrollo Web para los lectores a los que les falta este
tipo de experiencia.

Conocimientos de Python requeridos
----------------------------------

En esencia, Django es sencillamente una colección de bibliotecas escritas en el
lenguaje de programación Python. Para desarrollar un sitio usando Django escribes
código Python que utiliza esas bibliotecas. Aprender Django, entonces, es sólo
cuestión de aprender a programar en Python y comprender cómo funcionan las
bibliotecas Django.

Si tienes experiencia programando en Python, no deberías tener problema en
meterte de lleno. En conjunto, el código Django no produce "magia negra"
(es decir, trucos de programación cuya implementación es difícil de explicar o entender).
Para ti, aprender Django será sólo cuestión de aprender las convenciones y APIs de Django.

Si no tienes experiencia programando en Python, te espera una grata sorpresa.
Es fácil de aprender y muy divertido de usar. A pesar de que este libro no
incluye un tutorial completo de Python, sí hace hincapié en las características y
funcionalidades de Python cuando se considera apropiado, particularmente cuando
el código no cobra sentido de inmediato. Aún así, recomendamos leer el tutorial
oficial de Python, disponible en http://pyspanishdoc.sourceforge.net/tut/tut.html
o su versión más reciente en inglés en http://docs.python.org/tut/. También
recomendamos el libro libre y gratuito de Mark Pilgrim *Inmersión en Python*,
disponible en http://es.diveintopython.org/ y publicado en inglés en papel por
Apress.

Nuevas características de Django
--------------------------------

Tal como hicimos notar anteriormente, Django es mejorado con frecuencia, y
probablemente tendrá un gran número de nuevas -- e incluso *esenciales* --
características para cuando este libro sea publicado. Por ese motivo, nuestro
objetivo como autores de este libro es doble:

* Asegurarnos que este libro sea "a prueba de tiempo" tanto como nos sea
  posible, para que cualquier cosa que leas aquí todavía sea relevante en
  futuras versiones de Django.

* Actualizar este libro continuamente en el sitio Web en inglés,
  http://www.djangobook.com/, para que puedas acceder a la mejor y más reciente
  documentación tan pronto como la escribimos.
      


Si quieres implementar con Django algo que no está explicado en este libro,
revisa la versión más reciente de este libro en el sitio Web antes mencionado y
también revisa la documentación oficial de Django.

.. admonition:: Obteniendo ayuda:
                      

    Para ayuda con cualquier aspecto de Django -- desde instalación y
    diseño de aplicaciones, hasta diseño de bases de datos e implementaciones --
    siéntete libre de hacer preguntas online.

    * En la lista de correo en inglés de usuarios de Django se juntan miles de
      usuarios para preguntar y responder dudas. Suscríbete gratuitamente en
      http://www.djangoproject.com/r/django-users (inglés) o
      http://groups.google.es/group/django-es (español).

    * El canal de IRC de Django donde los usuarios de Django se juntan a chatear
      y se ayudan unos a otros en tiempo real. Únete a la diversión en #django
      (inglés) o #django-es (español) en la red de IRC Freenode.

¿Qué sigue?
===========

En el  :doc:`Capítulo 2 <chapter02>`, a continuación, empezaremos con Django, explicando su
instalación y configuración inicial.
