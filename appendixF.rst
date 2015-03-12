======================================
Apéndice F: El utilitario django-admin
======================================

``django-admin.py`` es **el utilitario de línea de comandos** de Django, diseñado
para realizar tareas administrativas.

Este apéndice explica sus múltiples poderes.

Usualmente accedes a ``django-admin.py`` a través del ``wrapper`` del proyecto
``manage.py``, ``manage.py`` es creado automáticamente en cada proyecto Django
y es un ``wrapper`` liviano en torno a ``django-admin.py``. Toma cuidado de dos
cosas por ti antes de delegar a ``django-admin.py``:

* Pone el paquete de tu proyecto en  ``sys.path``.

* Establece la variable de entorno ``DJANGO_SETTINGS_MODULE`` para que
  apunte al archivo ``settings.py`` de tu proyecto.

* Lama a :func:`django.setup()` para inicializar varias  funciones internas de
  Django.

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

.. code-block:: bash

    $ django-admin <comando> [opciones]
    $ manage.py <comando> [opciones]

``comando`` debe ser uno de los comandos listados en este documento. 
``optiones``, opcionalmente, deben ser cero o más opciones de las listadas en
este documento.

Obtener ayuda
-------------

.. django-admin:: help

Ejecuta ``django-admin help``  para mostrar la información de uso y una lista de
todos los comandos proporcionados por cada aplicación.

Ejecuta ``django-admin help --commands`` para mostrar una lista de todos los 
comandos disponibles.

Ejecuta ``django-admin help <command>`` para mostrar la descripción de un 
comando dado y una lista de las opciones disponibles.

Nombres de aplicaciones
-----------------------

Muchos de los subcomandos toman una lista de "nombres de aplicaciones". Un
``nombre de una aplicación`` es el nombre base del el paquete que contiene el 
modelo. Por ejemplo, si tu  ``INSTALLED_APPS`` contiene la cadena
``'misitio.blog'``,  el nombre de la aplicación es ``blog``.

Determinar la version
---------------------

.. django-admin:: version

Ejecuta ``django-admin.py --version`` para mostrar la version actual de Django.

Ejemplos de la salida::

    1.8
    1.4
    1.1
    1.0    

Mostrar la salida de depuración
--------------------------------

Usa ``--verbosity`` para especificar la cantidad de notificaciones e información
de depuración que ``django-admin.py``  debe imprimir en consola.  Para mas
información consulta la documentación de la opción :djadminopt:`--verbosity`.

Subcomandos Disponibles
=======================

Las siguientes secciones cubren las acciones disponibles.

check <appname appname ...>
---------------------------

.. django-admin:: check

Usa el ``framework check`` para inspeccionar  el proyecto completo para detectar
problemas comunes. 

El ``framework check`` Confirma que no haya ningún problema con los modelos 
instalados o los registros en la interfaz administrativa. También provee de  
advertencias para detectar problemas comunes de compatibilidad, introducidos al 
actualizar Django a una nueva versión. También se pueden realizar chequeos 
personalizados usando otras  bibliotecas y otras aplicaciones.

De forma predeterminada, todas las aplicaciones serán checadas. Puedes checar
un conjunto de aplicaciones proporcionando una lista, de cada una de las 
aplicaciones como argumentos::

    python manage.py check auth admin myapp

Si no especificas ninguna aplicación, todas las aplicaciones serán checadas.

.. django-admin-option:: --tag <tagname>

El ``framework check`` realiza diferentes tipos de chequeos. Estos tipos de 
chequeos están clasificados en diferentes categorías, agrupadas en etiquetas.
Puedes usar estas etiquetas para restringir el chequeo realizado a una categoría 
en especifico. Por ejemplo para únicamente realizar un chequeo de seguridad y 
compatibilidad, puedes  ejecutar::

    python manage.py check --tag security --tag compatibility

.. django-admin-option:: --list-tags

Para obtener una lista de todas las etiquetas de categorías disponibles,  usa::

.. django-admin-option:: --deploy

La opción ``--deploy`` activa una serie de chequeos adicionales, que son
relevantes únicamente en configuración de producción.

compilemessages
---------------

.. django-admin:: compilemessages

Compila archivos .po creados por :djadmin:`makemessages` a archivos .mo 
para ser usados por el soporte gettext.

Usa la opción :djadminopt:`--locale` (o su version corta ``-l``) para 
especificar la localidad(es) a procesar. Si no la provees, todas las
localidades serán procesadas.

Usa la opción :djadminopt:`--exclude` (o su version corta ``-x``) para  
especificar la localidad(es) a excluir del procesamiento. Si no la provees
ninguna localidad será excluida.

Ejemplos de su uso::

    django-admin compilemessages --locale=pt_BR
    django-admin compilemessages --locale=pt_BR --locale=fr
    django-admin compilemessages -l pt_BR
    django-admin compilemessages -l pt_BR -l fr
    django-admin compilemessages --exclude=pt_BR
    django-admin compilemessages --exclude=pt_BR --exclude=fr
    django-admin compilemessages -x pt_BR
    django-admin compilemessages -x pt_BR -x fr

createcachetable
----------------

.. django-admin:: createcachetable

Crea una tabla de cache llamada ``tablename`` para usar con el back-end de
cache de la base de datos. Ver el capítulo 15 para más información sobre la
cache.

La opción :djadminopt:`--database` puede ser usada para especificar la base
de datos en la cual se instalara la tabla de cache. Sin embargo no es necesario 
proveer el nombre para la tabla de la cache a la opción :djadminopt:`--database`. 
Django toma esta información de el archivo de configuración. Si tienes 
configuradas múltiples caches o múltiples bases de datos, todas las tablas de 
cache serán creadas.

