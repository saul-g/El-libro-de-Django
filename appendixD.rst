======================================
Apéndice D: Variables de configuración
======================================

El **archivo de configuración** ``setting.py`` contiene toda la configuración
de tu instalación Django. Este apéndice explica cómo funcionan la mayoria de
las variables de configuración y qué variables de configuración están disponibles.

.. admonition:: Nota:

    A medida que Django crece, es ocasionalmente necesario agregar o (raramente)
    cambiar variables de configuración. Debes siempre buscar la información mas
    reciente en la documentación de configuración en línea que se encuentra en
    http://www.djangoproject.com/documentation/.

Qué es un archivo de configuración
==================================

Un *archivo de configuración* es sólo un módulo Python con variables a nivel de
módulo.

Un par de ejemplos de variables de configuración::

    DEBUG = False
    DEFAULT_FROM_EMAIL = 'webmaster@example.com'
    TEMPLATE_DIRS = ('/home/templates/mike', '/home/templates/john')

Debido a que un archivo de configuración es un módulo Python, las siguientes
afirmaciones son ciertas:

* Debe ser código Python válido; no se permiten los errores de sintaxis.

* El mismo puede asignar valores a las variables dinámicamente usando
  sintaxis normal de Python, por ejemplo::

          MY_SETTING = [str(i) for i in range(30)]

* El mismo puede importar valores desde otros archivos de configuración.

Valores por omisión
-------------------

No es necesario que un archivo de configuración de Django defina una variable
de configuración si es que no es necesario. Cada variable de configuración tiene
un valor por omisión sensato. Dichos valores por omisión residen en el archivo
``django/conf/global_settings.py``.

Este es el algoritmo que usa Django cuando compila los valores de configuración:

* Carga las variables de configuración desde ``global_settings``.
* Carga las variables de configuración desde el archivo de configuración
  especificado, reemplazando de ser necesario los valores globales previos.

Nota que un archivo de configuración *no* debe importar desde
``global_settings``, ya que eso sería redundante.

Viendo cuáles variables de configuración has cambiado
-----------------------------------------------------

Existe una manera fácil de ver cuáles de tus variables de configuración difieren
del valor por omisión. El comando ``manage.py diffsettings`` visualiza las
diferencias entre el archivo de configuración actual y los valores por omisión
de Django.

``manage.py`` es descrito con más detalle en el Apéndice G.

Usando variables de configuración en código Python
--------------------------------------------------

En tus aplicaciones Django, usa variables de configuración importando el objeto
``django.conf.settings``, por ejemplo::

    from django.conf import settings

    if settings.DEBUG:
        # Do something

Nota que ``django.conf.settings`` no es un módulo -- es un objeto. De manera
que no es posible importar variables de configuración individualmente.::

    from django.conf.settings import DEBUG  # This won't work.

Ten en cuenta también que tu código *no* debe importar ni desde
``global_settings`` ni desde tu propio archivo de configuración.
``django.conf.settings`` provee abstracción para los conceptos de variables de
configuración por omisión y variables de configuración específicas de un sitio;
presenta una única interfaz. También desacopla el código que usa variables de
configuración de la ubicación de dicha configuración.

Modificando variables de configuración en tiempo de ejecución
-------------------------------------------------------------

No debes alterar variables de configuración en tiempo de ejecución. Por ejemplo,
no hagas esto en una vista::

    from django.conf import settings

    settings.DEBUG = True   # ¡No hagas esto!

El único lugar en el que debes asignar valores a ``settings`` es en un archivo
de configuración.

Seguridad
---------

Debido  que un archivo de configuración contiene información importante, tal
como la contraseña de la base de datos, debes hacer lo que esté e tus manos para
limitar el acceso al mismo. Por ejemplo, cambia los permisos de acceso en el
sistema de archivos de manera que solo tú y el usuario de tu servidor Web puedan
leerlo. Esto es especialmente importante en un entorno de alojamiento
compartido.

Creando tus propias variables de configuración
----------------------------------------------

No existe nada que impida que crees tus propias variables de configuración, para
tus propias aplicaciones Django. Sólo sigue las siguientes convenciones:

* Usa nombres de variables en mayúsculas.

* Para configuraciones que sean secuencias, usa tuplas en lugar de listas.
  Las variables de configuración deben ser consideradas inmutables y no
  deben ser modificadas una vez que se las ha definido. El usar tuplas
  refleja esa semántica.

* No reinventes una variable de configuración que ya existe.

Indicando la configuración: DJANGO_SETTINGS_MODULE
==================================================

Cuando usas Django tienes que indicarle qué configuración estás usando. Haz esto
mediante el uso de de la variable de entorno ``DJANGO_SETTINGS_MODULE``.

