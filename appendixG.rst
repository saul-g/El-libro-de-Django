======================================
Apéndice G: El utilitario django-admin
======================================

``django-admin.py`` es el utilitario de linea de comandos de Django para tareas
administrativas.

Este apéndice explica sus múltiples poderes.

Usualmente accedes a ``django-admin.py`` a través del wrapper del proyecto
``manage.py``. ``manage.py`` es creado automáticamente en cada proyecto Django
y es un wrapper liviano en torno a ``django-admin.py``. Toma cuidado de dos
cosas por ti antes de delegar a ``django-admin.py``:

* Pone el paquete de tu proyecto en  ``sys.path``.

* Establece la variable de entorno ``DJANGO_SETTINGS_MODULE`` para que
  apunte al archivo ``settings.py`` de tu proyecto.

El script ``django-admin.py`` debe estar en la ruta de tu sistema si instalaste
Django mediante su utilitario ``setup.py``. Si no está en tu ruta, puedes
encontrarlo en ``site-packages/django/bin`` dentro de tu instalación de Python.
Considera establecer un enlace simbólico a él desde algún lugar en tu ruta,
como en ``/usr/local/bin``.

Los usuarios de Windows, que no disponen de la funcionalidad de los enlaces
simbólicos, pueden copiar ``django-admin.py`` a una ubicación que esté en su
ruta existente o editar la configuración del ``PATH`` (bajo Configuración ~TRA
Panel de Control ~TRA Sistema ~TRA Avanzado ~TRA Entorno) para apuntar a la
ubicación de su instalación.

Generalmente, cuando se trabaja en un proyecto Django simple, es más fácil usar
``manage.py``. Usa ``django-admin.py`` con ``DJANGO_SETTINGS_MODULE`` o la
opción de línea de comando ``--settings``, si necesitas cambiar entre múltiples
archivos de configuración de Django.

Los ejemplos de línea de comandos a lo largo de este apéndice usan
``django-admin.py`` para ser consistentes, pero cada ejemplo puede usar de la
misma forma ``manage.py``.

Uso
===

El uso básico es::

    django-admin.py action [options]

o::

    manage.py action [options]

``action`` debe ser una de las acciones listadas en este documento.
``options``, que es opcional, deben ser cero o más opciones de las listadas en
este documento.

Ejecuta ``django-admin.py --help`` para ver un mensaje de ayuda que incluye
una larga lista de todas las opciones y acciones disponibles.

La mayoría de las acciones toman una lista de nombres de aplicación. Un
*nombre de aplicación* es el nombre base del paquete que contiene tus modelos.
Por ejemplo, si tu ``INSTALLED_APPS`` contiene el string ``'mysite.blog'``, el
nombre de la aplicación es ``blog``.

Acciones Disponibles
====================
Las siguientes secciones cubren las acciones disponibles.

adminindex [appname appname ...]
--------------------------------

Imprime el snippet de la plantilla de admin-index para los nombres de
aplicación dados. Usa los snippets de la plantilla de admin-index si quiere
personalizar la apariencia de la página del índice del administrador.

createcachetable [tablename]
----------------------------

Crea una tabla de cache llamada ``tablename`` para usar con el back-end de
cache de la base de datos. Ver el `Capítulo 13`_ para más acerca de caching.

dbshell
-------

Corre el cliente de línea de comandos del motor de base de datos especificado
en tu configuración de ``DATABASE_ENGINE``, con los parámetros de conexión
especificados en la configuración de ``DATABASE_USER``, ``DATABASE_PASSWORD``,
etc.

* Para PostgreSQL, esto ejecuta el cliente de línea de comandos ``psql`` .

* For MySQL, esto ejecuta el cliente de línea de comandos ``mysql``.

* For SQLite, esto ejecuta el cliente de línea de comandos ``sqlite3``.

Este comando asume que los programas están en tu ``PATH`` de manera que una
simple llamada con el nombre del programa (``psql``, ``mysql``, o ``sqlite3``)
encontrará el programa en el lugar correcto. No hay forma de especificar
en forma manual la localización del programa.

diffsettings
------------

Muestra las diferencias entre la configuración actual y la configuración por
omisión de Django.

