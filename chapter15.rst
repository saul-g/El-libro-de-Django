==================
Capítulo 15: Cache
==================

Los sitios Web estáticos, en los que las páginas son servidas directamente por el
servidor Web, generan un gran escalamiento. Una gran desventaja en los sitios Web
dinámicos, es precisamente eso, que son dinámicos. Cada vez que un usuario pide
una página, el servidor realiza una serie de cálculos --consultas a una base de
datos, renderizado de plantillas, lógica de negocio --para crear la página que
el visitante finalmente ve. Esto es costoso desde el punto de vista del
sobreprocesamiento.

Para la mayoría de las aplicaciones Web, esta sobrecarga no es gran cosa. La
mayoría de las aplicaciones Web no son el washingtonpost o Slashdot; son de
un tamaño pequeño a uno mediano, y con poco tráfico. Pero para los sitios con
tráfico de medio a alto es esencial bajar lo más que se pueda el costo de
procesamiento. He aquí cuando realizar un cache es de mucha ayuda.

**Colocar en cache** algo significa guardar el resultado de un cálculo costoso
para que no se tenga que realizar el mismo la próxima vez. Aquí mostramos un
pseudocódigo explicando cómo podría funcionar esto para una página Web
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

Django también trabaja muy bien con caches de "downstream", tales como `Squid
<http://www.squid-cache.org>`_  y las caches de los navegadores. Estos son los
tipos de cache que no controlas directamente pero a las cuales puedes proveerles
algunas pistas (vía cabeceras HTTP) acerca de qué partes de tu sitio deben ser
colocadas en cache y cómo.

Sigue leyendo para descubrir cómo usar el sistema de cache de Django. Cuando tu
sitio se parezca cada vez más a Slashdot, estarás contento de entender este
material.

Activar el Cache
================

El sistema de cache requiere sólo una pequeña configuración. A saber, tendrás
que decirle donde vivirán los datos de tu cache, si es en una base de datos, en
el sistema de archivos, o directamente en memoria. Esta es una decisión
importante que afecta el rendimiento de la cache (si, algunos tipos de cache son
más rápidos que otros). La cache en memoria generalmente será mucho más rápida
que la cache en el sistema de archivos o la cache en una base de datos, porque
carece del trabajo de tocar los mismos.

Tus preferencias acerca de la cache van en la variable ``CACHE`` en el archivo
de configuración. A continuación daremos un recorrido por todos los valores y
configuraciones disponibles que puedes usar para configurar la ``CACHE``.

Memcached
---------

Por mucho, el más rápido y eficiente soporte nativo de cache para Django es
memcached, el cual es un framework de cache basado enteramente en memoria,
originalmente desarrollado para manejar grandes cargas en LiveJournal
(http://www.livejournal.com/)y subsecuentemente por Danga Interactive
(http://danga.com/). Es usado por sitios como Slashdot y Wikipedia para reducir
el acceso a bases de datos e incrementar el rendimiento dramáticamente.

`Memcached`_ está disponible libremente para descargar. Corre como un demonio y
se le asigna una cantidad específica de memoria RAM. Su característica principal
es proveer una interfaz -- *super-liviana-y-rápida* para añadir, obtener y
eliminar arbitrariamente datos en la cache. Todos los datos son guardados
directamente en  memoria, por lo tanto no existe sobrecarga de uso en una base
de datos o en el sistema de archivos.

.. _`Memcached`: http://Memcached.org/

Después de haber instalado Memcached, es necesario que instales alguno de los
adaptadores disponibles para usar Python con Memcached, los cuales no vienen
incluidas con Django. Dichos *adaptadores* pueden ser  `python-memcached`_  y/o
`pylibmc`_. Los cuales están disponibles como módulos de Python.

.. _`python-memcached`: ftp://ftp.tummy.com/pub/python-memcached/
.. _`pylibmc`: http://sendapatch.se/projects/pylibmc/

Para usar Memcached con Django, usa como ``BACKEND``  a:
``django.core.cache.backends.memcached.MemcachedCache`` o
``django.core.cache.backends.memcached.PyLibMCCache`` (Dependiendo de
el adaptador que hayas elegido usar). Fija el valor de  ``LOCATION`` como
``ip:puerto``, donde ``ip`` es la dirección IP del demonio de Memcached y
``puerto`` es el puerto donde Memcached está corriendo o usa los valores
unix:path, donde ``path`` es la ruta al archivo usado como socket en unix por
Memcached.

En el siguiente ejemplo, Memcached está corriendo en localhost (127.0.0.1) en el
puerto 11211, usando como dependencia ``python-memcached``::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

En el siguiente ejemplo, Memcache está disponible a través de el socket local
unix, que usa el archivo ``/tmp/memcached.sock`` como socket, usando los enlaces
proporcionados por ``python-memcached``::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': 'unix:/tmp/memcached.sock',
        }
    }