dbshell
-------

.. django-admin:: dbshell
 
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

La opción :djadminopt:`--database` puede usarse para especificar la base de 
datos sobre la cual abrir el shell.

diffsettings
------------

.. django-admin:: diffsettings

Muestra las diferencias entre la configuración actual y la configuración por
omisión de Django.

Las configuraciones que no aparecen en la configuración por omisión están
seguidos por ``"###"``. Por ejemplo, la configuración por omisión no define
``ROOT_URLCONF``, por lo que si aparece ``ROOT_URLCONF`` en la salida de
``diffsettings`` lo hace seguido de ``"###"``.

La opción :djadminopt:`--all` puede ser usada para mostrar todas las 
configuraciones, incluso si tienen valores predefinidos por Django. Tales
configuraciones aparecen seguidas del prefijo de ``"###"``.

Observa que la configuración por omisión de Django habita en
``django.conf.global_settings``, si alguna vez sientes curiosidad por ver la
lista completa de valores por omisión. 

dumpdata <app_label app_label app_label.Model ...>
--------------------------------------------------

.. django-admin:: dumpdata

Dirige a la salida estándar todos los datos de la base de datos asociados con
la(s) aplicación(es) nombrada(s).

Si no se le provee el nombre de una aplicación, todas las aplicaciones instaladas
serán volcadas.

La salida de ``dumpdata`` puede ser usada como entrada para :djadmin:`loaddata`.

Observa que ``dumpdata`` usa el ``manager`` predeterminado en el modelo para
seleccionar el volcado. Si estas usando un ``manager`` personalizado como el 
manejador predeterminado y si filtras algunos registros disponibles, no todos
los objetos serán volcados.

La opción :djadminopt:`--all` puede ser usada para especificar el manejador base
que debería usar ``dumpdata``  como ``manager``, para volcar registros los cuales
han sido filtrados o modificados por un ``manager`` personalizado.

.. django-admin-option:: --format <fmt>

.. django-admin-option:: --indent <num>

Por omisión, la base de datos será volcada en formato JSON. Si quieres que la
salida esté en otro formato, usa la opción ``--format`` (ej.: ``format=xml``).
Puedes especificar cualquier back-end de serialización de Django (incluyendo
cualquier back-end de serialización especificado por el usuario mencionado en
la configuración de ``SERIALIZATION_MODULES`` setting).

De forma predeterminada la salida de ``dumpdata`` se da en una simple línea.
Que no es sencilla de leer,  puedes usar la opción ``--indent`` para mostrar
la salida indentada de acuerdo a  el numero de espacios.

La opción :djadminopt:`--exclude`  puede ayudar a prevenir que especificas 
aplicaciones o modelos (especificados en el formato ``app_label.ModelName``)
sean volcadas. Si especificas un nombre de un modelo a ``dumpdata``, la salida
del volcado será restringida a ese modelo, en lugar de la aplicación. Puedes
mezclar nombres de aplicaciones y nombres de modelos.

flush
-----

.. django-admin:: flush

Remueve todos los datos de la base de datos, esto significa que todos los datos 
serán eliminados de la base de datos, todo manejador de post-sincronización 
será reejecutado, y los datos iníciales serán reinstalados.

La opción :djadminopt:`--noinput`  puede proveerse para suprimir todos los 
mensajes de confirmación de los comandos en la terminal del usuario.

La opción :djadminopt:`--database`  puede ser usada para especificar la base de 
datos a vaciar (``flush``)

``--no-initial-data``
~~~~~~~~~~~~~~~~~~~~~

Usa ``--no-initial-data`` para evitar cargar en la instalación datos-iniciales.

inspectdb
---------

.. django-admin:: inspectdb

