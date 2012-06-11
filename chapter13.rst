==================
Capítulo 13: Cache
==================

Los sitios Web estáticos, en las que las páginas son servidas directamente a la
Web, generan un gran escalamiento. Una gran desventaja en los sitios Web
dinámicos, es precisamente eso, que son dinámicos. Cada vez que un usuario pide
una página, el servidor realiza una serie de cálculos--consultas a una base de
datos, renderizado de plantillas, lógica de negocio--para crear la página que el
visitante finalmente ve. Esto es costoso desde el punto de vista del
sobreprocesamiento.

Para la mayoría de las aplicaciones Web, esta sobrecarga no es gran cosa. La
mayoría de las aplicaciones Web no son el washingtonpost.com o Slashdot; son de
un tamaño pequeño a uno mediano, y con poco tráfico. Pero para los sitios con
tráfico de medio a alto es esencial bajar lo más que se pueda el costo de
procesamiento. He aquí cuando realizar un cache es de mucha ayuda.

*Colocar en cache* algo significa guardar el resultado de un cálculo costoso
para que no se tenga que realizar el mismo la próxima vez. Aquí mostramos un
pseudocódigo explicando como podría funcionar esto para una página Web
dinámica::

    dada una URL, buscar esa página en la cache
    si la página está en la cache:
        devolver la página en cache
    si no:
        generar la página
        guardar la página generada en la cache (para la próxima vez)
        devolver la página generada

Django incluye un sistema de cache robusto que permite guardar páginas
dinámicas para que no tengan que ser recalculadas cada vez que se piden. Por
conveniencia, Django ofrece diferentes niveles de granularidad de cache. Puedes
dejar en cache el resultado de diferentes vistas, sólo las piezas que son
difíciles de producir, o se puede dejar en cache el sitio entero.