El valor de ``DJANGO_SETTINGS_MODULE`` debe respetar la sintaxis de rutas de
Python (por ej. ``mysite.settings``. Notar que el módulo de configuración debe
ser encontrarse en la ruta de búsqueda para las importaciones de Python
(``PYTHONPATH``).

.. admonition:: Consejo:

    Puedes encontrar una buena guía acerca de `PYTHONPATH`` en
    http://diveintopython.org/getting_to_know_python/everything_is_an_object.html.

La utilidad django-admin.py
---------------------------

Cuando usas ``django-admin.py`` (ver Apéndice F), puedes ya sea fijar el valor
de la variable de entorno una vez o especificar explícitamente el módulo de
configuración cada vez que ejecutes la utilidad.

Este es un ejemplo usando el shell Bash de Unix::

    export DJANGO_SETTINGS_MODULE=mysite.settings
    django-admin.py runserver

Este es otro ejemplo, esta vez usando el shell de Windows::

    set DJANGO_SETTINGS_MODULE=mysite.settings
    django-admin.py runserver

Usa el argumento de línea de comandos ``--settings`` para especificar el módulo
de configuración en forma manual::

    django-admin.py runserver --settings=mysite.settings

La utilidad ``manage.py`` creada por ``startproject`` como parte del esqueleto
del proyecto asigna un valor a ``DJANGO_SETTINGS_MODULE`` en forma automática;
revisa el Apéndice G si deseas conocer más sobre ``manage.py``.

En el servidor (mod_wsgi)
---------------------------

En tu entorno del servidor activo, necesitarás indicarle a ``WSGI application``
qué archivo de configuración debe usar. Haz eso con ``os.environ``::

    import os

    os.environ['DJANGO_SETTINGS_MODULE'] = 'misitio.settings'

Usando variables de configuración sin fijar DJANGO_SETTINGS_MODULE
==================================================================

Es algunos casos, querrás saltearte la variable de entorno
``DJANGO_SETTINGS_MODULE``. Por ejemplo, si estás usando el sistema de
plantillas en forma aislada, muy probablemente no desearás tener que preparar
una variable de entorno que apunte a un módulo de configuración.

En esos casos, puedes fijar los valores de las variables de configuración de
Django manualmente. Haz esto llamando a ``django.conf.settings.configure()``.
Este es un ejemplo::

    from django.conf import settings

    settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
        TEMPLATE_DIRS=('/home/web-apps/myapp', '/home/web-apps/base'))

Pásale a ``configure()`` tantos argumentos de palabra clave como desees, con
cada argumento representando una variable de configuración y su valor. Cada
nombre de argumento debe estar escrito totalmente en mayúsculas, con el mismo
nombre que la variable de configuración que ya se describieron. Si una
variable de configuración no es pasada a ``configure()`` y es necesario luego,
Django usará el valor por omisión respectivo.

El configurar Django de esta manera es en general necesario -- y, en efecto,
recomendado,  cuando usas una parte del framework dentro de una aplicación más
grande.

En consecuencia, cuando es configurado vía ``settings.configured()``, Django no
hará modificación alguna a las variables de entorno del proceso (revisa la
explicación acerca de ``TIME_ZONE`` más adelante en este apéndice para conocer
por qué habría de ocurrir esto). Asumimos que en esos casos ya tienes completo
control de tu entorno.

Variables de configuración por omisión personalizados
-----------------------------------------------------

Si te gustaría que los valores por omisión provinieran desde otra ubicación
diferente a ``django.conf.global_settings``, puedes pasarle un módulo o clase
que provea las variables de configuración por omisión como el argumento
``default_settings`` (o como el primer argumento posicional) en la llamada a
``configure()``.

En este ejemplo, las variables de configuración por omisión se toman desde
``myapp-defaults``, y se fija el valor de ``DEBUG`` en ``True``,
independientemente de su valor en ``myapp_defaults``::

    from django.conf import settings
    from myapp import myapp_defaults

    settings.configure(default_settings=myapp_defaults, DEBUG=True)

El siguiente ejemplo, que usa ``myapp_defaults`` como un argumento posicional,
es equivalente::

    settings.configure(myapp_defaults, DEBUG = True)

Normalmente, no necesitarás sobrescribir los valores por omisión de esta
manera. Los valores por omisión provistos por Django son suficientemente
sensatos como para que puedas usarlos. Ten en cuenta que si pasas un nuevo valor
por omisión, este *reemplaza* completamente los valores de Django, así que debes
especificar un valor para cada variable de configuración posible que pudiera ser
usado en el código que estás importando. Examina
``django.conf.settings.global_settings`` para ver la lista completa.

Es necesario que uses configure() o DJANGO_SETTINGS_MODULE
----------------------------------------------------------

Si no estás fijando la variable de entorno ``DJANGO_SETTINGS_MODULE``, debes
llamar a ``configure()`` en algún punto antes de usar cualquier código que lea
las variables de configuración.

Si no fijas ``DJANGO_SETTINGS_MODULE`` y no llamas a ``configure()``, Django
lanzará una excepción ``EnvironmentError`` la primera vez que se accede a una
variable de configuración.

Si fijas el valor de ``DJANGO_SETTINGS_MODULE``, luego accedes a los valores de
las variables de configuración de alguna manera, y *entonces* llamas a
``configure()``, Django lanzará un ``EnvironmentError`` indicando que la
configuración ya ha sido preparada.

También es un error el llamar a ``configure()`` más de una vez, o llamar a
``configure`` luego de que ya se ha accedido a alguna variable de configuración.

En resumen: Usa exactamente una vez ya sea ``configure()`` o
``DJANGO_SETTINGS_MODULE``. No ambos, y no ninguno.

Variables de configuración disponibles
======================================

Las siguientes secciones consisten de una lista completa de todas las variables
de configuración en orden alfabético, y sus valores por omisión.

.. warning::

    Ten cuidado al sobrescribir alguna configuración, especialmente cuando
    el valor predeterminado no está vacío, es un diccionario o una tupla, tal 
    como :setting:`MIDDLEWARE_CLASSES` y :setting:`TEMPLATE_CONTEXT_PROCESSORS`.
    Asegúrate que los componentes requeridos estén disponibles para usar esta
    característica de  Django.

ABSOLUTE_URL_OVERRIDES
----------------------

.. setting:: ABSOLUTE_URL_OVERRIDES

*Valor por omisión*: ``{}`` (Diccionario vacío)

Un diccionario enlazando cadenas ``app_label.model_name`` a funciones que
toman un objeto modelo y retornan su URL. Esta es una forma de sobrescribir
métodos ``get_absolute_url()`` en cada instalación. Un ejemplo::

    ABSOLUTE_URL_OVERRIDES = {
        'blogs.weblog': lambda o: "/blogs/%s/" % o.slug,
        'news.story': lambda o: "/stories/%s/%s/" % (o.pub_year, o.slug),
    }

Notar que el nombre del modelo usado en esta variable de configuración debe
estar escrito totalmente en mayúsculas, con independencia de la combinación de
mayúsculas y minúsculas del nombre real de la clase del modelo.

``ABSOLUTE_URL_OVERRIDES`` no funciona en modelos que no tienen declarado un
metodo ``get_absolute_url()``.

ADMINS
------

*Valor por omisión*: ``()`` (Tupla vacía)

Una tupla que enumera las personas que recibirán notificaciones de errores en
el código. Cuando ``DEBUG=False`` y una vista laza una excepción, Django enviará
a esta gente un e-mail con la información completa de la información. Cada
miembro de la tupla debe ser una tupla de (Nombre completo, dirección de e-mail),
por ejemplo::

    (('John', 'john@example.com'), ('Mary', 'mary@example.com'))

Notar que Django el enviará e-mail a *todas* estas personas cada vez que ocurra
un error.

ALLOWED_HOSTS
-------------

*Valor por omisión*: ``[]`` (Lista vacía)

Una lista de cadenas que representa el nombre del  host/dominio que usa el
sitio de Django. Se trata de una medida de seguridad, que impide que un
atacante puede envenenar la cache y resetear contraseñas enviando emails
con links a sitios maliciosos, enviando peticiones HTTP con cabeceras falsas
``Host``, lo cual es posible incluso bajo muchos configuraciones 
aparentemente-seguras del servidor web.

ALLOWED_INCLUDE_ROOTS
---------------------

*Valor por omisión*: ``()`` (Tupla vacía)

Una tupla de cadenas que representan prefijos permitidos para la etiqueta de
plantillas ``{% ssi %}``. Se trata de una medida de seguridad, que impide que
los autores de plantillas puedan acceder a archivos a los que no deberían
acceder.

Por ejemplo, si ``ALLOWED_INCLUDE_ROOTS`` es ``('/home/html', '/var/www')``
entonces ``{% ssi /home/html/foo.txt %}`` funcionaría pero ``{% ssi /etc/passwd %}``
no.

APPEND_SLASH
------------

*Valor por omisión*: ``True``

Esta variable de configuración indica si debe anexarse barras al final de las
URLs. Se usa solamente si está instalado el ``CommonMiddleware`` (ver  
:doc:`capítulo 17<chapter17>`). 

CACHES
------

*Valor por omisión*:: 

    CACHES{
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

Un diccionario que contiene la configuración para todas las caches
que se usaran con Django. Es un diccionario jerarquizado cuyos 
contenidos asocian en forma de alias un diccionario que contiene
las opciones para usar la cache de forma individual.

La configuración de :setting:`CACHES` debe configurar el valor 
predeterminado ``default`` cache; y cualquier numero adicional de
caches debe ser especificado. Si estas usando algún tipo de 
``backend`` u otra cache en memoria o necesitas definir múltiples
caches, necesitas definir otras opciones. Las siguientes opciones
de cache están disponibles:

BACKEND
~~~~~~~

*Valor por omisión*: ``''`` (Una cadena vacía)

El  ``backend`` para usar como cache. Los ``backends`` incorporados
en la cache son:

* ``'django.core.cache.backends.db.DatabaseCache'``
* ``'django.core.cache.backends.dummy.DummyCache'``
* ``'django.core.cache.backends.filebased.FileBasedCache'``
* ``'django.core.cache.backends.locmem.LocMemCache'``
* ``'django.core.cache.backends.memcached.MemcachedCache'``
* ``'django.core.cache.backends.memcached.PyLibMCCache'``

Puedes usar algún otro tipo de almacenamiento para la cache o
``backend`` configurando :setting:`BACKEND <CACHES-BACKEND>` con
la ruta completa a la clase  ``backend`` que estés usando. 
Por ejemplo ``mipaquete.backends.whatever.WhateverCache``

KEY_FUNCTION
~~~~~~~~~~~~

Una cadena que contiene la ruta a la función (o cualquier llamable)
que define la forma en que se compone el prefijo, ``version`` y 
``key`` en la clave de la cache final. El valor predeterminado
es equivalente a la función::

    def make_key(key, key_prefix, version):
        return ':'.join([key_prefix, str(version), key])

Puedes usar cualquier función clave que quieras, siempre que
tenga los mismo argumentos.

KEY_PREFIX
~~~~~~~~~~

*Valor por omisión*: ``''`` (Cadena Vacía)

Una cadena que estará automáticamente incluida( agregada por omisión) 
en todas la claves de la cache usadas por el servidor.

LOCATION
~~~~~~~~

*Valor por omisión*: ``''`` (Cadena Vacía)

La localización de la cache a utilizar. Ésta puede ser el directorio
para usar un archivo como sistema de cache, un host o  un puerto para
el servidor de memcache, o simplemente un nombre para identificar la 
memoria local que se esté usando, por ejemplo::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
        }
    }

OPTIONS
~~~~~~~

*Valor por omisión*:  None

Parámetros extra para pasar a la cache.  Los parámetros disponibles
varían dependiendo del tipo de ``backend`` usado para la cache.

TIMEOUT
~~~~~~~

*Valor por omisión*:  300

El número de segundos antes de que una entrada en la cache expire.
Si el valor de la configuración es ``None``, la entrada en la cache no
expira.

VERSION
~~~~~~~

*Valor por omisión*: ``1``

El valor predeterminado para el numero de versión, generado por el servidor.

CACHE_MIDDLEWARE_ALIAS
----------------------

*Valor por omisión*:  ``default``

La conexión a la cache a usar por el middleware de cache.

CACHE_MIDDLEWARE_KEY_PREFIX
---------------------------

*Valor por omisión*: ``''`` (Cadena vacía)

El prefijo de las claves de cache que debe usar el middleware de cache (ver
:doc:`capítulo 17<chapter17>`).


CACHE_MIDDLEWARE_SECONDS
------------------------

*Valor por omisión*: ``600``

El valor predeterminado para el numero de segundos que se mantendrá en cache
una página, cuando se usen el middleware de cacheo o el decorador ``cache_page()``.

CSRF_COOKIE_AGE
---------------

*Valor por omisión*: ``31449600`` (1 año, en segundos)

La edad de las cookies CSRF, en segundos.

La razón para configurar el tiempo de vida y expiración de las cookies, es para
evitar problemas en el caso de que se cierre el navegador de un usuario o una
pagina de marcadores y se cargue la pagina desde la cache del navegador. Sin 
cookies persistentes, los formularios para subir datos fallaran.    

Algunos navegadores (especialmente Internet Explorer) pueden rechazar el
uso de cookies persistentes o pueden tener índices de cookies corrompidos
en el disco, por consiguiente causan que la comprobaciones de protección CSRF
falle (a veces intermitentemente). Cambia esta configuración  a ``None`` para
usar cookies basadas en sesión CSRF, que guardan en la memoria las cookies, 
en vez de usar el almacenamiento persistente.

CSRF_COOKIE_DOMAIN
------------------

*Valor por omisión*: ``None``

El dominio para usar cuando se usa la configuración para cookie CSRF. Esto
puede ser útil para fácilmente permitir peticiones de  dominios cruzados
para excluirlas normalmente de la  protección de falsificación de petición 
de sitio. Esta puede ser una cadena tal como ``".example.com"``, para permitir
que una petición POST de un formulario en un subdominio sea validada por una
vista que es servida por otro subdominio.

Nota que la presencia de esta configuración no implica que la protección
Django CSRF sea segura de ataques en subdominios cruzados de forma predeterminada. 

CSRF_COOKIE_HTTPONLY
--------------------

*Valor por omisión*:  ``False``

Usado solo si utilizas la bandera ``HttpOnly`` en la cookie de CSRF. Si se fija en 
``True``, Java Script del lado-cliente no podrá acceder a las cookie CSRF.

Esto puede ayudar a prevenir Java Script  malicioso que pueda sobrepasar la
protección CSRF. Si permites y necesitas enviar valores al CSRF con peticiones
Ajax, Java Script  necesitara empujar  el valor de un token CSRF oculto  en
los formularios de entrada en la página, en lugar de las cookie.

CSRF_COOKIE_NAME
----------------

*Valor por omisión*: ``'csrftoken'``

El nombre de la cookie para usar el token CSRF de autentificación. Este puede ser
el que quieras.

CSRF_COOKIE_PATH
----------------

*Valor por omisión*: ``'/'``

La ruta establecida en la cookie CSRF.  Este debería corresponder a la  URL de la
ruta de instalación Django o puede ser una ruta padre de esa ruta.

Esto es útil si tienes múltiples instancias de Django ejecutándose bajo el mismo
nombre de dominio o ```hostname``. Puedes usara diferentes rutas para las cookies
y cada caso considerará solamente su propia cookies CSRF.

CSRF_COOKIE_SECURE
------------------

*Valor por omisión*: ``False``

Se asegura que la cookie sea marcada como segura.  Si está establecido en ``True``, 
La cookie será marcada como "segura," lo cual quiere decir que los navegadores 
pueden asegurar que la cookie es sólo enviada bajo  una conexión HTTPS.

CSRF_FAILURE_VIEW
-----------------

*Valor por omisión*: ``'django.views.csrf.csrf_failure'``

La ruta a la función vista, para usar cuando una petición entrante sea
rechazada por la protección CSRF. La función debe tener esta firma::

    def csrf_failure(request, reason="")

donde ``reason`` es un mensaje corto (previsto para los desarrolladores,
no para los usuarios finales) indica la razón  por la que la petición
fue rechazada.

DATABASES
---------

*Valor por omisión*:  (Un diccionario vacio)

Un diccionario que contiene las configuraciones para todas las bases
de datos usadas con Django. Es un diccionario jerarquizado cuyo 
contenido mapea alias de la base de datos a un diccionario, conteniendo
las opciones para una base de datos individual.

La configuración :setting:`DATABASES` debe permitir configurar una
base de datos por ``default``  y cualquier numero de bases de datos
adicionales que puedan especificarse.

La configuración más simple posible es para una simple base de datos
usando SQLite. Esta se puede configurar de la siguiente forma::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'datos.db',
        }
    }