Realiza la introspección sobre las tablas de la base de datos apuntada por la
configuración :setting:`NAME`  y envía un modulo de modelo de Django (un
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
generados para personalizarlos. En particular, necesitarás reordenar los modelos
de manera tal que las relaciones estén ordenadas adecuadamente.

Las claves primarias son detectadas automáticamente durante la introspección
para PostgreSQL, MySQL, y SQLite, en cuyo caso Django coloca
``primary_key=True`` donde sea necesario.

``inspectdb`` trabaja con PostgreSQL, MySQL, y SQLite. La detección de claves
foráneas solo funciona en PostgreSQL y con ciertos tipos de tablas MySQL.

La opción :djadminopt:`--database` puede ser usada para especificar la base de
datos a introspecciónar.

loaddata <fixture fixture ...>
------------------------------

.. django-admin:: loaddata

Busca y carga el contenido del 'fixture' nombrado en la base de datos.

La opción :djadminopt:`--database` puede ser usada para especificar la base de 
datos sobre la cual cargar los datos.

.. django-admin-option:: --ignorenonexistent

La opción :djadminopt:`--ignorenonexistent` puede ser usada para ignorar campos
y modelos que hayan sido removidos desde que ``fixture`` fue generada 
originalmente

.. django-admin-option:: --app

La opción :djadminopt:`--app` puede ser usada para especificar una sola 
aplicación donde buscar ``fixtures`` en lugar de buscar en todas las 
aplicaciones.

¿Que es "fixture"?
~~~~~~~~~~~~~~~~~~

Un *fixture* es una colección de archivos que contienen los contenidos de la
base de datos serializados. Cada fixture tiene un nombre único; de todas
formas, los archivos que conforman el fixture pueden estar distribuidos en
varios directorios y en varias aplicaciones.

Django buscará fixtures en tres ubicaciones:

1. En el directorio ``fixtures`` de cada aplicación instalada.
2. En todo directorio nombrado en la configuración ``FIXTURE_DIRS``
3. En el path literal nombrado por el fixture

Django cargará todos los fixtures que encuentre en estas ubicaciones que
coincidan con los nombres de fixture dados.

Si el fixture nombrado tiene una extensión de archivo, sólo se cargarán
fixtures de ese tipo. Por ejemplo lo siguiente::

    django-admin loaddata mydata.json
    
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

El comando :djadmin:`dumpdata`  puede ser usado para generar la entrada para
``loaddata``.

Comprimir  fixtures
~~~~~~~~~~~~~~~~~~~

Los ``Fixtures`` pueden ser comprimidos en formato ``zip``, ``gz``, o ``bz2``.
Por ejemplo::

    django-admin loaddata mydata.json

El comando anterior buscaría cualesquiera de: ``mydata.json``, ``mydata.json.zip``,
``mydata.json.gz``, o ``mydata.json.bz2``. El primer archivo que contenga dentro
uno archivo comprimido ZIP será usado. 

.. admonition:: MySQL y los Fixtures

    Desafortunadamente, MySQL no es capaz de dar soporte completo para todas las
    características de las fixtures de Django. Si usas tablas MyISAM, MySQL no
    admite transacciones ni restricciones, por lo que no tendrás rollback
    si se encuentran varios archivos de transacción, ni validación de los datos
    de fixture. Si usas tablas InnoDB, no podrás tener referencias hacia
    adelante en tus archivos de datos -- MySQL no provee un mecanismo para
    retrasar el chequeo de las restricciones de registro hasta que la
    transacción es realizada.

Fixtures específicos en bases de datos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si estas instalando múltiples bases de datos, tal vez tengas algunos datos que
quieras cargar en una base de datos, pero no en otra. En esta situación puedes
agregar el identificador de la base de datos en el nombre de los ``fixtures``.

Por ejemplo, si la configuración :setting:`DATABASES` tiene una base de datos
definida como ``maestra`` , el nombre de el ``fixture``  puede ser 
``mydata.master.json`` o ``mydata.master.json.gz``, de esta forma el ``fixture``
únicamente cargara los datos en la base de datos llamada ``maestra``.

makemessages
------------

.. django-admin:: makemessages

Se ejecuta completamente sobre el directorio actual y recopila todas las cadenas
marcadas para traducción. Crea (o actualiza) un archivo de mensajes en 
conf/locale (en el árbol de Django) o en el directorio local (para el proyecto y 
aplicación). Después de hacer los cambios a los archivos de mensajes, es
necesario compilarlos con :djadmin:`compilemessages` para usarlos con el soporte
incorporado gettext.

Usa la opción  ``--all`` o ``-a`` para actualizar un archivo de mensajes para
todos los lenguajes disponibles.

Ejemplo de su uso::

    django-admin makemessages --all

.. django-admin-option:: --extension

Usa la opción ``--extension`` o ``-e`` para especificar una lista de extensiones 
de archivos a examinar (default: ".html", ".txt").

Ejemplo de su uso::

    django-admin makemessages --locale=de --extension xhtml

Separa múltiples extensiones con comas o usa -e o --extension varias veces::

    django-admin makemessages --locale=de --extension=html,txt --extension xml

Usa la opción :djadminopt:`--locale` (o su version corta ``-l``) para 
especificar procesos de localización(es).

Usa la opción  :djadminopt:`--exclude` (o su version corta``-x``) para 
especificar localización(es) para excluir del procesamiento. Si no se le provee,
ninguna localización será excluida.

Ejemplo de su uso::

    django-admin makemessages --locale=pt_BR
    django-admin makemessages --locale=pt_BR --locale=fr
    django-admin makemessages -l pt_BR
    django-admin makemessages -l pt_BR -l fr
    django-admin makemessages --exclude=pt_BR
    django-admin makemessages --exclude=pt_BR --exclude=fr
    django-admin makemessages -x pt_BR
    django-admin makemessages -x pt_BR -x fr

makemigrations [<app_label>]
----------------------------

.. django-admin:: makemigrations

Crea las nuevas migraciones basadas en los cambios detectados en los modelos.

Proveer uno o más nombres de aplicaciones como argumentos limitará las 
migraciones creadas en las aplicaciones especificadas y cualquier dependencia 
necesaria (por ejemplo en las tablas del otro extremo de las relaciones
``ForeignKey`` )

.. django-admin-option:: --empty

La opción ``--empty`` permitirá que la salida de ``makemigrations`` sea
una migración vacía para la aplicación especificada, para editarla manualmente.
Esta opción debería ser usada, solo por usuarios avanzados, que estén 
familiarizados con el formato de migraciones, operaciones de migraciones y las
dependencias entre migraciones.

.. django-admin-option:: --dry-run

La opción ``--dry-run`` muestra que migraciones serán aplicadas, sin escribir
en los archivos de migraciones del disco. Usa esta opción con ``--verbosity 3``
para mostrar los archivos completos de migraciones que serán escritos.

.. django-admin-option:: --merge

La opción ``--merge`` permite corregir conflictos de migraciones. La opción
:djadminopt:`--noinput` puede ser provista para suprimir mensajes de confirmación
en la terminal del usuario, como confirmaciones de borrado, etc. durante la fusión.

La opción ``--name`` permite dar a las migraciones un nombre personalizado en 
vez del generado automáticamente. 

.. django-admin-option:: --name, -n


migrate [<app_label> [<migrationname>]]
---------------------------------------

.. django-admin:: migrate

Sincroniza el estado de la base de datos, con el actual conjunto de modelos y
migraciones.

El comportamiento de este comando cambia dependiendo de los argumentos provistos:

* Sin argumentos: Todas las aplicaciones que contienen migraciones son migradas
  y todas las aplicaciones ``no emigradas`` son sincronizadas con la base de 
  datos.

* ``<app_label>``: La aplicación en particular que tiene migraciones a ejecutar,
  hasta la migración reciente. Esto puede implicar ejecutar las migraciones de 
  otras aplicaciones también, debido a las dependencias.

* ``<app_label> <migrationname>``:  Trae el esquema de la base de datos a un 
  estado donde se ejecuto la migración dada, pero no más allá -- esto conlleva
  ``desaplicar`` las migraciones si se ha emigrado previamente a la denominado 
  migración. Usa el nombre ``zero`` para ``desaplicar`` todas las migraciones
  para una aplicación. 

La opción :djadminopt:`--database` puede usarse para especificar la base de datos
a migrar.

.. django-admin-option:: --fake

La opción ``--fake`` le dice a Django que marque la migración como aplicadas o
no aplicadas, pero sin ejecutar SQl realmente, para cambiar el esquema de la base
de datos.

Está diseñado para el uso de usuarios avanzados que pueden manipular directamente
el estado actual de las migraciones, si están aplicando manualmente cambios; sea
cuidadoso usando y ejecutando ``--fake``, ya que se corre el riesgo de poner las 
tablas en un estado, donde será necesaria la recuperación manual, para que las 
migraciones se ejecutan correctamente.

.. django-admin-option:: --list, -l

La opción ``--list`` permite listar todas las aplicaciones que Django sabe que
tienen disponibles migraciones por cada aplicación y si están aplicadas o no
(marcándolas con una ``[X]`` junto al nombre de la migración) 

Las aplicaciones sin migraciones son únicamente incluidas en la lista, pero con
el nombre ``(no migrations)``  impreso abajo de ellas.

runserver [número de puerto opcional, o direcciónIP:puerto]
------------------------------------------------------------

.. django-admin:: runserver

Inicia un servidor Web liviano de desarrollo en la máquina local. machine. Por
omisión, el servidor ejecuta en el puerto 8000 de la dirección IP 127.0.0.1.
Puedes pasarle explícitamente una dirección IP y un número de puerto.

Si ejecutas este script como un usuario con privilegios normales (recomendado),
puedes no tener acceso a iniciar un puerto en un número de puerto bajo. Los
números de puerto bajos son reservados para el superusuario  (root).

.. admonition:: Advertencia:

    **No uses este servidor en una configuración de producción**. No se le han
    realizado auditorías de seguridad o tests de performance, y no hay planes de
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

    django-admin.py runserver 9000

O para ejecutar el servidos en el puerto 9000 en la dirección IP 1.2.3.4, usa
esto::

    django-admin.py runserver 1.2.3.4:9000

.. django-admin-option:: --noreload

Usa la opción ``--noreload`` para deshabilitar el uso de él recargado automático.
Esto significa que cualquiera de los cambios que hagas en el codigo, no hara que
el servidor se recargue, mientras el servidor se está ejecutando, por lo que solo
se usaran los módulos específicos  de Python que se hayan cargado en la memoria.

Ejemplo de su uso::

    django-admin runserver --noreload

.. django-admin-option:: --ipv6, -6

Usa la opción ``--ipv6`` (o su version corta ``-6``) para decirle a Django 
que use  IPv6 para el servidor de desarrollo.  Esta cambia la dirección 
predeterminada IP de  ``127.0.0.1`` a  ``::1``.

Example usage::

    django-admin runserver --ipv6

Ejemplos de diferentes usos de puertos y direcciones
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Puerto 8000 en dirección IP ``127.0.0.1``::

    django-admin runserver

Puerto 8000 en dirección IP ``1.2.3.4``::

    django-admin runserver 1.2.3.4:8000

Puerto 7000 en dirección IP ``127.0.0.1``::

    django-admin runserver 7000

Puerto 7000 en dirección IP ``1.2.3.4``::

    django-admin runserver 1.2.3.4:7000

Puerto 8000 en dirección IPv6 ``::1``::

    django-admin runserver -6

Puerto 7000 en dirección IPv6 ``::1``::

    django-admin runserver -6 7000

Puerto 7000 en dirección IPv6 ``2001:0db8:1234:5678::9``::

    django-admin runserver [2001:0db8:1234:5678::9]:7000

Puerto 8000 en dirección IPv4 del  host ``localhost``::

    django-admin runserver localhost:8000

Puerto 8000 en la dirección   IPv6 del  host ``localhost``::
    django-admin runserver -6 localhost:8000    

shell
-----

.. django-admin:: shell

Inicia el intérprete interactivo de Python.

Django utilizará IPython_ o bpython_  si están instalados, para iniciar un shell
mejorado. Pero si quieres forzar el uso del intérprete Python "plano",  usa la 
opción ``--plain``, como en::

    django-admin.py shell --plain

Si quieres especificar entre IPython o bpython como tu interprete, si tienes
ambos instalados, puedes especificar alternativamente la interface que 
quieras usar, usando la opción ``-i`` o ``--interface`` así:

IPython::

    django-admin shell -i ipython
    django-admin shell --interface ipython

bpython::

    django-admin shell -i bpython
    django-admin shell --interface bpython


.. _IPython: http://ipython.scipy.org/
.. _bpython: http://bpython-interpreter.org/

Cuando el interprete interactivo "plano" inicia,(ya sea porque usaste la opción
``--plain`` o porque no tienes otra interface disponible) este lee el script
que apunta a las variables de entorno de :envvar:`PYTHONSTARTUP` y al script de
la variable ``~/.pythonrc.py`` , si quieres cambiar este comportamiento usa la
opción ``--no-startup``, por ejemplo::

    django-admin shell --plain --no-startup

sql <app_label app_label ...>
-----------------------------

.. django-admin:: sql

Imprime las sentencias SQL ``CREATE TABLE`` para las aplicaciones mencionadas.

La opción :djadminopt:`--database` puede ser usada para especificar la base de
datos sobre la cual imprimir el  SQL.

sqlall <app_label app_label ...>
--------------------------------

.. django-admin:: sqlall

Imprime las sentencias SQL ``CREATE TABLE`` y los datos iniciales para las
aplicaciones mencionadas.

Busca en la descripción de :djadmin:`sqlcustom` para una explicación de como
especificar los datos iniciales.

La opción :djadminopt:`--database` puede ser usada para especificar la base de
datos sobre la cual imprimir el  SQL.

sqlclear <app_label app_label ...>
----------------------------------

.. django-admin:: sqlclear

Imprime las sentencias SQL ``DROP TABLE`` para las aplicaciones mencionadas.

La opción :djadminopt:`--database` puede ser usada para especificar la base de
datos sobre la cual imprimir el  SQL.

sqlcustom <app_label app_label ...>
-----------------------------------

.. django-admin:: sqlcustom

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

La opción :djadminopt:`--database` puede ser usada para especificar la base de
datos sobre la cual imprimir el  SQL.

sqldropindexes <app_label app_label ...>
----------------------------------------

.. django-admin:: sqldropindexes

Imprime las sentencias SQL ``DROP INDEX SQL`` para las aplicaciones mencionadas.

La opción :djadminopt:`--database` puede ser usada para especificar la base de
datos sobre la cual imprimir el  SQL.

sqlflush
--------

.. django-admin:: sqlflush

Imprime las sentencias SQL que serán ejecutadas por el comando :djadmin:`flush`.

La opción :djadminopt:`--database` puede ser usada para especificar la base de
datos sobre la cual imprimir el  SQL.

sqlindexes <app_label app_label ...>
------------------------------------

.. django-admin:: sqlindexes

Imprime las sentencias SQL ``CREATE INDEX`` para las aplicaciones mencionadas.

La opción :djadminopt:`--database` puede ser usada para especificar la base de
datos sobre la cual imprimir el  SQL.

sqlmigrate <app_label> <migrationname>
--------------------------------------

.. django-admin:: sqlmigrate

Imprime el SQL para el nombre de la migración. Esta requiere una conexión a una
base de datos activa, que se utilizara para resolver restricciones de nombres;
esto significa que se  debe generar el SQL contra una copia de la base de datos 
que se desea aplicar más adelante.

Observa que ``sqlmigrate`` no coloriza la salida.

La opción :djadminopt:`--database` puede ser usada para especificar la base de
datos sobre la cual imprimir el  SQL.

.. django-admin-option:: --backwards

De forma predeterminada el SQL creado, permite ``ejecuta`` las migraciones que
siguen. Pasándole la opción ``--backwards`` al SQL generado permite ``desaplicar`` 
las migraciones.

sqlsequencereset <app_label app_label ...>
------------------------------------------

.. django-admin:: sqlsequencereset

Imprime las sentencias SQL para resetear series para las aplicaciones mencionadas.

Las series o secuencias son índices usados por algunos motores de base de datos 
para rastrear el número disponible siguiente para los campos automáticamente 
incrementados.

Use este comando para generar SQL que corrija casos donde una secuencia está 
fuera de sincronización con campos automáticamente incrementados.

La opción :djadminopt:`--database` puede ser usada para especificar la base de
datos sobre la cual imprimir el  SQL.


squashmigrations <app_label> <migration_name>
---------------------------------------------

.. django-admin:: squashmigrations

Aplasta o compacta las migraciones para una aplicación dada (app_label), hasta 
el ``nombre de la migración`` (migration_name) incluyéndola y compactándolas lo 
mas posible, las migraciones resultantes pueden convivir de forma segura con 
migraciones ```no compactadas`` (unsquashed). 

.. django-admin-option:: --no-optimize

De forma predeterminada, Django trata de optimizar las operaciones de migraciones
para reducir el tamaño de los archivos resultantes. Sin embargo puedes usar la 
opción ``--no-optimize``, si el proceso está fallando o si está creando 
migraciones incorrectas. 

startapp <app_label> [destino]
------------------------------

.. django-admin:: startapp

Crea una estructura de directorios para una aplicación Django con el nombre de
la aplicación dada, en el directorio actual.

De forma predeterminada el directorio creado contiene un archivo ``models.py``
y otros archivos para una aplicación (```views.py``, ``admin.py``...).

