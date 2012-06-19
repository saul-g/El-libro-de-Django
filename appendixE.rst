======================================
Apéndice E: Variables de configuración
======================================

Tu archivo de configuración contiene toda la configuración de tu instalación de
Django. Este apéndice explica cómo funcionan las variables de configuración y
qué variables de configuración están disponibles.

.. admonition:: Nota:

    A medida que Django crece, es ocasionalmente necesario agregar o (raramente)
    cambiar variables de configuración. Debes siempre buscar la información mas
    reciente en la documentación de configuración en línea que se encuentra en
    http://www.djangoproject.com/documentation/0.96/settings/.

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

``manage.py`` es descripto con mas detalle en el Apéndice G.

Usando variables de configuración en código Python
--------------------------------------------------

En tus aplicaciones Django, usa variables de configuración importando el objeto
``django.conf.settings``, por ejemplo::

    from django.conf import settings

    if settings.DEBUG:
        # Do something

Nota que ``django.conf.settings`` no es un módulo -- es un objeto. De manera
que no es posible importar variables de configuración individualmente.

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

    settings.DEBUG = True   # Don't do this!

El único lugar en el que debes asignar valores a ``settings`` es en un archivo
de configuración.

Seguridad
---------

Debido  que un archivo de configuración contiene información importante, tal
como la contraseña de la base de datos, debes hacer lo que esté e tus manos para
limitar el acceso al mismo. Por ejemplo, cambia los permisos de acceso en el
sistema de archivos de manera que solo tu y el usuario de tu servidor Web puedan
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

Cuando usas ``django-admin.py`` (ver Apéndice G), puedes ya sea fijar el valor
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

En el servidor (mod_python)
---------------------------

En tu entorno del servidor activo, necesitarás indicarle a Apache/mod_python
qué archivo de configuración debe usar. Haz eso con ``SetEnv``::

    <Location "/mysite/">
        SetHandler python-program
        PythonHandler django.core.handlers.modpython
        SetEnv DJANGO_SETTINGS_MODULE mysite.settings
    </Location>

Para más información, revisa la documentación en línea de mod_python en
http://www.djangoproject.com/documentation/0.96/modpython/.

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

    settings.configure(
        DEBUG = True,
        TEMPLATE_DEBUG = True,
        TEMPLATE_DIRS = [
            '/home/web-apps/myapp',
            '/home/web-apps/base',
        ]
    )

Pásale a ``configure()`` tantos argumentos de palabra clave como desees, con
cada argumento representando una variable de configuración y su valor. Cada
nombre de argumento debe estar escrito totalmente en mayúsculas, con el mismo
nombre que que la variable de configuración que ya se describieron. Si una
variable de configuración no es pasada a ``configure()`` y es necesario luego,
Django usará el valor por omisión respectivo.

El configurar Django de esta manera es en general necesario -- y, en efecto,
recomendado -- cuando usas una parte del framework dentro de una aplicación más
grande.

En consecuencia, cuando es configurado vía ``settings.configured()``, Django no
hará modificación alguna a las variables de entorno del proceso (revisa la
explicación acerca de ``TIME_ZONE`` mas adelante en este apéndice para conocer
porqué habría de ocurrir esto). Asumimos que en esos casos ya tienes completo
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

Normalmente, no necesitarás sobreescribir los valores por omisión de esta
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

También es un error el llamar a ``configure()`` mas de una vez, o llamar a
``configure`` luego de que ya se ha accedido a alguna variable de configuración.

En resumen: Usa exactamente una vez ya sea ``configure()`` o
``DJANGO_SETTINGS_MODULE``. No ambos, y no ninguno.

Variables de configuración disponibles
======================================

Las siguientes secciones consisten de una lista completa de todas las variables
de configuración en orden alfabético, y sus valores por omisión.

ABSOLUTE_URL_OVERRIDES
----------------------

*Valor por omisión*: ``{}`` (diccionario vacío)

