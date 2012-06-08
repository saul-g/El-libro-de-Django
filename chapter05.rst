=============================================================
Capítulo 5: Interactuar con una base de datos: Modelos
=============================================================

En el :doc:`Capítulo 3<chapter03>`, recorrimos los conceptos fundamentales de la construcción
dinámica de sitios web con Django: La configuración de vistas y URLconfs. Como
explicamos, una vista es responsable de implementar *alguna lógica arbitraria*,
y luego retornar una respuesta. En el ejemplo, nuestra lógica arbitraria era
calcular la fecha y hora actual.

En las aplicaciones web modernas, la lógica arbitraria a menudo implica
interactuar con una base de datos. Detrás de escena, un *sitio web impulsado por
una base de datos* se conecta a un servidor de base de datos, recupera algunos
datos de esta, y los muestra con un formato agradable en una página web. O,
del mismo modo, el sitio puede proporcionar funcionalidad que permita a los
visitantes del sitio poblar la base de datos por su propia cuenta.

Muchos sitios web más complejos proporcionan alguna combinación de las dos.
Amazon.com, por ejemplo, es un gran ejemplo de un sitio que maneja una base de
datos. Cada página de un producto es esencialmente una consulta a la base de
datos de productos de Amazon formateada en HTML, y cuando envías una opinión
de cliente (*customer review*), esta es insertada en la base de datos de
opiniones.

Django es apropiado para crear sitios web que manejen una base de datos, ya que
incluye una manera fácil pero poderosa de realizar consultas a bases de
datos utilizando Python. Este capítulo explica esta funcionalidad: la capa de
la base de datos de Django.

(Nota: Aunque no es estrictamente necesario conocer teoría básica de bases de
datos y SQL para usar la capa de base de datos de Django, es altamente
recomendado. Una introducción a estos conceptos está más allá del alcance de
este libro, pero continúa leyendo si eres nuevo en el tema. Probablemente seas
capaz de seguir adelante y captar los conceptos básicos en base al contexto).

La manera "tonta" de hacer una consulta a la base de datos en las vistas
=========================================================================

Así como en el :doc:`Capítulo 3<chapter03>` detallamos la manera "tonta" de producir una salida
con la vista (codificando *en duro*) el texto directamente dentro de la vista),
hay una manera "tonta" de recuperar datos desde la base de datos en una vista.
Esto es simple: sólo usa una biblioteca de Python existente para ejecutar una
consulta SQL y haz algo con los resultados.