Cuando se conecta a otras bases de datos, tal como MySQL, Oracle o 
PostgreSQL es necesario agregar los parámetros de conexión que requiera. 

Por ejemplo para configurar PostgreSQL::    

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'datos.db',
            'USER': 'nombreusuario',
            'PASSWORD': 'contraseña',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

Las siguientes opciones internas disponibles pueden ser requeridas
para configurar conexiones más complejas.

ATOMIC_REQUESTS
~~~~~~~~~~~~~~~

*Valor por omisión*: ``False``

Fija este valor a  ``True`` para envolver cada petición HTTP request en
una sola transacción de la base de datos.

AUTOCOMMIT
~~~~~~~~~~

*Valor por omisión*: ``True``

Fija este valor a ``False`` si quieres desactivar el manejador de transacciones
de Django e implementar el tuyo.

ENGINE
~~~~~~

*Valor por omisión*: ``''`` (cadena vacía)

Esta variable de configuración indica qué back-end de base de datos debe
usarse,  los ``backends`` incorporados son:

* ``'django.db.backends.postgresql_psycopg2'``
* ``'django.db.backends.mysql'``
* ``'django.db.backends.sqlite3'``
* ``'django.db.backends.oracle'``

Puedes usar una base de datos como backend que no esté listada en Django
configurando ``ENGINE`` con la ruta completa a tu backend (por ejemplo 
``mipaquete.backends.whatever``).

