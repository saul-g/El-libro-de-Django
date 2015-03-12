=============================
Capitulo 12: Desplegar Django
=============================

Este capítulo cubre el último paso esencial para construir una aplicación
Django: **el despliegue en un servidor de producción**.

.. Warning: Esta pagina esta en progreso, existen errores y se esta agregando contenido adicional.

Si has estado siguiendo los ejemplos presentados, probablemente has estado usando
``runserver``, como ya sabes este comando inicia el servidor web y hace que las
cosas sean realmente muy fáciles -- con ``runserver``, no tienes que  preocuparte
por instalar un servidor Web. Sin embargo ``runserver`` está diseñado únicamente
para ser usado en el desarrollo de forma local, no para exponerlo en un sitio
publico Web. Para desplegar una aplicación Django, es necesario enlazarla a un
servidor Web poderoso  tal como Apache. En este capítulo te mostraremos como
hacerlo  -- pero primero, es necesario comprobar una lista de cosas que hacer
en el código antes de llevarlo a un entorno de producción.

Prepara tu código base para producción
======================================

Afortunadamente el comando ``runserver`` es bastante parecido a un servidor
"real", por lo que no necesitas realizar  muchos cambios a tu aplicación Django
para dejarla lista para producción. Sin embargo hay algunas *cosas esenciales*
que necesitas conocer antes de servirla en producción.

Desactiva el Modo Debug
-----------------------

Cuando creamos un proyecto en el  :doc:`capítulo 2<chapter02>`,  el comando
``django-admin.py startproject`` creo un archivo llamado ``settings.py`` el
cual contiene la variable ``DEBUG`` fijada en  ``True`` por defecto, es decir
que esta en modo de depuración. Muchas de las partes internas de Django
comprueban esta configuración y cambian su comportamiento  si el modo
``DEBUG`` esta activado. Por ejemplo, si ``DEBUG`` está fijado en ``True``,
entonces:

* Todas las consultas a la base de datos se guardan en memoria como objetos
  ``django.db.connection.queries``. Como puedes imaginar, ¡esto consume mucha
  memoria!

* Cualquier error 404, renderizara una página especial, a decir una página
  no encontrada (cubierta en el capítulo 3) más que retornar una apropiada
  respuesta 404. Esta página contiene información potencialmente sensible y
  *no* debe ser expuesta al público en Internet.

* Cualquier excepción no atrapada en tu aplicación Django -- desde errores básicos
  en la sintaxis Python, errores de la base de datos o en la sintaxis de la
  plantilla -- serán renderizados por la páginas de errores bonitas de Django
  que probablemente adoras. Esta página contiene *mas* información sensible
  incluso que las páginas 404, por lo que *nunca* deben ser expuestas al
  publico.

Resumiendo, la variable de configuración ``DEBUG`` = ``True`` le dice a Django
que asuma que únicamente desarrolladores confiables están usando el sitio.
La internet está llena de personas poco fiables, y la primera cosa que debes
hacer cuando estés preparando tu aplicación para el despliegue en producción
es fijar la variable ``DEBUG`` a ``False``.

Desactiva el modo Debug de la plantillas
----------------------------------------

De igual forma, es necesario fijar la variable ``TEMPLATE_DEBUG`` a ``False``
en producción. Esto para desactivar el modo depuración de las plantillas.
Ya que si está fijada en ``True``, esta configuración le dice al
sistema de plantillas de Django que guarde información extra acerca de cada
plantilla, para mostrarla en las útiles páginas de error, si el modo
``DEBUG``=``True`` (esta activado).


Implementa una plantilla 404
----------------------------

Si ``DEBUG`` es ``True``, Django mostrara una muy útil página de error 404. Pero
si ``DEBUG`` es ``False``, hará algo completamente diferente: renderizara
una plantilla llamada ``404.html`` en la raíz del directorio de plantillas.
Entonces, cuando estás listo para  el despliegue, necesitas crear esta
plantilla y ponerle algo útil,  como  un mensaje  de "Página no encontrada".

Aquí está un ejemplo de una  página ``404.html``, puedes usarla como el punto
de partida, para crear tu propia plantilla. La plantilla asume que estas
usando la herencia de plantillas y  tiene definida  una plantilla ``base.html``
con bloques llamados ``titulo`` y ``contenido``.

.. code-block:: html+django

    {% extends "base.html" %}

    {% block title %}Página no encontrada {% endblock %}

    {% block content %}
    <h1>Página no encontrada</h1>

    <p>Lo sentimos, pero la página que buscas no ha sido encontrada.</p>
    {% endblock %}

Para probar que la plantilla ``404.html`` funciona, solo cambia el modo ``DEBUG``
a ``False`` y visita una URL que no exista. (Esto trabaja de igual forma en
el servidor de desarrollo con ``runserver``, que en un servidor de producción.)

Implementa una plantilla 500
----------------------------

De igual forma si ``DEBUG`` es ``False``, Django no mostrara la útil página
de traza de errores, en caso de excepciones no manejadas. En su lugar mostrara y
renderizara una plantilla llamada ``500.html``. Tal como la página ``404.html``,
esta plantilla debe de localizarse en la raíz del directorio de plantillas.

Hay una ligera trampa acerca de las páginas ``500.html``. Nunca puedes
estar seguro por qué se renderiza esta plantilla, así que no deberías hacer
nada que requiere una conexión a la base de datos o confiar en cualquier parte
potencialmente rota de la infraestructura. (Por ejemplo, no deberías usar
etiquetas personalizadas en la plantilla.) Si usas la  herencia de plantillas,
entonces la plantilla padre,  no debería poder conectarse a la infraestructura
potencialmente rota. Por consiguiente, la mejor forma de aprovechar esto, es
evitar la herencia de  plantillas y usar algo muy simple y solo en HTML. Aquí
hay un  ejemplo de una página ``500.html``, como un punto de partida, para que
diseñes la tuya:

.. code-block:: html

    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
        "http://www.w3.org/TR/html4/strict.dtd">
    <html lang="en">
    <head>
        <title>Página no disponible</title>
    </head>
    <body>
        <h1>Página no disponible</h1>

        <p>Lo sentimos, pero la página pedida no está disponible por que
        el servidor tiene hipo.</p>

        <p>Los ingenieros han sido notificados, así que vuelva a revisar más
        tarde</p>
    </body>
    </html>

Establece errores de alerta
---------------------------

Cuando tu sitio creado con Django está corriendo y se lanza una excepción,
necesitas estar al tanto, para poder corregir cualquier defecto. Por omisión,
Django está configurado para enviar un e-mail a los desarrolladores del sitio,
cuando el código lanza una excepción; pero necesitas hacer algunas cosas para
configurarlo.

* Primero cambia la configuración  ``ADMINS`` para incluir la dirección de e-mail,
  con las direcciones de cada una de las personas que necesitan ser notificadas.
  Esta configuración es una tupla del tipo  ``(nombre, email)``, la tupla puede
  ser así ::

        ADMINS = (
            ('John Lennon', 'jlennon@example.com'),
            ('Paul McCartney', 'pmacca@example.com'),
        )

* Segundo, asegúrate de que tu servidor este configurado para enviar e-mails.
  Configurar ``postfix``, ``sendmail`` o cualquier otro servidor de e-mails, esta
  fuera del alcance de este libro, pero del lado de Django, debes de asegurarte
  de configurar ``EMAIL_HOST`` y establecer el "hostname" apropiado  para tu
  servidor de correo. Si lo estableces a ``'localhost'``  por defecto, trabajara
  fuera de la caja  en muchos entornos de servicios compartidos. También es
  necesario que establezcas los parámetros de las siguientes configuraciones:
  ``EMAIL_HOST_USER``, ``EMAIL_HOST_PASSWORD``, ``EMAIL_PORT`` o ``EMAIL_USE_TLS``,
  dependiendo de la complejidad de tu infraestructura.

* Por último, también establece el prefijo con ``EMAIL_SUBJECT_PREFIX`` el cual
  controla el nombre que Django usa delante de los errores en los correos
  electrónicos. Por defecto esta establecido en ``'[Django] '``.

Estable alertas para enlaces rotos
----------------------------------

Si tienes la clase  ``CommonMiddleware`` instalada (en tu archivo de configuración en
la variable ``MIDDLEWARE_CLASSES`` que incluye
``'django.middleware.common.CommonMiddleware'``,  lo cual ocurre  por defecto)
tienes la opción de recibir un e-mail cada vez que alguien visita una página
creada con Django que lanze un error 404 con una referencia a no-vacía -- esto
es cada vez que encuentre enlaces rotos. Si quieres activar esta característica,
establece ``SEND_BROKEN_LINK_EMAILS`` a ``True`` (esta es ``False`` por defecto)
y establece en la configuración ``MANAGERS`` a la persona o personas que recibirán
esos e-mails de enlaces rotos. ``MANAGERS`` usa la misma sintaxis que
``ADMINS``, un tupla.  por ejemplo::

    MANAGERS = (
        ('George Harrison', 'gharrison@example.com'),
        ('Ringo Starr', 'ringo@example.com'),
    )

Nota que los e-mails de errores pueden llegar a ser muy molestos; no son para todo el
mundo.

Como usar diferentes configuraciones para producción
====================================================

Hasta ahora en este libro, hemos tratado únicamente con un simple archivo
de configuraciones: ``settings.py`` generado por el comando ``django-admin.py
startproject``. Pero como estamos listos para desplegarlo, probablemente
nos encontremos con la necesidad de usar múltiples archivos de configuraciones
para mantener el entorno de desarrollo  aislado del ambiente de producción.
(Por ejemplo, probablemente no quieras cambiar  ``DEBUG`` de ``False`` a
``True`` cada vez que quieras probar los cambios al código,  en tu maquina de
forma local.) Django hace esto muy sencillo, permitiéndote usar múltiples archivos
de configuraciones.

Si quieres organizar tus archivos de configuraciones, dividiéndolos en
"desarrollo" y "producción", puedes lograrlo usando una de las siguientes tres
formas.

* Establece dos archivos de configuraciones completos, de forma independiente.

* Establece un archivo de configuraciones "base" (uno para desarrollo) y un
  segundo (para producción) el archivo de configuraciones  simplemente importa
  del primero y define lo que necesita y lo que debe sobrescribirse.

* Usa únicamente un archivo de configuraciones y deja que Python se encargue de
  la lógica y haga los cambios a las configuraciones, basado en el contexto.

Veamos estas tres opciones, una por una.

Primero, la forma más básica para aprovechar esto, es definir dos archivos
separados. Si estas siguiendo esto, ya tienes un archivo ``settings.py``. Ahora
solo es necesario realizar una copia llamada ``settings_production.py``.( Si no
te gusta el nombre, puedes llamarlo como quieras) En este nuevo archivo,
cambia las variables necesarias como ``DEBUG``, etc.

La segunda forma de aprovechar esto es muy parecida, pero reduce algo de
redundancia, En lugar de tener dos archivos de configuraciones con contenido
similar, tratamos solo con un archivo "base" y creamos otro archivo que lo
importe. Por ejemplo::

    # settings.py

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'devdb'
    DATABASE_USER = ''
    DATABASE_PASSWORD = ''
    DATABASE_PORT = ''

    # ...

    # settings_produccion.py

    from settings import *

    DEBUG = TEMPLATE_DEBUG = False
    DATABASE_NAME = 'production'
    DATABASE_USER = 'app'
    DATABASE_PASSWORD = 'dejameentrar'

Aquí tenemos que ``settings_production.py`` importa cualquier cosa de
``settings.py`` y solo redefine las configuraciones que son usadas especialmente
en producción. En este caso ``DEBUG`` está fijado en ``False``,   pero también
hemos fijado diversos parámetros, como el acceso a la base de datos para
configurarla  en  producción. (Mas adelante te mostraremos como redefinir
*cualquier* configuración, no únicamente las básicas como ``DEBUG``. )