Una muy buena característica de Memcached es su habilidad de compartir la cache
en varios servidores. Esto significa que puedes correr demonios de Memcached en
diferentes máquinas, y el programa seguirá tratando el grupo de diferentes
máquinas como una *sola* cache, sin la necesidad de duplicar los valores de la
cache en cada máquina. Para sacar provecho de esta característica con Django,
incluye todas las direcciones de los servidores en ``LOCATION``, separados
por punto y coma.

En el siguiente ejemplo, la cache es compartida en varias instancias de
Memcached en las direcciones IP 172.19.26.240 y 172.19.26.242, ambas en el
puerto 11211::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [
                '172.19.26.240:11211',
                '172.19.26.242:11211',
            ]
        }
    }

En el siguiente ejemplo, la cache es compartida en diferentes instancias de
Memcached corriendo en las direcciones IP 172.19.26.240 (puerto 11211),
172.19.126.242 (puerto 11212) y 172.19.26.244 (puerto 11213)::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': [
                '172.19.26.240:11211',
                '172.19.26.242:11212',
                '172.19.26.244:11213',
            ]
        }
    }

Una última observación acerca de Memcached es que la cache basada en memoria
tiene una importante desventaja. Como los datos de la cache son guardados en
memoria, serán perdidos si los servidores se caen. Más claramente, la memoria no
es para almacenamiento permanente, por lo tanto no te quedes solamente con una
cache basada en memoria. Sin duda, *ninguno* de los sistemas de cache de Django
debe ser utilizado para almacenamiento permanente --son todos una solución para
la cache, no para almacenamiento pero hacemos hincapié aquí porque la cache
basada en memoria es únicamente para uso temporal.

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

Una vez que se hayas creado la tabla, usa la propiedad ``LOCATION`` como
``LOCATION:nombre_tabla``, donde ``nombre_tabla`` es el nombre de la tabla en la
base de datos y usa como ``BACKEND`` ``django.core.cache.backends.db.DatabaseCache``

En el siguiente ejemplo, el nombre de la tabla para el cache es
``mi_tabla_cache``::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'mi_tabla_cache',
        }
    }

El sistema de cache usará la misma base de datos especificada en el archivo de
configuración. Por lo que no podrás usar una base de datos diferente, a menos
que la registres primero.

Cache en Sistema de Archivos
----------------------------

Para almacenar la cache en el sistema de archivos y almacenar cada valor de la
cache como un archivo separado, configura la propiedad ``BACKEND`` usando
``django.core.cache.backends.filebased.FileBasedCache`` y especificando en
``LOCATION`` el directorio en tu sistema de archivos que debería almacenar los
datos de la cache.

Por ejemplo, para almacenar los datos de la cache en ``/var/tmp/django_cache``,
coloca lo siguiente::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
        }

Si usas Windows, especifica la letra de la unidad al comienzo de la ruta de
directorios de esta forma::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': 'c:/usuarios/temp',
        }
    }

La ruta de directorios, debe ser *absoluta* --debe comenzar con la raíz de tu
sistema de archivos. No importa si colocas una barra al final de la misma.

Asegúrate que el directorio apuntado por esta propiedad exista y que pueda ser
leído y escrito por el usuario del sistema usado por tu servidor Web, para
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

Si quieres usar la ventaja que otorga la velocidad de la cache en memoria, pero
no tienes la capacidad de correr Memcached, puedes optar por el cache de
memoria-local. Esta cache es por proceso y usa hilos-seguros, pero no es tan
eficiente como Memcache dada su estrategia de bloqueo simple y reserva de memoria.

Para usarla, usa como ``BACKEND`` a ``django.core.cache.backends.locmem.LocMemCache``
por ejemplo::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unico-proceso'
        }
    }

El atributo ``LOCATION`` de la cache es usada para identificar de forma
individual el almacenamiento de la memoria. Si  utilizas únicamente un proceso
puedes omitir ``LOCATION``; sin embargo si utilizas más de uno, necesitas
asignar un nombre a al menos uno de los procesos para mantenerlos separados.