HOST
~~~~

*Valor por omisión*: ``''`` (cadena vacía)

Esta variable de configuración indica el ``dominio`` debe usarse cuando se
establezca una conexión a la base de datos. Una cadena vacía significa
``localhost``. No se usa con SQLite.

Si este valor comienza con una barra (``/``) y estás usando MySQL, MySQL se
conectará al socket vía un socket Unix::

    "HOST": '/var/run/mysql'

Si estás usando MySQL  este valor *no* comienza con una barra, entonces se asume
que el mismo es el nombre del equipo.

NAME
~~~~

*Valor por omisión*: ``''`` (cadena vacía)

El nombre de la base de datos a usarse. Para SQLite, es la ruta completa al
archivo de la base de datos.

CONN_MAX_AGE
~~~~~~~~~~~~

*Valor por omisión*: ``0``

El tiempo de vida de la conexión en segundos. Usa ``0`` para cerrar la conexión
a la base de datos al final de cada petición -- el comportamiento histórico de 
Django y ``None``  para  conexiones  persistentes ilimitadas.

OPTIONS
~~~~~~~

*Valor por omisión*: ``{}`` (Diccionario vacío)

Parámetros extra a usarse cuando se establece la conexión a la base de datos.
Los parámetros disponibles varían dependiendo de la base de datos.

PASSWORD
~~~~~~~~

*Valor por omisión*: ``''`` (cadena vacía)

Esta variable de configuración es la contraseña a usarse cuando se establece una
conexión a la base de datos. No se usa con SQLite.

PORT
~~~~

*Valor por omisión*: ``''`` (Cadena vacía)

El puerto a usarse cuando se establece una conexión a la base de datos. Una
cadena vacía significa el puerto por omisión. No se usa con SQLite.

USER
~~~~

*Valor por omisión*: ``''`` (Cadena vacía)

Esta variable de configuración es el nombre de usuario a usarse cuando se
establece una conexión a la base de datos. No se usa con SQLite.

TEST
~~~~

*Valor por omisión*: ``{}``

Un diccionario de configuraciones para pruebas o ``test`` en la base de datos.

.. faltan todas las opciones de test

DATABASE_ROUTERS
----------------

*Valor por omisión*: ``[]`` (Lista vacía)

La lista de routers que pueden usarse para determinar cual base de datos
es usada para optimizar las consultas a la base de datos.

DATE_FORMAT
-----------

*Valor por omisión*: ``'N j, Y'`` (por ej. ``Feb. 4, 2003``)

El formato a usar por omisión para los campos de fecha en las páginas lista de
cambios en el sitio de administración de Django -- y, posiblemente, por otras
partes del sistema. Acepta el mismo formato que la etiqueta ``now``.

Ver también ``DATETIME_FORMAT``, ``TIME_FORMAT``, ``YEAR_MONTH_FORMAT`` y
``MONTH_DAY_FORMAT``.

DATETIME_FORMAT
---------------

*Valor por omisión*: ``'N j, Y, P'`` (por ej. ``Feb. 4, 2003, 4 p.m.``)

El formato a usar por omisión para los campos de fecha-hora en las páginas lista
de cambios en el sitio de administración de Django -- y, posiblemente, por otras
partes del sistema. Acepta el mismo formato que la etiqueta ``now`` ver Apéndice
F, Tabla F-2).

Ver también ``DATE_FORMAT``, ``DATETIME_FORMAT``, ``TIME_FORMAT``,
``YEAR_MONTH_FORMAT`` y ``MONTH_DAY_FORMAT``.

DATE_INPUT_FORMATS
------------------

*Valor por omisión*::

    (
        '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', # '2006-10-25', '10/25/2006', '10/25/06'
        '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
        '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
        '%B %d %Y', '%B %d, %Y',            # 'Octubre 25 2006', 'Octubre 25, 2006'
        '%d %B %Y', '%d %B, %Y',            # '25 Octubre 2006', '25 Octubre, 2006'
    )

Una tupla de formatos que serán aceptados al introducir datos en un campo ``date``.     

DATETIME_FORMAT
---------------

*Valor por omisión*: ``'N j, Y, P'`` (e.g. ``Feb. 4, 2003, 4 p.m.``)