Django también trabaja muy bien con caches de "upstream", tales como Squid
(http://www.squid-cache.org/) y las caches de los navegadores. Estos son los
tipos de cache que no controlas directamente pero a las cuales puedes proveerles
algunas pistas (vía cabeceras HTTP) acerca de qué partes de tu sitio deben ser
colocadas en cache y cómo.

Sigue leyendo para descubrir como usar el sistema de cache de Django. Cuando tu
sitio se parezca cada vez más a Slashdot, estarás contento de entender este
material.

Activar el Cache
================

El sistema de cache requiere sólo una pequeña configuración. A saber, tendrás
que decirle donde vivirán los datos de tu cache, si es en una base de datos, en
el sistema de archivos, o directamente en memoria. Esta es una decisión
importante que afecta el rendimiento de tu cache (si, algunos tipos de cache son
más rápidos que otros). La cache en memoria generalmente será mucho más rápida
que la cache en el sistema de archivos o la cache en una base de datos, porque
carece del trabajo de tocar los mismos.

Tus preferencias acerca de la cache van en ``CACHE_BACKEND`` en tu archivo de
configuración. Si usas cache y no especificas ``CACHE_BACKEND``, Django usará
``simple:///`` por omisión. Las siguientes secciones explican todos los valores
disponibles para ``CACHE_BACKEND``.

Memcached
---------

Por lejos la más rápida, el tipo de cache más eficiente para Django, Memcached
es un framework de cache enteramente en memoria, originalmente desarrollado para
manejar grandes cargas en LiveJournal (http://www.livejournal.com/) y
subsecuentemente por Danga Interactive (http://danga.com/). Es usado por sitios
como Slashdot y Wikipedia para reducir el acceso a bases de datos e incrementar
el rendimiento dramáticamente.

Memcached está libremente disponible en http://danga.com/memcached/. Corre como
un demonio y se le asigna una cantidad específica de memoria RAM. Su
característica principal es proveer una interfaz--una *super-liviana-y-rápida*
interfaz--para añadir, obtener y eliminar arbitrariamente datos en la cache.
Todos los datos son guardados directamente en memoria, por lo tanto no existe
sobrecarga de uso en una base de datos o en el sistema de archivos.

Después de haber instalado Memcached, es necesario que instales los *bindings*
Python para Memcached, los cuales no vienen con Django. Dichos *bindings* vienen
en un módulo de Python, ``memcache.py``, el cual está disponible en
http://www.tummy.com/Community/software/python-memcached/.

Para usar Memcached con Django, coloca ``CACHE_BACKEND`` como
``memcached://ip:puerto/``, donde ``ip`` es la dirección IP del demonio de
Memcached y ``puerto`` es el puerto donde Memcached está corriendo.

En el siguiente ejemplo, Memcached está corriendo en localhost (127.0.0.1) en el
puerto 11211::

    CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

Una muy buena característica de Memcached es su habilidad de compartir la cache
en varios servidores. Esto significa que puedes correr demonios de Memcached en
diferentes máquinas, y el programa seguirá tratando el grupo de diferentes
máquinas como una *sola* cache, sin la necesidad de duplicar los valores de la
cache en cada máquina. Para sacar provecho de esta característica con Django,
incluye todas las direcciones de los servidores en ``CACHE_BACKEND``, separados
por punto y coma.

En el siguiente ejemplo, la cache es compartida en varias instancias de
Memcached en las direcciones IP 172.19.26.240 y 172.19.26.242, ambas en el
puerto 11211::

    CACHE_BACKEND = 'memcached://172.19.26.240:11211;172.19.26.242:11211/'

En el siguiente ejemplo, la cache es compartida en diferentes instancias de
Memcached corriendo en las direcciones IP 172.19.26.240 (puerto 11211),
172.19.126.242 (puerto 11212) y 172.19.26.244 (puerto 11213)::

    CACHE_BACKEND = 'memcached://172.19.26.240:11211;172.19.26.242:11212;172.19.26.244:11213/'

Una última observación acerca de Memcached es que la cache basada en memoria
tiene una importante desventaja. Como los datos de la cache son guardados en
memoria, serán perdidos si los servidores se caen. Más claramente, la memoria no
es para almacenamiento permanente, por lo tanto no te quedes solamente con una
cache basada en memoria. Sin duda, *ninguno* de los sistemas de cache de Django
debe ser utilizado para almacenamiento permanente--son todos una solución para
la cache, no para almacenamiento--pero hacemos hincapié aquí porque la cache
basada en memoria es particularmente temporaria.

Cache en Base de datos
----------------------

Para usar una tabla de una base de datos como cache, tienes que crear una tabla
en tu base de datos y apuntar el sistema de cache de Django a ella.

Primero, crea la tabla de cache corriendo el siguiente comando::

    python manage.py createcachetable [nombre_tabla_cache]

Donde ``[nombre_tabla_cache]`` es el nombre de la tabla a crear. Este nombre
puede ser cualquiera que desees, siempre y cuando sea un nombre válido para una
tabla y que no esté ya en uso en tu base de datos. Este comando crea una única
tabla en tu base de datos con un formato apropiado para el sistema de cache de
Django.

Una vez que se hayas creado la tabla, coloca la propiedad ``CACHE_BACKEND`` como
``"db://nombre_tabla"``, donde ``nombre_tabla`` es el nombre de la tabla en la
base de datos. En el siguiente ejemplo, el nombre de la tabla para el cache es
``mi_tabla_cache``::

    CACHE_BACKEND = 'db://mi_tabla_cache'

El sistema de cache usará la misma base de datos especificada en el archivo de
configuración. No podrás usar una base de datos diferente para tal.

Cache en Sistema de Archivos
----------------------------

Para almacenar la cache en el sistema de archivos, coloca el tipo ``"file://"``
en la propiedad ``CACHE_BACKEND``, especificando el directorio en tu sistema de
archivos que debería almacenar los datos de la cache.

Por ejemplo, para almacenar los datos de la cache en ``/var/tmp/django_cache``,
coloca lo siguiente::

    CACHE_BACKEND = 'file:///var/tmp/django_cache'

Observa que hay tres barras invertidas en el comienzo del ejemplo anterior. Las
primeras dos son para ``file://``, y la tercera es el primer caracter de la ruta
del directorio, ``/var/tmp/django_cache``. Si estás en Windows, coloca la letra
correspondiente al disco después de ``file://``, como aquí:: ``file://c:/foo/bar``.

La ruta del directorio debe ser *absoluta*--debe comenzar con la raíz de tu
sistema de archivos. No importa si colocas una barra al final de la misma.

Asegúrate que el directorio apuntado por esta propiedad exista y que pueda ser
leído y escrito por el usuario del sistema usado por tu servidor Web para
ejecutarse.

Continuando con el ejemplo anterior, si tu servidor corre como usuario
``apache``, asegúrate que el directorio ``/var/tmp/django_cache`` exista y
pueda ser leído y escrito por el usuario ``apache``.

Cada valor de la cache será almacenado como un archivo separado conteniendo los
datos de la cache serializados ("pickled"), usando el módulo Python ``pickle``.
Cada nombre de archivo es una clave de la cache, modificado convenientemente
para que pueda ser usado por el sistema de archivos.

Cache en Memoria local
----------------------

Si quieres la ventaja que otorga la velocidad de la cache en memoria pero no
tienes la capacidad de correr Memcached, puedes optar por el cache de
memoria-local. Esta cache es por proceso y thread-safe, pero no es tan eficiente
como Memcache dada su estrategia de bloqueo simple y reserva de memoria.

Para usarla, coloca ``CACHE_BACKEND`` como ``'locmem:///'``, por ejemplo::

    CACHE_BACKEND = 'locmem:///'

Cache Simple (para desarrollo)
------------------------------

Una cache simple, y de un solo proceso en memoria, está disponible como
``'simple:///'``, por ejemplo::

    CACHE_BACKEND = 'simple:///'

Esta cache apenas guarda los datos en proceso, lo que significa que sólo debe
ser usada para desarrollo o testing.

Cache Dummy (o estúpida)
------------------------

Finalmente, Django incluye una cache "dummy" que no realiza cache; sólo
implementa la interfaz de cache sin realizar ninguna acción.

Esto es útil cuando tienes un sitio en producción que usa mucho cache en varias
partes y en un entorno de desarrollo/prueba en cual no quieres hacer cache. En
ese caso, usa ``CACHE_BACKEND`` como ``'dummy:///'`` en el archivo de
configuración para tu entorno de desarrollo, por ejemplo::

    CACHE_BACKEND = 'dummy:///'

Como resultado de esto, tu entorno de desarrollo no usará cache, pero tu entorno
de producción si lo hará.

Argumentos de CACHE_BACKEND
---------------------------

Cada tipo de cache puede recibir argumentos. Estos son dados como una
query-string en la propiedad ``CACHE_BACKEND``. Los argumentos válidos son:

* ``timeout``: El tiempo de vida por omisión, en segundos, que usará la
  cache. Este argumento tomará el valor de 300 segundos (5 minutos) si no se
  lo especifica.

* ``max_entries``: Para la cache simple, la cache de memoria local, y la
  cache de base de datos, es el número máximo de entradas permitidas en la
  cache a partir del cual los valores más viejos serán eliminados. Tomará un
  valor de 300 si no se lo especifica.

* ``cull_frequency``: La proporción de entradas que serán sacrificadas
  cuando la cantidad de ``max_entries`` es alcanzada. La proporción real
  es ``1/cull_frequency``, si quieres sacrificar la mitad de las entradas
  cuando se llegue a una cantidad de ``max_entries`` coloca
  ``cull_frequency=2``.

  Un valor de ``0`` para ``cull_frequency`` significa que toda la cache será
  limpiada cuando se llegue a una cantidad de entradas igual a
  ``max_entries``. Esto hace que el proceso de limpieza de la cache sea *mucho*
  más rápido pero al costo de perder más datos de la cache. Este argumento
  tomará un valor de 3 si no se especifica.

En este ejemplo, ``timeout`` se fija en ``60``::

    CACHE_BACKEND = "locmem:///?timeout=60"

En este ejemplo, ``timeout`` se fija en ``30`` y ``max_entries`` en ``400``::

    CACHE_BACKEND = "locmem:///?timeout=30&max_entries=400"

Tanto los argumentos desconocidos asi como los valores inválidos de argumentos
conocidos son ignorados silenciosamente.

La cache por sitio
==================

Una vez que hayas especificado ``CACHE_BACKEND``, la manera más simple de usar
la cache es colocar en cache el sitio entero. Esto significa que cada página que
no tenga parámetros GET o POST será puesta en cache por un cierto período de
tiempo la primera vez que sean pedidas.

Para activar la cache por sitio solamente agrega
``'django.middleware.cache.CacheMiddleware'`` a la propiedad
``MIDDLEWARE_CLASSES``, como en el siguiente ejemplo::

    MIDDLEWARE_CLASSES = (
        'django.middleware.cache.CacheMiddleware',
        'django.middleware.common.CommonMiddleware',
    )

.. admonition:: Nota:

    El orden de ``MIDDLEWARE_CLASSES`` importa. Mira la sección "`Orden de
    MIDDLEWARE_CLASSES`_" más adelante en este capítulo.

Luego, agrega las siguientes propiedades en el archivo de configuración de
Django:

    * ``CACHE_MIDDLEWARE_SECONDS``: El tiempo en segundos que cada página será
      mantenida en la cache.

    * ``CACHE_MIDDLEWARE_KEY_PREFIX``: Si la cache es compartida a través de
      múltiples sitios usando la misma instalación Django, coloca esta propiedad
      como el nombre del sitio, u otra cadena que sea única para la instancia de
      Django, para prevenir colisiones. Usa una cadena vacía si no te interesa.

La cache middleware coloca en cache cada página que no tenga parámetros GET o
POST. Esto significa que si un usuario pide una página y pasa parámetros GET en
la cadena de consulta, o pasa parámetros POST, la cache middleware *no*
intentará obtener la versión en cache de la página. Si intentas usar la cache
por sitio ten esto en mente cuando diseñes tu aplicación; no uses URLs con
cadena de consulta, por ejemplo, a menos que sea aceptable que tu aplicación no
coloque en cache esas páginas.

Esta cache middleware admite otras característica,
``CACHE_MIDDLEWARE_ANONYMOUS_ONLY``. Si defines esta característica, y la
defines como ``True``, la cache middleware sólo colocará en cache pedidos
anónimos (p.e.: pedidos hechos por un usuario no logueado). Esta es una manera
simple y efectiva de deshabilitar la cache para cualquier página de algún
usuario específico, como la interfaz de administración de Django. Ten en cuenta
que si usas ``CACHE_MIDDLEWARE_ANONYMOUS_ONLY``, deberás asegurarte que has
activado ``AuthenticationMiddleware`` y que ``AuthenticationMiddleware``
aparezca antes de ``CacheMiddleware`` en tus ``MIDDLEWARE_CLASSES``

Finalmente, nota que ``CacheMiddleware`` automáticamente coloca unos pocos
encabezados en cada ``HttpResponse``:

* Coloca el encabezado ``Last-Modified`` con el valor actual de la fecha y
  hora cuando una página (aún no en cache) es requerida.

* Coloca el encabezado ``Expires`` con el valor de la fecha y hora más el
  tiempo definido en ``CACHE_MIDDLEWARE_SECONDS``.

* Coloca el encabezado ``Cache-Control`` para otorgarle una vida máxima a la
  página, como se especifica en ``CACHE_MIDDLEWARE_SECONDS``.

Cache por vista
===============

Una forma más granular de usar el framework de cache es colocar en cache la
salida de las diferentes vistas. Esto tiene el mismo efecto que la cache por
sitio (incluyendo la omisión de colocar en cache los pedidos con parámetros GET
y POST). Se aplica a cualquier vista que tu especifiques, en vez de aplicarse al
sitio entero.

Haz esto usando un *decorador*, que es un wrapper de la función de la vista que
altera su comportamiento para usar la cache. El decorador de cache por vista es
llamado ``cache_page`` y se encuentra en el módulo
``django.views.decorators.cache``, por ejemplo:

.. code-block:: python

    from django.views.decorators.cache import cache_page

    def my_view(request, param):
        # ...
    my_view = cache_page(my_view, 60 * 15)

De otra manera, si estás usando la versión 2.4 o superior de Python, puedes usar
la sintaxis de un decorador. El siguiente ejemplo es equivalente al anterior::

    from django.views.decorators.cache import cache_page

    @cache_page(60 * 15)
    def my_view(request, param):
        # ...

``cache_page`` recibe un único argumento: el tiempo de vida en segundos de la
cache. En el ejemplo anterior, el resultado de ``my_view()`` estará en cache
unos 15 minutos. (toma nota de que lo hemos escrito como ``60 * 15`` para que
sea entendible. ``60 * 15`` será evaluado como ``900``--que es igual a 15
minutos multiplicados por 60 segundos cada minuto.)

La cache por vista, como la cache por sitio, es indexada independientemente de
la URL. Si múltiples URLs apuntan a la misma vista, cada URL será puesta en
cache separadamente.
Continuando con el ejemplo de ``my_view``, si tu URLconf se ve como::

    urlpatterns = ('',
        (r'^foo/(\d{1,2})/$', my_view),
    )

los pedidos a ``/foo/1/`` y a ``/foo/23/`` serán puestos en cache separadamente,
como es de esperar. Pero una vez que una misma URL es pedida (p.e.
``/foo/23/``), los siguientes pedidos a esa URL utilizarán la cache.

Especificar la cache por vista en URLconf
-----------------------------------------

Los ejemplos en la sección anterior tienen codificado [#]_ que la vista se
coloque en cache, porque ``cache_page`` modifica la función ``my_view`` ahí
mismo. Este enfoque acopla tu vista con el sistema de cache, lo
cual no es lo ideal por varias razones. Por ejemplo, puede que quieras reusar
las funciones de la vista en otro sitio sin cache, o puede que quieras
distribuir las vistas a gente que quiera usarlas sin que sean colocadas en la
cache. La solución para estos problemas es especificar la cache por vista en
URLconf en vez de especificarla junto a las vistas mismas.

Hacer eso es muy fácil: simplemente envuelve la función de la vista con
``cache_page`` cuando hagas referencia a ella en URLconf. Aquí el URLconf como
estaba antes::

    urlpatterns = ('',
        (r'^foo/(\d{1,2})/$', my_view),
    )

Ahora la misma cosa con ``my_view`` envuelto con ``cache_page``::

    from django.views.decorators.cache import cache_page

    urlpatterns = ('',
        (r'^foo/(\d{1,2})/$', cache_page(my_view, 60 * 15)),
    )

Si tomas este enfoque no olvides de importar ``cache_page`` dentro de tu
URLconf.

La API de cache de bajo nivel
=============================

Algunas veces, colocar en cache una página entera no te hace ganar mucho y es,
de hecho, un inconveniente excesivo.

Quizás, por ejemplo, tu sitio incluye una vista cuyos resultados dependen de
diversas consultas costosas, lo resultados de las cuales cambian en intervalos
diferentes. En este caso, no sería ideal usar la página entera en cache que la
cache por sitio o por vista ofrecen, porque no querrás guardar en cache todo el
resultado (ya que los resultados cambian frecuentemente), pero querrás guardar
en cache los resultados que rara vez cambian.

Para casos como este, Django expone una simple API de cache de bajo nivel, la
cual vive en el módulo ``django.core.cache``. Puedes usar la API de cache de
bajo nivel para almacenar los objetos en la cache con cualquier nivel de
granularidad que te guste. Puedes colocar en la cache cualquier objeto Python
que pueda ser serializado de forma segura: strings, diccionarios, listas de
objetos del modelo, y demás. (La mayoría de los objetos comunes de Python pueden
ser serializados; revisa la documentación de Python para más información acerca
de serialización).  N.T.: pickling

Aquí vemos como importar la API::

    >>> from django.core.cache import cache

La interfaz básica es ``set(key, value, timeout_seconds)`` y ``get(key)``:

.. code-block:: python 

    >>> cache.set('my_key', 'hello, world!', 30)
    >>> cache.get('my_key')
    'hello, world!'

El argumento ``timeout_seconds`` es opcional y obtiene el valor del argumento
``timeout`` de ``CACHE_BACKEND``, explicado anteriormente, si no se lo
especifica.

Si el objeto no existe en la cache, o el sistema de cache no se puede alcanzar,
``cache.get()`` devuelve ``None``:

.. code-block:: python 

    # Wait 30 seconds for 'my_key' to expire...

    >>> cache.get('my_key')
    None

    >>> cache.get('some_unset_key')
    None

Te recomendamos que no almacenes el valor literal ``None`` en la cache, porque
no podrás distinguir entre tu valor ``None`` almacenado y el valor que devuelve
la cache cuando no encuentra un objeto.

``cache.get()`` puede recibir un argumento por omisión. Esto especifica qué
valor debe devolver si el objeto no existe en la cache::

    >>> cache.get('my_key', 'has expired')
    'has expired'

Para obtener múltiples valores de la cache de una sola vez, usa
``cache.get_many()``. Si al sistema de cache le es posible, ``get_many()``
tocará la cache sólo una vez, al contrario de tocar la cache por cada valor.
``get_many()`` devuelve un diccionario con todas las key que has pedido que
existen en la cache y todavía no han expirado::

    >>> cache.set('a', 1)
    >>> cache.set('b', 2)
    >>> cache.set('c', 3)
    >>> cache.get_many(['a', 'b', 'c'])
    {'a': 1, 'b': 2, 'c': 3}

Si una key no existe o ha expirado, no será incluida en el diccionario. Lo
siguiente es una continuación del ejemplo anterior::

    >>> cache.get_many(['a', 'b', 'c', 'd'])
    {'a': 1, 'b': 2, 'c': 3}

Finalmente, puedes eliminar keys explícitamente con ``cache.delete()``. Esta es
una manera fácil de limpiar la cache para un objeto en particular::

    >>> cache.delete('a')

``cache.delete()`` no tiene un valor de retorno, y funciona de la misma manera
si existe o no un valor en la cache.

Caches upstream
===============

Este capítulo se ha enfocado en la cache de tus *propios* datos. Pero existe
otro tipo de cache que es muy importante para los desarrolladores web: la cache
realizada por los *upstream*. Estos son sistemas que colocan en cache páginas
aún antes de que estas sean pedidas a tu sitio Web.

Aquí hay algunos ejemplos de caches para upstream:

* Tu ISP puede tener en cache algunas páginas, si tu pides una página de
  http://example.com/, tu ISP te enviará la página sin tener que acceder a
  example.com directamente. Los responsables de example.com no tienen idea
  que esto pasa; el ISP se coloca entre example.com y tu navegador,
  manejando todo lo que se refiera a cache transparentemente.

* Tu sitio en Django puede colocarse detrás de un *cache proxy*, como
  Squid Web Proxy Cache (http:://www.squid-cache.org/), que coloca en
  cache páginas para un mejor rendimiento. En este caso, cada pedido será
  controlado por el proxy antes que nada, y será pasado a tu aplicación sólo
  si es necesario.

* Tu navegador también pone páginas en un cache. Si una página Web envía
  unos encabezados apropiados, tu navegador usará su copia de la cache local
  para los siguientes pedidos a esa página, sin siquiera hacer nuevamente
  contacto con la página web para ver si esta ha cambiado.

La cache de upstream es un gran beneficio, pero puede ser peligroso. El
contenido de muchas páginas Web pueden cambiar según la autenticación que se
haya realizado u otras variables, y los sistemas basados en almacenar en cache
según la URL pueden exponer datos incorrectos o delicados a diferentes
visitantes de esas páginas.

Por ejemplo, digamos que manejas un sistema de e-mail basado en Web, el
contenido de la "bandeja de entrada" obviamente depende de que usuario esté
logueado. Si el ISP hace caching de tu sitio ciegamente, el primer usuario que
ingrese al sistema compartirá su bandeja de entrada, que está en cache, con los
demás usuarios del sistema. Eso, definitivamente no es bueno.

Afortunadamente, el protocolo HTTP provee una solución a este problema. Existen
un número de encabezados HTTP que indican a las cache de upstream que
diferencien sus contenidos de la cache dependiendo de algunas variables, y para
que algunas páginas particulares no se coloquen en cache. Veremos algunos de
estos encabezados en las secciones que siguen.

Usar el encabezado Vary
-----------------------

El encabezado ``Vary`` define cuales encabezados debería tener en cuenta un
sistema de cache cuando construye claves de su cache. Por ejemplo, si el
contenido de una página Web depende de las preferencias de lenguaje del usuario,
se dice que la página "varía según el lenguaje".

Por omisión, el sistema de cache de Django crea sus claves de cache usando la
ruta que se ha requerido (p.e.: ``"/stories/2005/jun/23/bank_robbed/"``). Esto
significa que cada pedido a esa URL usará la misma versión de cache,
independientemente de las características del navegador del cliente, como las
cookies o las preferencias del lenguaje. Sin embargo, si esta página produce
contenidos diferentes basándose en algunas cabeceras del request--como las
cookies, el lenguaje, o el navegador--necesitarás usar el encabezado ``Vary``
para indicarle a la cache que esa página depende de esas cosas.

Para hacer esto en Django, usa el decorador ``vary_on_headers`` como sigue:

.. code-block:: python 

    from django.views.decorators.vary import vary_on_headers

    # Python 2.3 syntax.
    def my_view(request):
        # ...
    my_view = vary_on_headers(my_view, 'User-Agent')

    # Python 2.4+ decorator syntax.
    @vary_on_headers('User-Agent')
    def my_view(request):
        # ...

En este caso, el mecanismo de cache (como middleware) colocará en cache una
versión distinta de la página para cada tipo de user-agent.

La ventaja de usar el decorador ``vary_on_headers`` en vez de fijar manualmente
el encabezado ``Vary`` (usando algo como ``response['Vary'] = 'user-agent'``) es
que el decorador *agrega* al encabezado ``Vary`` (el cual podría ya existir), en
vez de fijarlo desde cero y potencialmente sobrescribir lo que ya había ahí.

Puedes pasar múltiples encabezados a ``vary_on_headers()``:

.. code-block:: python 

    @vary_on_headers('User-Agent', 'Cookie')
    def my_view(request):
        # ...

Esto le dice a la cache de upstream que diferencie *ambos*, lo que significa que
cada combinación de una cookie y un navegador obtendrá su propio valor en cache.
Por ejemplo, un pedido con navegador ``Mozilla`` y una cookie con el valor
``foo=bar`` será considerada diferente a un pedido con el navegador ``Mozilla``
y una cookie con el valor ``foo=ham``.

Como las variaciones con las cookies son tan comunes existe un decorador
``vary_on_cookie``. Las siguientes dos vistas son equivalentes:

.. code-block:: python 


    @vary_on_cookie
    def my_view(request):
        # ...

    @vary_on_headers('Cookie')
    def my_view(request):
        # ...

El encabezado que le pasas a ``vary_on_headers`` no diferencia mayúsculas de
minúsculas; ``"User-Agent"`` es lo mismo que ``"user-agent"``.

También puedes usar ``django.utils.cache.patch_vary_headers`` como función de
ayuda. Esta función fija o añade al ``Vary header``, por ejemplo:

.. code-block:: python 

    from django.utils.cache import patch_vary_headers

    def my_view(request):
        # ...
        response = render_to_response('template_name', context)
        patch_vary_headers(response, ['Cookie'])
        return response

``patch_vary_headers`` obtiene una instancia de ``HttpResponse`` como su primer
argumento y una lista/tupla de nombres de encabezados, sin diferenciar
mayúsculas de minúsculas, como su segundo argumento.

Otros Encabezados de cache
--------------------------

Otro problema con la cache es la privacidad de los datos y donde deberían
almacenarse los datos cuando se hace un vuelco de la cache.

El usuario generalmente se enfrenta con dos tipos de cache: su propia cache de
su navegador (una cache privada) y la cache de su proveedor (una cache pública).
Una cache pública es usada por múltiples usuarios y controlada por algunos
otros. Esto genera un problema con datos sensibles--no quieres que, por ejemplo,
el número de tu cuenta bancaria sea almacenado en una cache pública. Por lo que
las aplicaciones Web necesitan una manera de indicarle a la cache cuales datos
son privados y cuales son públicos.

La solución es indicar que la copia en cache de una página es "privada". Para
hacer esto en Django usa el decorador de vista ``cache_control``:

.. code-block:: python 

    from django.views.decorators.cache import cache_control

    @cache_control(private=True)
    def my_view(request):
        # ...

Este decorador se encarga de enviar los encabezados HTTP apropiados detrás de
escena.

Existen otras pocas maneras de controlar los parámetros de cache. Por ejemplo,
HTTP permite a las aplicaciones hacer lo siguiente:

    * Definir el tiempo máximo que una página debe estar en cache.

    * Especificar si una cache debería comprobar siempre la existencia de nuevas
      versiones, entregando unicamente el contenido de la cache cuando no
      hubiesen cambios.  (Algunas caches pueden entregar contenido aun si la
      página en el servidor ha cambiado, simplemente porque la copia en cache
      todavía no ha expirado.)

En Django, utiliza el decorador ``cache_control`` para especificar estos
parámetros de la cache. En el siguiente ejemplo, ``cache_control`` le indica a
la cache revalidarse en cada acceso y almacenar versiones en cache hasta
3.600 segundos:

.. code-block:: python 

    from django.views.decorators.cache import cache_control
    @cache_control(must_revalidate=True, max_age=3600)
    def my_view(request):
        ...

Cualquier directiva ``Cache-Control`` de HTTP válida es válida en
``cache_control()``.
Aquí hay una lista completa:

    * ``public=True``
    * ``private=True``
    * ``no_cache=True``
    * ``no_transform=True``
    * ``must_revalidate=True``
    * ``proxy_revalidate=True``
    * ``max_age=num_seconds``
    * ``s_maxage=num_seconds``


.. admonition:: Tip

    Para una explicación de las directivas ``Cache-Control`` de HTTP, lea las
    especificaciones en
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9.

El middleware de caching ya fija el encabezado ``max-age`` con el valor de
``CACHE_MIDDLEWARE_SETTINGS``. Si utilizas un valor propio de ``max_age`` en
un decorador ``cache_control``, el decorador tendrá precedencia, y los
valores del encabezado serán fusionados correctamente.

Otras optimizaciones
====================

Django incluye otras piezas de middleware que pueden ser de ayuda para
optimizar el rendimiento de tus aplicaciones:

* ``django.middleware.http.ConditionalGetMiddleware`` agrega soporte para
  navegadores modernos para condicionar respuestas GET basadas en los
  encabezados ``ETag`` y ``Las-Modified``.

* ``django.middleware.gzip.GZipMiddleware`` comprime las respuestas para
  todos los navegadores modernos, ahorrando ancho de banda y tiempo de
  transferencia.

Orden de MIDDLEWARE_CLASSES
===========================

Si utilizas ``CacheMiddleware``, es importante colocarlas en el lugar
correcto dentro de la propiedad ``MIDDLEWARE_CLASSES``, porque el middleware
de cache necesita conocer los encabezados por los cuales cambiar el
almacenamiento en la cache.

Coloca el ``CacheMiddleware`` después de cualquier middleware que pueda agregar algo
al encabezado ``Vary``, incluyendo los siguientes:

* ``SessionMiddleware``, que agrega ``Cookie``
* ``GZipMiddleware``, que agrega ``Accept-Encoding``

¿Qué sigue?
===========

Django incluye un número de paquetes opcionales. Hemos cubierto algunos de los
mismos: el sistema de administración (:doc:`Capítulo 6<chapter06>`) y el marco de
sesiones/usuarios (:doc:`Capítulo 11<chapter11>`).

El :doc:`próximo capítulo<chapter14>` cubre el resto de los marcos de trabajos "de la
comunidad". Existen una cantidad interesante de herramientas disponibles; no
querrás perderte ninguna de ellas.


.. [#] \N. del T.: hard-coded