Un diccionario interrelacionando cadenas ``app_label.model_name`` a funciones que
toman un objeto modelo y retornan su URL. Esta es una forma de sobreescribir
métodos ``get_absolute_url()`` en cada instalación. Un ejemplo::

    ABSOLUTE_URL_OVERRIDES = {
        'blogs.weblog': lambda o: "/blogs/%s/" % o.slug,
        'news.story': lambda o: "/stories/%s/%s/" % (o.pub_year, o.slug),
    }

Notar que el nombre del modelo usado en esta variable de configuración debe
estar escrito totalmente en mayúsculas, con independencia de la combinación de
mayúsculas y minúsculas del nombre real de la clase del modelo.

ADMIN_FOR
---------

*Valor por omisión*: ``()`` (lista vacía)

Esta variable de configuración es usada en módulos de configuración de  sitios
de administración. Debe ser una tupla de módulos de configuración (en el formato
``'foo.bar.baz'``) para los cuales este sitio es una aplicación de
administración.

El sitio de administración usa esto en la documentación automáticamente
introspeccionada de modelos, vistas y etiquetas de plantillas.

ADMIN_MEDIA_PREFIX
------------------

*Valor por omisión*: ``'/media/'``

Esta variable de configuración es el prefijo de la URL para los medios del sitio
de administración: CSS, JavaScript e imágenes. Asegúrate de usar una barra al final.

ADMINS
------

*Valor por omisión*: ``()`` (tupla vacía)

Una tupla que enumera las personas que recibirán notificaciones de errores en
el código. Cuando ``DEBUG=False`` y una vista laza una excepción, Django enviará
a esta gente un e-mail con la información completa de la información. Cada
miembro de la tupla debe ser una tupla de (Nombre completo, dirección de e-mail),
por ejemplo::

    (('John', 'john@example.com'), ('Mary', 'mary@example.com'))

Notar que Django el enviará e-mail a *todas* estas personas cada vez que ocurra
un error.

ALLOWED_INCLUDE_ROOTS
---------------------

*Valor por omisión*: ``()`` (tupla vacía)

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
URLs. Se usa solamente si está instalado ``CommonMiddleware`` (ver `Capítulo 15`_).
Ver también ``PREPEND_WWW``.

CACHE_BACKEND
-------------

*Valor por omisión*: ``'simple://'``

El ***back-end*** de cache a usarse (ver :doc:`Capítulo 13<chapter13>`).

CACHE_MIDDLEWARE_KEY_PREFIX
---------------------------

*Valor por omisión*: ``''`` (cadena vacía)

El prefijo de las claves de cache que debe usar el middleware de cache (ver
:doc:`Capítulo 13<chapter13>`).

DATABASE_ENGINE
---------------

*Valor por omisión*: ``''`` (cadena vacía)

Esta variable de configuración indica qué ***back-end*** de base de datos debe
usarse: ``'postgresql_psycopg2'``, ``'postgresql'``, ``'mysql'``,
``'mysql_old'`` o ``'sqlite3'``.

DATABASE_HOST
-------------

*Valor por omisión*: ``''`` (cadena vacía)

Esta variable de configuración indica qué equipo debe usarse cuando se
establezca una conexión a la base de datos. Una cadena vacía significa
``localhost``. No se usa con SQLite.

Si este valor comienza con una barra (``/``) y estás usando MySQL, MySQL se
conectará al socket vía un socket Unix::

    DATABASE_HOST = '/var/run/mysql'

Si estás usando MySQL  este valor *no* comienza con una barra, entonces se asume
que el mismo es el nombre del equipo.

DATABASE_NAME
-------------

*Valor por omisión*: ``''`` (cadena vacía)

El nombre de la base de datos a usarse. Para SQLite, es la ruta completa al
archivo de la base de datos.

DATABASE_OPTIONS
----------------

*Valor por omisión*: ``{}`` (diccionario vacío)

Parámetros extra a usarse cuando se establece la conexión a la base de datos.
Consulta el módulo back-end para conocer las palabras claves disponibles.