El formato predeterminado para mostrar campos tipo fecha o ``datetime`` en 
cualquier parte del sistema. Nota que si la configuración local ``USE_L10N``
es ```True`` esta tendrá mayor precedencia.

DATETIME_INPUT_FORMATS
----------------------

*Valor por omisión*::

    (
        '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
        '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
        '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
        '%Y-%m-%d',              # '2006-10-25'
        '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
        '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
        '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
        '%m/%d/%Y',              # '10/25/2006'
        '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
        '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
        '%m/%d/%y %H:%M',        # '10/25/06 14:30'
        '%m/%d/%y',              # '10/25/06'
    )

Una tupla de formatos que serán aceptados al introducir datos en un campo 
``datetime``. 
 
DEBUG
-----

*Valor por omisión*: ``False``

Esta variable de configuración es un Booleano que activa y desactiva el modo de
depuración.

Si defines variables de configuración personalizadas, ``django/views/debug.py``
tiene una expresión regular ``HIDDEN_SETTINGS`` que ocultará de la vista
``DEBUG`` todo aquello que contenga ``SECRET``, ``PASSWORD`` o ``PROFANITIES``.
Esto permite que usuarios en los que no se confía puedan proveer trazas
sin ver variables de configuración con contenido importante (u ofensivo).

Sin embargo, nota que siempre existirán secciones de la salida de depuración que
son inapropiadas para el consumo del público. Rutas de archivos, opciones de
configuración y similares le proveen a potenciales atacantes información extra
acerca de tu servidor. Nunca instales un sitio con ``DEBUG`` activo.

DEBUG_PROPAGATE_EXCEPTIONS
--------------------------

*Valor por omisión*: ``False``

Si se establece en ``True`` El manejo normal que Django hace de las
excepciones de las funciones de vista será suprimido. Esto puede ser
útil para algunos tipos de pruebas, asegúrate de solo usarlo en desarrollo.

DECIMAL_SEPARATOR
-----------------

*Valor por omisión*: ``'.'`` (Punto)

El separador de decimales predeterminado, usado cuando se formatean números
decimales. Nota que si la configuración local ``USE_L10N`` es ```True`` esta
tendrá mayor precedencia.

DEFAULT_CHARSET
---------------

*Valor por omisión*: ``'utf-8'``

El conjunto de caracteres a usar por omisión para todos los objetos
``HttpResponse`` si no se especifica en forma manual un tipo MIME. Se usa en
conjunto con ``DEFAULT_CONTENT_TYPE`` para construir la cabecera
``Content-Type``. 

DEFAULT_CONTENT_TYPE
--------------------

*Valor por omisión*: ``'text/html'``

Tipo de contenido a usar por omisión para todos los objetos ``HttpResponse``,
si no se especifica manualmente un tipo MIME. Se usa en conjunto con
``DEFAULT_CHARSET`` para construir la cabecera ``Content-Type``. Ver el
Apéndice H para conocer más acerca de los objetos ``HttpResponse``.

DEFAULT_EXCEPTION_REPORTER_FILTER
---------------------------------

*Valor por omisión*: : :class:`django.views.debug.SafeExceptionReporterFilter`

Valor predeterminado para el filtro encargado del manejo de reportes de exepciones
usado si no se asigna uno.

DEFAULT_FILE_STORAGE
--------------------

*Valor por omisión*:  :class:`django.core.files.storage.FileSystemStorage`

Clase de almacenamiento de archivos predeterminado para usar por cualquiera
de las operaciones descritas,  que no especifiquen un sistema en particular 
de almacenamiento.

DEFAULT_FROM_EMAIL
------------------

*Valor por omisión*: ``'webmaster@localhost'``

La dirección de correo a usar por omisión para correspondencia automatizada
enviada por el administrador del sitio.

DEFAULT_INDEX_TABLESPACE
------------------------

*Valor por omisión*:  ``''`` (Cadena vacía)

Predeterminado ``tablespace`` para usar como índice en campos que no especifiquen
uno, si la base de datos lo soporta.

DEFAULT_TABLESPACE
------------------

*Valor por omisión*: ``''`` (Cadena vacía)

Predeterminado ``tablespace`` para usar en modelos que no especifiquen
uno, si la base de datos lo soporta.

DISALLOWED_USER_AGENTS
----------------------

*Valor por omisión*: ``()`` (Tupla vacía)

Una lista de objetos expresiones regulares compiladas que representan cadenas
User-Agent que no tiene permitido visitar ninguna página del sitio, a nivel
global para el sitio. Usa la misma para bloquear robots y *crawlers* con mal
comportamiento. Se usa únicamente si se ha instalado ``CommonMiddleware`` (ver
:doc:`capítulo 17<chapter17>`).

EMAIL_BACKEND
-------------

*Valor por omisión*:  ``'django.core.mail.backends.smtp.EmailBackend'``

El ``backend`` usado para enviar.  

EMAIL_FILE_PATH
---------------

*Valor por omisión*: No definido

El directorio usado por el ``backend`` de emails ``file`` para almacenar archivos.

EMAIL_HOST
----------

*Valor por omisión*: ``'localhost'``

El host a usarse para enviar e-mail. Ver también ``EMAIL_PORT``.

EMAIL_HOST_PASSWORD
-------------------

*Valor por omisión*: ``''`` (cadena vacía)

La contraseña a usarse para el servidor SMTP definido en ``EMAIL_HOST``. Esta
variable de configuración se usa en combinación con ``EMAIL_HOST_USER`` cuando
se está autenticando ante el servidor SMTP. Si alguna de estas variables de
configuración está vacía, Django no intentará usar autenticación.

Ver también ``EMAIL_HOST_USER``.

EMAIL_HOST_USER
---------------

*Valor por omisión*: ``''`` (cadena vacía)

El nombre de usuario a usarse para el servidor SMTP definido en ``EMAIL_HOST``.
Si está vacío, Django no intentará usar autenticación. Ver también
``EMAIL_HOST_PASSWORD``.

EMAIL_PORT
----------

*Valor por omisión*: ``25``

El puerto a usarse pata el servidor SMTP definido en ``EMAIL_HOST``.

EMAIL_SUBJECT_PREFIX
--------------------

*Valor por omisión*: ``'[Django] '``

El prefijo del asunto para mensajes de e-mail enviados con
``django.core.mail.mail_admins`` o ``django.core.mail.mail_managers``.
Probablemente querrás incluir un espacio al final.

FILE_CHARSET
------------

*Valor por omisión*: ``'utf-8'``

La codificación del carácteres usada para decodificar cualquier archivo
leído del disco. Esto incluye archivos de plantillas y ficheros de datos 
iniciales SQL.


FILE_UPLOAD_HANDLERS
--------------------

*Valor por omisión*::

    ("django.core.files.uploadhandler.MemoryFileUploadHandler",
     "django.core.files.uploadhandler.TemporaryFileUploadHandler")

Una tupla de manejadores usados para subir archivos.

FILE_UPLOAD_MAX_MEMORY_SIZE
---------------------------

*Valor por omisión* ``2621440`` (i.e. 2.5 MB).

El tamaño máximo(en bytes) que se permite subir, antes de usar ``streamed``
por el  sistema de archivos.

FILE_UPLOAD_DIRECTORY_PERMISSIONS
---------------------------------

*Valor por omisión*: ``None``

El modo numérico aplicado a directorios creados en el proceso de subir archivos.

