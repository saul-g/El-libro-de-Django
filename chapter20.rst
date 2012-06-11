======================================================
Capítulo 20: Puesta en marcha de Django en un servidor
======================================================

A lo largo de este libro, hemos mencionado algunos objetivos que conducen el
desarrollo de Django. Facilidad de uso, amigabilidad para nuevos programadores,
abstracción de tareas repetitivas -- todos esas metas marcaron el camino de los
desarrolladores.

Sin embargo, desde la concepción de Django, ha existido siempre otro objetivo
importante: Django debería ser fácil de implementar, y debería poder servir
una gran cantidad de tráfico con recursos limitados.

Las motivaciones para este objetivo se vuelven evidentes cuando observas el
trasfondo de Django: un pequeño periódico en Kansas difícilmente pueda costear
hardware de servidor de última tecnología, por lo que los desarrolladores
originales de Django trataron de extraer el máximo desempeño posible de los
escasos recursos disponibles. De hecho, por años los desarrolladores de Django
actuaron como sus propios administradores de sistema -- ya que simplemente no
había suficiente harware como para *necesitar* administradores dedicados a esa
tarea -- incluso manejando sitios con decenas de millones de entradas por día.

Como Django se volvió un proyecto open source, este enfoque en el desempeño y
la facilidad de implementación se tornó importante por diferentes razones: los
desarrolladores aficionados tienen los mismos requerimientos. Los individuos
que quieren usar Django están encantados de saber que pueden hospedar un sitio
con tráfico entre pequeño y mediano por menos de u$s 10 mensuales.

Pero ser capaz de escalar hacia abajo es solamente la mitad de la batalla. Django
también debe ser capaz de escalar *hacia arriba* para conocer las necesidades de
grandes empresas y corporaciones. Aquí, Django adopta una filosofía común entre
los grupos de software del tipo LAMP que suele llamarse *shared nothing* (nada
compartido).

.. admonition:: ¿Qué es LAMP?

    El acrónimo LAMP fue originalmente acuñado para describir un conjunto de
    software open source utilizado para propulsar muchos sitios web:

        * Linux (sistema operativo)
        * Apache (servidor web)
        * MySQL (base de datos)
        * PHP (lenguaje de programación)

    A lo largo del tiempo, el acrónimo se ha vuelto más una referencia a la
    filosofía de este tipo de agrupamiento de software que a cualquiera de estos
    en particular. Por ello, aunque Django usa Python y es *agnóstico* respecto al
    motor de base de datos a utilizar, las filosofías probadas por los agrupamientos
    tipo LAMP permanece en la mentalidad de implementación de Django.

    Han habido algunos (más que nada cómicos) intentos de acuñar acrónimos
    similares para describir los agrupamientos de tecnología que usa Django. Los
    autores de este libro están encariñados con LAPD (Linux, Apache, PostgreSQL,
    y Django) o PAID (PostgreSQL, Apache, Internet, y Django). Usa Django y
    consigue un PAID! (N. de T.: En inglés, PAID significa *pago*).


Nada Compartido
===============

Esencialmente, la filosofía *shared nothing* se trata de el acoplamiento débil
aplicado a todo el conjunto de software utilizado. Esta arquitectura se presentó
como respuesta directa a la que en su momento prevalecía: una aplicación de
servidor web monolítica que encapsulaba el lenguaje, la base de datos y el
servidor web -- e incluso partes del sistema operativo -- un único proceso (por
ejemplo, Java).

Cuando llega el momento de escalar, esto puede ser un problema serio; es casi
imposible separar el trabajo de un proceso monolítico entre muchas maquinas
físicas diferentes, por lo que las aplicaciones monolíticas requieren servidores
enormemente potentes. Estos servidores, por supuesto, cuestan decenas o a veces
centenas de miles de dolares, dejando a los sitios web de gran escala lejos del
alcance de individuos o pequeñas compañías con buenas ideas pero sin efectivo.

No obstante, lo que la comunidad LAMP descubrió fue que si se separa cada pieza
de esa pila de software Web en componentes individuales, se podría fácilmente
comenzar con un servidor barato y simplemente ir agregando más servidores
baratos a medida que se crece. Si un servidor de base de datos de u$s3000 ya no
puede manejar la carga, sencillamente se compraría un segundo (o un tercero, o
un cuarto) hasta que pueda. Si se necesita más capacidad de almacenamiento,
se agregaría un servidor NFS.

Aunque para que esto funcione, las aplicaciones Web deben dejar de asumir que
el mismo servidor es el que maneja cada petición -- o incluso las distintas
partes de una petición. En una implementación LAMP (y Django) de gran escala,
¡más de media docena de servidores pueden estar involucrados en servir una sola
petición! Las repercusiones a esta situación son numerosas, pero pueden reducirse
a estos puntos:

    * *El estado no puede ser guardado localmente*. En otras palabras, cualquier
      dato que deba estar disponible entre múltiples solicitudes, debe almacenarse
      en algún tipo de almacenamiento permanente como la base de datos o una
      caché centralizada.


    * *El software no puede asumir que los recursos son locales*. Por ejemplo,
      la plataforma web no puede asumir que la base de datos corre en el mismo
      servidor; por lo que debe ser capaz de conectarse a servidor de base de
      datos remoto.

    * *Cada pieza del conjunto debe ser fácilmente trasladable o reemplazable*.
      Si Apache por alguna razón no funciona para la implementación dada,
      deberías ser posible cambiarlo por otro servidor con mínimas
      complicaciones. O a nivel hardware, si un servidor web falla, debería ser
      posible reemplazarlo por otra maquina con ínfimos tiempos de caída. Recuerda,
      esta filosofía sobre implementación se basa enteramente en hardware barato.
      Fallas en maquinas individuales deben estar contempladas.