DATABASE_PASSWORD
-----------------

*Valor por omisión*: ``''`` (cadena vacía)

Esta variable de configuración es la contraseña a usarse cuando se establece una
conexión a la base de datos. No se usa con SQLite.

DATABASE_PORT
-------------

*Valor por omisión*: ``''`` (cadena vacía)

El puerto a usarse cuando se establece una conexión a la base de datos. Una
cadena vacía significa el puerto por omisión. No se usa con SQLite.

DATABASE_USER
-------------

*Valor por omisión*: ``''`` (cadena vacía)

Esta variable de configuración es el nombre de usuario a usarse cuando se
establece una conexión a la base da datos. No se usa con SQLite.

DATE_FORMAT
-----------

*Valor por omisión*: ``'N j, Y'`` (por ej. ``Feb. 4, 2003``)

El formato a usar por omisión para los campos de fecha en las páginas lista de
cambios en el sitio de administración de Django -- y, posiblemente, por otras
partes del sistema. Acepta el mismo formato que la etiqueta ``now`` ver Apéndice
F, Tabla F-2).

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

DEBUG
-----

*Valor por omisión*: ``False``

Esta variable de configuración es un Booleano que activa y desactiva el modo de
depuración.

Si defines variables de configuración personalizadas, ``django/views/debug.py``
tiene una expresión regular ``HIDDEN_SETTINGS`` que ocultará de la vista
``DEBUG`` todo aquello que contenga ``SECRET``, ``PASSWORD`` o ``PROFANITIES``.
Esto permite que usuarios en los que no se confía puedan proveer ***backtraces***
sin ver variables de configuración con contenido importante (u ofensivo).

Si embargo, nota que siempre existirán secciones de la salida de depuración que
son inapropiadas para el consumo del público. Rutas de archivos, opciones de
configuración y similares le proveen a potenciales atacantes información extra
acerca de tu servidor. Nunca instales un sitio con ``DEBUG`` activo.

DEFAULT_CHARSET
---------------

*Valor por omisión*: ``'utf-8'``

El conjunto de caracteres a usar por omisión para todos los objetos
``HttpResponse`` si no se especifica en forma manual un tipo MIME. Se usa en
conjunto con ``DEFAULT_CONTENT_TYPE`` para construir la cabecera
``Content-Type``. Ver el Apéndice H para más información acerca de los objetos
``HttpResponse``.

DEFAULT_CONTENT_TYPE
--------------------

*Valor por omisión*: ``'text/html'``

Tipo de contenido a usar por omisión para todos los objetos ``HttpResponse``,
si no se especifica manualmente un tipo MIME. Se usa en conjunto con
``DEFAULT_CHARSET`` para construir la cabecera ``Content-Type``. Ver el
Apéndice H para conocer más acerca de los objetos ``HttpResponse``.

DEFAULT_FROM_EMAIL
------------------

*Valor por omisión*: ``'webmaster@localhost'``

La dirección de correo a usar por omisión para correspondencia automatizada
enviada por el administrador del sitio.

DISALLOWED_USER_AGENTS
----------------------

*Valor por omisión*: ``()`` (tupla vacía)

Una lista de objetos expresiones regulares compiladas que representan cadenas
User-Agent que no tiene permitido visitar ninguna página del sitio, a nivel
global para el sitio. Usa la misma para bloquear robots y *crawlers* con mal
comportamiento. Se usa únicamente si se ha instalado ``CommonMiddleware`` (ver
`Capítulo 15`_).

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

FIXTURE_DIRS
-------------

*Valor por omisión*: ``()`` (tupla vacía)

Una lista de ubicaciones para los archivos con datos de ***fixtures***, en el
orden en el que se se buscará en las mismas. Notar que esas rutas deben usar
barras de estilo Unix aún en Windows. Es usado por el framework de pruebas de
Django, el cual se trata en
http://www.djangoproject.com/documentation/0.96/testing/.

IGNORABLE_404_ENDS
------------------