En este ejemplo de vista, usamos la biblioteca ``MySQLdb`` (disponible en
http://www.djangoproject.com/r/python-mysql/)  para conectarnos a una base de
datos de MySQL, recuperar algunos registros, y alimentar con ellos una plantilla
para mostrar una página web::

    from django.shortcuts import render_to_response
    import MySQLdb

    def book_list(request):
        db = MySQLdb.connect(user='me', db='mydb', passwd='secret', host='localhost')
        cursor = db.cursor()
        cursor.execute('SELECT name FROM books ORDER BY name')
        names = [row[0] for row in cursor.fetchall()]
        db.close()
        return render_to_response('book_list.html', {'names': names})

Este enfoque funciona, pero deberían hacerse evidentes inmediatamente algunos
problemas:

    * Estamos codificando *en duro* (*hard-coding*) los parámetros de la
      conexión a la base de datos. Lo ideal sería que esos parámetros se
      guardarsen en la configuración de Django.

    * Tenemos que escribir una cantidad de código estereotípico: crear una
      conexión, un cursor, ejecutar una sentencia, y cerrar la conexión. Lo
      ideal sería que todo lo que tuviéramos que hacer fuera especificar los
      resultados que queremos.

    * Nos ata a MySQL. Si, en el camino, cambiamos de MySQL a PostgreSQL,
      tenemos que usar un adaptador de base de datos diferente (por ej.
      ``psycopg`` en vez de ``MySQLdb``), alterar los parámetros de conexión
      y -- dependiendo de la naturaleza de las sentencia de SQL -- posiblemente
      reescribir el SQL. La idea es que el servidor de base de datos que usemos
      esté abstraído, entonces el pasarnos a otro servidor podría significar
      realizar un cambio en un único lugar.

Como esperabas, la capa de la base de datos de Django apunta a resolver estos
problemas. Este es un adelanto de cómo la vista anterior puede ser reescrita
usando la API de Django::

    from django.shortcuts import render_to_response
    from mysite.books.models import Book

    def book_list(request):
        books = Book.objects.order_by('name')
        return render_to_response('book_list.html', {'books': books})

Explicaremos este código enseguida en este capítulo. Por ahora, tengamos sólo
una idea de cómo es.

El patrón de diseño MTV
=======================

Antes de profundizar en más código, tomémonos un momento para considerar el
diseño global de una aplicación Web Django impulsada por bases de datos.

Como mencionamos en los capítulos anteriores, Django fue diseñado para promover
el acoplamiento débil y la estricta separación entre las piezas de una
aplicación. Si sigues esta filosofía, es fácil hacer cambios en un lugar
particular de la aplicación sin afectar otras piezas. En las funciones de vista,
por ejemplo, discutimos la importancia de separar la lógica de negocios de la
lógica de presentación usando un sistema de plantillas. Con la capa de la base
de datos, aplicamos esa misma filosofía para el acceso lógico a los datos.

Estas tres piezas juntas -- la lógica de acceso a la base de datos, la lógica
de negocios, y la lógica de presentación -- comprenden un concepto que a veces
es llamado el patrón de arquitectura de software *Modelo-Vista-Controlador* (MVC).
En este patrón, el "Modelo" hace referencia al acceso a la capa de datos, la
"Vista" se refiere a la parte del sistema que selecciona qué mostrar y cómo
mostrarlo, y el "Controlador" implica la parte del sistema que decide qué
vista usar, dependiendo de la entrada del usuario, accediendo al modelo si es
necesario.

.. admonition:: ¿Por qué el acrónimo?

    El objetivo de definir en forma explícita patrones como MVC es
    principalmente simplificar la comunicación entre los desarrolladores. En
    lugar de tener que decir a tus compañeros de trabajo, "Vamos a hacer una
    abstracción del acceso a la base de datos, luego vamos a tener una capa que
    se encarga de mostrar los datos, y vamos a poner una capa en el medio para
    que regule esto", puedes sacar provecho de un vocabulario compartido y
    decir, "Vamos a usar un patrón MVC aquí".

Django sigue el patrón MVC tan al pie de la letra que puede ser llamado
un framework MVC. Someramente, la M, V y C se separan en Django de la
siguiente manera:

    * *M*, la porción de acceso a la base de datos, es manejada por la capa de
      la base de datos de Django, la cual describiremos en este capítulo.

    * *V*, la porción que selecciona qué datos mostrar y cómo mostrarlos, es
      manejada por la vista y las plantillas.

    * *C*, la porción que delega a la vista dependiendo de la entrada del
      usuario, es manejada por el framework mismo siguiendo tu URLconf y
      llamando a la función apropiada de Python para la URL obtenida.

Debido a que la "C" es manejada por el mismo framework y la parte más
emocionante se produce en los modelos, las plantillas y las vistas, Django es
conocido como un *Framework MTV*. En el patrón de diseño MTV,

    * *M* significa "Model" (Modelo), la capa de acceso a la base de datos. Esta
      capa contiene toda la información sobre los datos: cómo acceder a estos,
      cómo validarlos, cuál es el comportamiento que tiene, y las relaciones
      entre los datos.

    * *T* significa "Template" (Plantilla), la capa de presentación. Esta capa
      contiene las decisiones relacionadas a la presentación: como algunas cosas
      son mostradas sobre una página web o otro tipo de documento.

    * *V* significa "View" (Vista), la capa de la lógica de negocios. Esta capa
      contiene la lógica que accede al modelo y la delega a la plantilla
      apropiada: puedes pensar en esto como un puente entre el modelos y las
      plantillas.

Si estás familiarizado con otros frameworks de desarrollo web MVC, como Ruby on
Rails, quizás consideres que las vistas de Django pueden ser el "controlador" y
las plantillas de Django pueden ser la "vista". Esto es una confusión
desafortunada a raíz de las diferentes interpretaciones de MVC. En la
interpretación de Django de MVC, la "vista" describe los datos que son
presentados al usuario; no necesariamente el *cómo* se mostrarán, pero si
*cuáles* datos son presentados. En contraste, Ruby on Rails y frameworks
similares sugieren que el trabajo del controlador incluya la decisión de cuales
datos son presentados al usuario, mientras que la vista sea estrictamente el
*cómo* serán presentados y no *cuáles*.

Ninguna de las interpretaciones es más "correcta" que otras. Lo importante es
entender los conceptos subyacentes.

Configuración de la base de datos
=================================

Con toda esta filosofía en mente, vamos a comenzar a explorar la capa de la base
de datos de Django. Primero, necesitamos tener en cuenta algunas configuraciones
iniciales: necesitamos indicarle a Django qué servidor de base de datos usar y
cómo conectarse con el mismo.

Asumimos que haz configurado un servidor de base de datos, lo has activado, y
has creado una base de datos en este (por ej. usando la sentencia
``CREATE DATABASE``). SQLite es un caso especial; es este caso, no hay que
crear una base de datos, porque SQLite usa un archivo autónomo sobre el
sistema de archivos para guardar los datos.

Como con ``TEMPLATE_DIRS`` en los capítulos anteriores, la configuración de la
base de datos se encuentra en el archivo de configuración de Django, llamado,
por omisión, ``settings.py``. Edita este archivo y busca las opciones de la
base de datos::

    DATABASE_ENGINE = ''
    DATABASE_NAME = ''
    DATABASE_USER = ''
    DATABASE_PASSWORD = ''
    DATABASE_HOST = ''
    DATABASE_PORT = ''

Aquí hay un resumen de cada propiedad.

    * ``DATABASE_ENGINE`` le indica a Django qué base de datos utilizar. Si
      usas una base de datos con Django, ``DATABASE_ENGINE`` debe configurarse
      con un string de los mostrados en la Tabla 5-1.

.. tabla:: Tabla 5-1. Configuración de motores de base de datos

=======================  ====================  =================================================
    Configuración            Base de datos         Adaptador requerido
=======================  ====================  =================================================
       ``postgresql``           PostgreSQL      ``psycopg`` version 1.x,
                                                  http://www.djangoproject.com/r/python-pgsql/1/

``postgresql_psycopg2``     PostgreSQL            ``psycopg`` versión 2.x,
                                                    http://www.djangoproject.com/r/python-pgsql/.

    ``mysql``                MySQL                 ``MySQLdb``,
                                                     http://www.djangoproject.com/r/python-mysql/. 
                                               
 ``sqlite3``              SQLite                No necesita adaptador si se usa Python 2.5+.
                                                En caso contrario, ``pysqlite``,
                                                http://www.djangoproject.com/r/python-sqlite/.
 
  ``ado_mssql``           Microsoft SQL          ``adodbapi`` version 2.0.1+,
                          Server                   http://www.djangoproject.com/r/python-ado/.

        ``oracle``               Oracle         ``cx_Oracle``,
                                                  http://www.djangoproject.com/r/python-oracle/.
=======================  ====================  =================================================

* ``NOTA:`` Cualquiera sea la base de datos que uses, necesitarás descargar
  e instalar el adaptador apropiado. Cada uno de estos está disponible
  libremente en la web; sólo sigue el enlace en la columna "Adaptador
  requerido" en la Tabla 5-1.

    * ``DATABASE_NAME`` la indica a Django el nombre de tu base de datos. Si
      estás usando SQLite, especifica la ruta completo del sistema de archivos
      hacia el archivo de la base de datos (por ej. ``'/home/django/mydata.db'``).

    * ``DATABASE_USER`` le indica a Django cual es el nombre de usuario a usar
      cuando se conecte con tu base de datos. Si estás usando SQLite, deja este
      en blanco.

    * ``DATABASE_PASSWORD`` le indica a Django cual es la contraseña a utilizar
      cuando se conecte con tu base de datos. Si estás utilizando SQLite o
      tienes una contraseña vacía, deja este en blanco.

    * ``DATABASE_HOST`` le indica a Django cual es el host a usar cuando se
      conecta a tu base de datos. Si tu base de datos está sobre la misma computadora
      que la instalación de Django (o sea localhost), deja este en blanco. Si
      estás usando SQLite, deja este en blanco.

      MySQL es un caso especial aquí. Si este valor comienza con una barra
      (``'/'``) y estás usando MySQL, MySQL se conectará al socket especificado
      por medio de un socket Unix, por ejemplo::

          DATABASE_HOST = '/var/run/mysql'

      Si estás utilizando MySQL y este valor *no* comienza con una barra,
      entonces este valor es asumido como el host.

    * ``DATABASE_PORT`` le indica a Django qué puerto usar cuando se conecte a
      la base de datos. Si estás utilizando SQLite, deja este en blanco. En otro
      caso, si dejas este en blanco, el adaptador de base de datos subyacente
      usará el puerto por omisión acorde al servidor de base de datos. En la
      mayoría de los casos, el puerto por omisión está bien, por lo tanto puedes
      dejar este en blanco.

Una vez que hayas ingresado estas configuraciones, compruébalas. Primero,
desde el directorio del proyecto que creaste en el :doc:`Capítulo 2<chapter02>`, ejecuta el
comando ``python manage.py shell``.

Notarás que comienza un intérprete interactivo de Python. Las apariencias pueden
engañar. Hay una diferencia importante entre ejecutar el comando
``python manage.py shell`` dentro del directorio del proyecto de Django y el
más genérico ``python``. El último es el Python shell básico, pero el anterior
le indica a Django cuales archivos de configuración usar antes de comenzar el
shell. Este es un requerimiento clave para hacer consultas a la base de datos:
Django necesita saber cuales son los archivos de configuraciones a usar para
obtener la información de la conexión a la base de datos.

Detrás de escena, ``python manage.py shell`` simplemente asume que tu
archivo de configuración está en el mismo directorio que ``manage.py``. Hay
otras maneras de indicarle a Django qué módulo de configuración usar, pero
este subtítulo lo cubriremos luego. Por ahora, usa ``python manage.py shell``
cuando necesites hacer modificaciones específicas a Django.

Una vez que hayas entrado al shell, escribe estos comando para probar la
configuración de tu base de datos::

    >>> from django.db import connection
    >>> cursor = connection.cursor()

Si no sucede nada, entonces tu base de datos está configurada correctamente. De
lo contrario revisa el mensaje de error para obtener un indicio sobre qué es lo
que está mal. La Tabla 5-2 muestra algunos mensajes de error comunes.

.. tabla:: Tabla 5-2. Mensajes de error de configuración de la base de datos

==========================================================  ===============================================================
    Mensaje de error                                                      Solución
==========================================================  ===============================================================
    You haven't set the DATABASE_ENGINE setting yet.           Configura la
                                                               variable ``DATABASE_ENGINE`` con otra cosa que
                                                               un string vacío.
Environment variable DJANGO_SETTINGS_MODULE is undefined.      Ejecuta el comando ``python manage.py shell``
                                                               en vez de ``python``.
    Error loading _____ module: No module named _____.         No tienes instalado el módulo apropiado para
                                                               la base de datos especificada (por ej. ``psycopg``
                                                               o ``MySQLdb``).
    _____ isn't an available database backend.                 Configura la variable ``DATABASE_ENGINE``
                                                               con un motor válido descrito previamente.
                                                               ¿Habrás cometido un error de tipeo?
    database _____ does not exist                              Cambia la variable ``DATABASE_NAME`` para que *apunte*
                                                               a una base de datos existente, o ejecuta la
                                                               sentencia ``CREATE DATABASE`` apropiada para
                                                               crearla.
    role _____ does not exist                                  Cambia la variable ``DATABASE_USER`` para que *apunte*
                                                               a un usuario que exista, o crea el usuario
                                                               en tu base de datos.
    could not connect to server                                Asegúrate de que ``DATABASE_HOST`` y
                                                               ``DATABASE_PORT`` estén configurados
                                                               correctamente y que el servidor esté corriendo.
==========================================================  ===============================================================

Tu primera aplicación
=====================

Ahora que verificamos que la conexión está funcionando, es hora de crear una
*Aplicación de Django* -- una colección de archivos de código fuente, incluyendo
modelos y vistas, que conviven en un solo paquete de Python y representen
una aplicación completa de Django.

Vale la pena explicar la terminología aquí, porque esto es algo que suele hacer
tropezar a los principiantes. Ya hemos creado un *proyecto*, en el :doc:`Capítulo 2<chapter02>`,
entonces, ¿cuál es la diferencia entre un *proyecto* y una *aplicación*? La
diferencia es la que existe entre la configuración y el código:

    * Un proyecto es una instancia de un cierto conjunto de aplicaciones de
      Django, más las configuraciones de esas aplicaciones.

      Técnicamente, el único requerimiento de un proyecto es que este
      suministre un archivo de configuración, el cual define la información
      hacia la conexión a la base de datos, la lista de las aplicaciones
      instaladas, la variable ``TEMPLATE_DIRS``, y así sucesivamente.

    * Una aplicación es un conjunto portable de una funcionalidad de Django,
      típicamente incluye modelos y vistas, que conviven en un solo paquete de
      Python.

      Por ejemplo, Django incluye un número de aplicaciones, tales como un
      sistema de comentarios y una interfaz de administración automática. Una
      cosa clave para notar sobre estas aplicaciones es que son portables y
      reusables en múltiples proyectos.

Hay pocas reglas estrictas sobre cómo encajar el código Django en este esquema;
es flexible. Si estás construyendo un sitio web simple, quizás uses una sola
aplicación. Si estás construyendo un sitio web complejo con varias piezas que
no se relacionan entre sí, tales como un sistema de comercio electrónico o un
foro, probablemente quieras dividir esto en aplicaciones para que te sea
posible reusar estas individualmente en un futuro.

Es más, no necesariamente debes crear aplicaciones en absoluto, como lo hace
evidente la función de la vista del ejemplo que creamos antes en este libro.  En
estos casos, simplemente creamos un archivo llamado ``views.py``, llenamos este
con una función de vista, y apuntamos nuestra URLconf a esa función. No se
necesitan "aplicaciones".

No obstante, existe un requisito respecto a la convención de la aplicación: si
estás usando la capa de base de datos de Django (modelos), debes crear una
aplicación de Django. Los modelos deben vivir dentro de aplicaciones.

Dentro del directorio del proyecto ``mysite`` que creaste en el :doc:`Capítulo 2<chapter02>`,
escribe este comando para crear una nueva aplicación llamada books::

    python manage.py startapp books

Este comando no produce ninguna salida, pero crea un directorio ``books``
dentro del directorio ``mysite``. Echemos un vistazo al contenido::

    books/
        __init__.py
        models.py
        views.py

Esos archivos contendrán los modelos y las vistas para esta aplicación.

Echa un vistazo a ``models.py`` y ``views.py`` en tu editor de texto favorito.
Ambos archivos están vacíos, excepto por la importación en ``models.py``. Este
es el espacio disponible para ser creativo con tu aplicación de Django.

Definir modelos en Python
=========================

Como discutimos en los capítulos anteriores, la "M" de "MTV" hace referencia al
"Modelo". Un modelo de Django es una descripción de los datos en la base de
datos, representada como código de Python. Esta es tu capa de datos -- lo
equivalente de tu sentencia SQL ``CREATE TABLE`` -- excepto que están en Python
en vez de SQL, e incluye más que sólo definición de columnas de la base de
datos. Django usa un modelo para ejecutar código SQL detrás de las escenas y
retornar estructuras de datos convenientes en Python representando las filas de
tus tablas de la base de datos. Django también usa modelos para representar
conceptos de alto nivel que no necesariamente pueden ser manejados por SQL.

Si estás familiarizado con base de datos, inmediatamente podría pensar, "¿No es
redundante definir modelos de datos en Python *y* en SQL?" Django trabaja de
este modo por varias razones:

    * La introspección requiere ***overhead*** y es imperfecta. Con el objetivo
      de proveer una API conveniente de acceso a los datos, Django necesita
      conocer *de alguna forma* la capa de la base de datos, y hay dos formas de
      lograr esto. La primera sería describir explícitamente los datos en
      Python, y la segunda sería la introspección de la base de datos en tiempo
      de ejecución para determinar el modelo de la base de datos.

      La segunda forma parece clara, porque los metadatos sobre tus tablas vive en
      un único lugar, pero introduce algunos problemas. Primero,
      introspeccionar una base de datos en tiempo de ejecución obviamente
      requiere overhead. Si el framework tuviera que introspeccionar la base
      de datos cada vez que se procese una petición, o incluso cuando el
      servidor web sea inicializado, esto podría provocar un nivel de overhead
      inaceptable. (Mientras algunos creen que el nivel de overhead es
      aceptable, los desarrolladores de Django apuntan a quitar del framework
      tanto overhead como sea posible, y esta aproximación hace que Django sea
      más rápido que los frameworks competidores de alto nivel en mediciones de
      desempeño). Segundo, algunas bases de datos, notablemente viejas
      versiones de MySQL, no guardan suficiente metadatos para asegurarse una
      completa introspección.

    * Escribir Python es divertido, y dejar todo en Python limita el número de
      veces que tu cerebro tiene que realizar un "cambio de contexto". Si te
      mantienes en un solo entorno/mentalidad de programación tanto tiempo
      como sea posible, ayuda para la productividad. Teniendo que escribir SQL,
      luego Python, y luego SQL otra vez es perjudicial.

    * Tener modelos de datos guardados como código en vez de en tu base de datos
      hace fácil dejar tus modelos bajo un control de versiones. De esta forma,
      puedes fácilmente dejar rastro de los cambios a tu capa de modelos.

    * SQL permite sólo un cierto nivel de metadatos acerca de un ***layout*** de
      datos.  La mayoría de sistemas de base de datos, por ejemplo, no provee un
      tipo de datos especializado para representar una dirección web o de email.
      Los modelos de Django sí. La ventaja de un tipo de datos de alto nivel es
      la alta productividad y la reusabilidad de código.

    * SQL es inconsistente a través de distintas plataformas. Si estás
      redistribuyendo una aplicación web, por ejemplo, es mucho más pragmático
      distribuir un módulo de Python que describa tu capa de datos que separar
      conjuntos de sentencias ``CREATE TABLE``  para MySQL, PostgreSQL y SQLite.

Una contra de esta aproximación, sin embargo, es que es posible que el código
Python quede fuera de sincronía respecto a lo que hay actualmente en la base. Si
haces cambios en un modelo Django, necesitarás hacer los mismos cambios dentro
de tu base de datos para mantenerla consistente con el modelo. Detallaremos
algunas estrategias para manejar este problema más adelante en este capítulo.

Finalmente, Django incluye una utilidad que puede generar modelos haciendo
introspección sobre una base de datos existente. Esto es útil para comenzar
a trabajar rápidamente sobre datos heredados.

Tu primer modelo
================

Como ejemplo continuo en este capítulo y el siguiente, nos enfocaremos en una
configuración de datos básica sobre libro/autor/editor. Usamos esto como ejemplo
porque las relaciones conceptuales entre libros, autores y editores son bien
conocidas, y es una configuración de datos comúnmente utilizada en libros de
texto introductorios de SQL. Por otra parte, ¡estás leyendo un libro que fue
escrito por autores y producido por un editor!

Supondremos los siguientes conceptos, campos y relaciones:

    * Un autor tiene un título (ej.: Sr. o Sra.), nombre, apellido, dirección
      de correo electrónico y una foto tipo carnet.

    * Un editor tiene un nombre, una dirección, una ciudad, un estado o
      provincia, un país y un sitio Web.

    * Un libro tiene un título y una fecha de publicación. También tiene uno o
      más autores (una relación muchos-a-muchos con autores) y un único editor
      (una relación uno a muchos -- también conocida como clave foránea -- con
      editores).

El primer paso para utilizar esta configuración de base de datos con Django es
expresarla como código Python. En el archivo ``models.py`` que se creó con el
comando ``startapp``, ingresa lo siguiente::

    from django.db import models

    class Publisher(models.Model):
        name = models.CharField(maxlength=30)
        address = models.CharField(maxlength=50)
        city = models.CharField(maxlength=60)
        state_province = models.CharField(maxlength=30)
        country = models.CharField(maxlength=50)
        website = models.URLField()

    class Author(models.Model):
        salutation = models.CharField(maxlength=10)
        first_name = models.CharField(maxlength=30)
        last_name = models.CharField(maxlength=40)
        email = models.EmailField()
        headshot = models.ImageField(upload_to='/tmp')

    class Book(models.Model):
        title = models.CharField(maxlength=100)
        authors = models.ManyToManyField(Author)
        publisher = models.ForeignKey(Publisher)
        publication_date = models.DateField()

Examinemos rápidamente este código para conocer lo básico. La primer cosa a
notar es que cada modelo es representado por una clase Python que es una
subclase de ``django.db.models.Model``. La clase antecesora, ``Model``,
contiene toda la maquinaria necesaria para hacer que estos objetos sean
capaces de interactuar con la base de datos --  y que hace que nuestros modelos
sólo sean responsables de definir sus campos, en una sintaxis compacta y
agradable. Lo creas o no, éste es todo el código que necesitamos para tener
acceso básico a los datos con Django.

Cada modelo generalmente corresponde a una tabla única de la base de datos, y
cada atributo de un modelo generalmente corresponde a una columna en esa tabla.
El nombre de atributo corresponde al nombre de columna, y el tipo de campo
(ej.: ``CharField``) corresponde al tipo de columna de la base de datos (ej.:
``varchar``). Por ejemplo, el modelo ``Publisher`` es equivalente a la
siguiente tabla (asumiendo la sintaxis de PostgreSQL para ``CREATE TABLE``):


.. code-block:: sql
  
    CREATE TABLE "books_publisher" (
        "id" serial NOT NULL PRIMARY KEY,
        "name" varchar(30) NOT NULL,
        "address" varchar(50) NOT NULL,
        "city" varchar(60) NOT NULL,
        "state_province" varchar(30) NOT NULL,
        "country" varchar(50) NOT NULL,
        "website" varchar(200) NOT NULL
    );

En efecto, Django puede generar esta sentencia ``CREATE TABLE`` automáticamente
como veremos en un momento.

La excepción a la regla una-clase-por-tabla es el caso de las relaciones
muchos-a-muchos. En nuestros modelos de ejemplo, ``Book`` tiene un
``ManyToManyField`` llamado ``authors``. Esto significa que un libro tiene uno
o más autores, pero la tabla de la base de datos ``Book``  no tiene una columna
``authors``. En su lugar, Django crea una tabla adicional -- una "tabla de
join" muchos-a-muchos -- que maneja la correlación entre libros y autores.

Para una lista completa de tipos de campo y opciones de sintaxis de modelos,
ver el Apéndice B.

Finalmente, debes notar que no hemos definido explícitamente una clave primaria
en ninguno de estos modelos. A no ser que le indiques lo contrario, Django dará
automáticamente a cada modelo un campo de clave primaria entera llamado ``id``.
Es un requerimiento el que cada modelo Django tenga una clave primaria de
columna simple.

Instalar el modelo
==================

Ya escribimos el código; creemos ahora las tablas en la base de datos. Para
hacerlo, el primer paso es *activar* estos modelos en nuestro proyecto Django.
Hacemos esto agregando la aplicación ``books`` a la lista de aplicaciones
instaladas en el archivo de configuración.

Edita el archivo ``settings.py`` otra vez, y examina la variable de
configuración ``INSTALLED_APPS``. ``INSTALLED_APPS`` le indica a Django qué
aplicaciones están activadas para un proyecto determinado. Por omisión, se ve
como esto::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
    )