Como probablemente esperabas, Django maneja todo esto más o menos de forma
transparente -- ninguna parte de Django viola estos principios -- pero conocer
la filosofía ayuda cuando es tiempo de escalar.

.. admonition:: ¿Pero esto funciona?

    Esta filosofía puede sonar bien en papel (o en tu pantalla), pero ¿funciona
    realmente?

    Bueno, en vez de responder directamente, permítanos mostrarle una lista no
    muy exhaustiva de compañías que han basado sus negocios en esta arquitectura.
    Probablemente reconozca algunos de estos nombres:

    * Amazon
    * Blogger
    * Craigslist
    * Facebook
    * Google
    * LiveJournal
    * Slashdot
    * Wikipedia
    * Yahoo
    * YouTube

    Parafraseando la famosa escena de *Cuando Harry conoció a Sally...*:
    "¡Tendremos lo que ellos tienen!"

Un nota sobre preferencias personales
=====================================

Antes de entrar en detalles, un rápido comentario.

El open source es famoso por sus llamadas guerras religiosas; mucha tinta
(digital) ha sido despilfarrada argumentando sobre editores de textos
(``emacs`` versus ``vi``),sistemas operativos (Linux versus Windows versus
Mac OS), motores de base de datos (MySQL versus PostgreSQL), y -- por supuesto --
lenguajes de programación.

Nosotros tratamos de permanecer lejos de esas batallas. Simplemente no hay tiempo
suficiente.

Sin embargo, hay algunas elecciones que tomar al momento de implementar Django,
y constantemente nos preguntar por nuestras preferencias. Conscientes de que
explicitar esas preferencias puede encender una de de esas batallas ya
mencionadas, la mayoría de las veces hemos tratado de evitarlo. Pero para
permitir un debate completo lo explicitaremos aquí. Preferimos lo siguiente:

    * Linux (específicamente Ubuntu) como nuestro sistema operativo

    * Apache y mod_python para el servidor web

    * PostgreSQL como servidor de base de datos

Por supuesto, podemos indicarles muchos usuarios de Django que han hecho otras
elecciones con gran éxito.

Usando Django con Apache y mod_python
=====================================

Apache con mod_python es actualmente la configuración más robusta para usar
Django en un servidor en producción.