*Valor por omisión*: ``('mail.pl', 'mailform.pl', 'mail.cgi', 'mailform.cgi', 'favicon.ico',
'.php')``

Ver también ``IGNORABLE_404_STARTS`` y ``Error reporting via e-mail``.

IGNORABLE_404_STARTS
--------------------

*Valor por omisión*: ``('/cgi-bin/', '/_vti_bin', '/_vti_inf')``

Una tupla de cadenas que especifican las partes iniciales de URLs que deben ser
ignoradas para el envío de mensajes de e-mail para errores 404. Ver también
``SEND_BROKEN_LINK_EMAILS`` y ``IGNORABLE_404_ENDS``.

INSTALLED_APPS
--------------

*Valor por omisión*: ``()`` (tupla vacía)

Una tupla de cadenas que indican todas las aplicaciones que están activas en esta
instalación de Django. Cada cadena debe ser una ruta completa de Python hacia un
paquete Python que contiene una aplicación Django. Ver el `Capítulo 5`_ para más
información acerca de aplicaciones.

INTERNAL_IPS
------------

*Valor por omisión*: ``()`` (tupla vacía)
 Una tupla de direcciones IP, como cadenas, que:

* Pueden ver comentarios de depuración cuando ``DEBUG`` es ``True``

* Reciben cabeceras X si está instalado ``XViewMiddleware`` (ver Capítulo
  15)

JING_PATH
---------

*Valor por omisión*: ``'/usr/bin/jing'``

La ruta al ejecutable Jing. Jing es un validador RELAX NG, y Django usa el mismo
para validar los campos ``XMLField`` en tus modelos. Ver
http://www.thaiopensource.com/relaxng/jing.html.

LANGUAGE_CODE
-------------

*Valor por omisión*: ``'en-us'``

Una cadena representando el código de idioma para esta instalación. Debe
estar expresado usando el formato estándar -- por ejemplo, Inglés de EUA es
"en-us". Ver el `Capítulo 18`_.

LANGUAGES
---------

*Valor por omisión*: Una tupla de todos los idiomas disponibles. Esta lista
está en continuo crecimiento y cualquier copia que incluyéramos aquí
inevitablemente quedaría rápidamente desactualizada. Puedes ver la lista actual
de idiomas traducidos examinando ``django/conf/global_settings.py``.

La lista es una tupla de tuplas de dos elementos en el formato (código de
idioma, nombre de idioma) -- por ejemplo, ``('ja', 'Japanese')``. Especifica
qué idiomas están disponibles para la selección de idioma. Ver el `Capítulo 18`_
para más información acerca de selección de idiomas.

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

*Valor por omisión*: ``''`` (cadena vacía)

Una ruta absoluta al directorio que contiene medios para esta instalación (por
ej. ``"/home/media/media.lawrence.com/"``). Ver también ``MEDIA_URL``.

MEDIA_URL
---------

*Valor por omisión*: ``''`` (cadena vacía)

Esta URL maneja los medios servidos desde ``MEDIA_ROOT`` (por ej.
``"http://media.lawrence.com"``).

Notar que esta debe tener una barra final si posee un componente de ruta:

* *Correcto*: ``"http://www.example.com/static/"``
* *Incorrecto*: ``"http://www.example.com/static"``

MIDDLEWARE_CLASSES
------------------

*Valor por omisión*::

    ("django.contrib.sessions.middleware.SessionMiddleware",
     "django.contrib.auth.middleware.AuthenticationMiddleware",
     "django.middleware.common.CommonMiddleware",
     "django.middleware.doc.XViewMiddleware")

Una tupla de clases middleware a usarse. Ver el :doc:`Capítulo 15<chapter15>`.

MONTH_DAY_FORMAT
----------------

*Valor por omisión*: ``'F j'``

