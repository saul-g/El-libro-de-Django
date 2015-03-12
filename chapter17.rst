=======================
Capítulo 17: Middleware
=======================

En ocasiones, necesitarás ejecutar una pieza de código en todas las peticiones
que maneja Django. Éste código puede necesitar modificar la petición antes de
que la vista se encargue de ella, puede necesitar registrar información sobre
la petición para propósitos de debugging,  y así sucesivamente.

Tu puedes hacer esto con el **framework middleware** de Django, que es un conjunto
de acoples dentro del procesamiento de petición/respuesta de Django. Es un
sistema de "plug-in" liviano y de bajo nivel capaz de alterar de forma global
tanto la entrada como la salida de Django.

Cada componente middleware es responsable de hacer alguna función específica. Si
estas leyendo este libro de forma lineal (disculpen, posmodernistas), has visto
middleware varias veces ya:

* Todas las herramientas de usuario y sesión que vimos en el
  :doc:`capítulo 14<chapter14>` son posibles gracias a unas pequeñas piezas de
  middleware (más específicamente, el middleware hace que ``request.session`` y
  ``request.user`` estén disponibles para ti en las vistas.

* La cache global del sitio discutida en él :doc:`capítulo 15<chapter15>` es
  solo una pieza de middleware que desvía la llamada a tu función de vista si
  la respuesta  para esa vista ya fue almacenada en la cache.

* Todas las aplicaciones del paquete ``contrib`` como ``flatpages``,
  ``redirects``, y ``csrf`` del :doc:`capítulo 16<chapter16>` hacen su magia a
  través de componentes  middleware.

En este capítulo nos sumergiremos en las profundidades del middleware y
conoceremos exactamente cómo funciona, y te explicaremos cómo puedes escribir
tu propio middleware.

Qué es middleware
=================

Un componente middleware es simplemente una clase Python que se ajusta a una
cierta API. Antes de entrar en los aspectos formales de los que es esa API,
miremos un ejemplo muy sencillo.

Sitios de tráfico alto a menudo necesitan implementar Django detrás de un proxy
de balanceo de carga (mira él :doc:`capítulo 12<chapter12>`). Esto puede causar
unas pequeñas complicaciones, una de las cuales es que la IP remota de cada
petición (request.META["REMOTE_IP"]) será la del balanceador de carga, no
la IP real que realiza la petición. Los balanceadores de carga manejan esto
estableciendo una cabecera especial, ``X-Forwarded-For``, con el valor real de
la dirección IP que realiza la petición.

Así que aquí está una pequeña parte de middleware que le permite a los sitios
que se ejecutan detrás de un proxy ver la dirección IP correcta en
request.META["REMOTE_ADDR"]:

.. code-block:: python

    class SetRemoteAddrFromForwardedFor(object):
        def process_request(self, request):
            try:
                real_ip = request.META['HTTP_X_FORWARDED_FOR']
            except KeyError:
                pass
            else:
                # HTTP_X_FORWARDED_FOR puede ser una lista de IPs separadas por comas.
                # Toma la primera IP.
                real_ip = real_ip.split(",")[0]

.. admonition:: Nota:

  (Nota: Aunque las cabeceras HTTP son llamadas ``X-Forwarded-For``, Django hace
  que estén disponibles como ``request.META['HTTP_X_FORWARDED_FOR']``. Con la
  excepción de ``content-length`` y ``content-type``, cualquier cabecera HTTP en
  la petición es convertida en una clave ``request.META`` convirtiendo todos los
  caracteres a mayúsculas, remplazando cualquier guion con guiones bajos y
  agregando el prefijo ``HTTP_`` al nombre.

Si el middleware está instalado (mira la siguiente sección), el valor de
de todas las peticiones ``X-Forwarded-For`` será automáticamente insertado en
``request.META['REMOTE_ADDR']``. Esto significa que tus aplicaciones Django no
necesitan conocer si están detrás de un proxy de balanceo de carga o no, pueden
simplemente acceder a ``request.META['REMOTE_ADDR']``, y eso funcionará si se
usa un proxy o no.

De hecho, es una necesidad tan común, que esta pieza de middleware ya viene
incorporada en Django. Está ubicada en ``django.middleware.http``, y puedes leer
más sobre ella en la siguiente sección.

Instalación de Middleware
=========================

Si has leído este libro completamente hasta aquí, ya has visto varios ejemplos
de instalación de middleware; muchos de los ejemplos en los capítulos previos
han requerido cierto middleware. Para completar, a continuación se muestra la
manera de instalar middleware.

Para activar algún componente del middleware, solo agrégalo a la tupla
``MIDDLEWARE_CLASSES`` en tu archivo de configuración. En ``MIDDLEWARE_CLASSES``,
cada componente middleware se representa con una cadena: la ruta Python
completa al nombre de la clase middleware. Por ejemplo, aquí se muestra la tupla
``MIDDLEWARE_CLASSES`` por omisión creada por ``django-admin.py startproject``::

  MIDDLEWARE_CLASSES = (
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',
  )

Una instalación Django no requiere ningún middleware -- La tupla ``MIDDLEWARE_CLASSES``
puede estar vacía, si tu quieres, pero te recomendamos que actives ``CommonMiddleware``,
la cual explicaremos en breve.

El orden es importante. En las fases de petición y vista, Django aplica el
middleware en el orden que figura en ``MIDDLEWARE_CLASSES``, y en las fases de
respuesta y excepción, Django aplica el middleware en el orden inverso. Es decir,
Django trata ``MIDDLEWARE_CLASSES`` como una especie de "wrapper" alrededor de
la función de vista: en la petición recorre hacia abajo la lista hasta la vista,
y en la respuesta la recorre hacia arriba. Mira la siguiente figura para un
repaso de las fases y el orden que sigue el middleware en una petición.

.. figure:: graphics/chapter17/middleware.png
   :alt: Orden del middleware en Django.

   **Figura 17-1.** Orden de Middleware en Django.

Como puedes observar, durante la fase de petición (request), antes de llamar a la
vista, Django aplica el Middleware en el orden definido en la tupla
``MIDDLEWARE_CLASSES``. De arriba hacia abajo. Mediante dos ganchos disponibles:

* ``process_request()``
* ``process_view()``

Durante la fase de respuesta, después de llamar a la vista, el middleware es aplicado en
orden inverso de abajo hacia arriba, Usando tres ganchos disponibles:

* ``process_exception()`` (únicamente si la vista lanza una excepción)
* ``process_template_response()`` (únicamente para la respuesta de la plantilla)
* ``process_response()``

Puedes pensar en este proceso, como si fuera una cebolla, donde cada clase del
middleware es una ```capa`` que envuelve la vista.

Métodos de un Middleware
========================

Ahora que sabes qué es un middleware y cómo instalarlo, echemos un vistazo a
todos los métodos disponibles que las clases middleware pueden definir.

Inicializar: __init__(self)
---------------------------

Utiliza ``__init__()`` para realizar una configuración a nivel de sistema de una
determinada clase middleware.

Por razones de rendimiento, cada clase middleware activada es instanciada sólo
*una vez* por proceso servidor. Esto significa que ``__init__()`` es llamada
sólo una vez -- al iniciar el servidor, no para peticiones individuales.

Una razón común para implementar un método ``__init__()`` es para verificar si
el middleware es en realidad necesario. Si ``__init__()`` emite
``django.core.exceptions.MiddlewareNotUsed``, entonces Django removerá el
middleware de la pila de middleware. Tú podrías usar esta característica para
verificar si existe una pieza de software que la clase middleware requiere, o
verificar si el servidor esta ejecutándose en modo *debug*, o cualquier otra
situación similar.

Si una clase middleware define un método ``__init__()``, éste no debe tomar
argumentos más allá del estándar ``self``.

Pre-procesador de petición: process_request(self, request)
----------------------------------------------------------

Éste método es llamado tan pronto como la petición ha sido recibida -- antes de
que Django haya analizado sintácticamente la URL para determinar cuál vista
ejecutar. Si se le pasa el objeto ``HttpRequest``, el cual puedes modificar a tu
voluntad,  ``process_request()`` debe retornar ya sea ``None`` o un objeto
``HttpResponse``.

* Si devuelve ``None``, Django continuará procesando esta petición,
  ejecutando cualquier otro middleware y la vista apropiada.

* Si devuelve un objeto ``HttpResponse``, Django no se encargará de llamar a
  *cualquier* otro middleware (de ningún tipo) o a la vista apropiada.
  Django inmediatamente devolverá ése objeto ``HttpResponse``.

Pre-procesador de vista: process_view(self, request, view, args, kwargs)
------------------------------------------------------------------------

Éste método es llamado después de la llamada al pre-procesador de petición y
después de que Django haya determinado qué vista ejecutar, pero antes de que ésa
vista sea realmente ejecutada.

Los argumentos que se pasan a esta vista son mostrados en la Tabla 15-1.

.. table:: Tabla 15-1. Argumentos que se pasan a process_view()

    =============== ========================================================
        Argumento       Explicación
    =============== ========================================================
    ``request``     El objeto ``HttpRequest``.

    ``view``        La función Python que Django llamará para manejar esta
                    petición. Este es en realidad el objeto función en sí,
                    no el nombre de la función como string.

    ``args``        La lista de argumentos posicionales que serán pasados
                    a la vista, no incluye el argumento ``request``
                    (el cual es siempre el primer argumento de una vista).

    ``kwargs``      El diccionario de palabras clave argumento que será
                    pasado a la vista.
    =============== ========================================================

Así como el método ``process_request()``, ``process_view()`` debe retornar ya sea
``None`` o un objeto ``HttpResponse``.

* Si devuelve ``None``, Django continuará procesando esta petición,
  ejecutando cualquier otro middleware y la vista apropiada.

* Si devuelve un objeto ``HttpResponse``, Django no se encargará de llamar a
  *cualquier* otro middleware (de ningún tipo) o a la vista apropiada.
  Django inmediatamente devolverá ése objeto ``HttpResponse``.

Pos-procesador de respuesta: process_response(self, request, response)
----------------------------------------------------------------------

Éste método es llamado después de que la función de vista es llamada y la
respuesta generada. Aquí, el procesador puede modificar el contenido de una
respuesta; un caso de uso obvio es la compresión de contenido, como por ejemplo
la compresión con gzip del HTML de la respuesta.

Los parámetros deben ser bastante auto-explicativos: ``request`` es el objeto
petición, y ``response`` es el objeto respuesta retornados por la vista.

A diferencia de los pre-procesadores de petición y vista, los cuales pueden
retornar ``None``, ``process_response()`` *debe* retornar un objeto
``HttpResponse``. Esa respuesta puede ser la respuesta original pasada a la
función (posiblemente modificada) o una totalmente nueva.

Pos-procesador de excepción: process_exception(self, request, excepción)
------------------------------------------------------------------------

Éste método es llamado sólo si ocurre algún error y la vista emite una excepción
sin capturar. Puedes usar este método para enviar notificaciones de error,
volcar información postmórtem a un registro, o incluso tratar de recuperarse del
error automáticamente.

Los parámetros para esta función son el mismo objeto ``request`` con el que
hemos venido tratando hasta aquí, y ``excepción``, el cual es el objeto
``Exception`` real emitido por la función de vista.

``process_exception()`` debe retornar ya sea ``None`` o un objeto ``HttpResponse``.

* Si devuelve ``None``, Django continuará procesando esta petición con el
  manejador de excepción incorporado en el framework.

* Si devuelve un objeto ``HttpResponse``, Django usará esa respuesta en vez
  del manejador de excepción incorporado en el framework.

.. admonition:: Nota:

    Django trae incorporado una serie de clases middleware (que se discuten en
    la sección siguiente) que hacen de buenos ejemplos. La lectura de su código
    debería darte una buena idea de la potencia del middleware.

    También puedes encontrar una serie de ejemplos contribuidos por la comunidad
    en el wiki de Django: http://code.djangoproject.com/wiki/ContributedMiddleware

Middleware incluido
===================

Django viene con algunos middleware incorporados para lidiar con problemas
comunes, los cuales discutiremos en las secciones que siguen.

Middleware de soporte para autenticación
----------------------------------------

Clase middleware: ``django.contrib.auth.middleware.AuthenticationMiddleware``.

Este middleware permite el soporte para autenticación. Agrega el atributo
``request.user``, que representa el usuario actual registrado, a todo objeto
``HttpRequest`` que se recibe.

Mira él :doc:`capítulo 12<chapter12>` para los detalles completos.

Middleware "Common"
-------------------

Clase middleware: ``django.middleware.common.CommonMiddleware``.

Este middleware agrega algunas conveniencias para los perfeccionistas:

* *Prohíbe el acceso a los agentes de usuario especificados en la*
  *configuración* ``DISALLOWED_USER_AGENTS``:  Si se especifica,
  esta configuración debería ser una lista de objetos de expresiones
  regulares compiladas que se comparan con el encabezado user-agent de
  cada petición que se recibe. Aquí está un pequeño ejemplo de un archivo
  de configuración::

        import re

        DISALLOWED_USER_AGENTS = (
            re.compile(r'^OmniExplorer_Bot'),
            re.compile(r'^Googlebot')
        )

  Nota el ``import re``, ya que ``DISALLOWED_USER_AGENTS`` requiere que sus
  valores sean expresiones regulares compiladas (es decir, el resultado de
  ``re.compile()``). El archivo de configuración es un archivo común de
  Python, por lo tanto es perfectamente adecuado incluir sentencias
  ``import`` en él.

* *Realiza re-escritura de URL basado en las configuraciones* ``APPEND_SLASH``
  y ``PREPEND_WWW``: Si ``APPEND_SLASH`` es igual a ``True``, las URLs que
  no poseen una barra al final serán redirigidas a la misma URL con una
  barra al final, a menos que el último componente en el path contenga un
  punto. De esta manera ``foo.com/bar`` es redirigido a ``foo.com/bar/``,
  pero ``foo.com/bar/file.txt`` es pasado a través sin cambios.

  Si ``PREPEND_WWW`` es igual a ``True``, las URLs que no poseen el prefijo
  "www." serán redirigidas a la misma URL con el prefijo "www.".

  Ambas opciones tienen por objeto normalizar URLs. La filosofía es que cada
  URL debería existir en un -- y sólo un -- lugar. Técnicamente la URL
  ``example.com/bar`` es distinta de ``example.com/bar/``, la cual a su vez
  es distinta de ``www.example.com/bar/``. Un motor de búsqueda indexador
  trataría de forma separada estas URLs, lo cual es perjudicial para la
  valoración de tu sitio en el motor de búsqueda, por lo tanto es una buena
  práctica normalizar las URLs.

* *Maneja ETags basado en la configuración* ``USE_ETAGS``: ``ETags`` son una
  optimización a nivel HTTP para almacenar condicionalmente las páginas en
  la caché. Si ``USE_ETAGS`` es igual a ``True``, Django calculará una ETag
  para cada petición mediante la generación de un hash MD5 del contenido de
  la página, y se hará cargo de enviar respuestas ``Not Modified``, si es
  apropiado.

  Nota también que existe un middleware de ``GET`` condicional, que veremos
  en breve, el cual maneja ETags y hace algo más.

Middleware de compresión
------------------------

Clase middleware: ``django.middleware.gzip.GZipMiddleware``.

Este middleware comprime automáticamente el contenido para aquellos navegadores
que comprenden la compresión gzip (todos los navegadores modernos). Esto puede
reducir mucho la cantidad de ancho de banda que consume un servidor Web. La
desventaja es que esto toma un poco de tiempo de procesamiento para comprimir
las páginas.

Nosotros por lo general preferimos velocidad sobre ancho de banda, pero si tu
prefieres lo contrario, solo habilita este middleware.

Middleware de GET condicional
-----------------------------

Clase middleware: ``django.middleware.http.ConditionalGetMiddleware``.

Este middleware provee soporte para operaciones ``GET`` condicionales. Si la
respuesta contiene un encabezado ``Last-Modified`` o ``ETag``, y la petición
contiene ``If-None-Match`` o ``If-Modified-Since``, la respuesta es reemplazada
por una respuesta 304 ("Not modified"). El soporte para ``ETag`` depende de la
configuración ``USE_ETAGS`` y espera que el encabezado ``ETag`` de la respuesta
ya este previamente fijado. Como se señaló anteriormente, el encabezado ``ETag``
es fijado por el middleware Common.

También elimina el contenido de cualquier respuesta a una petición ``HEAD`` y
fija los encabezados de respuesta ``Date`` y ``Content-Length`` para todas las
peticiones.

Soporte para uso de proxy inverso (Middleware X-Forwarded-For)
--------------------------------------------------------------

Clase middleware: ``django.middleware.http.SetRemoteAddrFromForwardedFor``.

Este es el ejemplo que examinamos en la sección anterior "`Qué es middleware`_".
Este establece el valor de ``request.META['REMOTE_ADDR']`` basándose en el
valor de ``request.META['HTTP_X_FORWARDED_FOR']``, si este último está fijado.
Esto es útil si estas parado detrás de un proxy inverso que provoca que cada
petición ``REMOTE_ADDR`` sea fijada a ``127.0.0.1``.

.. warning:: Este middleware *no* permite validar ``HTTP_X_FORWARDED_FOR``.

    Si no estás detrás de un proxy inverso que establece
    ``HTTP_X_FORWARDED_FOR`` automáticamente, no uses este middleware.
    Cualquiera puede inventar el valor de ``HTTP_X_FORWARDED_FOR``, y ya que
    este establece ``REMOTE_ADDR`` basándose en ``HTTP_X_FORWARDED_FOR``,
    significa que cualquiera puede falsear su dirección IP.

    Solo usa este middleware cuando confíes absolutamente en el valor de
    ``HTTP_X_FORWARDED_FOR``.

Middleware de soporte para sesiones
-----------------------------------

Clase middleware: ``django.contrib.sessions.middleware.SessionMiddleware``.

Este middleware habilita el soporte para sesiones. Mira el
:doc:`capítulo 14<chapter14>` para más detalles.

Middleware de cache de todo el sitio
------------------------------------

Clase middleware: ``django.middleware.cache.CacheMiddleware``.

Este middleware almacena en la cache cada página impulsada por Django.
Este se analizó en detalle en él :doc:`capítulo 15<chapter15>`.

Middleware de transacción
-------------------------

Clase middleware: ``django.middleware.transaction.TransactionMiddleware``.

Este middleware asocia un ``COMMIT`` o ``ROLLBACK`` de la base de datos con una
fase de petición/respuesta. Si una vista de función se ejecuta con éxito, se
emite un ``COMMIT``. Si la vista provoca una excepción, se emite un
``ROLLBACK``.

El orden de este middleware en la pila es importante. Los módulos middleware que
se ejecutan fuera de este, se ejecutan con commit-on-save -- el comportamiento
por omisión de Django. Los módulos middleware que se ejecutan dentro de este
(próximos al final de la pila) estarán bajo el mismo control de transacción que
las vistas de función.

Mira el Apéndice B para obtener más información sobre las transacciones de base
de datos.

Middleware "X-View"
-------------------

Clase middleware: ``django.middleware.doc.XViewMiddleware``.

Este middleware envía cabeceras HTTP ``X-View`` personalizadas a peticiones HEAD
que provienen de direcciones IP definidas en la configuración ``INTERNAL_IPS``.
Esto es usado por el sistema automático de documentación de Django.

¿Qué sigue?
===========

Los desarrolladores Web y los diseñadores de esquemas de bases de datos no
siempre tienen el lujo de comenzar desde cero. En el
:doc:`próximo capítulo<chapter19>`, vamos a cubrir el modo de integrarse con
sistemas existentes, tales como esquemas de bases de datos que has heredado de
la década de los 80.