Temporalmente, comenta estos cuatro strings poniendo un carácter (``#``)
al principio. (Están incluidos por omisión porque es frecuente usarlas, pero
las activaremos y las discutiremos más adelante) Cuando termines, modifica las
configuraciones por omisión de ``MIDDLEWARE_CLASSES`` y
``TEMPLATE_CONTEXT_PROCESSORS``.  Éstas dependen de algunas de las aplicaciones
que hemos comentado. Entonces, agrega ``'mysite.books'`` a la lista
``INSTALLED_APPS``, de manera que la configuración termine viéndose así::

    MIDDLEWARE_CLASSES = (
    #    'django.middleware.common.CommonMiddleware',
    #    'django.contrib.sessions.middleware.SessionMiddleware',
    #    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #    'django.middleware.doc.XViewMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = ()
    #...

    INSTALLED_APPS = (
        #'django.contrib.auth',
        #'django.contrib.contenttypes',
        #'django.contrib.sessions',
        #'django.contrib.sites',
        'mysite.books',
    )

(Como aquí estamos tratando con una tupla de un solo elemento, no olvides la
coma final. De paso, los autores de este libro prefieren poner una coma después
de *cada* elemento de una tupla, aunque la tupla tenga sólo un elemento. Esto
evita el problema de olvidar comas, y no hay penalización por el use de esa coma
extra)

``'mysite.books'`` se refiere a la aplicación ``books`` en la que estamos
trabajando. Cada aplicación en ``INSTALLED_APPS`` es representada por su ruta
Python completa -- esto es, la ruta de paquetes, separados por puntos,
que lleva al paquete de la aplicación.

Ahora que la aplicación Django ha sido activada en el archivo de configuración,
podemos crear las tablas en nuestra base de datos. Primero, validemos los
modelos ejecutando este comando::

    python manage.py validate

El comando ``validate`` verifica si la sintaxis y la lógica de tus modelos son
correctas. Si todo está bien, verás el mensaje ``0 errors found``. Si no,
asegúrate de haber escrito el código del modelo correctamente. La salida del
error debe brindarte información útil acerca de qué es lo que está mal en el
código.

Cada vez que piensas que tienes problemas con tus modelos, ejecuta
``python manage.py validate``. Tiende a capturar todos los problemas comunes
del modelo.

Si tus modelos son válidos, ejecuta el siguiente comando para que Django genere
sentencias ``CREATE TABLE`` para tus modelos en la aplicación ``books`` (con
sintaxis resaltada en colores disponible si estás usando Unix)::

    python manage.py sqlall books

En este comando, ``books`` es el nombre de la aplicación. Es lo que hayas
especificado cuando ejecutaste el comando ``manage.py startapp``. Cuando
ejecutes el comando, debes ver algo como esto:

.. code-block:: sql


    BEGIN;
    CREATE TABLE "books_publisher" (
        "id" serial NOT NULL PRIMARY KEY,
        "name" varchar(30) NOT NULL,
        "address" varchar(50) NOT NULL,
        "city" varchar(60) NOT NULL,
        "state_province" varchar(30) NOT NULL,
        "country" varchar(50) NOT NULL,
        "website" varchar(200) NOT NULL
    );
    CREATE TABLE "books_book" (
        "id" serial NOT NULL PRIMARY KEY,
        "title" varchar(100) NOT NULL,
        "publisher_id" integer NOT NULL REFERENCES "books_publisher" ("id"),
        "publication_date" date NOT NULL
    );
    CREATE TABLE "books_author" (
        "id" serial NOT NULL PRIMARY KEY,
        "salutation" varchar(10) NOT NULL,
        "first_name" varchar(30) NOT NULL,
        "last_name" varchar(40) NOT NULL,
        "email" varchar(75) NOT NULL,
        "headshot" varchar(100) NOT NULL
    );
    CREATE TABLE "books_book_authors" (
        "id" serial NOT NULL PRIMARY KEY,
        "book_id" integer NOT NULL REFERENCES "books_book" ("id"),
        "author_id" integer NOT NULL REFERENCES "books_author" ("id"),
        UNIQUE ("book_id", "author_id")
    );
    CREATE INDEX books_book_publisher_id ON "books_book" ("publisher_id");
    COMMIT;

Observa lo siguiente:

    * Los nombres de tabla se generan automáticamente combinando el nombre de
      la aplicación (``books``) y el nombre en minúsculas del modelo
      (``publisher``, ``book``, y ``author``). Puedes sobreescribir este
      comportamiento, como se detalla en el Apéndice B.

    * Como mencionamos antes, Django agrega una clave primaria para cada tabla
      automáticamente -- los campos ``id``. También puedes sobreescribir esto.

    * Por convención, Django agrega ``"_id"`` al nombre de campo de las claves
      foráneas. Como ya puedes imaginar, también puedes sobreescribir esto.

    * La relación de clave foránea se hace explícita con una sentencia
      ``REFERENCES``

    * Estas sentencias ``CREATE TABLE`` son adaptadas a medida de la base de
      datos que estás usando, de manera que Django maneja automáticamente los
      tipos de campo específicos de cada base de datos, como ``auto_increment``
      (MySQL), ``serial`` (PostgreSQL), o ``integer primary key`` (SQLite),
      por ti. Lo mismo sucede con el uso de las comillas simples o dobles en
      los nombres de columna. La salida del ejemplo está en la sintaxis de
      PostgreSQL.

El comando ``sqlall`` no crea ni toca de ninguna forma tu base de datos -- sólo
imprime una salida en la pantalla para que puedas ver qué SQL ejecutaría Django
si le pidieras que lo hiciera. Si quieres, puedes copiar y pegar este fragmento
de SQL en tu cliente de base de datos, o usa los pipes de Unix para pasarlo
directamente. De todas formas, Django provee una manera más fácil de confirmar
el envío del SQL a la base de datos. Ejecuta el comando ``syncdb`` de esta
manera::

    python manage.py syncdb

Verás algo como esto::

    Creating table books_publisher
    Creating table books_book
    Creating table books_author
    Installing index for books.Book model

El comando ``syncdb`` es una simple sincronización de tus modelos hacia tu base
de datos. El mismo examina todos los modelos en cada aplicación que figure en tu
variable de configuración ``INSTALLED_APPS``, verifica la base de datos para ver
si las tablas apropiadas ya existen, y las crea si no existen. Observa que
``syncdb`` *no* sincroniza los cambios o eliminaciones de los modelos; si haces
un cambio o modificas un modelo, y quieres actualizar la base de datos,
``syncdb`` no maneja esto. (Más sobre esto después.)

Si ejecutas ``python manage.py syncdb`` de nuevo, nada sucede, porque no has
agregado ningún modelo a la aplicación ``books`` ni has incorporado ninguna
aplicación en ``INSTALLED_APPS``. Ergo, siempre es seguro ejecutar
``python manage.py syncdb`` -- no hará desaparecer cosas.

Si estás interesado, toma un momento para bucear en el cliente de línea de
comandos de tu servidor de bases de datos y ver las tablas que creó Django.
Puedes ejecutar manualmente el cliente de línea de comandos (ej.: ``psql`` para
PostgreSQL) o puedes ejecutar el comando ``python manage.py dbshell``, que
deducirá qué cliente de linea de comando ejecutar, dependiendo de tu
configuración ``DATABASE_SERVER``. Esto último es casi siempre más conveniente.


Acceso básico a datos
=====================

Una vez que has creado un modelo, Django provee automáticamente una API Python
de alto nivel para trabajar con estos modelos. Prueba ejecutando
``python manage.py shell`` y escribiendo lo siguiente::

    >>> from books.models import Publisher
    >>> p1 = Publisher(name='Addison-Wesley', address='75 Arlington Street',
    ...     city='Boston', state_province='MA', country='U.S.A.',
    ...     website='http://www.apress.com/')
    >>> p1.save()
    >>> p2 = Publisher(name="O'Reilly", address='10 Fawcett St.',
    ...     city='Cambridge', state_province='MA', country='U.S.A.',
    ...     website='http://www.oreilly.com/')
    >>> p2.save()
    >>> publisher_list = Publisher.objects.all()
    >>> publisher_list
    [<Publisher: Publisher object>, <Publisher: Publisher object>]

Estas pocas líneas logran bastantes resultados. Estos son los puntos salientes:

    * Para crear un objeto, sólo importa la clase del modelo apropiada y
      crea una instancia pasándole valores para cada campo.

    * Para guardar el objeto en la base de datos, llama el método ``save()``
      del objeto. Detrás de la escena, Django ejecuta aquí una sentencia
      SQL ``INSERT``.

    * Para recuperar objetos de la base de datos, usa el atributo
      ``Publisher.objects``. Busca una lista de todos los objetos ``Publisher``
      en la base de datos con la sentencia ``Publisher.objects.all()``. Detrás
      de escenas, Django ejecuta aquí una sentencia SQL ``SELECT``.

Naturalmente, puedes hacer mucho con la API de base de datos de Django -- pero
primero, tengamos cuidado de una pequeña incomodidad.

Agregar strings de representación del modelo
============================================

Cuando imprimimos la lista de editores, todo lo que obtuvimos fue esta salida
poco útil que hacía difícil distinguir los objetos ``Publisher``::

    [<Publisher: Publisher object>, <Publisher: Publisher object>]

Podemos arreglar esto fácilmente agregando un método llamado ``__str__()`` a
nuestro objeto ``Publisher``. Un método ``__str__()`` le dice a Python como
mostrar la representación "string" de un objeto. Puedes ver esto en acción
agregando un método ``__str__()`` a los tres modelos:

.. literal-evaluado::

    from django.db import models

    class Publisher(models.Model):
        name = models.CharField(maxlength=30)
        address = models.CharField(maxlength=50)
        city = models.CharField(maxlength=60)
        state_province = models.CharField(maxlength=30)
        country = models.CharField(maxlength=50)
        website = models.URLField()

        **def __str__(self):**
            **return self.name**

    class Author(models.Model):
        salutation = models.CharField(maxlength=10)
        first_name = models.CharField(maxlength=30)
        last_name = models.CharField(maxlength=40)
        email = models.EmailField()
        headshot = models.ImageField(upload_to='/tmp')

        **def __str__(self):**
            **return '%s %s' % (self.first_name, self.last_name)**

    class Book(models.Model):
        title = models.CharField(maxlength=100)
        authors = models.ManyToManyField(Author)
        publisher = models.ForeignKey(Publisher)
        publication_date = models.DateField()

        **def __str__(self):**
            **return self.title**

Como puedes ver, un método ``__str__()`` puede hacer lo que sea que necesite
hacer para devolver una representación textual. Aquí, los métodos ``__str__()``
de ``Publisher`` y ``Book`` devuelven simplemente el nombre y título del objeto
respectivamente, pero el ``__str__()`` del ``Author`` es un poco más complejo --
junta los campos ``first_name`` y ``last_name``. El único requerimiento para
``__str__()`` es que devuelva un string. Si ``__str__()`` no devuelve un string
-- si retorna, digamos, un entero -- entonces Python generará un ``TypeError``
con un mensaje como ``"__str__ returned non-string"``.

Para que los cambios sean efectivos, sal del shell Python y entra de nuevo con
``python manage.py shell``. (Esta es la manera más simple de hacer que los
cambios en el código tengan efecto.) Ahora la lista de objetos ``Publisher`` es
más fácil de entender::

    >>> from books.models import Publisher
    >>> publisher_list = Publisher.objects.all()
    >>> publisher_list
    [<Publisher: Addison-Wesley>, <Publisher: O'Reilly>]

Asegúrate de que cada modelo que definas tenga un método ``__str__()`` -- no
solo por tu propia conveniencia cuando usas el intérprete interactivo, sino
también porque Django usa la salida de ``__str__()`` en muchos lugares cuando
necesita mostrar objetos.

Finalmente, observa que ``__str__()`` es un buen ejemplo de agregar
*comportamiento* a los modelos. Un modelo Django describe más que la
configuración de la tabla de la base de datos; también describe toda
funcionalidad que el objeto sepa hacer.  ``__str__()`` es un ejemplo de esa
funcionalidad -- un modelo sabe cómo mostrarse.

Insertar y actualizar datos
===========================

Ya has visto cómo se hace: para insertar una fila en tu base de datos, primero
crea una instancia de tu modelo usando argumentos por nombre, como::

    >>> p = Publisher(name='Apress',
    ...         address='2855 Telegraph Ave.',
    ...         city='Berkeley',
    ...         state_province='CA',
    ...         country='U.S.A.',
    ...         website='http://www.apress.com/')

Este acto de instanciar una clase modelo *no* toca la base de datos.

Para guardar el registro en la base de datos (esto es, para realizar la
sentencia SQL ``INSERT``), llama al método ``save()`` del objeto::

    >>> p.save()

En SQL, esto puede ser traducido directamente en lo siguiente::

    INSERT INTO book_publisher
        (name, address, city, state_province, country, website)
    VALUES
        ('Apress', '2855 Telegraph Ave.', 'Berkeley', 'CA',
         'U.S.A.', 'http://www.apress.com/');

Como el modelo ``Publisher`` usa una clave primaria autoincremental ``id``, la
llamada inicial a ``save()`` hace una cosa más: calcula el valor de la clave
primaria para el registro y lo establece como el valor del atributo ``id``  de
la instancia::

    >>> p.id
    52    # esto será diferente según tus datos

Las subsecuentes llamadas a ``save()`` guardarán el registro en su lugar, sin
crear un nuevo registro (es decir, ejecutarán una sentencia SQL ``UPDATE`` en
lugar de un ``INSERT``)::

    >>> p.name = 'Apress Publishing'
    >>> p.save()

La sentencia ``save()`` del párrafo anterior resulta aproximadamente en la
sentencia SQL siguiente::

    UPDATE book_publisher SET
        name = 'Apress Publishing',
        address = '2855 Telegraph Ave.',
        city = 'Berkeley',
        state_province = 'CA',
        country = 'U.S.A.',
        website = 'http://www.apress.com'
    WHERE id = 52;

Seleccionar objetos
===================

La creación y actualización de datos seguro es divertida, pero también es inútil
sin una forma de tamizar los datos. Ya hemos visto una forma de examinar todos
los datos de un determinado modelo::

    >>> Publisher.objects.all()
    [<Publisher: Addison-Wesley>, <Publisher: O'Reilly>, <Publisher: Apress Publishing>]

Eso se traslada a esto en SQL::

    SELECT
        id, name, address, city, state_province, country, website
    FROM book_publisher;

.. nota::

    Nota que Django no usa ``SELECT *`` cuando busca datos y en cambio lista
    todos los campos explícitamente. Esto es una decisión de diseño: en
    determinadas circunstancias ``SELECT *`` puede ser lento, y (más importante)
    listar los campos sigue el principio del Zen de Python: "Explícito es mejor
    que implícito".

    Para más sobre el Zen de Python, intenta escribiendo ``import this`` en el
    prompt de Python.

Echemos un vistazo a cada parte de esta linea ``Publisher.objects.all()``:

    * En primer lugar, tenemos nuestro modelo definido, ``Publisher``. Aquí no
      hay nada extraño: cuando quieras buscar datos, usa el modelo para esto.

    * Luego, tenemos ``objects``. Técnicamente, esto es un *administrador*
      (*manager*). Los administradores son discutidos en el Apéndice B. Por
      ahora, todo lo que necesitas saber es que los administradores se encargan
      de todas las operaciones a "nivel de tablas" sobre los datos incluidos, y
      lo más importante, las consultas.

      Todos los modelos automáticamente obtienen un administrador ``objects``;
      debes usar el mismo cada vez que quieras consultar sobre una instancia del
      modelo.

    * Finalmente, tenemos ``all()``. Este es un método del administrador
      ``objects`` que retorna todas las filas de la base de datos. Aunque este
      objeto se *parece* a una lista, es realmente un *QuerySet* -- un objeto
      que representa algún conjunto de filas de la base de datos. El Apéndice C
      describe QuerySets en detalle. Para el resto de este capítulo, sólo
      trataremos estos como listas emuladas.

Cualquier búsqueda en base de datos va a seguir esta pauta general -- llamaremos
métodos del administrador adjunto al modelo en el cual queremos hacer nuestra
consulta.

Filtrar datos
-------------

Aunque obtener todos los objetos es algo que ciertamente tiene su utilidad, la
mayoría de las veces lo que vamos a necesitar es manejarnos sólo con un
subconjunto de los datos. Para ello usaremos el método ``filter()``::

    >>> Publisher.objects.filter(name="Apress Publishing")
    [<Publisher: Apress Publishing>]

``filter()`` toma argumentos de palabra clave que son traducidos en las
cláusulas SQL ``WHERE`` apropiadas. El ejemplo anterior sería traducido en algo
como::

    SELECT
        id, name, address, city, state_province, country, website
    FROM book_publisher
    WHERE name = 'Apress Publishing';

Puedes pasarle a ``filter()`` múltiples argumentos para reducir las cosas aún
más::

    >>> Publisher.objects.filter(country="U.S.A.", state_province="CA")
    [<Publisher: Apress Publishing>]

Esos múltiples argumentos son traducidos a cláusulas SQL ``AND``. Por lo tanto
el ejemplo en el fragmento de código se traduce a lo siguiente::

    SELECT
        id, name, address, city, state_province, country, website
    FROM book_publisher
    WHERE country = 'U.S.A.' AND state_province = 'CA';

Notar que por omisión la búsqueda usa el operador SQL ``=`` para realizar
búsquedas exactas. Existen también otros tipos de búsquedas::

    >>> Publisher.objects.filter(name__contains="press")
    [<Publisher: Apress Publishing>]

Notar el doble guión bajo entre ``name`` y ``contains``. Del mismo modo que
Python, Django usa el doble guión bajo para indicar que algo "mágico" está
sucediendo -- aquí la parte ``__contains`` es traducida por Django en una
sentencia SQL ``LIKE``::

    SELECT
        id, name, address, city, state_province, country, website
    FROM book_publisher
    WHERE name LIKE '%press%';

Hay disponibles varios otos tipos de búsqueda, incluyendo ``icontains`` (``LIKE`` no
sensible a diferencias de mayúsculas/minúsculas), ``startswith`` y ``endswith``,
y ``range`` (consultas SQL ``BETWEEN``). El Apéndice C describe en detalle todos
esos tipos de búsqueda.

Obtener objetos individuales
----------------------------

En ocasiones desearás obtener un único objeto. Para esto existe el método
``get()``::

    >>> Publisher.objects.get(name="Apress Publishing")
    <Publisher: Apress Publishing>

En lugar de una lista (o más bien, un QuerySet), este método retorna un objeto
individual. Debido a eso, una consulta cuyo resultado sean múltiples objetos
causará una excepción::

    >>> Publisher.objects.get(country="U.S.A.")
    Traceback (most recent call last):
        ...
    AssertionError: get() returned more than one Publisher -- it returned 2!

Una consulta que no retorne objeto alguno también causará una excepción::

    >>> Publisher.objects.get(name="Penguin")
    Traceback (most recent call last):
        ...
    DoesNotExist: Publisher matching query does not exist.

Ordenar datos
-------------

A medida que juegas con los ejemplos anteriores, podrías descubrir que los
objetos son devueltos en lo que parece ser un orden aleatorio. No estás
imaginándote cosas, hasta ahora no le hemos indicado a la base de datos cómo
ordenar sus resultados, de manera que simplemente estamos recibiendo datos con
algún orden arbitrario seleccionado por la base de datos.

Eso es, obviamente, un poco ingenuo. No quisiéramos que una página Web que
muestra una lista de editores estuviera ordenada aleatoriamente. Así que, en la
práctica, probablemente querremos usar ``order_by()`` para reordenar nuestros
datos en listas más útiles::

    >>> Publisher.objects.order_by("name")
    [<Publisher: Addison-Wesley>, <Publisher: Apress Publishing>, <Publisher: O'Reilly>]

Esto no se ve muy diferente del ejemplo de ``all()`` anterior, pero el SQL
incluye ahora un ordenamiento específico::

    SELECT
        id, name, address, city, state_province, country, website
    FROM book_publisher
    ORDER BY name;

Podemos ordenar por cualquier campo que deseemos::

    >>> Publisher.objects.order_by("address")
    [<Publisher: O'Reilly>, <Publisher: Apress Publishing>, <Publisher: Addison-Wesley>]

    >>> Publisher.objects.order_by("state_province")
    [<Publisher: Apress Publishing>, <Publisher: Addison-Wesley>, <Publisher: O'Reilly>]

y por múltiples campos::

    >>> Publisher.objects.order_by("state_provice", "address")
     [<Publisher: Apress Publishing>, <Publisher: O'Reilly>, <Publisher: Addison-Wesley>]

También podemos especificar un ordenamiento inverso antecediendo al nombre del
campo un prefijo ``-`` (el símbolo menos)::

    >>> Publisher.objects.order_by("-name")
    [<Publisher: O'Reilly>, <Publisher: Apress Publishing>, <Publisher: Addison-Wesley>]

Aunque esta flexibilidad es útil, usar ``order_by()`` todo el tiempo puede ser
demasiado repetitivo. La mayor parte del tiempo tendrás un campo particular por
el que usualmente desearás ordenar. Es esos casos Django te permite anexar al
modelo un ordenamiento por omisión para el mismo:

.. literal-evaluado::

    class Publisher(models.Model):
        name = models.CharField(maxlength=30)
        address = models.CharField(maxlength=50)
        city = models.CharField(maxlength=60)
        state_province = models.CharField(maxlength=30)
        country = models.CharField(maxlength=50)
        website = models.URLField()

        def __str__(self):
            return self.name

        **class Meta:**
            **ordering = ["name"]**

Este fragmento ``ordering = ["name"]`` le indica a Django que a menos que se
proporcione un ordenamiento mediante ``order_by()``, todos los editores deberán
ser ordenados por su nombre.

.. exhortacion:: ¿Qué es este asunto de Meta?

    Django usa esta ``class Meta`` interna como un lugar en el cual se pueden
    especificar metadatos  adicionales acerca de un modelo. Es completamente
    opcional, pero puede realizar algunas cosas muy útiles. Examina el Apéndice
    B para conocer las opciones que puede poner bajo ``Meta``.

Encadenar búsquedas
-------------------

Has visto cómo puedes filtrar datos y has visto cómo ordenarlos. En ocasiones,
por supuesto, vas a desear realizar ambas cosas. En esos casos simplemente
"encadenas" las búsquedas entre sí::

    >>> Publisher.objects.filter(country="U.S.A.").order_by("-name")
    [<Publisher: O'Reilly>, <Publisher: Apress Publishing>, <Publisher: Addison-Wesley>]

Como podrías esperar, esto se traduce a una consulta SQL conteniendo tanto un
``WHERE`` como un ``ORDER BY``::

    SELECT
        id, name, address, city, state_province, .. code-block:: sqlcountry, website
    FROM book_publisher
    WHERE country = 'U.S.A.'
    ORDER BY name DESC;

Puedes encadenar consultas en forma consecutiva tantas veces como desees. No
existe un límite para esto.

Rebanar datos
-------------

Otra necesidad común es buscar sólo un número fijo de filas. Imagina que tienes
miles de editores en tu base de datos, pero quieres mostrar sólo el primero.
Puedes hacer eso usando la sintaxis estándar de Python para el rebanado de
listas::

    >>> Publisher.objects.all()[0]
    <Publisher: Addison-Wesley>

Esto se traduce, someramente, a::

    SELECT
        id, name, address, city, state_province, country, website
    FROM book_publisher
    ORDER BY name
    LIMIT 1;

.. exhortacion::  Y más...

    Hemos sólo arañado la superficie del manejo de modelos, pero deberías ya
    conocer lo suficiente para entender todos los ejemplos del resto del libro.
    Cuando estés listo para aprender los detalles completos detrás de las
    búsquedas de objetos, échale una mirada al Apéndice C.

Eliminar objetos
================

Para eliminar objetos, simplemente llama al método ``delete()`` de tu objeto::

    >>> p = Publisher.objects.get(name="Addison-Wesley")
    >>> p.delete()
    >>> Publisher.objects.all()
    [<Publisher: Apress Publishing>, <Publisher: O'Reilly>]

Puedes también borrar objetos al por mayor llamando a ``delete()`` en el
resultado de algunas búsquedas::

    >>> publishers = Publisher.objects.all()
    >>> publishers.delete()
    >>> Publisher.objects.all()
    []

.. nota::

    Los borrados son *permanentes*, así que, ¡se cuidadoso!. En efecto, es
    usualmente una buena idea evitar eliminar objetos a menos que realmente
    tengas que hacerlo -- las base de datos relacionales no tiene una
    característica "deshacer" muy buena, y recuperar desde copias de respaldo es
    doloroso.

    A menudo es una buena idea agregar banderas "activo" a tus modelos de datos.
    Puedes buscar sólo objetos "activos", y simplemente fijar el campo activo a
    ``False`` en lugar de eliminar el objeto. Entonces, si descubres que has
    cometido un error, puedes simplemente volver a conmutar el estado de la
    bandera.

Realizar cambios en el esquema de una base de datos
===================================================

Cuando presentamos el comando ``syncdb`` previamente en este capítulo, hicimos
notar que ``syncdb`` simplemente crea tablas que todavía no existen en tu base
de datos -- *no* sincroniza cambios en modelos ni borra modelos. Si agregas o
modificas un campo de un modelo o si eliminas un modelo, será necesario que
realices el cambio en tu base de datos en forma manual. Esta sección explica cómo
hacerlo.

Cuando estás realizando cambios de esquema, es importante tener presente algunas
características de la capa de base de datos de Django:

    * Django se quejará estrepitosamente si un modelo contiene un campo que
      todavía no ha sido creado en la tabla de la base de datos. Esto causará un
      error la primera vez que uses la API de base de datos de Django para
      consultar la tabla en cuestión (esto es, ocurrirá en tiempo de ejecución y
      no en tiempo de compilación).

    * A Django no le importa si una tabla de base de datos contiene columnas que
      no están definidas en el modelo.

    * A Django no le importa si una base de datos contiene una tabla que no está
      representada por un modelo.

El realizar cambios al esquema de una base de datos es cuestión  de cambiar las
distintas piezas -- el código Python y la base de datos en sí misma -- en el
orden correcto.

Agregar campos
--------------

Cuando se agrega un campo a una tabla/modelo en un entorno de producción, el
truco es sacar ventaja del hecho que a Django no le importa si una tabla
contiene columnas que no están definidas en el modelo. La estrategia es agregar
la columna en la base de datos y luego actualizar el modelo Django para que
incluya el nuevo campo.

Sin embargo, tenemos aquí un pequeño problema del huevo y la gallina, porque
para poder saber cómo debe expresarse la nueva columna en SQL, necesitas ver la
salida producida por el comando ``manage.py sqlall`` de Django, el cual requiere
que el campo exista en el modelo. (Notar que *no* es un requerimiento el que
crees tu columna con exactamente el mismo SQL que usaría Django, pero es una
buena idea el hacerlo para estar seguros de que todo está en sincronía).

La solución al problema del huevo y la gallina es usar un entorno de desarrollo
en lugar de realizar los cambios en un servidor de producción. (*Estás* usando
un entorno de pruebas/desarrollo, ¿no es cierto?). Este es el detalle de los
pasos a seguir.

Primero, realiza los siguientes pasos en el entorno de desarrollo (o sea, no en
el servidor de producción):

    1. Agrega el campo a tu modelo.

    2. Ejecuta ``manage.py sqlall [yourapp]`` para ver la nueva sentencia
       ``CREATE TABLE`` para el modelo. Toma nota de la definición de la columna
       para el nuevo campo.

    3. Arranca el shell interactivo de tu base de datos (por  ej. ``psql`` o
       ``mysql``, o puedes usar ``manage.py dbshell``). Ejecuta una sentencia
       ``ALTER TABLE`` que agregue tu nueva columna.

    4. (Opcional) Arranca el shell interactivo de Python con ``manage.py shell``
       y verifica que el nuevo campo haya sido agregado correctamente importando
       el modelo y seleccionando desde la tabla (por ej.
       ``MyModel.objects.all()[:5]``).

Entonces en el servidor de producción realiza los siguientes pasos:

    1. Arranca el shell interactivo de tu base de datos.

    2. Ejecuta la sentencia ``ALTER TABLE`` que usaste en el paso 3 de
       arriba.

    3. Agrega el campo a tu modelo. Si estás usando un sistema de control de
       revisiones de código fuente y has realizado un *check in* de la
       modificación del paso 1 del trabajo en el entorno de desarrollo, entonces
       puedes actualizar el código (por ej. ``svn update`` si usas Subversion)
       en el servidor de producción.

    4. Reinicia el servidor Web para que los cambios en el código surtan efecto.

Por ejemplo, hagamos un repaso de los que haríamos si agregáramos un campo
``num_pages`` al modelo ``Book`` descrito previamente en este capítulo. Primero,
alteraríamos el modelo en nuestro entorno de desarrollo para que se viera así:

.. literal-evaluado::

    class Book(models.Model):
        title = models.CharField(maxlength=100)
        authors = models.ManyToManyField(Author)
        publisher = models.ForeignKey(Publisher)
        publication_date = models.DateField()
        **num_pages = models.IntegerField(blank=True, null=True)**

        def __str__(self):
            return self.title

(Nota: Revisa el apartado "Agregando columnas NOT NULL" para conocer detalles
importantes acerca de porqué hemos incluido ``blank=True`` y ``null=True``).

Luego ejecutaríamos el comando ``manage.py sqlall books`` para ver la sentencia
``CREATE TABLE``. La misma se vería similar a esto::

    CREATE TABLE "books_book" (
        "id" serial NOT NULL PRIMARY KEY,
        "title" varchar(100) NOT NULL,
        "publisher_id" integer NOT NULL REFERENCES "books_publisher" ("id"),
        "publication_date" date NOT NULL,
        "num_pages" integer NULL
    );

La nueva columna está representada de la siguiente manera::

    "num_pages" integer NULL

A continuación, arrancaríamos el shell interactivo de base de datos en nuestra
base de datos de desarrollo escribiendo ``psql`` (para PostgreSQL), y
ejecutaríamos la siguiente sentencia::

    ALTER TABLE books_book ADD COLUMN num_pages integer;

.. exhortacion:: Agregando columnas NOT NULL

    Existe un detalle sutil aquí que merece ser mencionado. Cuando agregamos el
    campo ``num_pages`` a nuestro modelo, incluimos las opciones ``blank=True``
    y ``null=True``. Lo hicimos porque una columna de una base de datos
    contendrá inicialmente valores NULL desde el momento que la crees.

    Sin embargo, es también posible agregar columnas que no puedan contener
    valores NULL. Para hacer esto, tienes que crear la columna como ``NULL``,
    luego poblar los valores de la columna usando algunos valor(es) por omisión,
    y luego modificar la columna para activar el modificador ``NOT NULL``. Por
    ejemplo::

        BEGIN;
        ALTER TABLE books_book ADD COLUMN num_pages integer;
        UPDATE books_book SET num_pages=0;
        ALTER TABLE books_book ALTER COLUMN num_pages SET NOT NULL;
        COMMIT;

    Si sigues este camino, recuerda que debes quitar ``blank=True`` y
    ``null=True`` de tu modelo.

Luego de la sentencia ``ALTER TABLE``, verificaríamos que el cambio haya
funcionado correctamente, para ello iniciaríamos el shell de Python y
ejecutaríamos este código::

    >>> from mysite.books.models import Book
    >>> Book.objects.all()[:5]

Si dicho código no produjera errores, podríamos movernos a nuestro servidor de
producción y ejecutaríamos la sentencia ``ALTER TABLE`` en la base de datos de
producción. Entonces, actualizaríamos el modelo en el entorno de producción y
reiniciaríamos el servidor Web.

Eliminar campos
---------------

Eliminar un campo de un modelo es mucho más fácil que agregar uno. Para borrar
un campo, sólo sigue los siguientes pasos:

    1. Elimina el campo de tu modelo y reinicia el servidor Web.

    2. Elimina la columna de tu base de datos, usando un comando como este::

           ALTER TABLE books_book DROP COLUMN num_pages;

Eliminar campos Many-to-Many
----------------------------

Debido a que los campos many-to-many son diferentes a los campos normales, el
proceso de borrado es diferente:

    1. Elimina el campo ``ManyToManyField`` de tu modelo y reinicia el servidor
       Web.

    2. Elimina la tabla many-to-many de tu base de datos, usando un comando como
       este::

           DROP TABLE books_books_publishers;

Eliminar modelos
----------------

Eliminar completamente un modelo es tan fácil como el eliminar un campo. Para
borrar un modelo, sigue los siguientes pasos:

    1. Elimina el modelo de tu archivo ``models.py`` y reinicia el servidor Web.

    2. Elimina la tabla de tu base de datos, usando un comando como este::

           DROP TABLE books_book;

¿Qué sigue?
===========

Una vez que has definido tus modelos, el paso siguiente es el poblar tu base de
datos con datos. Podrías tener datos legados, en cuyo caso el :doc:`Capítulo 16<chapter16>` te
aconsejará acerca de cómo integrar bases de datos heredadas. Podrías delegar en
los usuario del sitio la provisión de los datos, en cuyo caso el :doc:`Capítulo 7<chapter07>` te
enseñará cómo procesar datos enviados por los usuarios mediante formularios.

Pero en algunos casos, tú o tu equipo podrían necesitar ingresar datos en forma
manual, en cuyo caso sería de ayuda el disponer de una interfaz basada en Web
para el ingreso y el manejo de los datos. El :doc:`próximo capítulo<chapter06>`  está dedicado
a la interfaz de administración de Django, la cual existe precisamente por esa
razón.