El formato a usar por omisión para campos de fecha en las páginas de lista de
cambios en la aplicación de administración de Django -- y, probablemente, en
otras partes del sistema -- en casos en los que sólo se muestran el mes y el
día. Acepta el mismo formato que la etiqueta ``now`` (ver Apéndice F, tabla
F-2)

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
``CommonMiddleware`` está instalado (ver ::doc`Capítulo 15<chapter15>`). Ver también
``APPEND_SLASH``.

PROFANITIES_LIST
----------------

Una tupla de profanidades, como cadenas, que dispararán un error de validación
cuando se llama al validador ``hasNoProfanities``.

No enumeramos aquí los valores por omisión, debido a que esto podría hacer que
nos cayera encima la comisión de clasificación de la MPAA. Para ver los valores
por omisión examina el archivo ``django/conf/global_settings.py``.

ROOT_URLCONF
------------

*Valor por omisión*: No definido

Una cadena que representa la ruta completa de importación Python hacia tu URLconf
raíz (por ej. ``"mydjangoapps.urls"``). Ver :doc:`Capítulo 3<chapter03>`.

SECRET_KEY
----------

*Valor por omisión*: (Generado automáticamente cuando creas un proyecto)

Una clave secreta para esta instalación particular de Django. Es usada para
proveer una semilla para los algoritmos de hashing. Asigna un valor de una
cadena con caracteres al azar -- mientras mas larga mejor.
``django-admin startproject`` crea una en forma automática y en la mayoría de
los casos no será necesario que la modifiques.

SEND_BROKEN_LINK_EMAILS
-----------------------

*Valor por omisión*: ``False``

Esta variable de configuración indica si se debe enviar un e-mail a los
``MANAGERS`` cada vez que alguien visita una página impulsada por Django que
generará un error 404 y que posea una cabecera referer no vacía (en otras
palabras un enlace roto). Es solamente usado si está instalado
``CommonMiddleware`` (ver :doc:`Capítulo 15<chapter15>`). Ver también ``IGNORABLE_404_STARTS`` y
``IGNORABLE_404_ENDS``.

SERIALIZATION_MODULES
---------------------

*Valor por omisión*: No definida.

La serialización es una característica que todavía está bajo fuerte desarrollo.
Revisa la documentación en línea en
http://www.djangoproject.com/documentation/0.96/serialization/
si deseas más información.

SERVER_EMAIL
------------

*Valor por omisión*: ``'root@localhost'``

La dirección de e-mail a usarse como remitente para los mensajes de error, tales
como los enviados a ``ADMINS`` y ``MANAGERS``.

SESSION_COOKIE_AGE
------------------

*Valor por omisión*: ``1209600`` (dos semanas, en segundos)

Esta es la edad de las cookies de sesión, en segundos. Ver :doc:`Capítulo 12<chapter12>`.

SESSION_COOKIE_DOMAIN
---------------------

*Valor por omisión*: ``None``

El dominio a usarse para las cookies de sesión. Asigna como valor una cadena
tal como ``".lawrence.com"`` para cookies inter-dominio, o usa ``None`` para una
cookie de dominio estándar. Ver `Capítulo 12`_.

SESSION_COOKIE_NAME
-------------------

*Valor por omisión*: ``'sessionid'``

El nombre de la cookie a usarse para las sesiones; puede tener el valor que tu
desees. Ver :doc:`Capítulo 12<chapter12>`.

SESSION_COOKIE_SECURE
---------------------

*Valor por omisión*: ``False``

Esta variable de configuración indica si debe usarse una cookie segura para la
cookie de sesión. Si tiene un valor ``True``, la cookie será marcada como
"segura", lo que significa que los navegadores podrían asegurarse que la cookie
sólo se envíe vía una conexión HTTPS. Ver :doc:`Capítulo 12<chapter12>`.

SESSION_EXPIRE_AT_BROWSER_CLOSE
-------------------------------

*Valor por omisión*: ``False``

Esta variable de configuración indica si las sesiones deben caducar cuando el
usuario cierre su navegador. Ver :doc:`Capítulo 12<chapter12>`.

SESSION_SAVE_EVERY_REQUEST
--------------------------