FILE_UPLOAD_TEMP_DIR
--------------------

*Valor por omisión*:  ``None``

El directorio para almacenar datos (en particular  archivos más grandes que
:setting:`FILE_UPLOAD_MAX_MEMORY_SIZE`) temporalmente cuando se suben archivos.
Si es ``None``, Django usara el directorio temporal usado por el sistema
operativo. Por ejemplo, en sistemas estilo-'nix el valor predeterminado es:
``/tmp``.

FIRST_DAY_OF_WEEK
-----------------

*Valor por omisión* ``0`` (Domingo)

Numero que representa el primer día de la semana. Especialmente útil cuando
se muestra un calendario. Este valor únicamente es usado cuando se usa el 
formato de ``internacionalización`` o cuando no se puede encontrar el actual
formato local.

Este valor debe ser un entero entre 0 y 6, donde 0 es Domingo, 1 es Lunes y
así sucesivamente. 

FIXTURE_DIRS
-------------

*Valor por omisión*: ``()`` (tupla vacía)

Una lista de ubicaciones para los archivos con datos de ``fixtures``, en el
orden en el que se buscará en las mismas. Notar que esas rutas deben usar
barras de estilo Unix aún en Windows. 

IGNORABLE_404_ENDS
------------------

*Valor por omisión*: ``('mail.pl', 'mailform.pl', 'mail.cgi', 'mailform.cgi', 'favicon.ico',
'.php')``

Ver también ``IGNORABLE_404_STARTS`` y ``Error reporting via e-mail``.


IGNORABLE_404_URLS
------------------

*Valor por omisión*: ``()``

Lista de expresiones regulares compiladas que describen las URL que deben ser
ignoradas cuando se reportan errores HTTP 404 via  email.

INSTALLED_APPS
--------------

*Valor por omisión*: ``()`` (tupla vacía)

Una tupla de cadenas que indican todas las aplicaciones que están activas en esta
instalación de Django. Cada cadena debe ser una ruta completa de Python hacia:

* Una clase para configurar una aplicación, o
* Un paquete que contiene una aplicación.

INTERNAL_IPS
------------

*Valor por omisión*: ``()`` (tupla vacía)

Una tupla de direcciones IP, como cadenas, que:

* Pueden ver comentarios de depuración cuando ``DEBUG`` es ``True``.
* Reciben cabeceras X si está instalado ``XViewMiddleware``.

LANGUAGES
---------

*Valor por omisión*: Una tupla de todos los idiomas disponibles. Esta lista
está en continuo crecimiento y cualquier copia que incluyéramos aquí
inevitablemente quedaría rápidamente desactualizada. Puedes ver la lista actual
de idiomas traducidos examinando ``django/conf/global_settings.py``. (o consulta
la documentación `online`_).

.. _online: https://github.com/django/django/blob/master/django/conf/global_settings.py

La lista es una tupla de tuplas de dos elementos en el formato (código de
idioma, nombre de idioma) -- por ejemplo, ``('ja', 'Japanese')``. Especifica
qué idiomas están disponibles para la selección de idioma. Ver el 
:doc:`capítulo 19<chapter19>` para más información acerca de selección de idiomas.

Generalmente, el valor por omisión debería ser suficiente. Solo asigna valor a
esta variable de configuración si deseas restringir la selección de idiomas a un
subconjunto de los idiomas provistos con Django.

Si asignas un valor personalizado a ``LANGUAGES``, está permitido marcar los
idiomas como cadenas de traducción, pero *nunca* debes importar
``django.utils.translation`` desde el archivo de configuración, porque ese
módulo a su vez depende de la configuración y esto crearía una importación
circular.

La solución es usar una función ``gettext()`` "boba". A continuación un archivo
de configuración ejemplo::

    gettext = lambda s: s

    LANGUAGES = (
        ('de', gettext('German')),
        ('en', gettext('English')),
    )

Con este esquema, ``make-messages.py`` todavía podrá encontrar y marcar esas
cadenas para traducción, pero la traducción no ocurrirá en tiempo de ejecución
-- así que tendrás que recordar envolver los idiomas con la ``gettext()`` *real*
en todo código que use ``LANGUAGES`` en tiempo de ejecución.

MANAGERS
--------

*Valor por omisión*: ``()`` (tupla vacía)

Esta tupla está en el mismo formato que ``ADMINS`` que especifica quiénes deben
recibir notificaciones de enlaces rotos cuando ``SEND_BROKEN_LINK_EMAILS`` tiene
el valor ``True``.

MEDIA_ROOT
----------

MEDIA_ROOT
----------

Default: ``''`` (Empty string)
*Valor por omisión*: ``''`` (cadena vacía)
La ruta absoluta al directorio del sistema que contiene los archivos subidos
por los usuarios.
.. warning::

    Los valores para :setting:`MEDIA_ROOT` y :setting:`STATIC_ROOT` deben de
    contener valores distintos.

MEDIA_URL
---------

Default: ``''`` (Empty string)

*Valor por omisión*: ``''`` (cadena vacía)

Esta URL maneja los medios servidos desde ``MEDIA_ROOT`` (por ej.
``"http://media.lawrence.com"``).

Notar que esta debe tener una barra final si posee un componente de ruta:

* *Correcto*: ``"http://www.example.com/static/"``
* *Incorrecto*: ``"http://www.example.com/static"``

Para usar ``{{ MEDIA_URL }}`` en las plantillas, es necesario configurar 
``'django.core.context_processors.media'`` en el 
:setting:`TEMPLATE_CONTEXT_PROCESSORS`. 

MIDDLEWARE_CLASSES
------------------

*Valor por omisión*::

    ('django.middleware.common.CommonMiddleware',
     'django.middleware.csrf.CsrfViewMiddleware')

Una tupla de clases middleware a usarse. Ver el :doc:`capítulo 17<chapter17>`.

MIGRATION_MODULES
-----------------

*Valor por omisión*::

    {}  # Un diccionario vacio

Un diccionario que especifica los paquetes donde los módulos de migraciónes
se pueden encontrar, uno por aplicación. El valor predeterminado de esta
configuración es un diccionario vacio, pero el nombre del paquete predeterminado
para el modulo de migraciones es ``migrations``.

Ejemplo::

    {'blog': 'blog.db_migrations'}

En este caso, las migraciones relacionado con la aplicación ``blog`` estarán 
contenidas en el paquete  ``blog.db_migrations``

El comando :djadmin:`makemigrations` automáticamente crea el paquete  si este no
existe.

MONTH_DAY_FORMAT
----------------

*Valor por omisión*: ``'F j'``

El formato a usar por omisión para campos de fecha en las páginas de lista de
cambios en la aplicación de administración de Django -- y, probablemente, en
otras partes del sistema -- en casos en los que sólo se muestran el mes y el
día. Acepta el mismo formato que la etiqueta ``now``.