mod_python (http://www.djangoproject.com/r/mod_python/) es un plugin de Apache
que embebe Python dentro de Apache y carga código Python en memoria cuando el
servidor se inicia. El código permanece en memoria a lo largo de la vida del
proceso Apache, lo que repercute en aumentos significativos de desempeño
comparado con otros arreglos de servidor.

Django requiere Apache 2.x y mod_python 3.x, y nosotros preferimos el módulo de
multiprocesamiento (MPM) prefork de Apache, por sobre el MPM worker.

.. admonition:: Nota:

    Configurar Apache está *claramente* más allá del alcance de este libro,
    por lo que simplemente mencionaremos algunos detalles que necesitamos.
    Afortunadamente existen grandes recursos disponibles para aprender más
    sobre Apache. Algunos de los que nos gustan son los siguientes:


        * La documentación gratuita de Apache, disponible via
          http://www.djangoproject.com/r/apache/docs/

        * *Pro Apache, Third Edition* (Apress, 2004) de Peter Wainwright,
          disponible via http://www.djangoproject.com/r/books/pro-apache/

        * *Apache: The Definitive Guide, Third Edition* (O'Reilly, 2002) de Ben
          Laurie y Peter Laurie, disponible via
          http://www.djangoproject.com/r/books/apache-pra/

Configuración básica
--------------------

Para configurar Django con mod_python, primero debe asegurarse de que tiene
Apache instalado con el módulo mod_python activado. Esto usualmente significa
tener una directiva ``LoadModule`` en tu archivo de configuración de Apache.
Puede parecerse a esto::


    LoadModule python_module /usr/lib/apache2/modules/mod_python.so

Luego, edite su archivo de configuración de Apache y agregue lo siguiente::

    <Location "/">
        SetHandler python-program
        PythonHandler django.core.handlers.modpython
        SetEnv DJANGO_SETTINGS_MODULE misitio.settings
        PythonDebug On
    </Location>

Asegurese de reemplazar ``misitio.settings`` por el ``DJANGO_SETTINGS_MODULE``
apropiado para tu sitio.

Esto le dice a Apache, "Usa mod_python para cualquier URL en '/' o bajo ella,
usando el manejado mod_python de Django". Le pasa el valor de ``DJANGO_SETTINGS_MODULE``
de modo que mod_python conoce que configuración utilizar.

Nota que estamos usando la directiva ``<Location>`` y no ``<Directory>``. Esta
última se utiliza para apuntar a lugares de nuestra sistema de archivos, mientras
que ``<Location>`` apunta a lugares en la estructura de la URL de un sitio web.
``<Directory>`` no tendría sentido aquí.

Apache comunmente corre como un usuario diferente de tu usuario normal y puede
tener una ruta y un sys.path distintos. Puedes necesitar decirle a mod_python
cómo encontrar tu proyecto y a Django mismo::


    PythonPath "['/ruta/al/proyecto', '/ruta/a/django'] + sys.path"


También puedes agregar directivas como `PythonAutoReload Off`` para ajustar
la performance. Mira la documentación de mod_python para un obtener un listado
completo de opciones.

Ten en cuenta que deberias configurar ``PythonDebug Off`` en un servidor de
producción. Si dejas ``PythonDebug On``, tus usuarios verán feas trazas de error
de Python si algo sale dentro de mod_python.

Reinicia Apache, y cualquier petición a tu sitio (o a tu host virtual si pusiste
las directivas dentro de un bloque ``<VirtualHost>``) será servida por Django.

.. admonition::

    Si implementas Django en un subdirectorio -- esto es, en algun lugar más
    profundo que "/" -- Django no recortará el prefijo de la URL para tu
    URLpatterns. Entonces, si tu configuración de Apache luce como esto::

        <Location "/misitio/">
            SetHandler python-program
            PythonHandler django.core.handlers.modpython
            SetEnv DJANGO_SETTINGS_MODULE misitio.settings
            PythonDebug On
        </Location>

    entonces *todos* tus patrones de URL deberán comenzar con ``"/misitio/"``.
    Por esta razón es que usualmente recomendamos implementar Django sobre la
    raiz de tu dominio o host virtual. Alternativamente, simplemente puede
    hacer descender el nivel de tu URL usando una cuña de URLconf::

        urlpatterns = patterns('',
            (r'^misitio/', include('normal.root.urls')),
        )


Corriendo multiples instalaciones de Django en la misma instancia Apache
------------------------------------------------------------------------

Es enteramente posible correr multiples instalaciones de Django en la misma
instancia de Apache. Probablemente quieras hacer esto si eres un desarrollador
web independiente con multiples clientes pero un sólo un único servidor.

Para lograr esto, simplemente usa ``VirtualHost`` así::


    NameVirtualHost *

    <VirtualHost *>
        ServerName www.ejemplo.com
        # ...
        SetEnv DJANGO_SETTINGS_MODULE misitio.settings
    </VirtualHost>

    <VirtualHost *>
        ServerName www2.ejemplo.com
        # ...
        SetEnv DJANGO_SETTINGS_MODULE misitio.other_settings
    </VirtualHost>


Si necesitar poner dos instalaciones de Django sobre el mismo ``VirtualHost``,
necesitar prestar especial atención para asegurarte de que el caché de código
de mod_python no mezcle las cosas. Usa la directiva ``PythonInterpreter`` para
brindar diferentes directivas ``<Location>`` a interpretes distintos::

    <VirtualHost *>
        ServerName www.ejemplo.com
        # ...
        <Location "/algo">
            SetEnv DJANGO_SETTINGS_MODULE misitio.settings
            PythonInterpreter misitio
        </Location>

        <Location "/otracosa">
            SetEnv DJANGO_SETTINGS_MODULE misitio.other_settings
            PythonInterpreter misitio_otro
        </Location>
    </VirtualHost>

Los valores de ``PythonInterpreter`` no importante realmente ya que se encuentran
en dos bloques ``Location`` diferentes.


Corriendo un servidor de desarrollo con mod_python
--------------------------------------------------

Debido a que mod_python cachea el código python cargado, cuando implemantas sitios
Django sobre mod_python necesitarás reiniciar Apache cada vez que realizar cambios
en tu código. Esto puede ser tedioso, por lo que aqui compartimos un pequeño truco
para evitarlo: simplemente agrega ``MaxRequestsPerChild 1`` a tu archivo de
configuración para forzar a Apache a recargar todo con cada petición. Pero no hagas
esto en un servidor de producción, o revocaremos tus privilegios Django.

Si eres el tipo de programador que depuran dispersando sentencias ``print`` por
el código (nosotros somos), ten en cuenta que ``print`` no tiene efectos sobre
mod_python; estas no aparecen en el log de Apache como pudrías esperar.
Si necesitas imprimir información de depuración en una configuración mod_python,
probablemente quieras usar el paquete de registro de eventos estándar de Python
(Python's standard logging package). Hay más información disponible en
http://docs.python.org/lib/module-logging.html. Alternativamente, puedes agregar
la información de depuración a las plantillas de tu página.

Sirviendo Django y archivos multimedia desde la misma instancia Apache
----------------------------------------------------------------------

Django no debería ser utilizado para servir archivos multimedia (imágen, audio,
video, flash) por sí mismo; mejor deja ese trabajo al servidor web que hayas elegido.
Recomendamos usar un servidor Web separado (es decir, uno que no está corriendo
a la vez Django) para servir estos archivos. Para más información, mira
la sección "`Escalamiento`_".

Sin embargo, si no tienes opción para servir los archivos multimedia que no sea
el mismo ``VirtualHost`` Apache que usa Django, aquí te mostramos como desactivar
mod_python para una parte particular del sitio::


    <Location "/media/">
        SetHandler None
    </Location>

Cambia ``Location`` a la URL raiz donde se encuentran tus archivos.

Tambien puedes usar ``<LocationMatch>`` para comparar con una expresión regular.
Por ejemplo, esto configura Django en la raiz del sitio pero deshabilitando
Django para el subdirectorio ``media`` y cualquier URL que termine en
``.jpg``, ``.gif``, o ``.png``::


    <Location "/">
        SetHandler python-program
        PythonHandler django.core.handlers.modpython
        SetEnv DJANGO_SETTINGS_MODULE mysite.settings
    </Location>

    <Location "/media/">
        SetHandler None
    </Location>

    <LocationMatch "\.(jpg|gif|png)$">
        SetHandler None
    </LocationMatch>

En todos estos casos, necesitarás configurar la directiva ``DocumentRoot`` para
que Apache sepa dónde encontrar tus archivos estáticos.

Manejo de errores
-----------------

Cuando usas Apache/mod_python, los errores serán canalizados por Django -- en otras
palabras, estos no se propagan al nivel de Apache y no aparecerán en el ``error_log``
del servidor.

La excepción a esto sucede si algo está realmente desordenado en tu configuración
Django. En este caso, verás una página "Internal Server Error" en tu navegador,
y el volcado de error (traceback) de Python completo en tu archivo ``error_log``
de Apache. Este volcado de error se difunde por multiples líneas. (Sí, es feo
y bastante difícil de leer, pero así como mod_python hace las cosas).


Manejando fallas de segmentación
--------------------------------

Algunas veces, Apache produce fallas de segmentación (Segmentation faults, en inglés)
cuando instalas Django. Cuando esto sucede, se trata casi *siempre* de una o dos
causas no muy relacionadas con Django en sí:

    * Puede ser que tu código Python está importando el módulo ``pyexpat``
      (usado para parseo XML), lo que puede entrar en conflicto con la versión
      embebida en Apache. Para información detallada, revisa "Expat Causing Apache Crash"
      en http://www.djangoproject.com/r/articles/expat-apache-crash/.


    * Puede deberse a que estás corriendo mod_python y mod_php sobre la misma
      instancia de Apache, con MySQL como motor de base de datos. En algunos
      casos, esto ocasiona un conocido problema que mod_python tiene debido a
      conflictos de versión en PHP y el back-end MySQL de la base. Hay información
      detallada en un listado FAQ de mod_python, accesible via
      http://www.djangoproject.com/r/articles/php-modpython-faq/

Si continuas teniendo problemas para configurar mod_python, una buena cosa para hacer
es poner un esqueleto de sitio sobre mod_python a funcionar, sin el framework Django.
Esta es una manera fácil de aislar los problemas específicos de mod_python.
El artículo "Getting mod_python Working" detalla el procedimiento:
http://www.djangoproject.com/r/articles/getting-modpython-working/.

El siguiente paso debería ser editar tu código de pruebas y agregar la importación
de cualquier código específico de Django que estes usando -- tus vistas, tus modelos,
tu URLconf, la configuración de RSS, y así. Incluye estas importaciones en
tu función de gestión de pruebas, y accede a la URL correspondiente desde tu
navegador. Si esto causa un colapso, habrás confirmado que es la importación de
código Django la causa del problema. Gradulamente reduce el conjunto de importaciones
hasta que el colapso desaparezca, de manera de encontrar el módulo específico
que es el culpable. Profundiza en los módulos y revisa sus importaciones si es
necesario. Para más ayuda, herramientas de sistema como ``ldconfig`` en Linux,
``otool`` en Mac OS, y  ``ListDLLs`` (de SysInternals) en Windows pueden
ayudarte a indentificar dependencias compartidas y posibles conflictos de version.

Usando Django con FastCGI
=========================

Aunque Django bajo Apache y mod_python es la configuración más robusta de
implementación, mucha gente usa hosting compartido, en los que FastCGI es
la única opción de implementación.

Adicionalmente, en algunas situaciones, FastCGI permite mayor seguridad
y posiblemente una mejor performance que mod_python. Para sitios pequeños,
FastCGI además puede ser más liviano que Apache.

Descripción de FastCGI
----------------------

FastCGI es una manera eficiente de dejar que una aplicación externa genere páginas
para un servidor Web. El servidor delega las peticiones Web entrantes (a través de
un socket) a FastCGI, quien ejecuta el código y devuelve la respuesta al servidor,
quien, a su turno, la remitirá al navegador del cliente.

Como mod_python, FastCGI permite que el código permanezca en memoria, logrando
que las peticiones sean servidas sin tiempo de inicialización. A diferencia
de mod_python, un proceso FastCGI no corre dentro del proceso del servidor Web,
sino en un proceso separado y persistente.

.. admonition:: ¿Por qué ejecutar código en un proceso separado?

    Los módulos tradicionales ``mod_*`` en Apache embeben varios lenguajes de
    scripting (los más notables son PHP, Python/mod_python, y Perl/mod_perl)
    dentro del espacion de procesos de tu servidor Web. A pesar de que esto
    reduce el tiempo de inicio (porque el código no tiene que ser leído del
    disco para cara consulta), lo hace al costo de ocupar espacio en memoria.

    Cada proceso Apache consigue una copia completa del motor de Apache, con
    todas las características de Apache que Django simplemente no aprovecha.
    Los procesos FastCGI, por otro lado, solo tienen el overhead de memoria de
    Python y Django.

    Debido a la naturaleza de FastCGI, también es posible tener procesos
    ejecutando bajo una cuenta de usuario diferente de la del proceso del
    servidor Web. Este es un buen beneficio de seguridad es sistemas
    compartidos, dado que significa que puedes asegurar tu código de otros
    usuarios.

Antes de que puedas empezar a usar FastCGI con Django, necesitas instalar
``flup``, una biblioteca Python para manejar FastCGI. Algunos usuarios han
reportado páginas que explotaron con versiones antiguas de ``flup``, por lo
cual puedes querer utilizar la última versión SVN. Puedes conseguir ``flup`` en
http://www.djangoproject.com/r/flup/.

Ejecutando tu Servidor FastCGI
------------------------------

FastCGI opera sobre un modelo cliente/servidor, y en la mayoría de los casos
estarás iniciando el proceso servidor FastCGI por tu cuenta. Tu servidor Web
(ya sea Apache, lighttpd, o algún otro) hace contacto con tu proceso Django-
FastCGI solo cuando el servidor necesita cargar una página dinámica. Como el
demonio ya está ejecutando su código en memoria, puede servir la respuesta muy
rápido.

.. exhortacion:: Nota

    Si estás en un sistema de hosting compartido, probablemente estés forzado
    a usar procesos FastCGI manejados por el Web server. Si estás en esta
    situación, debes leer la sección titulada "`Ejecutando Django en un
    proveedor de Hosting compartido con Apache`_", más abajo.

Un servidor Web puede conectarse a un servidor FastCGI de dos formas: usando
un socket de dominio Unix, (un *named pipe* en sistemas Win32) o un socket
TCP. Lo que elijas es una cuestión de preferencias; usualmente un socket TCP
es más fácil debido a cuestiones de permisos.

Para iniciar tu servidor, primero cambia al directorio de tu proyecto (donde
está tu ``manage.py``), y ejecuta ``manage.py`` con el comando ``runfcgi``::

    ./manage.py runfcgi [options]

Si especificas ``help`` como única opción después de ``runfcgi``, se mostrará
una lista de todas las opciones disponibles.

Necesitarás especificar un ``socket`` o si no ``host`` y ``port``.
Entonces, cuando configures tu servidor Web, solo necesitas apuntarlo al
socket o host/port que especificaste cuando iniciaste el servidor FastCGI.

Algunos ejemplos pueden ayudar a explicarlo:

* Ejecutar un servidor 'threaded' en un puerto TCP::

  ./manage.py runfcgi method=threaded host=127.0.0.1 port=3033

* Ejecutar un servidor preforked sobre un socket de dominio Unix::

  ./manage.py runfcgi method=prefork socket=/home/user/mysite.sock pidfile=django.pid

* Ejecutar sin demonizar (ejecutar en segundo plano) el proceso (es bueno
  para el debugging)::

  ./manage.py runfcgi daemonize=false socket=/tmp/mysite.sock

Detener el Demonio FastCGI
~~~~~~~~~~~~~~~~~~~~~~~~~~

Si tienes el proceso ejecutando en primer plano, es fácil detenerlo:
simplemente presiona Ctrl+C para detenerlo y salir del servidor FastCGI. Si
estás tratando con procesos en segundo plano, necesitarás recurrir al comando
``kill`` de Unix.

Si especificas la opción ``pidfile`` en  ``manage.py runfcgi``, puedes detener
el demonio FastCGI en ejecución de esta forma::

    kill `cat $PIDFILE`

donde ``$PIDFILE`` es el ``pidfile`` que especificaste.

Para reiniciar con facilidad tu demonio FastCGI en Unix, pedes usar este
breve script en la línea de comandos:

.. code-block:: bash

    #!/bin/bash

    # Replace these three settings.
    PROJDIR="/home/user/myproject"
    PIDFILE="$PROJDIR/mysite.pid"
    SOCKET="$PROJDIR/mysite.sock"

    cd $PROJDIR
    if [ -f $PIDFILE ]; then
        kill `cat -- $PIDFILE`
        rm -f -- $PIDFILE
    fi

    exec /usr/bin/env - \
      PYTHONPATH="../python:.." \
      ./manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE

Usando Django con Apache y FastCGI
----------------------------------

Para usar Django con Apache y FastCGI, necesitarás que Apache esté instalado y
configurado, con mod_fastcgi instalado y habilitado. Consulta la documentación
de Apache y  mod_fastcgi para instrucciones detalladas:
http://www.djangoproject.com/r/mod_fastcgi/.

Una vez que hayas completado la configuración, apunta Apache a tu instancia
FastCGI de Django editando el archivo ``httpd.conf`` (de la configuración de
Apache). Necesitarás hacer dos cosas:

* Usar la directiva ``FastCGIExternalServer`` para especificar la
  localización de tu servidor FastCGI.

* Usar ``mod_rewrite`` para apuntar las URLs a FastCGI según sea necesario.

Especificando la Localización del Servidor FastCGI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La directiva ``FastCGIExternalServer`` le dice a Apache como encontrar tu
servidor FastCGI. Como se explica en los documentos de FastCGIExternalServer
(http://www.djangoproject.com/r/mod_fastcgi/FastCGIExternalServer/), puedes
especificar un ``socket`` o un ``host``. Aquí hay ejemplos de ambos:

Connect to FastCGI via a socket/named pipe:
FastCGIExternalServer /home/user/public_html/mysite.fcgi -socket /home/user/mysite.sock

Connect to FastCGI via a TCP host/port:
FastCGIExternalServer /home/user/public_html/mysite.fcgi -host 127.0.0.1:3033

En los dos casos, el directorio /home/user/public_html/ debe existir,
aunque el archivo ``/home/user/public_html/mysite.fcgi`` no necesariamente
tiene que existir. Es solo una URL usada por el servidor Web internamente --
un enganche para indicar que las consultas en esa URL deben ser manejadas por
FastCGI. (Más sobre esto en la siguiente sección.)

Usando mod_rewrite para apuntar URLs hacia FastCGI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El segundo paso es decirle a Apache que use FastCGI para las URLS que coincidan
con cierto patrón. PAra hacer esto, usa el módulo mod_rewrite y reescribe las
URLs hacia ``mysite.fcgi`` (o donde hayas especificado en la directiva
``FastCGIExternalServer``, como se explicó en la sección anterior).

En este ejemplo, le decimos a Apache que use FastCGI para manejar cualquier
consulta que no represente un archivo del sistema de archivos y no empiece con
``/media/``. Probablemente éste sea el caso más común, si estás usando el sitio
de administración de Django::

    <VirtualHost 12.34.56.78>
      ServerName example.com
      DocumentRoot /home/user/public_html
      Alias /media /home/user/python/django/contrib/admin/media
      RewriteEngine On
      RewriteRule ^/(media.*)$ /$1 [QSA,L]
      RewriteCond %{REQUEST_FILENAME} !-f
      RewriteRule ^/(.*)$ /mysite.fcgi/$1 [QSA,L]
    </VirtualHost>

FastCGI y lighttpd
------------------

lighttpd (http://www.djangoproject.com/r/lighttpd/) es un servidor Web liviano
usado habitualmente para servir archivos estáticos. Admite FastCGI en forma
nativa y por lo tanto es también una opción ideal para servir tanto páginas
estáticas como dinámicas, si tu sitio no tiene necesidades específicas de
Apache.

Asegúrate que ``mod_fastcgi`` está en tu lista de modulos, en algún lugar
después  de ``mod_rewrite`` y ``mod_access``, y antes de ``mod_accesslog``.
Probablemente desees también ``mod_alias``, para servir medios de
administración.

Agrega lo siguiente a tu archivo de configuración de lighttpd::

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
        "/media/" => "/home/user/django/contrib/admin/media/",
    )

    url.rewrite-once = (
        "^(/media.*)$" => "$1",
        "^/favicon\.ico$" => "/media/favicon.ico",
        "^(/.*)$" => "/mysite.fcgi$1",
    )

Ejecutando Múltiples Sitios Django en Una Instancia lighttpd
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lighttpd te permite usar "configuración condicional" para permitir la
configuración personalizada para cada host. Para especificar múltiples sitios
FastCGI, solo agrega un bloque condicional en torno a tu configuración  FastCGI
para cada sitio::

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
simplemente especificando múltiples entradas en la directiva ``fastcgi.server``.
Agrega un host FastCGI para cada una.

Ejecutando Django en un Proveedor de Hosting Compartido con Apache
------------------------------------------------------------------

Muchos proveedores de hosting compartido no te permiten ejecutar tus propios
demonios servidores o editar el archivo ``httpd.conf``. En estos casos, aún es
posible ejecutar Django usando procesos iniciados por el sevidor Web.

.. admonition:: Nota

    Si estás usando procesos iniciados por el servidor Web, como se explica en
    esta sección, no necesitas iniciar el servidor FastCGI por tu cuenta.
    Apache iniciará una cantidad de procesos, escalando según lo necesite.

En el directorio raíz de tu Web, agrega esto a un archivo llamado ``.htaccess`` ::

    AddHandler fastcgi-script .fcgi
    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteRule ^(.*)$ mysite.fcgi/$1 [QSA,L]

Después, crea un pequeño script que le diga a Apache como iniciar tu programa
FastCGI. Crea un archivo ``mysite.fcgi``, colócalo en tu directorio Web, y
asegúrate de hacerlo ejecutable::

    #!/usr/bin/python
    import sys, os

    # Add a custom Python path.
    sys.path.insert(0, "/home/user/python")

    # Switch to the directory of your project. (Optional.)
    # os.chdir("/home/user/myproject")

    # Set the DJANGO_SETTINGS_MODULE environment variable.
    os.environ['DJANGO_SETTINGS_MODULE'] = "myproject.settings"

    from django.core.servers.fastcgi import runfastcgi
    runfastcgi(method="threaded", daemonize="false")

Reiniciando el Server Iniciado
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si cambias cualquier código Python en tu sitio, necesitarás decirle a FastCGI
que el código ha cambiado. Pero no hay necesidad de reiniciar Apache en este
caso the. Sólo volver a subir ``mysite.fcgi`` -- o editar el archivo -- de
manera que la fecha y hora del archivo cambien. Cuando Apache ve que el archivo
ha sido actualizado, reiniciará tu aplicación Django por ti.

Si tienen acceso a la línea de comandos en un sistema Unix system, puedes hacer
esto fácilmente usando el comando ``touch``::

    touch mysite.fcgi

Escalamiento
============

Ahora que sabes como tener a Django ejecutando en un servidor simple, veamos
como puedes escalar una instalación Django. Esta sección explica como puede
escalar un sitio desde un servidor único a un cluster de gran escala que pueda
servir millones de hits por hora.

Es importante notar, sin embargo, que cada sitio grande es grande de diferentes
formas, por lo que escalar es cualquier cosa menos una operación de una
solución única para todos los casos. La siguiente cobertura debe ser suficiente
para mostrat el principio general, y cuando sea posible, trateremos de señalar
donde se puedan elegir distintas opciones.

Primero, haremos una buena presuposición, y hablaremos exclusivamente acerca
de escalamiento bajo Apache y mod_python. A pesar de que conocemos vario casos
exitosos de desarrollos FastCGI medios y grandes, estamos mucho más
familiarizados con Apache.

Ejecutando en un Servidor Único
-------------------------------

La mayoría de los sitios empiezan ejecutando en un servidor único, con una
arquitectura que se ve como en la Figura 20-1.

.. image:: graficos/chapter20/scaling-1.png

Figura 20-1: configuración de Django en un servidor único .

Esto funciona bien para sitios pequeños y medianos, y es relativamente barato
-- puedes instalar un servidor único diseñado para Django por menos de 3,000
dólares.

Sin embargo, a medida que el tráfico se incemente, caerás rápidamente en
*contención de recursos* entre las diferentes piezas de software. Los
servidores de base de datos y los servidores Web *adoran* tener el servidor
entero para ellos, y cuando corren en el mismo servidos siempre terminan
"peleando" por los mismos recursos (RAM, CPU) que prefieren monopolizar.

Esto se resuelve fácilmente moviendo el servidor de base de datos a una segunda
máquina, como se explica en la siguiente sección.

Separando el Servidor de Bases de Datos
---------------------------------------

En lo que tiene que ver con Django, el proceso de separar el servidor de bases
de datos es extremadamente sencillo: simplemente necesitas cambiar la
configuración de ``DATABASE_HOST``  a la IP o nombre DNS de tu servidor.
Probablemente sea una buena idea usar la IP si es posible, ya que depender de
la DNS para la conexión entre el servidor Web y el servidor de bases de datos
no se recomienda.

Con un servidor de base de datos separado, nuestra arquitectura ahora se ve
como en la Figura 20-2.

.. image:: graficos/chapter20/scaling-2.png

   Figura 20-2: Moviendo la base de datos a un servidor dedicado.

Aqui es donde empezamos a movernos hacia lo que usualmente se llama
arquitectura *n-tier*. No te asustes por la terminilogía -- sólo se refiere al
hecho de que diferentes "tiers" de la pila Web separadas en diferentes máquinas
físicas.

A esta altura, si anticipas que en algún momento vas a necesitar crecer más
allá de un servidor de base de datos único, probablemente sea una buena idea
empezar a pensar en pooling de conexiones y/o replicación de bases de datos.
Desafortunadamente, no hay suficiente espacio para hacerle justicia a estos
temas en este libro, así que vas a necesitar consultar la documentación y/o
a la comunidad de tu base de datos para más información.

Ejecutando un Servidor de Medios Separado
-----------------------------------------

Aún tenemos un gran problema por delante desde la configuración del servidor
único: el servicio de medios desde la misma caja que maneja el contenido
dinámico.

Estas dos actividades tienen su mejor performance bajo distintas
circunstancias, y encerrándolas en la misma caja terminarás con que ninguna de
las dos tendrá particularmente buena performance. Así que el siguiente paso es
separar los medios -- esto es, todo lo que *no* es generado por una vista de
Django -- a un servidor dedicado (ver Figura 20-3).

.. image:: graficos/chapter20/scaling-3.png

Figura 20-3: Separando el servidor de medios.

Idealmente, este servidor de medios debería correr un servidor Web desnudo,
optimizado para la entrega de medios estáticos. lighttpd y tux
(http://www.djangoproject.com/r/tux/) son dos excelentes elecciones aquí, pero
un servidor Apache bien 'pelado' también puede funcionar.

Para sitios pesados en contenidos estáticos (fotos, videos, etc.), moverse a un
servidor de medios separado es doblemente importante y debería ser el *primer*
paso en el escalamiento hacia arriba.

De todos modos, este paso puede ser un poco delicado. El administrador de
Django necesita poder escribir medios 'subidos' en el servidor de medios. (la
configuración de ``MEDIA_ROOT`` controla donde se esciben estos medios). Si un
medio habita en otro servidor, de todas formas necesitas organizar una forma de
que esa escritura se pueda hacer a traves de la red.

La manera más fácil de hacer esto es usar el NFS para montar los directorios de
medios del servidor de medios en el servidor Web (o los servidores Web). Si los
montas en la misma ubicación apuntada por ``MEDIA_ROOT``, el uploading de
medios Simplemente Funciona¿.

Implementando Balance de Carga y Redundancia
--------------------------------------------

A esta altura, ya hemos separado las cosas todo lo posible. Esta configuración
de tres servers debería manejar una cantidad muy grande de tráfico -- nosotros
servimos alrededor de 10 millones de hits por día con una arquitectura de este
tipo-- así que si creces más allá, necesitarás empezar a agregar redundancia.

En realidad, esto es algo bueno. Una mirada a la Figura 20-3 te permitirá cer
que si falla aunque sea uno solo de los servidores, el sitio entero se cae. Asi
que a medida que agregas servidores redundantes, no sólo incrementas capacidad,
sino también confiabilidad.

Para este ejemplo, asumamos que el primero que se ve superado en capacidad es
el servidor Web. Es fácil tener múltiples copias de un sitio Djando ejecutando
en diferente hardware. -- simplemente copia el código en varias máquinas, y
inicia Apache en cada una de ellas.

Sin embargo, necesitas otra pieza de software para distribuir el tráfico entre
los servidores: un *balanceador de carga*. Puedes comprar balanceadores de
carga por hardware caros y propietarios, pero existen algunos balanceadores de
carga por software de alta calidad que son open source.

``mod_proxy`` de Apache es una opción, pero hemos encontrado que Perlbal
(http://www.djangoproject.com/r/perlbal/) es simplemente fantástico. Es un
balanceador de carga y proxy inverso escrito por las mismas personas que
escribieron ``memcached`` (ver `Capítulo 13`_).

.. admonition::  Si estás usando FastCGI:

    Puedes realizar este mismo paso distribución y
    balance de carga separando los servidores Web front-end y los procesos
    FastCGI back-end en diferentes máquinas. El servidor front-end se convierte
    esencialmente en el balanceador de carga, y los procesos FastCGI back-end
    reemplaza a los servidores Apache/mod_python/Django.

Con los servidores Web en cluster, nuestra arquitectura en evolución empieza a
verse más compleja, como se ve en la Figura 20-4.

.. image:: graficos/chapter20/scaling-4.png

Figura 20-4: Configuración de un server redundante con balance de carga.

Observar que en el diagrama nos referimos a los servidores Web como "el
cluster" para indicar que el numero de servidores basicamente es variable.
Una vez que tienes un balanceador de carga en el frente, pueder agregar y
eliminar servidores Web back-end sin perder un segundo fuera de servicio.

Vamos a lo grande
-----------------

En este punto, los siguientes pasos son derivaciones del último:

* A menida que necesites más performance en la base de datos, necesitarás
  agregar servidores de base de datos relicados. MySQL tiene replicación
  incorporada; los usuarios de PostgreSQL deberían mirar a  Slony
  (http://www.djangoproject.com/r/slony/) y pgpool
  (http://www.djangoproject.com/r/pgpool/) para replicación y pooling
  de conexiones, respectivamente.

* Si un solo balanceador de carga no es suficiente, puedes agregar más
  máquinas balanceadoras de carga y distribuir entre ellas usando DNS
  round-robin.

* Si un servidor único de medios no es suficiente, puedes agregar más
  servidores de medios y distribuir la carga con tu cluster de
  balanceadores de carga.

* Si necesitas más almacenamiento cache, puedes agregar servidores de
  cache dedicados.

* En cualquier etapa, si un cluster no tiene buena performance, puedes
  agregar más servidores al cluster.

Después de algunas de estas iteraciones, una arquitectura de gran escala
debe verse como en la Figura 20-5.

.. image:: chapter20/scaling-5.png

Figura 20-5. Un ejemplo de configuración de Django de gran escala.

A pesar de que mostramos solo dos o tres servidores en cada nivel, no hay un
límite fundamental a cuantos puedes agregar.

Una vez que haz llegado a este nivel, te quedan pocas opciones. El Apéndice A
tiene alguna información proveniente de desarrolladores responsables de algunas
instalaciones Django de gran escala. Si estás planificando un sitio Django de
alto tráfico, es una lectura recomendada.

Ajuste de Performance
=====================

Si tienes grandes cantidades de dinero, simplemente puedes irle arrojando
hardware a los problemas de escalado. Para el resto de nosotros, sin embargo,
el ajuste de performance es una obligación.

.. admonition:: Incidentalmente

    Si alguien con monstruosas cantidades de dinero está
    leyendo este libro, por favor considere una donación sustancial al proyecto
    Django. Aceptamos diamantes en bruto y lingotes de oro.

Desafortunadamente, el ajuste de performance es más un arte que una ciencia,
y es aun más dificil de escribir sobre eso que sobre escalamiento. Si estás
pensando seriamente en desplegar una aplicación Django de gran escala, deberás
pasar un un buen tiempo aprendiendo como ajustar cada pieza de tu stack.

Las siguientes secciones, sin embargo, presentan algunos tips específicos del
ajuste de performance de Django que hemos descubiero a traves de los años.

No hay tal cosa como demasiada RAM
----------------------------------

Cuando escribimos esto, la RAM realmente cara cuesta aproximadamente 200
dólares por gigabyte -- moneditas comparado con el tiempo empleado en ajustes
de performance. Compra toda la RAM que puedas, y después compra un poco más.

Los procesadores más rápidos no mejoran la performance tanto. La mayoría de los
servidores Web desperdician el 90% de su tiempo esperando I/O del disco. En
cuanto empieces a swappear, la performance directamente se muere. Los discos
más rápidos pueden ayudar levemente, pero son mucho más caros que la RAM, así
que no cuentan.

Si tienes varios servidores, el primer lugar donde poner tu RAM es en el
servidor de base de datos. Si puedes, compra suficiente ram como para tener
toda tu base de datos en memoria. Esto no es tan difícil. La base de datos de
LJWorld.com -- que incluye medio millón de artículos desde 1989 -- tiene menos
de 2 GB.

Después, maximiza la RAM de tu servidor Web. La situación ideal es aquella en
la que ningún servidor swapea -- nunca. Si llegas a ese punto, debes poder
manejar la mayor parte del tráfico normal.

Deshabilita Keep-Alive
----------------------

``Keep-Alive`` es una característica de HTTP que permite que múltiples pedidos
HTTP sean servidos sobre una conexión TCP única, evitando el overhead de
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
ellos *siquiera se acerca* a ser tan rápido como memcached. Si tienes un sitio con
tráfico alto, ni pierdas tiempo con los otros -- ve directamente a memcached.

Usa memcached siempre
---------------------

Por supuesto, seleccionar memcached no te hace mejor si no lo usas realmente.
El `Capítulo 13`_ es tu mejor amigo aquí: aprende como usar el framework de
cache de Django, y usalo en todas partes que te sea posible. Un uso de cache
agresivo y preemptico es usualmente lo único que se puede hacer para mantener
un sitio funcionando bajo el mayor tráfico.

.. _Capítulo 13: ../chapter13/

Únete a la Conversación
-----------------------

Cada pieza del stack de Django -- desde Linux a Apache a PostgreSQL o MySQL
-- tiene una comunidad maravillosa detrás. Si realmente quieres obtener ese
último 1% de tus servidores, únete a las comunidades open source que están
detrás de tu software y pide ayuda. La mayoría de los miembros de la comunidad
del software libre estarán felices de ayudar.

Y también asegúrate de unirte a la comunidad Django. Tus humildes autores son
solo dos miembros de un grupo increíblemente activo y creciente de
desarrolladores Django. Nuestra comunidad tiene una enorme cantidad
de experiencia colectiva para ofrecer.

¿Qué sigue?
===========

Has alcanzado el final de nuestro programa regular. Los siguientes apéndices
contienen material de referencia que puedes necesitar a medida que trabajes
sobre tus proyectos Django

Te deseamos la mejor de las suertes en la puesta en marcha de tu sitio Django,
ya sea un pequeño juguete para tí o el próximo Google.

