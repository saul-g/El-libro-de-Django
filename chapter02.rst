=====================
Capítulo 2: Empezando
=====================

Creemos que es mejor empezar con fuerza. En los capítulos que le
siguen a este descubrirás los detalles y el alcance del framework Django,
pero por ahora, confía en nosotros, este capítulo es divertido.

Instalar Django es fácil. Django se puede usar en cualquier sistema que
corra Python, por eso es posible instalarlo de varias maneras. En
este capítulo explicamos las situaciones más comunes de instalación de Django.
El :doc:`Capítulo 20<chapter20>` explica cómo utilizar Django en producción.

Instalar Python
===============

Django está escrito 100% en puro código Python, así que necesitarás
instalar Python en tu computadora. Django necesita Python 2.3 o superior.

Si estás usando Linux o Mac OS X probablemente ya tienes Python instalado.
Escribe ``python`` en una terminal. Si ves algo así, Python está instalado::

    Python 2.6.6 (r266:84292, Sep 15 2010, 15:52:39) 
    [GCC 4.4.5] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 


Si ves un error como: ``"command not found"`` u ``"orden no encontrada"``,
tienes que bajar e instalar Python. Fíjate en http://www.python.org/download/
para empezar. La instalación es rápida y fácil.

Instalar Django
===============

En esta sección explicamos dos opciones de instalación: instalar un
lanzamiento oficial e instalar desde Subversion.

Instalar un lanzamiento oficial
----------------------------------

La mayoría de la gente querrá instalar el lanzamiento oficial más reciente
de http://www.djangoproject.com/download/. Django usa el método ``distutils``
estándar de instalación de Python, que en el mundo de Linux es así:

   #. Baja el tarball, que se llamará algo así como *Django-version.tar.gz*

   #. ``tar xzvf Django-*.tar.gz``

   #. ``cd Django-*``

   #. ``sudo python setup.py install``

En Windows, recomendamos usar 7-Zip para manejar archivos comprimidos de todo
tipo, incluyendo ``.tar.gz``. Puedes bajar 7-Zip de http://www.djangoproject.com/r/7zip/.

Cambia a algún otro directorio e inicia ``python``. Si todo está funcionando
bien, deberías poder importar el módulo ``django``::

    >>> import django
    >>> django.VERSION
    (TU VERSION)

.. nota::

    El intérprete interactivo de Python es un programa de línea de comandos que
    te permite escribir un programa Python de forma interactiva. Para iniciarlo
    sólo ejecuta el comando ``python`` en la línea de comandos. Durante
    todo este libro, mostraremos ejemplos de código Python como si estuviesen
    escritos en el intérprete interactivo. El triple signo de *mayor que* (``>>>``)
    es el prompt de Python.

Instalar Django desde Subversion
--------------------------------

Si quieres trabajar sobre la versión de desarrollo, o si quieres contribuir con
el código de Django en sí mismo, deberías instalar Django desde el repositorio
de Subversion.

Subversion es libre, es un sistema de control de versiones de código abierto
similar a CVS, y es el que el equipo de Django utiliza para administrar cambios
en el código base de Django. Puedes utilizar un cliente de Subversion para
hacerte con el código fuente más actual de Django y, en cualquier momento,
puedes actualizar tu copia local del código de Django, conocido como un
*checkout local*, para obtener los últimos cambios y mejoras hechas por los
desarrolladores de Django.

Al último código de desarrollo de Django se hace referencia como el *trunk*.
El equipo de Django ejecuta sitios de producción sobre el trunk y procura
permanecer estable.

Para obtener el trunk de Django, sigue los siguientes pasos:

    #. Asegúrate de tener un cliente de Subversion instalado. Puedes conseguir
       este programa libremente desde http://subversion.tigris.org/, y puedes
       encontrar documentación excelente en http://svnbook.red-bean.com/.

    #. Haz un check out del trunk usando el comando ``svn co
       http://code.djangoproject.com/svn/django/trunk djtrunk``.

    #. Crea ``site-packages/django.pth`` y agrega el directorio ``djtrunk``
       a este, o actualiza tu ``PYTHONPATH`` agregando ``djtrunk``.

    #. Incluye ``djtrunk/django/bin`` en el PATH de tu sistema. Este directorio
       incluye utilidades de administración como ``django-admin.py``.

.. exhortacion:: Consejo:

    Si los archivo ``.pth`` son nuevos para ti, puedes aprender más de ellos en
    http://www.djangoproject.com/r/python/site-module/.

Luego de descargarlo desde Subversion y haber seguido los pasos anteriores, no
necesitas ejecutar ``python setup.py install`` --¡Acabas de hacer este trabajo a
mano!