Las configuraciones que no aparecen en la configuración por omisión están
seguidos por ``"###"``. Por ejemplo, la configuración por omisión no define
``ROOT_URLCONF``, por lo que si aparece ``ROOT_URLCONF`` en la salida de
``diffsettings`` lo hace seguido de ``"###"``.

Observa que la configuración por omisión de Django habita en
``django.conf.global_settings``, si alguna vez sientes curiosidad por ver la
lista completa de valores por omisión.

dumpdata [appname appname ...]
------------------------------

Dirige a la salida estándar todos los datos de la base de datos asociados con
la(s) aplicación(es) nombrada(s).

Por omisión, la base de datos será volcada en formato JSON. Si quieres que la
salida esté en otro formato, usa la opción ``--format`` (ej.: ``format=xml``).
Puedes especificar cualquier back-end de serialización de Django (incluyendo
cualquier back-end de serialización especificado por el usuario mencionado en
la configuración de ``SERIALIZATION_MODULES`` setting). La opción ``--indent``
puede ser usada para lograr una impresión diseñada de la salida.

Si no se provee niingún nombre de aplicación, se volcarán todas las
aplicaciones instaladas.

La salida de ``dumpdata`` puede usarse como entrada para ``loaddata``.

flush
-----

Devuelve la base de datos al estado en el que estaba inmediatemente después de
que se ejecutó syncdb. Esto significa que todos los datos serán eliminados de
la base de datos, todo manejador de postsinchronización será reejecutado, y el
componente ``initial_data`` será reinstalado.

inspectdb
---------

Realiza la introspección sobre las tablas de la base de datos apuntada por la
configuración ``DATABASE_NAME`` y envía un modulo de modelo de Django (un
archivo ``models.py``) a la salida estándar.

Usa esto si tienes una base de datos personalizada con la cual quieres usar
Django. El script inspeccionará la base de datos y creará un modelo para cada
tabla que contenga.

Como podrás esperar, los modelos creados tendrán un atributo por cada campo de
la tabla. Observa que ``inspectdb`` tiene algunos casos especiales en los
nombres de campo resultantes:

* Si ``inspectdb`` no puede mapear un tipo de columna a un tipo de campo
  del modelo, usará ``TextField`` e insertará el comentario Python
  ``'This field type is a guess.'`` junto al campo en el modelo generado.

* Si el nombre de columna de la base de datos es una palabra reservada de
  Python( como ``'pass'``, ``'class'``, o ``'for'``), ``inspectdb``
  agregará ``'_field'`` al nombre de atributo. Por ejemplo, si una tabla
  tiene una columna ``'for'``, el modelo generado tendrá un campo
  ``'for_field'``, con el atributo ``db_column`` establecido en  ``'for'``.
  ``inspectdb`` insertará el comentario Python ``'Field renamed because it
  was a Python reserved word.'`` junto al campo.

Esta característica está pensada como un atajo, no como la generación
de un modelo definitivo. Después de ejecutarla, querrás revisar los modelos
genrados para personalizarlos. En particular, necesitarás reordenar los modelos
de manera tal que las relaciones esten ordenadas adecuadamente.

Las claves primarias son detectadas automáticamente durante la introspección
para PostgreSQL, MySQL, y SQLite, en cuyo caso Django coloca
``primary_key=True`` donde sea necesario.

``inspectdb`` trabaja con PostgreSQL, MySQL, y SQLite. La detección de claves
foráneas solo funciona en PostgreSQL y con ciertos tipos de tablas MySQL.

loaddata [fixture fixture ...]
------------------------------

Busca y carga el contenido del 'fixture' nombrado en la base de datos.

Un *fixture* es una colección de archivos que contienen los contenidos de la
base de datos serializados. Cada fixture tiene un nombre único; de todas
formas, los archivos que conforman el fixture pueden estar distribuidos en
varios directorios y en varias aplicaciones.

Django buscará fixtures en tres ubicaciones:

* En el directorio ``fixtures`` de cada aplicación instalada.
* En todo directorio nombreado en la configuración ``FIXTURE_DIRS``
* En el path literal nombrado por el fixture

Django cargará todos los fixtures que encuentre en estas ubucaciones que
coincidan con los nombres de fixture dados.

Si el fixture nombrado tiene una extensión de archivo, sólo se cargarán
fixtures de ese tipo. Por ejemplo lo siguiente::

    django-admin.py loaddata mydata.json