Por ejemplo, cuando en una página de lista de cambios la aplicación de
administración de Django se filtra por una fecha, la cabecera para un día
determinado muestra el día y mes.  Diferentes locales tienen diferentes
formatos. Por ejemplo, el Inglés de EUA tendría "January 1" mientras que Español
podría tener "1 Enero".

Ver también ``DATE_FORMAT``, ``DATETIME_FORMAT``, ``TIME_FORMAT`` y
``YEAR_MONTH_FORMAT``.

PREPEND_WWW
-----------

*Valor por omisión*: ``False``

Esta variable de configuración indica si se debe agregar el prefijo de
subdominio "www." a URLs que no lo poseen. Se usa únicamente si
``CommonMiddleware`` está instalado (ver ::doc`capítulo 17<chapter17>`). 
Ver también ``APPEND_SLASH``.

NUMBER_GROUPING
----------------

*Valor por omisión*:  ``0``

Numero de dígitos agrupados 

Número de dígitos agrupados juntos en la parte entera de un número.

De uso común para visualizar separadores de mil. Si la configuración es ``0``,
entonces no se aplicara el agrupamiento a los números. Si la configuración
es más grande que ``0`` entonces :setting:`THOUSAND_SEPARATOR` se usara para
separar entre esos grupos.

Nota que si el valor de :setting:`USE_L10N` está fijado en ``True``, el formato
local tendrá precedencia sobre esta configuración.

ROOT_URLCONF
------------

*Valor por omisión*: No definido

Una cadena que representa la ruta completa de importación Python hacia tu URLconf
raíz (por ej. ``"mydjangoapps.urls"``). Ver :doc:`capítulo 3<chapter03>`.

STATIC_ROOT
-----------

*Valor por omisión* ``None``

La ruta absoluta al directorio donde se recolectaran los archivos estáticos
para el despliegue, usando el comando :djadmin:`collectstatic`.

Por ejemplo: ``"/var/www/example.com/static/"``

STATIC_URL
----------

*Valor por omisión*: ``None``

URL usada para referirse a la ubicación de los archivos estáticos en
:setting:`STATIC_ROOT`.

Por ejemplo: ``"/static/"`` o  ``"http://static.example.com/"``

SECRET_KEY
----------

*Valor por omisión*: (Generado automáticamente cuando creas un proyecto)

Una clave secreta para esta instalación particular de Django. Es usada para
proveer una semilla para los algoritmos de hashing. Asigna un valor de una
cadena con caracteres al azar -- mientras más larga mejor.
``django-admin startproject`` crea una en forma automática y en la mayoría de
los casos no será necesario que la modifiques.

SEND_BROKEN_LINK_EMAILS
-----------------------

*Valor por omisión*: ``False``

Esta variable de configuración indica si se debe enviar un e-mail a los
``MANAGERS`` cada vez que alguien visita una página impulsada por Django que
generará un error 404 y que posea una cabecera referir no vacía (en otras
palabras un enlace roto). Es solamente usado si está instalado
``CommonMiddleware`` (ver :doc:`capítulo 17<chapter17>`). 

SERIALIZATION_MODULES
---------------------

*Valor por omisión*: No definida.

Un diccionario de módulos que contiene las definiciones de serialización (previstas
como strings) Con llave para un identificador de cadena para el tipo de 
serialización. Por ejemplo, para definir un serializador YAML, usa::

    SERIALIZATION_MODULES = {'yaml': 'path.to.yaml_serializer'}

SERVER_EMAIL
------------

*Valor por omisión*: ``'root@localhost'``

La dirección de e-mail a usarse como remitente para los mensajes de error, tales
como los enviados a :setting:`ADMINS` and :setting:`MANAGERS`.

SHORT_DATE_FORMAT
-----------------

*Valor por omisión*:  ``m/d/Y`` (e.g. ``12/31/2003``)

Un formato disponible que puede usarse para mostrar campos ``date``
en las plantillas. Nota que si :setting:`USE_L10N` está fijado en ``True``,
el formato local tendrá mayor precedencia y será aplicado.

SHORT_DATETIME_FORMAT
---------------------

*Valor por omisión*:  ``m/d/Y P`` (e.g. ``12/31/2003 4 p.m.``)

Un formato disponible que puede usarse para mostrar campos ``datetime``
en las plantillas. Nota que si :setting:`USE_L10N` está fijado en ``True``,
el formato local tendrá mayor precedencia y será aplicado.

SIGNING_BACKEND
---------------

*Valor por omisión*: ``'django.core.signing.TimestampSigner'``

El ``backend`` usado para firma las cookies y otros datos.

SESSION_COOKIE_AGE
------------------

*Valor por omisión*: ``1209600`` (dos semanas, en segundos)

Esta es la edad de las cookies de sesión, en segundos. Ver :doc:`capítulo 14<chapter14>`.

SESSION_COOKIE_DOMAIN
---------------------

*Valor por omisión*: ``None``

El dominio a usarse para las cookies de sesión. Asigna como valor una cadena
tal como ``".lawrence.com"`` para cookies inter-dominio, o usa ``None`` para una
cookie de dominio estándar. Ver  :doc:`capítulo 14<chapter14>`.

SESSION_COOKIE_NAME
-------------------

*Valor por omisión*: ``'sessionid'``

El nombre de la cookie a usarse para las sesiones; puede tener el valor que tu
desees. Ver :doc:`capítulo 14<chapter14>`.

SESSION_COOKIE_SECURE
---------------------

*Valor por omisión*: ``False``

Esta variable de configuración indica si debe usarse una cookie segura para la
cookie de sesión. Si tiene un valor ``True``, la cookie será marcada como
"segura", lo que significa que los navegadores podrían asegurarse que la cookie
sólo se envíe vía una conexión HTTPS. Ver :doc:`capítulo 14<chapter14>`.

SESSION_EXPIRE_AT_BROWSER_CLOSE
-------------------------------

*Valor por omisión*: ``False``

Esta variable de configuración indica si las sesiones deben caducar cuando el
usuario cierre su navegador. Ver :doc:`capítulo 12<chapter12>`.

SESSION_SAVE_EVERY_REQUEST
--------------------------

*Valor por omisión*: ``False``

Esta variable de configuración indica si la sesión debe ser grabada en cada
petición. Ver :doc:`capítulo 14<chapter14>`.

SITE_ID
-------

*Valor por omisión*: No definida.

El identificador, como un entero, del sitio actual en la tabla
``django_site`` de la base de datos. Es usada de manera que datos de aplicación
puede conectarse en sitio(s) específico(s) y una única base de datos pueda
manejar contenido de múltiples sitios. Ver :doc:`capítulo 14<chapter14>`.

TEMPLATE_CONTEXT_PROCESSORS
---------------------------

*Valor por omisión*::

    ("django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages")

Una tupla de llamables que son usados para poblar el contexto en
``RequestContext``. Esos llamables reciben como argumento un objeto
petición y retornan un diccionario de ítems a ser fusionados con el contexto.

TEMPLATE_DEBUG
--------------