Debido a que el trunk de Django cambia a menudo corrigiendo bugs y
agregando funcionalidades, probablemente quieras actualizarlo con
frecuencia -- a cada hora, si eres un obsesivo. Para actualizar el código,
solo ejecuta el comando ``svn update`` desde el directorio ``djtrunk``. Cuando
ejecutes este comando, Subversion contactará http://code.djangoproject.com,
determinará si el código ha cambiado, y actualizará tu versión local del
código con cualquier cambio que se haya hecho desde la última actualización.
Es muy bueno.

Configurar la base de datos
===========================

El único prerequisito de Django es una instalación funcionando de Python. Sin
embargo, este libro se centra en una de las mejores funcionalidades de
Django, el desarrollo de sitios web *con soporte de base de datos*, para esto
necesitarás instalar un servidor de base de datos de algún tipo, para almacenar
tus datos.

Si sólo quieres comenzar a jugar con Django, salta a la sección 
:doc:`Capítulo 20<chapter20>` -- pero créenos, querrás instalar
una base de datos finalmente.Todos los ejemplos de este libro asumen
que tienes una base de datos configurada.

Hasta el momento de escribir esto, Django admite tres motores de base de
datos:

    * PostgreSQL (http://www.postgresql.org/)
    * SQLite 3 (http://www.sqlite.org/)
    * MySQL (http://www.mysql.com/)

Se está trabajando para admitir Microsoft SQL Server y Oracle. El sitio
web de Django siempre contendrá la última información acerca de las base de
datos admitidas.

A nosotros el que más nos gusta es PostgreSQL, por razones que exceden el
alcance de este libro, por eso lo mencionamos primero. Sin embargo, todos
los motores que listamos aquí trabajan bien con Django.

SQLite merece especial atención como herramienta de desarrollo. Es un motor de
base de datos extremadamente simple y no requiere ningún tipo de instalación y
configuración del servidor. Es por lejos el más fácil de configurar si sólo
quieres jugar con Django, y viene incluido en la biblioteca estándar de Python
2.5.

En Windows, obtener los drivers binarios de la base de datos es a veces un
proceso complicado. Ya que sólo estás iniciándote con Django, recomendamos usar
Python 2.5 y el soporte incluido para SQLite. La compilación de drivers
puede ser estresante.

Usar Django con PostgreSQL
--------------------------

Si estás utilizando PostgreSQL, necesitarás el paquete ``psycopg`` disponible
en http://www.djangoproject.com/r/python-pgsql/. Toma nota de la versión que
estás usando (1 ó 2); necesitarás esta información luego.

Si estás usando PostgresSQL en Windows, puedes encontrar los binarios
precompilados de ``psycopg`` en http://www.djangoproject.com/r/python-pgsql/windows/.

Usar Django con SQLite 3
------------------------

Si estás usando una versión de Python igual o posterior a 2.5, ya tienes
SQLite. Si estás trabajando con Python 2.4 o menor, necesitas SQLite 3 --no la
versión 2-- desde http://www.djangoproject.com/r/sqlite/ y el paquete
``pysqlite`` desde http://www.djangoproject.com/r/python-sqlite/. Asegúrate de
tener ``pysqlite`` en una versión 2.0.3 o superior.

En Windows, puedes omitir la instalación separada de los binarios de SQLite,
ya que están enlazados dentro de los binarios de ``pysqlite``.

Usar Django con MySQL
---------------------

Django requiere MySQL 4.0 o superior; la versión 3.x no admite subconsultas
anidadas ni algunas otras sentencias SQL perfectamente estándar. También
necesitas instalar el paquete ``MySQLdb`` desde
http://www.djangoproject.com/r/python-mysql/.

Usar Django sin una base de datos
---------------------------------

Como mencionamos anteriormente, Django actualmente no requiere una base de
datos. Si sólo quieres usar este como un servidor dinámico de páginas que no
use una base de datos, está perfectamente bien.

Con esto dicho, ten en cuenta que algunas de las herramientas extras de Django
*requieren* una base de datos, por lo tanto si eliges no usar una base de
datos, perderás estas utilidades. (Señalaremos estas utilidades a lo largo del
libro).

Comenzar un proyecto
====================

.. The below (down to "The rest of this section") is adapted from "Initial
.. setup" in tutorial01.txt.

Un *proyecto* es una colección de configuraciones para una instancia de Django,
incluyendo configuración de base de datos, opciones específicas de Django y
configuraciones específicas de aplicaciones.

Si esta es la primera vez que usas Django, tendrás que tener cuidado de algunas
configuraciones iniciales. Crea un nuevo directorio para empezar a trabajar,
por ejemplo algo como ``/home/username/djcode/``, e ingresa a este directorio.

.. nota::

    ``django-admin.py`` debería estar en el PATH de tu sistema si instalaste
    Django con la utilidad ``setup.py``. Si hiciste un check out desde
    Subversion, puedes encontrarlo en ``djtrunk/django/bin``. Como vas a
    utilizar con frecuencia ``django-admin.py``, considera agregarlo a tu PATH.
    En Unix, puedes hacer un link simbólico de ``/usr/local/bin``, usando un
    comando como ``sudo ln -s
    /path/to/django/bin/django-admin.py /usr/local/bin/django-admin.py``. En
    Windows, necesitarás actualizar tu variable de entorno ``PATH`` .

Ejecuta el comando ``django-admin.py startproject mysite`` para crear el
directorio ``mysite`` en el directorio actual.

Echemos un vistazo a lo que ``startproject`` creó::

    mysite/
           manage.py
           mysite/
               __init__.py
               settings.py
               urls.py
               wsgi.py
	    
.. admonition:: ¿ No es lo mismo que ves ?	
 
     Si estamos viendo un arbol de directorios diferentes al anterior
     problablemente estamos usando una version de Django anterior.

Estos archivos son los siguientes:

* :file:`mysite/`:  El Directorio que contiene nuestro projecto. Podemos cambiarle el 
  nombre en cualquier momento sin afectar nuestro proyecto.
      
* :file:`manage.py`: Una utilidad de línea de comandos que te deja interactuar
  con este proyecto de Django de varias formas.
      
* :file:`mysite/mysite/`:El directorio de nuestro paquete que contiene nuestro projecto
  el cual es un paquete python  y el que se usara para importar cualquier cosa dentro
  de el.       
       
* :file:`mysite/__init__.py`: Un archivo requerido para que Python trate a este
  directorio como un paquete (i.e. un grupo de módulos).

* :file:`mysite/settings.py`: Opciones/configuraciones para este proyecto de Django.

* :file:`mysite/urls.py`: La declaración de las URL para este proyecto de Django; una
  "tabla de contenidos" de tu sitio hecho con Django.
      
* :file:`mysite/wsgi.py`: El archivo encargado de ser compatible con el  servidor
  web.

.. exhortacion:: ¿Dónde debería estar este directorio?

    Si vienes de PHP, probablemente pondrías el código debajo de la carpeta raíz
    del servidor web (en lugares como ``/var/www``). Con Django, no tienes que
    hacer esto. No es una buena idea poner cualquier código Python en la
    carpeta raíz del servidor web, porque al hacerlo se arriesga a que la
    gente sea capaz de ver el código en la web. Esto no es bueno para la
    seguridad.

    Pon tu código en algún directorio **fuera** de la carpeta raíz.

El servidor de desarrollo
-------------------------

Django incluye un servidor web ligero que puedes usar mientras estás
desarrollando tu sitio. Incluimos este servidor para que puedas desarrollar tu
sitio rápidamente, sin tener que lidiar con configuraciones de servidores web
de producción (i.e., Apache) hasta que estés listo para la producción. Este
servidor de desarrollo vigila tu código a la espera de cambios y se reinicia
automáticamente, ayudándote a hacer algunos cambios rápidos en tu proyecto sin
necesidad de reiniciar nada.

Entra en el directorio ``mysite``, si aún no lo has hecho, y ejecuta el
comando ``python manage.py runserver``. Verás algo parecido a esto::

    Validating models...
    0 errors found.

    Django version 1.0, using settings 'mysite.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Aunque el servidor de desarrollo es extremadamente útil para, bueno,
desarrollar, resiste la tentación de usar este servidor en cualquier entorno
parecido a producción. El servidor de desarrollo puede manejar fiablemente una
sola petición a la vez, y no ha pasado por una auditoría de seguridad de ningún
tipo. Cuando sea el momento de lanzar tu sitio, mira el :doc:`Capítulo 20<chapter20>` para
información sobre cómo hacerlo con Django.

.. exhortacion:: Cambiar el host o el puerto

    Por defecto, el comando ``runserver`` inicia el servidor de desarrollo en
    el puerto 8000, escuchando sólo conexiones locales. Si quieres cambiar el
    puerto del servidor, pasa este como un argumento de línea de comandos::

        python manage.py runserver 8080

    También puedes cambiar las direcciones de IP que escucha el servidor. Esto
    es utilizado especialmente si quieres compartir el desarrollo de un sitio
    con otros desarrolladores. Lo siguiente::

        python manage.py runserver 0.0.0.0:8080

    hará que Django escuche sobre cualquier interfaz de red, permitiendo que
    los demás equipos puedan conectarse al servidor de desarrollo.

Ahora que el servidor está corriendo, visita http://127.0.0.1:8000/ con tu
navegador web. Verás una página de "Bienvenido a Django" sombreada con un azul
pastel agradable. ¡Funciona!

    .. image:: graficos/chapter02/it-worked.png
        :alt: "Bienvenido a Django" 

¿Qué sigue?
===========

Ahora que tienes todo instalado y el servidor de desarrollo corriendo, en el  :doc:`próximo capítulo<chapter03>` escribirás algo de código básico que muestra cómo servir
páginas Web usando Django.