sólo cargará fixtures JSON llamados ``mydata``. La extensión del fixture debe
corresponder al nombre registrado de un serializador (ej.: ``json`` o ``xml``).

Si omites la extensión, Django buscará todos los tipos de fixture disponibles
para un fixture coincidente. Por ejemplo, lo siguiente::

    django-admin.py loaddata mydata

buscará todos los fixture de cualquier tipo de fixture llamado ``mydata``. Si
un directorio de fixture contiene ``mydata.json``, ese fixture será cargado
como un fixture JSON. De todas formas, si se descubren dos fixtures con el
mismo nombre pero diferente tipo (ej.: si se encuentran ``mydata.json`` y
``mydata.xml`` en el mismo directorio de fixture), la instalación de fixture
será abortada, y todo dato instalado en la llamada a ``loaddata`` será removido
de la base de datos.

Los fixtures que son nombrados pueden incluir como componentes directorios.
Estos directorios serán incluidos en la ruta de búsqueda. Por ejemplo, lo
siguiente::

    django-admin.py loaddata foo/bar/mydata.json

buscará ``<appname>/fixtures/foo/bar/mydata.json`` para cada aplicación
instalada, ``<dirname>/foo/bar/mydata.json`` para cada directorio en
``FIXTURE_DIRS``, y la ruta literal ``foo/bar/mydata.json``.

Observa que el orden en que cada fixture es procesado es indefinido. De todas
formas, todos los datos de fixture son instalados en una única transacción, por
lo que los datos en un fixture pueden referenciar datos en otro fixture. Si el
back-end de la base de datos admite restricciones a nivel de registro, estas
restricciones serán chequeadas al final de la transacción.

El comando ``dumpdata`` puede ser usado para generar la entrada para
``loaddata``.

.. admonition:: MySQL y los Fixtures

    Desafortunadamente, MySQL no es capaz de dar soporte completo para todas las
    características de las fixtures de Django. Si usas tablas MyISAM, MySQL no
    admite transacciones ni restricciones, por lo que no tendrás rollback
    si se encuentran varios archivos de transacción, ni validación de los datos
    de fixture. Si usas tablas InnoDB tables, no podrás tener referencias hacia
    adelante en tus archivos de datos -- MySQL no provee un mecanismo para
    retrasar el chequeo de las restricciones de registro hasta que la
    transacción es realizada.

reset [appname appname ...]
---------------------------
Ejecuta el equivalente de ``sqlreset`` para los nombres de aplicación dados.

runfcgi [options]
-----------------
Inicia un conjunto de procesos FastCGI adecuados para su uso con cualquier
servidor Web que admita el protocolo FastCGI. Ver `Capítulo 20`_ para más
información acerca del desarrollo bajo FastCGI.