*Valor por omisión*: ``False``

Este Booleano controla el estado encendido/apagado del modo de depuración de
plantillas. Si es ``True`` la página de error vistosa mostrará un reporte
detallado para cada ``TemplateSyntaxError``. Este reporte contiene los
fragmentos relevantes de la plantilla, en los cuales se han resaltado las líneas
relevantes.

Notar que Django solo muestra páginas de error vistosas si ``DEBUG`` es
``True``, así que es posible que desees activar dicha variable para sacar
provecho de esta variable.

Ver también ``DEBUG``.

TEMPLATE_DIRS
-------------

*Valor por omisión*: ``()`` (tupla vacía)

Un lista de ubicaciones de los archivos de código fuente de plantillas, en el
orden en el que serán examinadas. Notar que esas rutas deben usar barras al
estilo Unix, aun en Windows. Ver :doc:`capítulo 4<chapter04>` y  
:doc:`capítulo 10<chapter10>`.

TEMPLATE_LOADERS
----------------

*Valor por omisión*::

     ('django.template.loaders.filesystem.Loader',
      'django.template.loaders.app_directories.Loader')

Una tupla de cargadores de plantillas, especificados como cadenas. Cada clase
``Loader`` sabe como  importar plantillas desde un particular origen. Opcionalmente,
una tupla puede usarse en lugar de una cadena. El primer ítem en la tupla debe ser
el modulo  ``Loader`` los ítems subsecuentes se pasan a ``Loader`` durante la 
inicialización. 
TEMPLATE_STRING_IF_INVALID
--------------------------

*Valor por omisión*: ``''`` (cadena vacía)

La salida, como una cadena, que debe usar el sistema de plantillas para
variables inválidas (por ej. con errores de sintaxis en el nombre). Ver Capítulo
10.

TEST_RUNNER
-----------

*Valor por omisión*: ``'django.test.simple.run_tests'``

El nombre del método a usarse para arrancar la batería de pruebas (por *test
suite*). Es usado por el framework de pruebas de Django, el cual se describe en
línea en http://www.djangoproject.com/documentation/0.96/testing/.

TIME_FORMAT
-----------

*Valor por omisión*: ``'P'`` (e.g., ``4 p.m.``)

El formato a usar por omisión para los campos de hora en las páginas
lista de cambios en el sitio de administración de Django -- y, posiblemente, por
otras partes del sistema. Acepta el mismo formato que la etiqueta ``now`` ver
Apéndice F, Tabla F-2).

Ver también ``DATE_FORMAT``, ``DATETIME_FORMAT``, ``TIME_FORMAT``,
``YEAR_MONTH_FORMAT`` y ``MONTH_DAY_FORMAT``.
TIME_ZONE
---------

*Valor por omisión*: ``'America/Chicago'``

Una cadena que representa la zona horaria para esta instalación o ``None``. 

Esta es la zona a la cual Django convertirá todas las fechas/horas -- no
necesariamente la zona horaria del servidor. Por ejemplo, un servidor podría
servir múltiples sitios impulsados por Django, cada uno con una configuración de
zona horaria separada.

Normalmente, Django fija la variable ``os.environ['TZ']`` a la zona horaria que
especificas en la variable de configuración ``TIME_ZONE``. Por lo tanto, todas
tus vistas y modelos operarán automáticamente en la zona horaria correcta. Sin
embargo, si estás usando el método de configuración manual (descrito arriba en
la sección "`Usando variables de configuración sin fijar DJANGO_SETTINGS_MODULE`_"
) Django *no* tocará la variable de entorno ``TZ`` y quedará en tus manos
asegurarte de que tus procesos se ejecuten en el entorno correcto.

.. admonition:: Nota:

    Django no puede usar en forma confiable zonas horarias alternativas en un
    entorno Windows. Si estás ejecutando Django en Windows debes asignar a esta
    variable un valor que coincida con la zona horaria del sistema.

USE_ETAGS
---------

*Valor por omisión*: ``False``

Este Booleano especifica si debe generarse la cabecera ``ETag``. La misma
permite ahorrar ancho de banda pero disminuye el rendimiento. Se usa solamente
si se ha instalado ``CommonMiddleware`` (ver :doc:`capítulo 17<chapter17>`).

USE_I18N
--------

*Valor por omisión*: ``True``

Un Booleano que especifica si debe activarse el sistema de ``internacionalización`` de
Django (ver :doc:`capítulo 19<chapter19>`). Provee una forma sencilla de desactivar la
internacionalización, para mejorar el rendimiento. Si se asigna a esta variable
el valor ``False`` Django realizará algunas optimizaciones de manera que no se
cargue la maquinaria de internacionalización.

USE_L10N
--------

*Valor por omisión*: ``False``

Un Booleano que especifica si debe activarse el sistema de ``localización`` de
Django (ver :doc:`capítulo 19<chapter19>`). Si se fija a ``True`` Django mostrara
números y fechas usando el formato de la localización actual.

.. admonition:: Nota:
    
    El archivo :file:`settings.py` creado por :djadmin:`django-admin
    startproject <startproject>` incluye por conveniencia ``USE_L10N = True``.

USE_TZ
------

*Valor por omisión*: ``False``

Un valor booleano  que especifica si se tendrán en cuenta los formatos de fecha y tiempo
por defecto o no. Django toma en cuenta los formatos de fechas y tiempos internamente
de otra forma Django usara los valores en  tiempo local.

.. admonition:: Nota:

    El archivo :file:`settings.py` creado por :djadmin:`django-admin
    startproject <startproject>` incluye por conveniencia ``USE_TZ = True``.

WSGI_APPLICATION
----------------

*Valor por omisión*:  ``None``

La ruta completa al objeto incorporado ``WSGI application`` que Django  sirve.
usando (e.g. :djadmin:`runserver`) El comando djadmin:`django-admin
startproject <startproject>` crea un simple archivo ``wsgi.py`` con un llamable
llamado ``application`` y apunta a este a la configuración de ``application``. 

Si no se fija, el valor se usara el valor de retorno de 
``django.core.wsgi.get_wsgi_application()``. En este caso el comportamiento de
:djadmin:`runserver`  será idéntico al de versiones anteriores de Django.  

YEAR_MONTH_FORMAT
-----------------

*Valor por omisión*: ``'F Y'``

El formato a usar por omisión para los campos de fecha en las páginas lista de
cambios en el sitio de administración de Django -- y, posiblemente, por otras
partes del sistema-  en los casos en los que sólo se muestran el mes y el año.
Acepta el mismo formato que la etiqueta ``now`` ver Apéndice F).

Por ejemplo, cuando se está filtrando una página lista de cambios de la aplicación
de administración de Django mediante un detalle de fecha, la cabecera de un mes 
determinado muestra el mes y el año. Los distintos ``locales`` tienen diferentes 
formatos. Por ejemplo, el Inglés de EUA usaría "January 2006" mientras que otro 
``locale`` podría usar "2006/January".