Observa que cada proceso tendrá su propia instancia de cache privada, lo cual
significa que no es posible el proceso cruzado de cache. Esto obviamente también
significa que la memoria local de cache no es particularmente muy eficiente,
así que no es una buena opción para usar en ambientes de producción. Es
recomendable solo para desarrollo.

Cache personalizada
-------------------

A pesar de que Django incluye soporte para el uso de un buen número de sistemas
de cache fuera de la caja, algunas veces puede que quieras usar un
almacenamiento de cache personalizado, para fines específicos.

Para usar almacenamiento externo de cache con  Django, usa la ruta de
importaciones de  Python como ``BACKEND`` y carga la configuración de la cache
así::

      CACHES = {
          'default': {
              'BACKEND': 'ruta.a.backend',
          }
      }

Si estas construyendo tu propio sistema de cache, puedes usar  el sistema de
almacenamiento de caches de Django como referencia para implementar el tuyo.
Puedes encontrar el código fuente en el directorio ubicado en:
``django/core/cache/backends/``

Cache tonta (para desarrollo)
-----------------------------

Finalmente, Django incluye una cache tonta formalmente llamada: "dummy" que no
realiza cache; sólo implementa la interfaz de cache sin realizar ninguna acción.

Esta es útil cuando tienes un sitio en producción que usa mucho cache en varias
partes y en un entorno de desarrollo/prueba en el cual no quieres hacer cache.
En ese caso, usa ``BACKEND`` como ``django.core.cache.backends.dummy.DummyCache``
en el archivo de configuración para tu entorno de desarrollo, por ejemplo::

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }

Como resultado de esto, tu entorno de desarrollo no usará cache, pero tu entorno
de producción si lo hará.

Argumentos de cache
-------------------

Cada tipo de cache puede recibir argumentos adicionales para controlar el
comportamiento de la cache. Estos son dados como una  clave adicional a la
configuración de ``CACHES``. Los argumentos válidos son los siguientes:

* ``TIMEOUT``: El tiempo de vida por omisión, en segundos, que usará la
  cache. Este argumento tomará el valor de 300 segundos (5 minutos) si no se
  lo especifica.

  También puedes especificar ``TIMEOUT`` como ``None``, por defecto la clave de
  la cache nunca expira.

* ``OPTIONS``: Cualquier opción que se necesite pasar a la cache. La lista de
  opciones validas dependerá de cada ``backend``, por lo que el almacenamiento
  de cache proporcionado por librerías de terceros, será pasado con sus opciones
  directamente bajo la cache de la librería.

Los almacenamientos de cache que implementan sus propias estrategias de selección
(por ejemplo: en memoria, archivos y en base de datos) respetan las siguientes
opciones:

* ``MAX_ENTRIES``: Para la cache de memoria local, y la cache de base de datos,
  es el número máximo de entradas permitidas en la cache a partir del cual los
  valores más viejos serán eliminados. Tomará un valor de 300 si no se lo
  especifica.

* ``CULL_FREQUENCY``: La proporción de entradas que serán sacrificadas
  cuando la cantidad de ``MAX_ENTRIES`` es alcanzada. La proporción real
  es ``1/CULL_FREQUENCY``, si quieres sacrificar la mitad de las entradas
  cuando se llegue a una cantidad de ``MAX_ENTRIES`` coloca
  ``CULL_FREQUENCY=2``. Este argumento tomará un valor de 3 si no se especifica.

  Un valor de ``0`` para ``CULL_FREQUENCY`` significa que toda la cache será
  limpiada cuando se llegue a una cantidad de entradas igual a
  ``MAX_ENTRIES``. Esto hace que el proceso de limpieza de la cache sea *mucho*
  más rápido,  con el costo de perder más datos de la cache. Este argumento
  tomará un valor de 3 si no se especifica.

* ``KEY_PREFIX``: Una cadena que automáticamente incluye (agrega por default)
  todas las claves de caches usadas por el servidor Django.

* ``VERSION`` El número de versión de las claves de cache generadas por el
  servidor Django.

* ``KEY_FUNCTION``: Una cadena que contiene la ruta (usando el punto) a la
  función que define la forma en que está compuesta el prefijo, la versión y la
  clave, en la clave de la cache final

En este ejemplo, usamos un "archivo" como almacenamiento de cache (BACKEND),
configurado con un valor de tiempo de 60 segundos (TIMEOUT) y con una capacidad
máxima (MAX_ENTRIES) de 1000 ítems::

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/var/tmp/django_cache',
                'TIMEOUT': 60,
                'OPTIONS': {
                    'MAX_ENTRIES': 1000
                }
            }
        }