Finalmente, la forma más concisa para lograr tener dos entornos de
configuraciones es usar un solo archivo,  que se ramifique basado en el entorno.
Una de las formas de lograr esto es comprobar el actual "hostname."
Por ejemplo::

    # settings.py

    import socket

    if socket.gethostname() == 'my-laptop':
        DEBUG = TEMPLATE_DEBUG = True
    else:
        DEBUG = TEMPLATE_DEBUG = False

    # ...

Aquí, importamos el modulo ``socket`` de la librería estándar de Python y lo
usamos para comprobar el nombre actual  del sistema. Podemos comprobar el
"nombre" para determinar si el código está siendo ejecutado en un servidor de
producción.

La lección central, es que el archivo de configuraciones es *solo código Python*.
Que puede importar otros archivos, puede ejecutar lógica arbitraria, etc. Solo
asegúrate de que el código Python en tu archivo de configuraciones sea a prueba
de balas. Si lanza una excepción, Django probablemente  se estrellara de
fea manera.

.. admonition:: Renombrar settings.py


    Siéntete libre de renombrar tu archivo ``settings.py`` a ``settings_dev.py``
    o ``settings/dev.py`` o ``foobar.py`` -- A Django no le importa como lo
    llames, solo necesita saber que archivo estas usando para usarl las
    configuraciones.

    Solo ten en cuenta que si renombras el archivo ``settings.py`` que es
    generado por el comando ``django-admin.py startproject``, te encontraras con
    que ``manage.py`` lanza un mensaje de error, diciendo que no puede encontrar
    el archivo de configuraciones. Esto es debido a que trata de importar un
    modulo llamado ``settings``.  Puedes arreglar esto editando ``manage.py`` y
    cambiándole  el nombre de ``settings`` por el nombre de tu modulo o usando
    ``django-admin.py``  en lugar de ``manage.py``. En este último caso, necesitas
    fijar ``DJANGO_SETTINGS_MODULE``  con las variables de entorno de la ruta
    de búsqueda Python en tu archivo de configuraciones (por ejemplo
    ``'misitio.settings'``)