Este comando requiere el módulo Python FastCGI de ``flup``
(http://www.djangoproject.com/r/flup/).

runserver [número de puerto opcional, or direcciónIP:puerto]
------------------------------------------------------------

Inicia un servidor Web liviano de desarollo en la máquina local. machine. Por
omisión, el servidor ejecuta en el puerto 8000 de la dirección IP 127.0.0.1.
Puedes pasarle explícitamente una dirección IP y un número de puerto.

Si ejecutas este script como un usuario con privilegios normales (recomendado),
puedes no tener acceso a iniciar un puerto en un número de puerto bajo. Los
números de puerto bajos son reservados para el superusuario  (root).

.. admonition:: Advertencia:

    **No uses este servidor en una configuración de producción**. No se le han
    relizado auditorías de seguridad o tests de performance, y no hay planes de
    cambiar este hecho. Los desarrolladores de Django están en el negocio de
    hacer Web frameworks, no servidores Web, por lo que mejorar este servidor
    para que pueda manejar un entorno de producción está fuera del alcance de
    Django.

El servidor de desarrollo carga automáticamente el código Python para cada
pedido según sea necesario. No necesitas reiniciar el servidor para que los
cambios en el código tengan efecto.

Cuando inicias el servidor, y cada vez que cambies código Python mientras el
servidor está ejecutando, éste validará todos tus modelos instalados. (Ver la
sección que viene sobre el comando ``validate``.) Si el validador encuentra
errores, los imprimirá en la salida estándar, pero no detendrá el servidor.

Puedes ejecutar tantos servidores como quieras, siempre que ejecuten en puertos
separados. Sólo ejecuta ``django-admin.py runserver`` más de una vez.

Observa que la dirección IP por omisión, 127.0.0.1, no es accesible desde las
otras máquinas de la red. Para hacer que el servidor de desarrollo sea visible
a las otras máquinas de la red, usa su propia dirección IP (ej.: 192.168.2.1) o
0.0.0.0.

Por ejemplo, para ejecutar el servidor en el puerto 7000 en la dirección IP
127.0.0.1, usa esto::

    django-admin.py runserver 7000

O para ejecutar el servidos en el puerto 7000 en la dirección IP 1.2.3.4, usa
esto::

    django-admin.py runserver 1.2.3.4:7000

Sirviendo Archivos Estáticos con el Servidor de Desarrollo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Por omisión, el servidor de desarrollo no sirve archivos estáticos para tu
sitio (como archivos CSS, imágenes, cosas bajo ``MEDIA_ROOT_URL``, etc.). Si
quieres configurar Django para servir medios estáticos, lee acerca de esto en
http://www.djangoproject.com/documentation/0.96/static_files/.

Deshabilitando Autoreload
~~~~~~~~~~~~~~~~~~~~~~~~~

Para deshabilitar la recarga automática del código mientras el servidor de
desarrollo se ejecuta, usa la opción ``--noreload``, como en::

    django-admin.py runserver --noreload

shell
-----

Inicia el intérprete interactivo de Python.

Django utilizará IPython (http://ipython.scipy.org/) si no está instalado. Si
tienes IPython instalado y quieres forzar el uso del intérprete Python "plano",
usa la opción ``--plain``, como en::

    django-admin.py shell --plain

sql [appname appname ...]
-------------------------

Imprime las sentencias SQL ``CREATE TABLE`` para las aplicaciones mencionadas.

sqlall [appname appname ...]
----------------------------

Imprime las sentencias SQL ``CREATE TABLE`` y los datos iniciales para las
aplicaciones mencionadas.

Busca en la descripción de ``sqlcustom`` para una explicación de como
especificar los datos iniciales.

sqlclear [appname appname ...]
------------------------------

Imprime las sentencias SQL ``DROP TABLE`` para las aplicaciones mencionadas.

sqlcustom [appname appname ...]
-------------------------------

Imprime las sentencias SQL personalizadas para las aplicaciones mencionadas.

Para cada modelo en cada aplicación especificada, este comando busca el archivo
``<appname>/sql/<modelname>.sql``, donde ``<appname>`` es el nombre de la
aplicación dada y ``<modelname>`` es el nombre del modelo en minúsculas. Por
ejemplo, si tienes una aplicación ``news`` que incluye un modelo ``Story``,
``sqlcustom`` tratará de leer un archivo ``news/sql/story.sql`` y lo agregará
a la salida de este comando.

Se espera que cada uno de los archivos SQL, si son dados, contengan SQL válido.
Los archivos SQL son canalizados directamente a la base de datos después que se
hayan ejecutado todas las sentencias de creación de tablas de los modelos.
Usa este enlace SQL para hacer cualquier modificación de tablas, o insertar
funciones SQL en las bases de datos.

Observa que el orden en que se procesan los archivos SQL es indefinido.

sqlindexes [appname appname ...]
--------------------------------

Imprime las sentencias SQL ``CREATE INDEX`` para las aplicaciones mencionadas.

sqlreset [appname appname ...]
------------------------------

Imprime las sentencias SQL ``DROP TABLE`` seguidas de las ``CREATE TABLE`` para
las aplicaciones mencionadas.

sqlsequencereset [appname appname ...]
--------------------------------------

Imprime las sentencias SQL para reinicializar las secuencias de las aplicaciones
mencionadas.

Necesitarás esta SQL solo si estás usando PostgreSQL y has insertado datos a
mano. Cuando haces eso, las secuencias de las claves primarias de PostgreSQL
pueden quedar fuera de sincronismo con las que están en la base de datos, y las
SQL que genera este comando las limpiarán.

startapp [appname]
------------------

Crea una estructura de directorios para una aplicación Django con el nombre de
aplicación dado, en el directorio actual.

startproject [projectname]
--------------------------

Crea una estructura de directorios Django para el nombre de proyecto dado, en
el directorio actual.

syncdb
------

Crea las tablas de la base de datos para todas las aplicaciones en
``INSTALLED_APPS`` cuyas tablas aún no hayan sido creadas.

Usa este comando cuando hayas agregado nuevas aplicaciones a tu proyecto y
quieras instalarlas en la base de datos. Esto incluye cualquier aplicación
incorporada en Django que esté en ``INSTALLED_APPS`` por omisión. Cuando
empieces un nuevo proyecto, ejecuta este comando para instalas las aplicaciones
predeterminadas.

Si estás instalando la aplicación ``django.contrib.auth``, ``syncdb`` te dará
la opción de crear un superusuario inmediatamente. ``syncdb`` también buscará e
instalará algun fixture llamado ``initial_data``. Ver la documentación de
``loaddata`` para los detalles de la especificación de los archivos de datos de
fixture.

test
----

Descubre y ejecuta las pruebas para todos los modelos instalados. El testeo aún
está en desarrollo mientras se escribe este libro, así que para aprender más
necesitarás leer la documentación online en
http://www.djangoproject.com/documentation/0.96/testing/.

validate
--------

Valida todos los modelos instalados (según la configuración de
``INSTALLED_APPS``) e imprime errores de validación en la salida estándar.

Opciones Disponibles
====================

Las secciones que siguen delinean las opciones que puede tomar
``django-admin.py``.

--settings
----------

Ejemplo de uso::

    django-admin.py syncdb --settings=mysite.settings

Especifica explícitamente el módulo de configuración a usar. El módulo de
configuración debe estar en la sintaxis de paquetes de Python (ej.:
``mysite.settings``). Si no se proveen, ``django-admin.py`` utilizará la
variable de entorno ``DJANGO_SETTINGS_MODULE``.

Observa que esta opción no es necesaria en ``manage.py``, ya que toma en cuenta
la configuración de ``DJANGO_SETTINGS_MODULE`` por tí.

--pythonpath
------------

Ejemplo de uso::

    django-admin.py syncdb --pythonpath='/home/djangoprojects/myproject'

Agrega la ruta del sistema de archivos a la ruta de búsqueda de importación de
Python. Si no se define, ``django-admin.py`` usará la variable de entorno ``PYTHONPATH``.

Observa que esta opción no es necesaria en ``manage.py``, ya que tiene cuidado
de configurar la ruta de Python por tí.

--format
--------

Ejemplo de uso::

    django-admin.py dumpdata --format=xml

Especifica el formato de salida que será utilizado. El nombre provisto debe
ser el nombre de un serializador registrado.

--help
------

Muestra un mensaje de ayuda que incluye una larga lista de todas las opciones
y acciones disponibles.

--indent
--------

Ejemplo de uso::

    django-admin.py dumpdata --indent=4

Especifica el número de espacios que se utilizarán para la indentación cuando
se imprima una salida con formato de impresión. Por omisión, la salida *no*
tendrá formato de impresión.
El formato de impresión solo estará habilitado si se provee la opción de
indentación.

--noinput
---------

Indica que no quieres que se te pida ninguna entrada. Es útil cuando el script
``django-admin`` se ejecutará en forma automática y desatendida.

--noreload
----------

Deshabilita el uso del autoreloader cuando se ejecuta el servidor de desarrollo.

--version
---------

Muestra la versión actual de Django.

Ejemplo de salida::

    0.9.1
    0.9.1 (SVN)

--verbosity
-----------

Ejemplo de uso::

    django-admin.py syncdb --verbosity=2

Determina la cantidad de notificaciones e información de depuración que se
imprimirá en la consola. ``0`` es sin salida, ``1`` es salida normal, y ``2``
es salida con explicaciones.

--adminmedia
------------

Ejemplo de uso::

    django-admin.py --adminmedia=/tmp/new-admin-style/

Le dice a Django donde encontrar los archivos CSS y JavaScript para la
interfaz de administración cuando se ejecuta el servidor de desarrollo.
Normalmente estos archivos son servidos por fuera del arbol de fuentes Django
pero como algunos diseñadores personalizan estos archivos para su sitio, esta
opción te permite testear con versiones personalizadas.