Si se le proporciona un destino opcional, Django utilizará el directorio 
existente para crear uno nuevo. Puedes utilizar "." para denotar el directorio 
de trabajo actual. 

Por ejemplo::

    django-admin startapp myapp /Users/jezdez/Code/myapp

.. django-admin-option:: --template

Con la opción template ``--template``, puedes  utilizar plantillas personalizadas
para una aplicación, proporcionando la ruta al directorio que contiene las
plantillas de archivos o la ruta a los archivos comprimidos (``.tar.gz``,
``.tar.bz2``, ``.tgz``, ``.tbz``, ``.zip``) que puedan contener los archivos de 
plantillas para la aplicación.

Por ejemplo, esto buscaría plantillas para una aplicación en el directorio
``miapp``::

    django-admin startapp --template=/Users/jezdez/Code/my_app_template myapp

Django también acepta URLs (``http``, ``https``, ``ftp``) para archivos 
comprimidos que contengan archivos de plantillas para una aplicación, 
descargando y extrayendo los archivos al vuelo.

Por ejemplo, aprovechándo la característica de Github de exponer repositorios
como archivos zip, puedes utilizar un URL como esta::

    django-admin startapp --template=https://github.com/githubuser/django-app-template/archive/master.zip myapp

Cuando Django copia los archivos de plantillas de una aplicación, también 
renderiza ciertos archivos a través del motor de plantillas: los archivos 
cuyas extensiones coincidan con la opción  ``--extension`` (``py`` por defecto) 
y los archivos cuyos nombres sean pasados con la opción  ``--name``. 
La clase ``django.template.Context`` usa para esto:

- Cualquier opción pasada al comando ``startapp``  (Entre las opciones 
  soportadas por el comando)
- ``app_name`` -- el nombre de la aplicación pasada al comando.
- ``app_directory`` -- la ruta completa a la aplicación  recién creada.
- ``docs_version`` -- la versión de la documentación: ``'dev'`` o ``'1.x'``

startproject <projectname> [destino]
------------------------------------

.. django-admin:: startproject

Crea una estructura de directorios Django para el nombre de proyecto dado, en
el directorio actual o en el directorio dado.

De forma predeterminada, el nuevo directorio contiene un archivo ``manage.py`` y
un paquete de proyecto (que contiene un archivo ``settings.py`` y otros archivos) 

Si sólo el nombre de proyecto es dado, tanto el directorio del proyecto y el 
paquete del proyecto serán llamados ``<projectname>`` y el directorio del proyecto
será creado en el directorio de trabajo actual. 

Si se le provee la opción ``destino``, Django usara el directorio existente
como el directorio del proyecto y creara un archivo ``manage.py`` y el paquete
del proyecto dentro del. Usa '.' para denotar el actual directorio de trabajo.

Por ejemplo::

    django-admin startproject myproject /Users/jezdez/Code/myproject_repo

Al igual que el comando  :djadmin:`startapp`, la opción ``--template`` permite
especificar un directorio, una ruta de archivos o una URL para proveer de 
plantillas personalizadas al proyecto.