Cuando usas Django tienes que indicarle qué configuración estás usando. Haz esto
mediante el uso de de la variable de entorno ``DJANGO_SETTINGS_MODULE``.
El valor de ``DJANGO_SETTINGS_MODULE`` debe respetar la sintaxis de rutas de Python
(por ej. misitio.settings. Observa que el módulo de configuración debe de
encontrarse en la ruta de búsqueda para las importaciones de Python (PYTHONPATH).

DJANGO_SETTINGS_MODULE
======================

Con todos estos cambios en el código, la siguiente parte de este capítulo se
centra en las instrucciones especificas para desplegar distintos entornos, tal
como Apache, Gunicorn... Las instrucciones son diferentes para cada entorno, pero
una cosa es la misma: en cada caso necesitas decirle al servidor Web cuál es tu:
``DJANGO_SETTINGS_MODULE``. Este es el punto de entrada de tu aplicación Django.
``DJANGO_SETTINGS_MODULE`` enlaza tu archivo de configuraciones, el cual apunta
a ``ROOT_URLCONF``, que a su vez enlaza tus vistas y así sucesivamente.

El objeto application
---------------------

El concepto clave para implementar usando ``WSGI``  es el llamable ``application``
que es el servidor de aplicaciones utiliza para comunicarse con el código. Este
comúnmente se  provee como un objeto llamado ``application`` el cual es un
modulo Python accesible por el servidor.

El comando  ``startproject`` crea un archivo llamado **wsgi.py** este contiene
una ``application`` llamable. Este es usado tanto en el servidor de  desarrollo,
como en el despliegue para producción, por lo que no necesitas crearlo.

El servidor WSGI obtiene la ruta de el llamable ``application`` de su
configuración. El servidor de desarrollo "runserver" lee la configuración  de
``WSGI_APPLICATION``, la cual enlaza a el llamable ``application`` en el archivo
``wsgi.py``, lo mismo pasa con un servidor en producción.

Configura el modulo settings
----------------------------

Cuando el servidor WSGI carga tu aplicación, Django necesita importar
el modulo de configuraciones ``settings``  -- que es donde se define
completamente la aplicación.

Django usa la variable de entorno ``DJANGO_SETTINGS_MODULE`` que contiene la
ruta para localizar apropiadamente  este modulo. Puedes usar diferentes valores
para desarrollo y producción; todo depende de cómo organices tus configuraciones.

Si esta variable no está establecida, el valor por defecto es ``misitio.settings``,
donde ``misitio`` es el nombre de tu proyecto y ``settings`` es el nombre del archivo
``settings.py``. Esta es la forma en que ``runserver`` carga el archivo de
configuraciones por defecto.

Como desplegar con WSGI
=======================

La plataforma dominante de implementación para Django es WSGI_, el estándar
Python para servidores y aplicaciones Web.

.. _WSGI: http://www.wsgi.org

El comando administrativo  ``startproject``  establece por defecto, un simple
archivo de configuración WSGI, el cual puedes personalizarse según las
necesidades de tu proyecto, y directamente adaptarse a cualquier servidor que
ofrezca soporte para WSGI, como los siguientes servidores:

* mod_wsgi
* apache
* gunicorn
* uwsgi

Usando Django con Apache y mod_wsgi
===================================

Desplegar Django con Apache_ y `mod_wsgi`_  es la manera probada y comprobada de
usar Django en un servidor en producción.

.. _Apache: http://httpd.apache.org/
.. _mod_wsgi: http://code.google.com/p/modwsgi/

mod_wsgi es un modulo de Apache que puede hospedar cualquier aplicación Python
WSGI_, incluyendo Django. El cual trabaja con cualquier versión de Apache que
soporte mod_wsgi.

.. _WSGI: http://www.wsgi.org

La `Documentación oficial`_ es fantástica, y el código fuente incluye detalles sobre
el modo de usar mod_wsgi. Por lo que probablemente quieras empezar por leer
`la documentación sobre instalación y configuración`_.

.. _Documentación oficial: http://code.google.com/p/modwsgi/
.. _la documentación sobre instalación y configuración: http://code.google.com/p/modwsgi/wiki/InstallationInstructions

Configuración básica
====================

Para configurar Django con mod_wsgi, primero debes asegurarte de que tienes
instalado  Apache con el módulo mod_wsgi activado. Esto usualmente significa
tener una directiva LoadModule en tu archivo de configuración de Apache.
Parecida a esta:::

    LoadModule wsgi_module  /modules/mod_wsgi.so


.. # LoadModule foo_module modules/mod_foo.so

Una vez que has instalado y activado mod_wsgi, edita el archivo ``httpd.conf``
de tu servidor Web Apache y agrega lo siguiente. Si estas usando una versión
de Apache anterior a la 2.4, remplaza  ``Require all granted`` con
``Allow from all`` y tambien agrega la línea ``Order deny,allow`` arriba de esta.

.. code-block:: apache

    WSGIScriptAlias / /path/to/mysite.com/mysite/wsgi.py
    WSGIPythonPath /path/to/mysite.com

    <Directory /path/to/mysite.com/mysite>
    <Files wsgi.py>
    Require all granted
    </Files>
    </Directory>

El primer fragmento de la línea ``WSGIScriptAlias`` es la ruta base que quieres
servir tu aplicaciones  en (``/`` indica la raíz de la url) y la segunda es la
localización de el "archivo WSGI" --ver más abajo  en tu sistema, usualmente
dentro del paquete de tu proyecto (``misitio`` en este ejemplo.) Esto le dice
al servidor Apache “Usa mod_wsgi para cualquier petición URL en ‘/’ o bajo ella,
usando la aplicación WSGI definida en ese archivo".

La línea ``WSGIPythonPath`` se asegura que el paquete del proyecto este
disponible para importar la ruta de búsqueda de Python; en otras palabras se
asegura que ``import misitio`` trabaje.

La  pieza ``<Directory>`` solo  se asegura de que Apache pueda acceder al archivo
``wsgi.py``, ya que se utiliza para apuntar a lugares de nuestra sistema de
archivos,

Lo siguiente que necesitas hacer, es asegurarte que  exista una archivo
``wsgi.py``, como seguramente te diste cuenta el comando ``startproject`` crea
este archivo por defecto al crear el proyecto, de otra forma tendrías que crear
este archivo manualmente.

.. warning::

   Si varios sitios están siendo ejecutados en un simple proceso mod_wsgi,
   todos ellos usarán las configuraciones de cualquiera de los procesos que
   corra primero. Esto puede se solventado con un pequeño cambio en  el archivo
   ``wsgi.py`` (ve los comentarios en el archivo para detalles) o puedes
   asegurarte de cada sitio sea ejecutado en un proceso independiente, usando su
   propio demonio, sobrescribiendo el valor por defecto usando:
   ``os.environ["DJANGO_SETTINGS_MODULE"] = "misitio.settings"`` en el arhvio
   ``wsgi.py``


Usando virtualenv
=================

Si has instalado las dependencias Python de tu proyecto dentro de `virtualenv`_,
necesitas agregar la ruta de "virtualenv's" al directorio ``site-packages``, así
como el camino de búsqueda. Para hacer esto agrega una ruta de búsqueda adicional
a la directiva ``WSGIPythonPath``, con las múltiples rutas separadas por dos
puntos (``:``) si estas usando un sistema del tipo UNIX, o punto y coma  (``;``)
si estas usando Windows. Si cualquier parte de la ruta al directorio contiene
caracteres como espacios, la cadena completa de argumentos para ``WSGIPythonPath``
debe ser citada::

    WSGIPythonPath /path/to/mysite.com:/path/to/your/venv/lib/python3.X/site-packages

Asegúrate de darle la ruta correcta a tu  virtualenv, y remplazar ``python3.X``
con la versión correcta de Python (por ejemplo ``python3.4``).

.. _virtualenv: http://www.virtualenv.org

Usando mod_wsgi en modo demonio
===============================

"Modo Demonio" es el modo recomendado para ejecutar mod_wsgi (en plataformas que
no son Windows). Para crear el grupo de procesos requeridos por el demonio y
delegar la instancia Django para ejecutarse, necesitas agregar apropiadamente
las directivas  ``WSGIDaemonProcess`` y  ``WSGIProcessGroup``. Un cambio mas
es requerido en la anterior configuración si utilizas el modo demonio no
puedes usar ``WSGIPythonPath``, en lugar de eso debes usar la opción
``python-path`` para ``WSGIDaemonProcess``, por ejemplo::

    WSGIDaemonProcess example.com python-path=/path/to/mysite.com:/path/to/venv/lib/python2.7/site-packages
    WSGIProcessGroup example.com

Puedes consultar `La documentación oficial de mode_wsgi`_ para más detalles.

.. _La documentación oficial de mode_wsgi: http://code.google.com/p/modwsgi/wiki/QuickConfigurationGuide#Delegation_To_Daemon_Process


Sirviendo archivos
==================

Django no debería ser utilizado para servir archivos multimedia (imágen, audio,
video, pdf) por sí mismo; mejor deja ese trabajo a un servidor Web especializado
en estas tareas.

Recomendamos usar un servidor Web separado (es decir, uno que no
está corriendo a la vez Django) para servir estos archivos. Estos son algunas
buenas opciones:

* lighttpd_
* Nginx_
* TUX_
* Una versión personalizada de Apache_
* Cherokee_

Sin embargo, si no tienes otra opción para servir los archivos multimedia, que
no sea el mismo ``VirtualHost`` Apache que usa Django, puedes configurar Apache
para que sirva algunas URLs estáticas y otras usando la interface mod_wsgi
para Django

Este ejemplo configura Django en la raíz del sitio, pero explícitamente sirve
``robots.txt``, ``favicon.ico``, y cualquier archivo CSS, y cualquier cosa en
el espacio de URL ``/static/`` y ``/media/`` será tratado como archivos
estáticos. Todas las demás URLs será servidas usando mod_wsgi:

.. code-block:: apache

    Alias /robots.txt /path/to/mysite.com/static/robots.txt
    Alias /favicon.ico /path/to/mysite.com/static/favicon.ico

    AliasMatch ^/([^/]*\.css) /path/to/mysite.com/static/styles/$1

    Alias /media/ /path/to/mysite.com/media/
    Alias /static/ /path/to/mysite.com/static/

    <Directory /path/to/mysite.com/static>
    Require all granted
    </Directory>

    <Directory /path/to/mysite.com/media>
    Require all granted
    </Directory>

    WSGIScriptAlias / /path/to/mysite.com/mysite/wsgi.py

    <Directory /path/to/mysite.com/mysite>
    <Files wsgi.py>
    Require all granted
    </Files>
    </Directory>

Si estas usando una versión de Apache anterior a la 2.4, remplaza
``Require all granted`` con ``Allow from all`` y tambien agrega la línea
``Order deny,allow`` arriba de esta.

.. _lighttpd: http://www.lighttpd.net/
.. _Nginx: http://wiki.nginx.org/Main
.. _TUX: http://en.wikipedia.org/wiki/TUX_web_server
.. _Apache: http://httpd.apache.org/
.. _Cherokee: http://www.cherokee-project.com/

Sirviendo los archivos de la interfaz administrativa
====================================================

Cuando ``django.contrib.staticfiles`` está en el archivo de configuraciones en
la variable ``INSTALLED_APPS`` El entorno de desarrollo de Django sirve
automáticamente los archivos estáticos de la interfaz administrativa (y de
cualquier aplicación instalada). Este no es el caso cuando usas otro servidor
para este trabajo. Tu eres responsable de configurar Apache o cualquier  otro
servidor Web que utilices, para servir los archivos de la interfaz
administrativa.

Los archivos de la interfaz administrativa se localizan en
``django/contrib/admin/static/admin``  en la distribucion de Django
Es *fuertemente* recomendable usar ``django.contrib.staticfiles`` para manejar
los archivos de la interfaz administrativa (Junto con el servidor Web, esto
significa que puedes usar el comando ``collectstatic`` para recolectar todos
los archivos estáticos en  ``STATIC_ROOT``  y luego configurar el servidor Web
para servir ``STATIC_ROOT``, pero aquí estan otras tres formas de hacer lo mismo:

1. Crea un enlace simbólico a los archivos estáticos de la interfaz
   administrativa desde la raíz de Apache (esto puede requerir usar
   ``+FollowSymLinks`` en la configuración de Apache)

2. Usa una directiva ``Alias``, como mostramos arriba, un alias apropiado a la
   URL (probablemente ``STATIC_URL`` + ``admin/``) a la posición  actual  de los
   archivos estáticos.

3. Copia los archivos estáticos de la interfaz administrativa de modo que
   se localicen dentro de la raíz de Apache.

Como usar Django con Gunicorn
===============================

Gunicorn_ ('Unicornio verde') es un servidor WSGI implementado en Python. No
tiene dependencias y es fácil de instalar y usar.

.. _Gunicorn: http://gunicorn.org/

Hay dos formas de usar Gunicorn con Django. La primera es tratar a Gunicorn
simplemente como otra aplicación WSGI. La segunda es usar Gunicorn de forma
especial `integrándolo con Django`_.

.. _integrándolo con Django: http://docs.gunicorn.org/en/latest/run.html#django-manage-py

Una vez instalado Gunicorn, tenemos disponible un comando ``gunicorn`` que
inicia el proceso del servidor Gunicorn.  Esto es tan simple, ya que gunicorn
solo necesita ser llamado con la localización del objeto ``aplication``
del WSGI.::

    gunicorn [OPTIONS] APP_MODULE

Donde ``APP_MODULE`` es un patron del tipo ``NOMBRE_MODULO:NOMBRE_VARIABLE_``.
El nombre del modulo debe ser la ruta completa al proyecto, mientras que el
nombre de la variable se refiere al llamable WSGI el cual debe de encontrarse
en el modo especificado.

Así para un típico proyecto Django, invocar a gunicorn se vería así::

    gunicorn misitio.wsgi:application

Donde ``misitio`` es el nombre del proyecto y ``application`` es el llamable
del WSGI.

(Esto requiere que el proyecto este en la ruta de búsqueda de Python;
la forma más simple de hacer esto, es asegurarse de ejecutar  el comando
"gunicorn" desde el mismo directorio en que esta el archivo ``manage.py``)

Gunicorn integrado a Django
===========================

.. admonition:: Nota:

    Es altamente recomendable simplemente ejecutar la aplicación con la interface
    WSGI usando el comando ``gunicorn``  descrito anteriormente.

Para usar Gunicorn integrado con Django, primero agrega ``"gunicorn"`` a tus
aplicaciones instaladas, en la variable  ``INSTALLED_APPS``. Luego ejecuta el
comando ``python manage.py run_gunicorn``

Este ofrece algunas sutiles opciones  específicas para Django.

* Fija el nombre del proceso de gunicorn para ser el del proyecto

* Valida los modelos instalados

* Permite agregar una opción ``--adminmedia`` para pasarle la localización de
  los archivos media  de la interfaz administrativa.

Puedes consultar la documentación oficial para encontrar consejos adicionales
sobre cómo empezar a usar y mantener un servidor `Gunicorn`_.

Como usar Django con uWSGI
==========================

`uWSGI`_  es un servidor rápido codificado en C, autoregenerable y desarrollado
como una aplicación amigable para los administradores de sistemas.

.. _uWSGI: http://projects.unbit.it/uwsgi/

Prerrequisitos: uWSGI
=====================

La wiki de WSGI describe algunos `método de instalación`_. Usando pip, el
manejador de paquetes python puedes instalar cualquier versión de uWSGI con un
simple comando. Por ejemplo:

.. code-block:: bash

    # Instala la actual versión estable.
    sudo pip install uwsgi

    # O installa la LTS (Soporte a largo plazo).
    sudo pip install http://projects.unbit.it/downloads/uwsgi-lts.tar.gz

.. _método de instalación: http://uwsgi-docs.readthedocs.org/en/latest/Install.html

.. warning::

    Algunas distribuciones, incluidas Debían y Ubuntu, incluyen versiones
    antiguas de uWSGI que no cumplen las especificaciones WSGI. Versiones
    anteriores a la 1.2.6 no llaman a ``close`` en el objeto de repuesta
    después de manejar una petición. En estos casos
    ``django.core.signals.request_finished`` no envía las señales. Esto
    puede dar lugar a conexiones lentas a los servidores de la base de datos y
    memcache.

uWSGI model
-----------

uWSGI opera en un modelo cliente-servidor. El servidor web (por ejemplo
nginx, Apache) se comunicacn con un proceso del "trabajo" django-uwsgi para
servir dinámicamente el contexto. Consulta la `documentación a fondo`_ de uWSGI's
para obtener más detalles.

.. _documentación a fondo: http://projects.unbit.it/uwsgi/wiki/Background

Configurar e iniciar el servidor uWSGI
--------------------------------------

uWSGI soporta múltiples formas para configurar el proceso. Puede iniciar
mediante un comando o leyendo un archivo de configuraciones de inicio. Puedes
consultar más `ejemplos`_ y la documentación de `configuraciones`_ para obtener
detalles mas específicos.

.. _configuraciones: https://uwsgi.readthedocs.org/en/latest/Configuration.html
.. _ejemplos: http://projects.unbit.it/uwsgi/wiki/Example

Este es un ejemplo de un comando para iniciar el servidor uWSGI:

.. code-block:: bash

    uwsgi --chdir=/path/to/your/project \
        --module=misitio.wsgi:application \
        --env DJANGO_SETTINGS_MODULE=misitio.settings \
        --master --pidfile=/tmp/project-master.pid \
        --socket=127.0.0.1:49152 \      # can also be a file
        --processes=5 \                 # number of worker processes
        --uid=1000 --gid=2000 \         # if root, uwsgi can drop privileges
        --harakiri=20 \                 # respawn processes taking more than 20 seconds
        --max-requests=5000 \           # respawn processes after serving 5000 requests
        --vacuum \                      # clear environment on exit
        --home=/path/to/virtual/env \   # optional path to a virtualenv
        --daemonize=/var/log/uwsgi/yourproject.log      # background the process


Este asume que estas situado en el nivel superior de un paquete llamado
``misitio`` y dentro del existe un modulo wsgi.py, que contienen un objeto
``application`` WSGI. No deberías tener ningún problema si ejecutaste el comando
``django-admin.py startproject misitio``, ya que este se encarga de crear la
estructura del proyecto por default. Si este archivo no existe necesitas
crearlo.

Las opciones especificas de Django son:

* ``chdir``:  La ruta al directorio, que necesita estar en la ruta de importacion
  de Python. -- es decir el directorio que contiene el paquete ``misitio``

* ``module``: El modulo WSGI para usar --probablemente  el modulo ``misitio.wsgi``
  que ``startproject`` creo.

* ``env``: Debe contener por lo menos ``DJANGO_SETTINGS_MODULE``.

* ``home``: Opcionalmente la ruta al proyecto, si estas usando virtualenv.

Ejemplo de un archivo de configuración ini:

.. code-block:: bash

    [uwsgi]
    chdir=/path/to/your/project
    module=misitio.wsgi:application
    master=True
    pidfile=/tmp/project-master.pid
    vacuum=True
    max-requests=5000
    daemonize=/var/log/uwsgi/yourproject.log

Ejemplo del uso de un archivo de configuración ini::

    uwsgi --ini uwsgi.ini

Consulta el `manejo de procesos uWSGI`_  para más información sobre iniciar,
detener y recargar los procesos del servidor uWSGI.

.. _manejo de procesos uWSGI: http://uwsgi-docs.readthedocs.org/en/latest/Management.html

Lighttpd
========

`lighttpd`_ es un servidor Web liviano usado habitualmente para servir archivos
estáticos. Admite FastCGI en forma nativa y por lo tanto es también una opción
ideal para servir tanto páginas estáticas como dinámicas, si tu sitio no tiene
necesidades específicas de Apache.

.. _lighttpd: http://www.lighttpd.net/

Asegúrate que ``mod_fastcgi`` está en tu lista de módulos, en algún lugar
después de ``mod_rewrite`` y ``mod_access``, pero no antes de ``mod_accesslog``.
Probablemente desees también ``mod_alias``, para servir los archivos media de
la interfaz administrativa.

Agrega lo siguiente a tu archivo de configuración de lighttpd:

.. code-block:: lua

    server.document-root = "/home/user/public_html"
    fastcgi.server = (
        "/mysite.fcgi" => (
            "main" => (
                # Use host / port instead of socket for TCP fastcgi
                # "host" => "127.0.0.1",
                # "port" => 3033,
                "socket" => "/home/user/mysite.sock",
                "check-local" => "disable",
            )
        ),
    )
    alias.url = (
        "/media" => "/home/user/django/contrib/admin/media/",
    )

    url.rewrite-once = (
        "^(/media.*)$" => "$1",
        "^/favicon\.ico$" => "/media/favicon.ico",
        "^(/.*)$" => "/mysite.fcgi$1",
    )

Ejecutando Múltiples Sitios Django en Una Instancia lighttpd
-------------------------------------------------------------

lighttpd te permite usar “configuración condicional” para permitir la
configuración personalizada para cada host. Para especificar múltiples sitios
FastCGI, solo agrega un bloque condicional en torno a tu configuración
FastCGI para cada sitio:

.. code-block:: bash

    # If the hostname is 'www.example1.com'...
    $HTTP["host"] == "www.example1.com" {
        server.document-root = "/foo/site1"
        fastcgi.server = (
           ...
        )
        ...
    }

    # If the hostname is 'www.example2.com'...
    $HTTP["host"] == "www.example2.com" {
        server.document-root = "/foo/site2"
        fastcgi.server = (
           ...
        )
        ...
    }

Puedes también ejecutar múltiples instalaciones de Django en el mismo sitio
simplemente especificando múltiples entradas en la directiva fastcgi.server.
Agrega un host FastCGI para cada una.

Escalamiento
============

Ahora que sabes cómo tener a Django ejecutando en un servidor simple, veamos
como puedes escalar una instalación Django. Esta sección explica cómo puede
escalar un sitio desde un servidor único a un clúster de gran escala que
pueda servir millones de hits por hora.

Es importante notar, sin embargo, que cada sitio grande es grande de diferentes
formas, por lo que escalar es cualquier cosa menos una operación de una solución
única para todos los casos. La siguiente cobertura debe ser suficiente para
mostrar el principio general, y cuando sea posible, trataremos de señalar donde
se puedan elegir distintas opciones.

Primero, haremos una buena presuposición, y hablaremos exclusivamente acerca de
escalamiento bajo Apache y wsgi. A pesar de que conocemos vario casos exitosos
de desarrollos FastCGI y mod_python  medios y grandes, estamos mucho más
familiarizados con Apache.

Ejecutando en un Servidor Único
-------------------------------

La mayoría de los sitios Web, empiezan ejecutándose en un servidor único, con
una arquitectura parecida a la de la Figura 12-1.


.. figure:: graphics/chapter12/scaling-1.png

   Figure 12-1: Ejecutando únicamente un servidor.

Esto funciona bien para sitios pequeños y medianos, y es relativamente barato
– puedes instalar un servidor único diseñado para Django por menos de 3,000 dólares.

Sin embargo, a medida que el tráfico se incremente, caerás rápidamente en
*contención de recursos* entre las diferentes piezas de software. Los
servidores de base de datos y los servidores Web *adoran* tener el servidor
entero para ellos, y cuando corren en el mismo servidor siempre terminan
“peleando” por los mismos recursos (RAM, CPU) que prefieren monopolizar.

Esto se resuelve fácilmente moviendo el servidor de base de datos a una segunda
máquina, como se explica en la siguiente sección.

Separando el Servidor de Bases de Datos
----------------------------------------

En lo que tiene que ver con Django, el proceso de separar el servidor de bases
de datos es extremadamente sencillo: simplemente necesitas cambiar la
configuración de ``DATABASE_HOST`` a la IP o nombre DNS de tu servidor.
Probablemente sea una buena idea usar la IP si es posible, ya que depender de
la DNS para la conexión entre el servidor Web y el servidor de bases de datos
no se recomienda.

Con un servidor de base de datos separado, nuestra arquitectura ahora se ve
como en la Figura 12-2.

.. figure:: graphics/chapter12/scaling-2.png

   Figure 12-2: Moviendo la base de datos a un servidor dedicado.

Aquí es donde empezamos a movernos hacia lo que usualmente se llama una
arquitectura *n-tier*. No te asustes por la terminología – sólo se refiere al
hecho de que diferentes “tiers” de la pila Web separadas en diferentes máquinas
físicas.

A esta altura, si anticipas que en algún momento vas a necesitar crecer más
allá de un servidor de base de datos único, probablemente sea una buena idea
empezar a pensar en pooling de conexiones y/o replicación de bases de datos.
Desafortunadamente, no hay suficiente espacio para hacerle justicia a estos
temas en este libro, así que vas a necesitar consultar la documentación y/o a
la comunidad de tu base de datos para más información.

Ejecutando un Servidor de Medios Separado
-----------------------------------------

Aún tenemos un gran problema por delante,  usando únicamente un servidor: servir
los archivos media  desde la misma caja que maneja el contenido dinámico.

Estas dos actividades tienen su mejor performance bajo distintas circunstancias,
y encerrándolas en la misma caja terminarás con que ninguna de las dos tendrá
un buen rendimiento. Así que el siguiente paso es separar los medios – esto es,
todo lo que *no* es generado por una vista de Django – a un servidor dedicado
(ver Figura 12-3).

.. figure:: graphics/chapter12/scaling-3.png

   Figure 12-3: Separando el servidor de medios.

Idealmente, este servidor de medios debería ejecutarse en un servidor Web,
optimizado para la entrega de medios estáticos. lighttpd y tux
(http://www.djangoproject.com/r/tux/) son dos excelentes elecciones aquí, pero
un servidor Apache bien ‘personalizado’ también puede funcionar.

Para sitios pesados en contenidos estáticos (fotos, videos, etc.), moverse a
un servidor de medios separado es doblemente importante y debería ser el *primer*
paso en el escalamiento hacia arriba.

De todos modos, este paso puede ser un poco delicado. Si tu aplicación
necesita subir archivos Django necesita poder escribir sobre los medios
‘subidos’ en el servidor de medios.  (la configuración de MEDIA_ROOT controla
donde  escriben estos medios). Si un medio habita en otro servidor, de todas
formas necesitas organizar una forma de que esa escritura se pueda hacer a
través de la red.

Implementando Balance de Carga y Redundancia
--------------------------------------------

A esta altura, ya hemos separado las cosas todo lo posible. Esta configuración
de tres servers debería manejar una cantidad muy grande de tráfico – nosotros
servimos alrededor de 10 millones de hits por día con una arquitectura de este
tipo– así que si creces más allá, necesitarás empezar a agregar redundancia.

En realidad, esto es algo bueno. Una mirada a la Figura 20-3 te permitirá ver
que si falla aunque sea uno solo de los servidores, el sitio entero se cae.
Así que a medida que agregas servidores redundantes, no sólo incrementas
capacidad, sino también confiabilidad.

Para este ejemplo, asumamos que el primero que se ve superado en capacidad es
el servidor Web. Es fácil tener múltiples copias de un sitio Django ejecutando
en diferente hardware. – simplemente copia el código en varias máquinas, e
inicia Apache en cada una de ellas.

Sin embargo, necesitas otra pieza de software para distribuir el tráfico entre
los servidores: un balanceador de carga. Puedes comprar balanceadores de carga
por hardware caros y propietarios, pero existen algunos balanceadores de carga
por software de alta calidad que son open source.

mod_proxy de Apache es una opción, pero hemos encontrado que Perlbal
(http://www.djangoproject.com/r/perlbal/) es simplemente fantástico.
Es un balanceador de carga y proxy inverso escrito por las mismas personas que
escribieron memcached.

Con los servidores Web en cluster, nuestra arquitectura en evolución empieza a
verse más compleja, como se ve en la Figura 12-4.

.. figure:: graphics/chapter12/scaling-4.png

   Figure 12-4: Configuración de un server redundante con balance de carga.

Observar que en el diagrama nos referimos a los servidores Web como “el cluster”
para indicar que el numero de servidores básicamente es variable. Una vez que
tienes un balanceador de carga en el frente, puedes agregar y eliminar
servidores Web back-end sin perder un segundo fuera de servicio.

Vamos a lo grande
-----------------

En este punto, los siguientes pasos son derivaciones del último:

* A medida que necesites más performance en la base de datos, necesitarás
  agregar servidores de base de datos replicados. MySQL tiene replicación
  incorporada; los usuarios de PostgreSQL deberían mirar a Slony
  (http://www.djangoproject.com/r/slony/) y pgpool
  (http://www.djangoproject.com/r/pgpool/) para replicación y pooling de
  conexiones, respectivamente.

* Si un solo balanceador de carga no es suficiente, puedes agregar más
  máquinas balanceadoras de carga y distribuir entre ellas usando DNS
  round-robin.

* Si un servidor único de medios no es suficiente, puedes agregar más servidores
  de medios y distribuir la carga con tu cluster de balanceadores de carga.

* Si necesitas más almacenamiento cache, puedes agregar servidores de cache dedicados.

* En cualquier etapa, si un cluster no tiene buena performance, puedes
  agregar más servidores al cluster.

Después de algunas de estas iteraciones, una arquitectura de gran escala debe
verse como en la Figura 12-5

.. figure:: graphics/chapter12/scaling-5.png

   Figure 12-5. Un ejemplo de configuración de Django de gran escala.

A pesar de que mostramos solo dos o tres servidores en cada nivel, no hay un
límite fundamental a cuantos puedes agregar.

Ajuste de Performance
---------------------

Si tienes grandes cantidades de dinero, simplemente puedes irle arrojando
hardware a los problemas de escalado. Para el resto de nosotros, sin embargo,
el ajuste de performance es una obligación.

.. admonition:: Nota:

   Incidentalmente, si alguien con monstruosas cantidades de dinero está
   leyendo este libro, por favor considere una donación sustancial al
   proyecto Django. Aceptamos diamantes en bruto y lingotes de oro.

Desafortunadamente, el ajuste de performance es más un arte que una ciencia,
y es aun más difícil de escribir sobre eso que sobre escalamiento. Si estás
pensando seriamente en desplegar una aplicación Django de gran escala,
deberás pasar un buen tiempo aprendiendo como ajustar cada pieza de tu stack.

Las siguientes secciones, sin embargo, presentan algunos tips específicos del
ajuste de performance de Django que hemos descubierto a través de los años.

No hay tal cosa como demasí ada RAM
-----------------------------------

Incluso la RAM más costosa es relativamente costeable en estos días. Compra
toda la RAM que puedas, y después compra un poco más.

Los procesadores más rápidos no mejoran la performance tanto. La mayoría de los
servidores Web desperdician el 90% de su tiempo esperando I/O del disco. En
cuanto empieces a swappear, la performance directamente se muere. Los discos
más rápidos pueden ayudar levemente, pero son mucho más caros que la RAM,
así que no cuentan.

Si tienes varios servidores, el primer lugar donde poner tu RAM es en el
servidor de base de datos. Si puedes, compra suficiente ram como para tener
toda tu base de datos en memoria. Esto no es tan difícil. Hemos diseñado
sitios que incluye medio millón de artículos en menos de menos de 2 GB de
espacio.

Después, maximiza la RAM de tu servidor Web. La situación ideal es aquella en
la que ningún servidor swapea – nunca. Si llegas a ese punto, debes poder
manejar la mayor parte del tráfico normal.

Deshabilita Keep-Alive
----------------------

``Keep-Alive`` es una característica de HTTP que permite que múltiples pedidos
HTTP sean servidos sobre una conexión TCP única, evitando la sobrecarga de
conectar y desconectar.

Esto parece bueno a primera vista, pero puede asesinar al performance de un
sitio Django. Si estás sirviendo medios desde un servidor separado, cada
usuario que esté navegando tu sitio solo requerirá una página del servidor
Django cada diez segundos aproximadamente. Esto deja a los servidores HTTP
esperando el siguiente pedido keep-alive, y un servidor HTTP ocioso consume
RAM que debería estar usando un servidor activo.

Usa memcached
-------------

A pesar de que Django admite varios back-ends de cache diferentes, ninguno de
ellos siquiera se acerca a ser tan rápido como memcached. Si tienes un sitio
con tráfico alto, ni pierdas tiempo con los otros –- usa directamente memcached.

Usa memcached siempre
---------------------

Por supuesto, seleccionar memcached no te hace mejor si no lo usas realmente.
EL :doc:`capítulo  <chapter15>` te dice como usarlo: aprende a usar el framework
de cache de Django, y úsalo en todas las partes que te sea posible. Un uso de
cache agresivo y preemptico es usualmente lo único que se puede hacer para
mantener un sitio Web funcionando bajo el mayor tráfico.


Únete a la Conversación
-----------------------

Cada pieza del stack de Django – desde Linux a Apache a PostgreSQL o MySQL –
tiene una comunidad maravillosa detrás. Si realmente quieres obtener ese último
1% de tus servidores, únete a las comunidades open source que están detrás de
tu software y pide ayuda. La mayoría de los miembros de la comunidad del
software libre estarán felices de ayudar.

Y también asegúrate de unirte a la comunidad Django. Tus humildes autores son
solo dos miembros de un grupo increíblemente activo y creciente de
desarrolladores Django. Nuestra comunidad tiene una enorme cantidad de
experiencia colectiva para ofrecer.

¿Qué sigue?
===========

El resto de los capítulos se enfocan en otras  características de Django, que
puedes o no necesitar, dependiendo de tus aplicaciones. Siéntete libre de
leerlos en el orden que prefieras.