*Valor por omisión*: ``False``

Esta variable de configuración indica si la sesión debe ser grabada en cada
petición. Ver :doc:`Capítulo 12<chapter12>`.

SITE_ID
-------

*Valor por omisión*: No definida.

El identificador, como un entero, del sitio actual en la tabla
``django_site`` de la base de datos. Es usada de manera que datos de aplicación
puede conectarse en sitio(s) específico(s) y una única base de datos pueda
manejar contenido de múltiples sitios. Ver :doc:`Capítulo 14<chapter14>`.

TEMPLATE_CONTEXT_PROCESSORS
---------------------------

*Valor por omisión*::

    ("django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n")

Una tupla de ***callables*** que son usados para poblar el contexto en
``RequestContext``. Esos ***callables*** reciben como argumento un objeto
petición y retornan un diccionario de items a ser fusionados con el contexto.
Ver `Capítulo 10`_.

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
estilo Unix, aun en Windows. Ver Capítulos 4 y 10.

TEMPLATE_LOADERS
----------------

*Valor por omisión*: ``('django.template.loaders.filesystem.load_template_source',)``

Una tupla de ***callables*** (como cadenas) que saben como importar plantillas
desde diferentes orígenes. Ver :doc:`Capítulo 10<chapter10>`.

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

TEST_DATABASE_NAME
------------------

*Valor por omisión*: ``None``

El nombre de la base de datos a usarse cuando se ejecute la batería de pruebas
(por *test suite*). Si se especifica un valor ``None``, el nombre de la base de datos de
pruebas será ``'test_' + settings.DATABASE_NAME``. Ver la documentación del
framework de pruebas de Django el cual se describe en línea en
http://www.djangoproject.com/documentation/.

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

Una cadena que representa la zona horaria para esta instalación. Las zonas
horarias se expresan en el formato ``zic`` estándar de Unix. Puede encontrarse
una lista relativamente completa de cadenas de zonas horarias en
http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE.

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

URL_VALIDATOR_USER_AGENT
------------------------

*Valor por omisión*: ``Django/<version> (http://www.djangoproject.com/)``

La cadena usarse como la cabecera ``User-Agent`` cuando se realizan
verificaciones acerca e si las URLs existen (ver la opción ``verify_exists`` de
``URLField``; ver Apéndice B).

USE_ETAGS
---------

*Valor por omisión*: ``False``

Este Booleano especifica si debe generarse la cabecera ``ETag``. La misma
permite ahorrar ancho de banda pero disminuye el rendimiento. Se usa solamente
si se ha instalado ``CommonMiddleware`` (ver :doc:`Capítulo 15<chapter15>`).

USE_I18N
--------

*Valor por omisión*: ``True``

Este Booleano especifica si debe activarse el sistema de internacionalización de
Django (ver :doc:`Capítulo 18<chapter18>`). Provee una forma sencilla de desactivar la
internacionalización, para mejorar el rendimiento. Si se asigna a esta variable
el valor ``False`` Django realizará algunas optimizaciones de manera que no se
cargue la maquinaria de internacionalización.

YEAR_MONTH_FORMAT
-----------------

*Valor por omisión*: ``'F Y'``

El formato a usar por omisión para los campos de fecha en las páginas lista de
cambios en el sitio de administración de Django -- y, posiblemente, por otras
partes del sistema-  en los casos en los que sólo se muestran el mes y el año.
Acepta el mismo formato que la etiqueta ``now`` ver Apéndice F).

Por ejemplo, cuando se está filtrando una página lista de cambios de la aplicación de administración
de Django mediante un detalle de fecha, la cabecera de un mes determinado
muestra el mes y el año. Los distintos locales tienen diferentes formatos. Por
ejemplo, el Inglés de EUA usaría "January 2006" mientras que otro locale podría
usar "2006/January".

Ver también ``DATE_FORMAT``, ``DATETIME_FORMAT``, ``TIME_FORMAT`` y
``MONTH_DAY_FORMAT``.