Por ejemplo, esto buscara plantillas para un proyecto en el directorio dado, 
cuando se cree el proyecto  ``myproject``::

    django-admin startproject --template=/Users/jezdez/Code/my_project_template myproject

También acepta URLs (``http``, ``https``, ``ftp``) para archivos comprimidos que
contengan archivos de plantillas para un proyecto, descargando y extrayendo los 
archivos al vuelo.

Por ejemplo, aprovechándo la característica de Github de exponer repositorios
como archivos zip, puedes utilizar un URL como esta::

     django-admin startproject --template=https://github.com/githubuser/django-project-template/archive/master.zip myproject

Cuando Django copia los archivos de plantillas de un proyecto, también 
renderiza ciertos archivos a través del motor de plantillas: los archivos 
cuyas extensiones coincidan con la opción  ``--extension`` (``py`` por defecto) 
y los archivos cuyos nombres sean pasados con la opción  ``--name``. 
La clase ``django.template.Context`` usa para esto:

- Cualquier opción pasada al comando ``startapp``  (Entre las opciones 
  soportadas por el comando)
- ``project_name`` -- el nombre del proyecto pasado al comando.  
- ``project_directory`` -- la ruta completa al proyecto recién creado.
- ``secret_key`` -- una clave al azar para la configuración de :setting:`SECRET_KEY`.
- ``docs_version`` -- la versión de la documentación: ``'dev'`` o ``'1.x'``   

test
----

.. django-admin:: test

Ejecuta todas las pruebas para todos los modelos instalados. 

.. django-admin-option:: --failfast

La opción ``--failfast`` se usa para detener las pruebas y reportar las fallas
inmediatamente después de que una prueba falla.

.. django-admin-option:: --testrunner

La opción  ``--testrunner`` es usada para controlar la clase de pruebas que
es usada para ejecutar las pruebas. Si este valor es proporcionado al comando, 
sobrescribirá el valor provisto por la configuración :setting:`TEST_RUNNER`. 

.. django-admin-option:: --liveserver

La opción ``--liveserver`` es usada para sobrescribir la dirección predeterminada
que usa el servidor de pruebas, 
(usado con :class:`~django.test.LiveServerTestCase`.) El valor predeterminado
es ``localhost:8081``.

.. django-admin-option:: --keepdb

La opción ``--keepdb`` es usada para preservar los test en la base de datos entre
la ejecución de pruebas. Este toma la ventaja de saltarse el crear y destruir
las tablas entre prueba y prueba, esto disminuye en gran medida el tiempo  de 
pruebas, especialmente en grandes ``suits`` de pruebas. Si la base de datos de tests
no existe, esta se crea la primera vez que se ejecuta y se preserva en cada 
subsecuente ejecución.  Cualquier migración no aplicada será aplicada a la 
base de datos de pruebas antes de ejecutar todas las pruebas.


testserver <fixture fixture ...>
--------------------------------

.. django-admin:: testserver

Ejecuta un servidor de desarrollo Django (como :djadmin:`runserver`) usando datos
proporcionados por ``fixture(s)``

Por ejemplo, este comando:: 

    django-admin testserver mydata.json

Realizara los siguientes pasos:

1. Creara una base de datos de pruebas.
2. Poblara la base de datos de pruebas con datos provistos por los ``fixtures``.
3. Ejecutar el servidor de desarrollo (tal como :djadmin:`runserver`) apuntado a
   la base de datos recién creada en lugar de la base de datos de producción.

Comandos provistos por aplicaciones
===================================

Algunos comando son únicamente disponibles cuando la aplicación ``django.contrib`` 
ha sido activada. Esta sección describe los comandos provistos por cada 
aplicación.

``django.contrib.auth``
-----------------------

changepassword
~~~~~~~~~~~~~~

.. django-admin:: changepassword

Este comando se encuentra únicamente disponible,  si se instala el sistema de 
autentificación (``django.contrib.auth``.)

Permite cambiar las contraseñas de los usuarios. Instiga a entrar dos veces la 
contraseña de un usuario dado, como parámetro.  Si ambos coinciden, la nueva
contraseña será cambiada de inmediato. Si no se le pasa un usuario, el comando
intentara usar el usuario actual para cambiar la contraseña.

Usa la opción ``--database`` para especificar la base de datos a consultar para
el usuario. Si esta no se le proporciona, Django usara la base de datos por
``default`` 

Ejemplo de sus uso::

    django-admin changepassword ringo


createsuperuser
~~~~~~~~~~~~~~~

.. django-admin:: createsuperuser

Este comando se encuentra únicamente disponible,  si se instala el sistema de 
autentificación (``django.contrib.auth``.)

Crea una cuenta de superusuario (un usuario que tiene todos los permisos). Esto
es útil si necesitas crear una cuenta inicial para un superusuario o si necesitas
generar programáticamente cuentas de superusuarios para tu sitio(s).

Cuando se ejecuta interactivamente, este comando preguntara por una contraseña
para crear la cuenta del superusuario. Cuando se ejecuta de forma ``no interactiva``,
es necesario configurar la contraseña de forma manual.

.. django-admin-option:: --username
.. django-admin-option:: --email

El nombre de usuario y la dirección de email para la nueva cuenta, pueden
proporcionarse usando los argumentos ``--username`` y ``--email`` en la línea de
comandos. Si cualquiera de ellos no se provee, ``createsuperuser`` preguntara
por ellos al ejecutarse de forma interactiva. 

Usa la opción ``--database`` para especificar la base de datos en la que quieras
guardar los objetos superusuarios.

``django.contrib.gis``
----------------------

ogrinspect
~~~~~~~~~~

Este comando se encuentra únicamente disponible,  si se instala el sistema de 
Geodjango(``django.contrib.gis``). 


``django.contrib.sessions``
---------------------------

clearsessions
~~~~~~~~~~~~~~~

.. django-admin:: clearsessions

Puede ser usado como una tarea por cron o directamente para limpiar las sesiones
que han expirado.

``django.contrib.sitemaps``
---------------------------

ping_google
~~~~~~~~~~~

Este comando se encuentra únicamente disponible, si se instala el framework 
de Sitemaps (``django.contrib.sitemaps``).

Usado para hacer ``ping`` a Google, para que indexe nuestro sitio(s).
Una vez que has agregado la aplicación sitemap a tu proyecto, puedes hacer ping
a Google usando este comando de la siguiente forma::

    python manage.py ping_google [/sitemap.xml]

``django.contrib.staticfiles``
------------------------------

collectstatic
~~~~~~~~~~~~~

Este comando se encuentra únicamente disponible, si se instala el framework
de archivos estáticos (``django.contrib.staticfiles``).

Usado para coleccionar los archivos estáticos (hojas de estilo css, js...) que 
serán servidos por el servidor web en un entorno de producción. Los nombres 
duplicados de los archivos de forma predeterminada se resuelven de una manera 
similar a cómo lo hacen las plantillas: el archivo que es primero localizado, 
es el que se usara.

Colecciona los archivos estáticos en :setting:`STATIC_ROOT`. Para una lista 
completa de opciones, usa ``--help``::
   
   $ python manage.py collectstatic --help

Duplicate file names are by default resolved in a similar way to how template 
resolution works: the file that is first found in one of the specified locations will be used. 
If you’re confused, the findstatic command can help show you which files are 
found.

findstatic
~~~~~~~~~~

Búsca uno o más caminos relativos, a la ruta de los buscadores habilitados.

Por ejemplo::

   $ python manage.py findstatic css/base.css admin/js/core.js
   Found 'css/base.css' here:
     /home/special.polls.com/core/static/css/base.css
     /home/polls.com/core/static/css/base.css
   Found 'admin/js/core.js' here:
     /home/polls.com/src/django/contrib/admin/media/js/core.js

De forma predeterminada, todas las localidades que coincidan serán encontradas.
Si únicamente quieres que devuelva la primera coincidencia por cada ruta relativa,
usa la opción ``--first`` así::

   $ python manage.py findstatic css/base.css --first
   Found 'css/base.css' here:
     /home/special.polls.com/core/static/css/base.css     

Opciones Predeterminadas
========================

Aunque algunos comandos pueden permitir sus propias opciones personalizadas, 
cada  comando permite usar las siguientes opciones:

Las secciones que siguen delinean las opciones que puede tomar
``django-admin.py`` en  la mayoría de casos.

--settings
----------

.. django-admin-option:: --settings

Especifica explícitamente el módulo de configuración a usar. El módulo de
configuración debe estar en la sintaxis de paquetes de Python (ej.:
``mysite.settings``). Si no se proveen, ``django-admin.py`` utilizará la
variable de entorno ``DJANGO_SETTINGS_MODULE``.
Ejemplo de uso::

    django-admin.py migrate --settings=mysite.settings