Tanto los argumentos desconocidos,  así como los valores inválidos de argumentos
conocidos son ignorados silenciosamente.

La cache por sitio
==================

Una vez que hayas especificado ``CACHE``, la manera más simple de usar
la cache es colocar en cache el sitio entero. Esto significa que cada página que
no tenga parámetros GET o POST será puesta en cache por un cierto período de
tiempo la primera vez que sean pedidas.

Para activar la cache por sitio solamente agrega
``'django.middleware.cache.CacheMiddleware'`` y
``django.middleware.cache.FetchFromCacheMiddleware`` a la propiedad
``MIDDLEWARE_CLASSES``, como en el siguiente ejemplo::

        MIDDLEWARE_CLASSES = (
            'django.middleware.cache.UpdateCacheMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.cache.FetchFromCacheMiddleware',
        )

.. admonition:: Nota:

    El orden de ``MIDDLEWARE_CLASSES`` importa. Mira la sección "`Orden de
    MIDDLEWARE_CLASSES`_" más adelante en este capítulo.

Luego, agrega las siguientes propiedades en el archivo de configuración de
Django:

* ``CACHE_MIDDLEWARE_ALIAS``: El nombre del alias para usar como almacenaje.

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

Finalmente, nota que ``CacheMiddleware`` automáticamente coloca unos pocos
encabezados en cada ``HttpResponse``:

* Coloca el encabezado ``Last-Modified`` con el valor actual de la fecha y
  hora cuando una página (aún no en cache) es requerida.

* Coloca el encabezado ``Expires`` con el valor de la fecha y hora más el
  tiempo definido en ``CACHE_MIDDLEWARE_SECONDS``.

* Coloca el encabezado ``Cache-Control`` para otorgarle una vida máxima a la
  página, como se especifica en ``CACHE_MIDDLEWARE_SECONDS``.

Cache para vistas
=================

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

    def mi_vista(request, param):
        # ...
    mi_vista = cache_page(mi_vista, 60 * 15)

De otra manera, si estás usando alguna versión de Python, superior a la 2.7,
puedes usar un decorador. El siguiente ejemplo es equivalente al anterior:

.. code-block:: python

    from django.views.decorators.cache import cache_page

    @cache_page(60 * 15)
    def mi_vista(request, param):

    # ...

``cache_page`` recibe un único argumento: el tiempo de vida en segundos de la
cache. En el ejemplo anterior, el resultado de ``mi_vista()`` estará en cache
unos 15 minutos. (toma nota de que lo hemos escrito como ``60 * 15`` para que
sea entendible. ``60 * 15`` será evaluado como ``900`` --que es igual a 15
minutos multiplicados por 60 segundos cada minuto.)

La cache por vista, como la cache por sitio, es indexada independientemente de
la URL. Si múltiples URLs apuntan a la misma vista, cada URL será puesta en
cache separadamente.

Continuando con el ejemplo de ``mi_vista``, si tu URLconf se ve como::

    urlpatterns = [
        url(r'^foo/([0-9]{1,2})/$', mi_vista),
    ]

los pedidos a ``/foo/1/`` y a ``/foo/23/`` serán puestos en cache separadamente,
como es de esperar. Pero una vez que una misma URL es pedida (p.e.
``/foo/23/``), los siguientes pedidos a esa URL utilizarán la cache.

``cache_page``  toma un argumento de clave opcional: llamado ``cache``, el cual
puede usarse directamente en el decorador especificando la cache (tomada de el
archivo de configuración de la variable ``CACHE``) para cachear la vista. Por
defecto, el cache para usar será especificado con cualquier cache que queramos,
por ejemplo:

.. code-block:: python

      @cache_page(60 * 15, cache="cache_especial")
      def mi_vista(request):
          ...
          algun_metodo()

También es posible sobrescribir el prefijo de la cache en la vista. el
decorador ``cache_page`` toma un argumento de clave ``key_prefix``, el cual
trabaja de la misma forma que la configuración ``CACHE_MIDDLEWARE_KEY_PREFIX``
en el middleware. Puede usarse de la siguiente forma:

.. code-block:: python

        @cache_page(60 * 15, key_prefix="sitio1")
        def mi_vista(request):
            ...
            algun_metodo()

Las dos configuraciones pueden ser combinadas. Si especificas ``cache`` y
``key_prefix`` puedes traer todas las configuraciones en la petición usando
alias en la cache, solo que esto sobrescribirá  el argumento ``key_prefix``.

Cache por vista en la URLconf
-----------------------------

Los ejemplos en la sección anterior incrustan [#]_  la cache en las vistas,
porque el decorador ``cache_page`` modifica la función ``mi_vista`` en la misma
vista. Este enfoque acopla tu vista con el sistema de cache, lo cual no es lo
ideal por varias razones. Por ejemplo, puede que quieras rehusar las funciones
de la vista en otro sitio sin cache, o puede que quieras distribuir las vistas
a gente que quiera usarlas sin que sean colocadas en la cache. La solución para
estos problemas es especificar la cache por vista en URLconf en vez de
especificarla junto a las vistas mismas.

Hacer eso es muy fácil: simplemente envuelve la función de la vista con
``cache_page`` cuando hagas referencia a ella en la URLconf. Aquí el URLconf
como estaba antes::

    urlpatterns = [
        url(r'^foo/([0-9]{1,2})/$', mi_vista),
    ]

Ahora la misma cosa con ``mi_vista`` envuelto con ``cache_page``::

    from django.views.decorators.cache import cache_page

    urlpatterns = [
        url(r'^foo/([0-9]{1,2})/$', cache_page(60 * 15)(mi_vista)),
    ]

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

La interfaz básica es ``set(key, value, timeout)`` y ``get(key)``:

.. code-block:: python

    >>> cache.set('mi_clave', '¡Hola Mundo!', 30)
    >>> cache.get('mi_clave')
    '¡Hola Mundo!'

El argumento ``timeout`` es opcional y obtiene el valor del argumento
``timeout`` de la variable ``CACHE``, explicado anteriormente, si no se lo
especifica.

Si el objeto no existe en la cache, o el sistema de cache no se puede alcanzar,
``cache.get()`` devuelve ``None``:

.. code-block:: python

    # Wait 30 seconds for 'mi_clave' to expire...

    >>> cache.get('mi_clave')
    None

    >>> cache.get('otra_clave')
    None

Te recomendamos que no almacenes el valor literal ``None`` en la cache, porque
no podrás distinguir entre tu valor ``None`` almacenado y el valor que devuelve
la cache cuando no encuentra un objeto.

``cache.get()`` puede recibir un argumento por omisión. Esto especifica qué
valor debe devolver si el objeto no existe en la cache::

    >>> cache.get('mi_clave', 'ha expirado')
    'ha expirado'

Para obtener múltiples valores de la cache de una sola vez, usa
``cache.get_many()``. Si al sistema de cache le es posible, ``get_many()``
tocará la cache sólo una vez, al contrario de tocar la cache por cada valor.
``get_many()`` devuelve un diccionario con todas las claves que has pedido que
existen en la cache y todavía no han expirado::

    >>> cache.set('a', 1)
    >>> cache.set('b', 2)
    >>> cache.set('c', 3)
    >>> cache.get_many(['a', 'b', 'c'])
    {'a': 1, 'b': 2, 'c': 3}

Si una clave no existe o ha expirado, no será incluida en el diccionario. Lo
siguiente es una continuación del ejemplo anterior::

    >>> cache.get_many(['a', 'b', 'c', 'd'])
    {'a': 1, 'b': 2, 'c': 3}

Finalmente, puedes eliminar claves explícitamente con ``cache.delete()``. Esta
es una manera fácil de limpiar la cache para un objeto en particular::

    >>> cache.delete('a')

``cache.delete()`` no tiene un valor de retorno, y funciona de la misma manera
si existe o no un valor en la cache.


Caches downstream
=================

Este capítulo se ha enfocado en la cache de tus *propios* datos. Pero existe
otro tipo de cache que es muy importante para los desarrolladores web: la cache
realizada por los *downstream*. Estos son sistemas que colocan en cache páginas
aún antes de que estas sean pedidas a tu sitio Web.

Aquí hay algunos ejemplos de caches para downstream:

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

La cache de downstream es un gran beneficio, pero puede ser peligroso. El
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
un número de encabezados HTTP que indican a las cache de downstream que
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
    def mi_vista(request):
        # ...

Esto le dice a la cache de downstream que diferencie *ambos*, lo que significa que
cada combinación de una cookie y un navegador obtendrá su propio valor en cache.
Por ejemplo, un pedido con navegador ``Mozilla`` y una cookie con el valor
``foo=bar`` será considerada diferente a un pedido con el navegador ``Mozilla``
y una cookie con el valor ``foo=ham``.

Como las variaciones con las cookies son tan comunes existe un decorador
``vary_on_cookie``. Las siguientes dos vistas son equivalentes:

.. code-block:: python

    @vary_on_cookie
    def mi_vista(request):
        # ...

    @vary_on_headers('Cookie')
    def mi_vista(request):
        # ...

El encabezado que le pasas a ``vary_on_headers`` no diferencia mayúsculas de
minúsculas; ``"User-Agent"`` es lo mismo que ``"user-agent"``.

También puedes usar ``django.utils.cache.patch_vary_headers`` como función de
ayuda. Esta función fija o añade al ``Vary header``, por ejemplo:

.. code-block:: python

    from django.utils.cache import patch_vary_headers

    def mi_vista(request):
        # ...
        response = render_to_response('template_name', context)
        patch_vary_headers(response, ['Cookie'])
        return response

``patch_vary_headers`` obtiene una instancia de ``HttpResponse`` como su primer
argumento y una lista/tupla de nombres de encabezados, sin diferenciar
mayúsculas de minúsculas, como su segundo argumento.

Controlando el cache: usando otros Encabezados
----------------------------------------------

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
    def mi_vista(request):
        # ...

Este decorador se encarga de enviar los encabezados HTTP apropiados detrás de
escena.

Nota que el control de configuraciones de cache "privado" y "publico" son
mutuamente excluyentes. El decorador se asegura que la directiva "publico" sea
removida si se encuentra configurado como "privado" (y viceversa). Un ejemplo
del uso de estas dos directivas, puede ser un sitio de un blog que ofrece
entradas públicas y privadas. Las entradas publicas pueden ser cacheadas en la
cache compartida. El siguiente código usa ``django.utils.cache.patch_cache_control()``
para manualmente modificar el control de las cabeceras de la cache (Es
internamente llamado por el decorador ``cache_control``).

.. code-block:: python

    from django.views.decorators.cache import patch_cache_control
    from django.views.decorators.vary import vary_on_cookie

    @vary_on_cookie
    def lista_de entradas_blog(request):
        if request.user.is_anonymous():
            response = render_only_public_entries()
            patch_cache_control(response, public=True)
        else:
            response = render_private_and_public_entries(request.user)
            patch_cache_control(response, private=True)

        return response

Existen otras pocas maneras de controlar los parámetros de cache. Por ejemplo,
HTTP permite a las aplicaciones hacer lo siguiente:

* Definir el tiempo máximo que una página debe estar en cache.

* Especificar si una cache debería comprobar siempre la existencia de nuevas
  versiones, entregando únicamente el contenido de la cache cuando no
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
    def mi_vista(request):
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
    especificaciones en http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9.

El middleware de caching ya fija el encabezado ``max-age`` con el valor de
``CACHE_MIDDLEWARE_SETTINGS``. Si utilizas un valor propio de ``max_age`` en
un decorador ``cache_control``, el decorador tendrá precedencia, y los
valores del encabezado serán fusionados correctamente.

Si quieres usar cabeceras para desactivar el cache por completo, usa el decorador
``never_cache`` del paquete ``django.views.decorators.cache.never_cache`` en
una vista, a la que le quieras agregar la cabecera, para asegurarte  que la
respuesta no sea cacheada por el navegador u otros caches. Por ejemplo:

.. code-block:: python

    from django.views.decorators.cache import never_cache

    @never_cache
    def mi_vista(request):
        # ...

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

Coloca el ``CacheMiddleware`` después de cualquier middleware que pueda agregar
algo al encabezado ``Vary``, incluyendo los siguientes:

* ``SessionMiddleware``, que agrega ``Cookie``
* ``GZipMiddleware``, que agrega ``Accept-Encoding``
* ``LocaleMiddleware`` que agrega  ``Accept-Language``

¿Qué sigue?
===========

Django incluye un número de paquetes  opcionales. Hemos cubierto algunos de los
mismos: como el sistema de administración  en él :doc:`capítulo 6<chapter06>`),
el marco de sesiones/usuarios del :doc:`capítulo 14<chapter14>`).

Él :doc:`próximo capítulo<chapter16>` cubre el resto de paquetes incluidos en el
modulo "contrib", que provee una cantidad interesante de herramientas disponibles;
que pueden hacer más fácil tu vida, no querrás perderte ninguno de ellos.

.. [#] \N. del T.: hard-coded