Observa que esta opción no es necesaria en ``manage.py``, ya que toma en cuenta
la configuración de ``DJANGO_SETTINGS_MODULE`` por tí.

--pythonpath
------------

.. django-admin-option:: --pythonpath

Agrega la ruta del sistema de archivos a la ruta de búsqueda de importación de
Python. Si no se define, ``django-admin.py`` usará la variable de entorno ``PYTHONPATH``.

Ejemplo de uso::

    django-admin.py migrate --pythonpath='/home/djangoprojects/myproject'

Observa que esta opción no es necesaria en ``manage.py``, ya que este comando
tiene cuidado de configurar la ruta de Python por tí.

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

--traceback
------------

.. django-admin-option:: --traceback

De forma predeterminada ``django-admin`` muestra un simple mensaje de error
cuando ocurre un :class:`~django.core.management.CommandError`, pero muestra una
traza completa para cualquier otra excepción. Si especificas la opción 
``--traceback``,  ``django-admin`` también mostrara la traza de pila completa 
cuando ocurra algún error de comando o ``CommandError``.

Por ejemplo::

    django-admin migrate --traceback

--no-color
----------

.. django-admin-option:: --no-color

De forma predeterminada el formato que usa ``django-admin`` para mostrar las 
salidas es ``colorizado``. Por ejemplo, los errores se imprimen en la consola
en rojo y las declaraciones en SQL  aparecen con resaltado de sintaxis. Para
prevenir esto y mostrar la salida de texto plano, es necesario pasarle la opción
``--no-color`` al ejecutar el comando, de la siguiente forma::

    django-admin sqlall --no-color

--version
---------

Muestra la versión actual de Django.

Ejemplo de salida::

    1.4
    1.8

--verbosity
-----------

Determina la cantidad de notificaciones e información de depuración que se
imprimirá en la consola. 

Ejemplo de uso::

    django-admin.py migrate --verbosity=2

Usa niveles para determinar la cantidad de información a mostrar: 

* ``0`` significa sin salida.
* ``1`` significa salida normal (default).
* ``2`` significa salida con explicaciones.
* ``3`` significa *muy* explicado.

Opciones comunes
=================

La siguientes opciones no están disponibles en cada comando, pero son muy
comunes en un gran número de comandos.

--database
-----------

.. django-admin-option:: --database

Usado para especificar la base de datos en la cual  opera el comando. Si no
se especifica, esta opción usara el valor predeterminado por el alias
``default``.

Por ejemplo, para volcar datos de una base de datos con el alias ``master``::

    django-admin dumpdata --database=master

--exclude
---------

.. django-admin-option:: --exclude

Excluye una aplicación en especifico de las aplicaciones cuyo contenido se espera
en la salida. Por ejemplo, para específicamente excluir la aplicación ``auth``
de la salida de ``dumpdata``.  Por ejemplo:: 

    django-admin dumpdata --exclude=auth

Si quieres excluir múltiples aplicaciones, usa múltiples directivas
``--exclude``::

    django-admin dumpdata --exclude=auth --exclude=contenttypes    

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

.. django-admin-option:: --noinput

Indica que no quieres que se te pida ninguna entrada. Es útil cuando el script
``django-admin`` se ejecutará en forma automática y desatendida.

--noreload
----------

Deshabilita el uso del autoreloader cuando se ejecuta el servidor de desarrollo.  

--locale
--------

.. django-admin-option:: --locale

Usa la opción ``--locale`` o ``-l`` para específicamente procesar una localidad.
Si no provees esta opción todas las localidades serán procesadas.

Sutilezas extras
================

.. _syntax-coloring:

Sintaxis de colores
-------------------

Los comandos  ``django-admin`` / ``manage.py`` usan un agradable resaltado
de codigo en la salida (colores) mostrada en la terminales con soporte para 
salida  ``ANSI-colored```. 

Bajo Windows, la nativa consola no soporta el escape de secuencias ANSI, por
lo que la salida no es mostrada con colores. Pero puedes instalar una herramienta
de terceros llamada `ANSICON`_, el comando de Django puede detectar si esta
presente y usarla para mostrar el resaltado de sintaxis, tal como en plataformas
basadas en Unix.

.. _ANSICON: http://adoxa.altervista.org/ansicon/

Los colores usados por el resaltado de sintaxis pueden personalizarse. Django
viene con tres paletas de colores.

* ``dark``, adaptado apara terminales que muestran texto en blanco y el fondo en
  negro. Esta es la paleta predeterminada.

* ``light``, adaptado para terminales que muestran el texto en negro en un fondo
  blanco.

* ``nocolor``, desactiva el resaltado de sintaxis.

Puedes seleccionar una paleta configurando las variables de entorno para
``DJANGO_COLORS`` especificando la paleta a usar. Por ejemplo, para especificar
la paleta ``light`` bajo un shell tipo Unix o OS/X BASH shell, puedes usar el 
siguiente comando en una terminal::

    export DJANGO_COLORS="light"

Autocompletado para bash
------------------------

Si estas usando el shell Bash, considera instalar el script ``bash completion``
el cual se localiza en  ``extras/django_bash_completion`` en la distribución
de Django. Este habilita el autocompletado usando la tecla ``tab`` de los
comandos  ``django-admin`` y ``manage.py``, con lo que es posible, por ejemplo... 

* Tipea ``django-admin``.
* Presionar [TAB] para ver las opciones disponibles.
* Tipea ``sql``, luego [TAB], para ver todas las opciones disponibles cuyos 
  nombres comienzan con ``sql``.