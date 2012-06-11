=======================================================
Capítulo 3: Los principios de las páginas Web dinámicas
=======================================================

En el capítulo anterior, explicamos cómo crear un proyecto en Django y cómo
poner en marcha el servidor de desarrollo de Django. Por supuesto, el sitio no
hace nada útil todavía -- sólo muestra el mensaje "It worked!". Cambiemos eso.
Este capítulo presenta cómo crear paginas web dinámicas con Django.

Tu primera Vista: Contenido dinámico
====================================

Lo primero que haremos es crear una página web que muestre la fecha y la hora
actual. Este es un buen ejemplo de una página *dinámica*, porque el contenido de
la misma no es estático -- al contrario, los contenidos cambian de acuerdo con
el resultado de un cálculo (en este caso, el cálculo de la hora actual). Este
simple ejemplo no involucra una base de datos cualquier tipo de entrada del
usuario, sólo muestra la salida del reloj interno del servidor.

Para crear esta página, crearemos una *función de vista*. Una función de vista,
o *vista* en pocas palabras, es una simple función de Python que toma como
argumento una petición Web y retorna una respuesta Web. Esta respuesta puede ser
el contenido HTML de la página web, una redirección, o un error 404, o un
documento XML, o una imagen... o en realidad, cualquier cosa. La vista en sí
contiene toda la lógica necesaria para retornar esa respuesta. El código puede
encontrarse donde quieras, mientras que se encuentre dentro de tu Python path.
No hay otro requerimiento -- no hay "magia", por así decirlo. Por poner el
código en *algún lugar*, creemos un archivo llamado ``views.py`` en el
directorio ``mysite``, el cual creamos en el capítulo anterior.

Esta es la vista que retorna la fecha y hora actual, como un documento HTML::

    from django.http import HttpResponse
    import datetime

    def current_datetime(request):
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

Repasemos el código anterior línea a línea:

    * Primero, importamos la clase ``HttpResponse``, la cual pertenece al
      módulo ``django.http``. Para ver más detalles de los objetos
      ``HttpRequest`` y ``HttpResponse`` puedes consultar el Apéndice H.

    * Luego importamos el módulo ``datetime`` de la biblioteca estándar de
      Python, el conjunto de módulos útiles que vienen con Python. El módulo
      ``datetime`` contiene varias funciones y clases para trabajar con fechas y
      horas, incluyendo una función que retorna la hora actual.

    * A continuación, definimos la función llamada ``current_datetime``. Esta es
      una función de vista. Cada función de vista toma como primer argumento un
      objeto ``HttpRequest``, al que típicamente se le asigna el nombre
      ``request``.

      Nota que el nombre de la función de vista no importa; no tiene que ser
      nombrada de una determinada manera para que Django la reconozca. La llamamos
      ``current_datetime`` aquí, porque el nombre indica claramente
      lo que hace, pero se podría llamar
      ``super_duper_awesome_current_time``, o algo más repugnante. A Django no
      le interesa. La siguiente sección explica cómo Django encuentra
      esta funcion.

    * La primera línea de código dentro de la función calcula la fecha/hora
      actual, como un objeto ``datetime.datetime``, y almacena el resultado en
      la variable local ``now``.

    * La segunda línea de código dentro de la función construye la respuesta
      HTML usando el formato de cadena de caracteres de Python. El ``%s``
      dentro de la cadena de caracteres es un marcador de posición, y el signo
      porcentaje después de la cadena de caracteres, significa "Reemplaza el
      ``%s`` por el valor de la variable now.". (Sí, el HTML es inválido, pero
      estamos tratando de mantener el ejemplo simple y corto)

    * Por último, la vista retorna un objeto ``HttpResponse`` que contiene la
      respuesta generada. Cada función de vista es responsable de retornar un
      objeto ``HttpResponse``. (Hay excepciones, pero lo haremos más adelante)

.. admonition:: Zona Horaria de Django

    Django incluye una opción ``TIME_ZONE`` que por omisión es
    ``America/Chicago``. Probablemente no es donde vivas, por lo que puedes
    cambiarlo en tu ``settings.py``. Veáse el Apéndice E para más
    detalles.

Mapeando URLs a Vistas
======================

Repasemos, esta función de vista retorna un página HTML que contiene la fecha y
hora actual. ¿Pero cómo le decimos a Django que utilice ese código?. Ahí es
donde vienen las *URLconfs*.

Una *URLconf* es como una tabla de contenido para tu sitio web hecho con Django.
Básicamente, es un mapeo entre los patrones URL y las funciones de vista que deben
ser llamadas por esos patrones URL. Es como decirle a Django, "Para esta URL,
llama a este código, y para esta URL, llama a este otro código". Recuerda que
estas funciones de vista deben estar en tu Python path.

.. admonition:: Python Path

    *Python path* es la lista de directorios en tu sistema en donde Python
    buscará cuando uses la sentencia ``import`` de Python.

    Por ejemplo, supongamos que tu Python path tiene el valor ``['',
    '/usr/lib/python2.4/site-packages', '/home/username/djcode/']``. Si ejecutas
    el código Python ``from foo import bar``, Python en primer lugar va a buscar
    el módulo llamado ``foo.py`` en el directorio actual. (La primera entrada
    en el Python path, una cadena de caracteres vacía, significa "el directorio
    actual.") Si ese archivo no existe, Python va a buscar el módulo en
    ``/usr/lib/python2.4/site-packages/foo.py``. Si ese archivo no existe,
    entonces probará en ``/home/username/djcode/foo.py``. Finalmente, si *ese*
    archivo no existe, Python lanzará ``ImportError``

    Si estás interesado en ver el valor de tu Python path, abre un interprete
    interactivo de Python y escribe ``import sys``, seguido de ``print sys.path``.

    Generalmente no tienes que preocuparte de asigarle valores al Python path --
    Python y Django se encargan automáticamente de hacer esas cosas por ti entre
    bastidores. (Si eres curioso, establecer el Python path es una de las cosas
    que hace el archivo ``manage.py``).

Cuando ejecutaste ``django-admin.py startproject`` en el capítulo anterior, el
script creó automáticamente una URLconf por tí: el archivo ``urls.py``.
Editemos ese archivo. Por omisión, se verá como::

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        # Example:
        # (r'^mysite/', include('mysite.apps.foo.urls.foo')),

        # Uncomment this for admin:
    #     (r'^admin/', include('django.contrib.admin.urls')),
    )

Repasemos el código anterior línea a línea:

    * La primera línea importa todos los objetos desde el módulo ``django.conf.urls.defaults``,
      incluyendo una función llamada ``patterns``.

    * La segunda línea llama a la función ``patterns()`` y guarda el resultado
      en una variable llamada ``urlpatterns``. La función ``patterns()`` sólo
      recibe un argumento -- la cadena de caracteres vacía. El resto de las
      líneas están comentadas. (La cadena de caracteres puede ser usada para
      proveer un prefijo común para las funciones de vista, pero dejemos este
      uso más avanzado para más adelante).

Lo principal que debemos notar aquí es la variable ``urlpatterns``, la cual
Django espera encontrar en tu módulo ``ROOT_URLCONF``. Esta variable define
el mapeo entre las URLs y el código que manejan esas URLs.

Por defecto, todo lo que está en URLconf está comentado -- tu aplicación de
Django es una pizarra blanca. (Como nota adicional, esta es la forma en la que
Django sabía que debía mostrar la página "It worked!" en el capítulo anterior.
Si la URLconf esta vacía, Django asume que acabas de crear el proyecto, por lo
tanto, muestra ese mensaje).

Editemos este archivo para exponer nuestra vista ``current_datetime``::

    from django.conf.urls.defaults import *
    from mysite.views import current_datetime

    urlpatterns = patterns('',
        (r'^time/$', current_datetime),
    )

Hicimos dos cambios aquí. Primero, importamos la vista ``current_datetime``
desde el módulo (``mysite/views.py``, que en la sintaxis de import de Python se
traduce a ``mysite.views``). Luego, agregamos la línea
``(r'^time/$', current_datetime),``. Esta línea hace referencia a un
*URLpattern* -- es una tupla de Python en dónde el primer elemento es una
expresión regular simple y el segundo elemento es la función de vista que usa
para ese patrón.

En pocas palabras, le estamos diciendo a Django que cualquier petición a la
URL ``/time`` será manejada por la función de vista ``current_datetime``.

Algunas cosas que vale la pena resaltar:

    * Notemos que, en este ejemplo, pasamos la función de vista
      ``current_datetime`` como un objeto sin llamar a la función. Esto es una
      característica de Python (y otros lenguajes dinámicos): las funciones son
      objetos de primera clase, lo cual significa que puedes pasarlas como
      cualquier otra variable. ¡Qué bueno!, ¿no?

    * La ``r`` en ``r'^time/$'`` significa que ``'^time/$'`` es una cadena de
      caracteres en crudo de Python. Esto permite que las expresiones
      regulares sean escritas sin demasiadas sentencias de escape.

    * Puedes excluir la barra al comienzo de la expresión
      ``'^time/$'`` para que coincida con ``/time/``. Django
      automáticamente agrega una barra antes de toda expresión. A primera vista
      esto parece raro, pero una URLconf puede ser incluida en otra URLconf, y
      el dejar la barra de lado simplifica mucho las cosas. Esto se retoma en
      el :doc:`Capítulo 8<chapter08>`.

    * El caracter *acento circunflejo* (``^``) y el carácter *signo de dólar*
      (``$``) son importantes. El acento circunflejo significa que "requiere
      que el patrón concuerde con el inicio de la cadena de caracteres", y el
      signo de dólar significa que "exige que el patrón concuerde con el fin
      de la cadena".

      Este concepto se explica mejor con un ejemplo. Si hubiéramos utilizado el
      patrón ``'^time/'`` (sin el signo de dólar al final), entonces *cualquier*
      URL que comience con ``time/`` concordaría, así como ``/time/foo`` y
      ``/time/bar``, no sólo ``/time/``. Del mismo modo, si dejamos de lado el
      carácter acento circunflejo inicial (``'time/$'``), Django concordaría con
      *cualquier* URL que termine con ``time/``, así como ``/foo/bar/time/``.
      Por lo tanto, usamos tanto el acento circunflejo como el signo de dólar
      para asegurarnos que sólo la URL ``/time/`` concuerde. Nada más y nada
      menos.

      Quizás te preguntes qué pasa si alguien intenta acceder a ``/time``. Esto
      es manejado como esperarías (a través de un redireccionamiento) siempre y
      cuando ``APPEND_SLASH`` tenga asignado el valor ``True``. (Veáse el
      Apéndice E para una buena lectura sobre este tema).

Para probar nuestro cambios en la URLconf, inicia el servidor de
desarrollo de Django, como hiciste en el :doc:`Capítulo 2<chapter02>`, ejecutando el comando ``python
manage.py runserver``. (Si ya lo tenías corriendo, está bien también. El
servidor de desarrollo automáticamente detecta los cambios en tu código de
Python y recarga de ser necesario, así no tienes que reiniciar el servidor al
hacer cambios). El servidor está corriendo en la dirección
``http://127.0.0.1:8000/``, entonces abre tu navegador web y ve a
``http://127.0.0.1:8000/time/``. Deberías ver la salida de tu vista de Django.

¡Enhorabuena! Has creado tu primera página Web hecha con Django.

Expresiones Regulares:


    Las *Expresiones Regulares* (o *regexes*) son la forma compacta de
    especificar patrones en un texto. Aunque las URLconfs de Django permiten el
    uso de regexes arbitrarias para tener un potente sistema de definición de
    URLs, probablemente en la práctica no utilices más que un par de patrones
    regex. Esta es una pequeña selección de patrones comunes:

+----------------------------+--------------------------------------------------------------------------------------------------+
|       Símbolo              |                        Coincide con                                                              |
+----------------------------+--------------------------------------------------------------------------------------------------+
|       ``. (punto)``        |  Cualquier carácter                                                                              | 
+----------------------------+--------------------------------------------------------------------------------------------------+	
|        ``\d``              |    Cualquier dígito                                                                              |
+----------------------------+--------------------------------------------------------------------------------------------------+
|       ``[A-Z]``            |  Cualquier carácter, A-Z (mayúsculas)                                                            |
+----------------------------+--------------------------------------------------------------------------------------------------+
|       ``[a-z]``            |  Cualquier carácter, a-z (minúsculas)                                                            | 
+----------------------------+--------------------------------------------------------------------------------------------------+
|       ``[A-Za-z]``         |  Cualquier carácter, a-z (no distingue entre                                                     |
|                            |	mayúscula y minúscula)                                                                          |
+----------------------------+--------------------------------------------------------------------------------------------------+
|        ``+``               | Una o más ocurrencias de la expresión anterior (ejemplo, ``\d+``                                 |
|                            | coincidirá con uno o más dígitos)                                                                |
+----------------------------+--------------------------------------------------------------------------------------------------+
|        ``[^/]+``           | Todos los caracteres excepto la barra.                                                           |
+----------------------------+--------------------------------------------------------------------------------------------------+
|       ``*``                | Cero o más ocurrencias de la expresión anterior (ejemplo, ``\d*``                                |
|                            | coincidirá con cero o más dígitos)                                                               |
+----------------------------+--------------------------------------------------------------------------------------------------+
|       ``{1,3}``            | Entre una y tres (inclusive) ocurrencias de la expresión anterior                                |
+----------------------------+--------------------------------------------------------------------------------------------------+

    Para más información acerca de las expresiones regulares, mira el módulo
    http://www.djangoproject.com/r/python/re-module/.

Cómo procesa una petición Django
================================

Debemos señalar varias cosas en lo que hemos visto. Este es el detalle de lo que
sucede cuando ejecutas el servidor de desarrollo de Django y hacemos una
petición a una página Web.

    * El comando ``python manage.py runserver`` importa un archivo llamado
      ``settings.py`` desde el mismo directorio. Este archivo contiene todo
      tipo de configuraciones opcionales para esta instancia de Django en particular,
      pero una de las configuraciones más importantes  es ``ROOT_URLCONF``. La
      variable ``ROOT_URLCONF`` le dice a Django qué módulo de Python debería
      usar para la URLconf de este sitio Web.

      ¿Recuerdas cuando ``django-admin.py startproject`` creó el archivo
      ``settings.py`` y ``urls.py``? Bueno, el ``settings.py`` generado
      automáticamente tenía un ``ROOT_URLCONF`` que apunta al ``urls.py``
      generado automáticamente. ¡Qué conveniente!

    * Cuando llega una petición-- digamos, una petición a la URL ``/time/``
      -- Django carga la URLconf apuntada por la variable ``ROOT_URLCONF``.
      Luego comprueba cada uno de los patrones de URL en la URLconf en orden, comparando
      la URL solicitada con un patrón a la vez, hasta que encuentra uno que
      coincida. Cuando encuentra uno que coincide, llama a la función de vista
      asociada con ese patrón, pasando un objeto ``HttpRequest`` como primer
      parámetro de la función. (Veremos más de ``HttpRequest`` luego).

    * La función de vista es responsable de retornar un objeto ``HttpResponse``.

Conoces ahora lo básico sobre cómo hacer páginas Web con Django. Es muy
sencillo, realmente -- sólo tenemos que escribir funciones de vista y
relacionarlas con URLs mediante URLconfs. Podrías pensar que es lento enlazar
las URL con funciones usando una serie de expresiones regulares, pero te
sorprenderás.

Cómo procesa una petición Django: Detalles completos
----------------------------------------------------

Además del mapeo directo de URLs con funciones vista que acabamos de describir,
Django nos provee un poco más de flexibilidad en el procesamiento de peticiones.

El flujo típico -- resolución de URLconf a una función de vista que retorna un
``HttpResponse``-- puede ser corto-circuitado o ***augmented*** mediante
middleware.  Los secretos del middleware serán tratados en profundidad en el
:doc:`Capítulo15<chapter15>`, pero un esquema (ver Figura 3-1) te ayudará conceptualmente a
poner todas las piezas juntas.

.. image:: graficos/chapter03/get_response.png
   :alt: El flujo completo de un petición y una respuesta Django.

Figura 3-1: El flujo completo de un petición y una respuesta Django.

Cuando llega una petición HTTP desde el navegador, un *manejador* específico a
cada servidor construye la ``HttpRequest``, para pasarla a los componentes y
maneja el flujo del procesamiento de la respuesta.

El manejador luego llama a cualquier middleware de Petición o Vista disponible.
Estos tipos de middleware son útiles para ***augmenting*** los objetos
``HttpRequest`` así como también para proveer manejo especial a determinados
tipos de peticiones.  En el caso de que alguno de los mismos retornara un
``HttpResponse`` la vista no es invocada.

Hasta a los mejores programadores se le escapan errores (*bugs*), pero el
*middleware de excepción* ayuda a aplastarlos. Si una función de vista lanza una
excepción, el control pasa al middleware de Excepción. Si este middleware no
retorna un ``HttpResponse``, la excepción se vuelve a lanzar.

Sin embargo, no todo está perdido. Django incluye vistas por omisión para
respuestas amigables a errores 404 y 500.

Finalmente, el *middleware de respuesta* es bueno para el procesamiento posterior
a un ``HttpResponse`` justo antes de que se envíe al navegador o haciendo una
limpieza de recursos específicos a una petición.

URLconfs y el acoplamiento débil
================================

Ahora es el momento de resaltar una parte clave de filosofía detrás de las
URLconf y detrás de Django en general: el principio de acoplamiento débil
(*loose coupling*). Para explicarlo simplemente, el acoplamiento débil es una
manera de diseñar software aprovechando el valor de la importancia de que se
puedan cambiar las piezas. Si dos piezas de código están débilmente acopladas
(*loosely coupled*) los cambios realizados sobre una de dichas piezas va a tener
poco o ningún efecto sobre la otra.

Las URLconfs de Django son un claro ejemplo de este principio en la práctica. En
una aplicación Web de Django, la definición de la URL y la función de vista que
se llamará están débilmente acopladas; de esta manera, la decisión de cuál debe
ser la URL para una función, y la implementación de la función misma, residen en
dos lugares separados. Esto permite el desarrollo de una pieza sin afectar a la
otra.

En contraste, otras plataformas de desarrollo Web acoplan la URL con el
programa. En las típicas aplicaciones PHP (http://www.php.net/), por ejemplo,
la URL de tu aplicación es designada por dónde colocas el código en el sistema
de archivos. En versiones anteriores del framework Web Python CherryPy
(http://www.cherrypy.org/) la URL de tu aplicación correspondía al nombre del
método donde residía tu código. Esto puede parecer un atajo conveniente en el
corto plazo, pero puede tornarse inmanejable a largo plazo.

Por ejemplo, consideremos la función de vista que escribimos antes, la cuál nos
mostraba la fecha y la hora actual. Si quieres cambiar la URL de tu aplicación
-- digamos, mover desde ``/time`` a ``/currenttime/`` -- puedes hacer un rápido
cambio en la URLconf, sin preocuparte acerca de la implementación subyacente de
la función. Similarmente, si quieres cambiar la función de vista -- alterando
la lógica de alguna manera -- puedes hacerlo sin afectar la URL a la que está
asociada tu función de vista. Además, si quisiéramos exponer la funcionalidad de
fecha actual en varias URL podríamos hacerlo editando el URLconf con cuidado,
sin tener que tocar una sola línea de código de la vista.

Eso es el acoplamiento débil en acción. Continuaremos exponiendo ejemplos de
esta importante filosofía de desarrollo a lo largo del libro.

Errores 404
===========

En las URLconf anteriores, hemos definido un solo patrón URL: el que maneja la
petición para la URL ``/time``. ¿Qué pasaría si se solicita una URL diferente?

Para averiguarlo, prueba ejecutar el servidor de desarrollo Django e intenta
acceder a una página Web como http://127.0.0.1:8000/hello/ o
http://127.0.0.1:8000/does-not-exist/, o mejor como
http://127.0.0.1:8000/ (la "raíz" del sitio). Deberías ver el mensaje "Page
not found" (ver la Figura 3-2). (Es linda, ¿no? A la gente de Django seguro le
gustan los colores pasteles). Django muestra este mensaje porque solicitaste una
URL que no está definida en tu URLconf.

.. image:: graficos/chapter03/404.png
   :alt: Captura de pantalla de la página 404 de Django.

Figura 3-2. Página 404 de Django

La utilidad de esta página va más allá del mensaje básico de error 404; nos dice
también, qué URLconf utilizó Django y todos los patrones de esa URLconf. Con
esa información, tendríamos que ser capaces de establecer porqué la URL
solicitada lanzó un error 404.

Naturalmente, esta es información importante sólo destinada a ti, el
administrador Web. Si esto fuera un sitio en producción alojado en Internet, no
quisiéramos mostrar esta información al público. Por esta razón, la página "Page
not found" es sólo mostrada si nuestro proyecto en Django está en modo de
depuración (*debug mode*). Explicaremos cómo desactivar este modo más adelante.
Por ahora, sólo diremos que todos los proyectos están en modo de depuración
cuando los creamos, y si el proyecto no lo estuviese, se retornaría una
respuesta diferente.

Tu segunda Vista: URLs dinámicas
================================

En la primer vista de ejemplo, el contenido de la página
-- la fecha/hora actual -- eran dinámicas, pero la URL (``/time``) era
estática. En la mayoría de las aplicaciones Web, sin embargo, la URL contiene
parámetros que influyen en la salida de la página.

Vamos a crear una segunda vista que nos muestre la fecha y hora actual con un
adelanto de ciertas horas. El objetivo es montar un sitio en la que la página
``/time/plus/1/`` muestre la fecha/hora una hora más adelantada, la página
``/time/plus/2/`` muestre la fecha/hora dos horas más adelantada, la página
``/time/plus/3/`` muestre la fecha/hora tres horas más adelantada, y así.

A un novato se le ocurriría escribir una función de vista distinta para cada
adelanto de horas, lo que resultaría una URLconf como esta::

    urlpatterns = patterns('',
        (r'^time/$', current_datetime),
        (r'^time/plus/1/$', one_hour_ahead),
        (r'^time/plus/2/$', two_hours_ahead),
        (r'^time/plus/3/$', three_hours_ahead),
        (r'^time/plus/4/$', four_hours_ahead),
    )

Claramente, esta línea de pensamiento es incorrecta. No sólo porque producirá
redundancia entre las funciones de vista, sino también la aplicación estará
limitada a admitir sólo el rango horario definido -- uno, dos, tres o
cuatro horas. Si, de repente, quisiéramos crear una página que mostrara la hora
cinco horas adelantada, tendríamos que crear una vista distinta y una línea
URLconf, perpetuando la duplicación y la demencia. Aquí necesitamos algo de
abstracción.

Algunas palabras acerca de las URLs bonitas
-------------------------------------------

Si tienes experiencia en otra plataforma de diseño Web, como PHP o Java, es
posible que estés pensado, "¡Oye, usemos un parámetro cadena de consulta!", algo
como ``/time/plus?hours=3``, en la cual la hora será designada por el parámetro
``hours`` de la cadena de consulta de la URL (la parte a continuación de ``?``).

Con Django *puedes* hacer eso (pero te diremos cómo más adelante, si es que
realmente quieres saberlo), pero una de las filosofías del núcleo de Django es que
las URLs deben ser bonitas. La URL ``/time/plus/3`` es mucho más limpia, más
simple, más legible, más fácil de dictarse a alguien y . . . justamente más
bonita que su homóloga forma de cadena de consulta. Las URLs bonitas son un
signo de calidad en las aplicaciones Web.

El sistema de URLconf que usa Django estimula a generar URLs bonitas, haciendo
más fácil el usarlas que el no usarlas.

Comodines en los patrones URL
-----------------------------

Continuando con nuestro ejemplo ``hours_ahead``, pongámosle un comodín al
patrón URL. Como ya se mencionó antes, un patrón URL es una expresión regular;
de aquí, es que usamos el patrón de expresión regular ``\d+`` para que
coincida con uno o más dígitos::

    from django.conf.urls.defaults import *
    from mysite.views import current_datetime, hours_ahead

    urlpatterns = patterns('',
        (r'^time/$', current_datetime),
        (r'^time/plus/\d+/$', hours_ahead),
    )

Este patrón coincidirá con cualquier URL que sea como ``/time/plus/2/``,
``/time/plus/25/``, o también ``/time/plus/100000000000/``. Ahora que lo
pienso, podemos limitar el lapso máximo de horas en 99. Eso significa que
queremos tener números de uno o dos dígitos en la sintaxis de las expresiones
regulares, con lo que nos quedaría así ``\d{1,2}``::

    (r'^time/plus/\d{1,2}/$', hours_ahead),

.. admonition::

    Cuando construimos aplicaciones Web, siempre es importante considerar el
    caso más descabellado posible de entrada, y decidir si la aplicación
    admitirá o no esa entrada. Aquí hemos limitado a los exagerados
    reconociendo lapsos de hasta 99 horas. Y, por cierto, *Los Limitadores
    exagerados*, aunque largo, sería un nombre fantástico para una banda
    musical.

Ahora designaremos el comodín para la URL, necesitamos una forma de pasar esa
información a la función de vista, así podremos usar una sola función de vista
para cualquier adelanto de hora. Lo haremos colocando paréntesis alrededor de
los datos en el patrón URL que querramos guardar. En el caso del ejemplo,
queremos guardar cualquier número que se anotará en la URL, entonces pongamos
paréntesis alrededor de ``\d{1,2}``::

    (r'^time/plus/(\d{1,2})/$', hours_ahead),

Si estás familiarizado con las expresiones regulares, te sentirás como en casa
aquí; estamos usando paréntesis para *capturar* los datos del texto que
coincide.

La URLconf final, incluyendo la vista anterior ``current_datetime``, nos
quedará algo así::

    from django.conf.urls.defaults import *
    from mysite.views import current_datetime, hours_ahead

    urlpatterns = patterns('',
        (r'^time/$', current_datetime),
        (r'^time/plus/(\d{1,2})/$', hours_ahead),
    )

Con cuidado, vamos a escribir la vista ``hours_ahead``.

.. admonition:: Orden para programar

    En este ejemplo, primero escribimos el patrón URL y en segundo lugar la
    vista, pero en el ejemplo anterior, escribimos la vista primero y luego el
    patrón de URL. ¿Qué técnica es mejor? Bien, cada programador es diferente.

    Si eres del tipo de programadores que piensan globalmente, puede que tenga
    más sentido que escribas todos los patrones de URL para la aplicación al
    mismo tiempo, al inicio del proyecto, y después el código de las funciones
    de vista. Esto tiene la ventaja de darnos una lista de objetivos clara, y es
    esencial definir los parámetros requeridos por las funciones de vista que
    necesitaremos desarrollar.

    Si eres del tipo de programadores que les gusta ir de abajo hacia arriba,
    tal vez prefieras escribir las funciones de vista primero, y luego
    asociarlas a URLs. Esto también está bien.

    Al final, todo se reduce a elegir qué técnica se amolda más a tu cerebro.
    Ambos enfoques son válidos.

``hours_ahead`` es muy similar a ``current_datetime``, vista que escribimos
antes, sólo que con una diferencia: tomará un argumento extra, el número de
horas que debemos adelantar. Agrega al archivo ``views.py`` lo siguiente::

    import django.http.HttpResponse
    import datetime

    def hours_ahead(request, offset):
        offset = int(offset)
        dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
        html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
        return HttpResponse(html)

Repasemos el código anterior línea a línea:

* Tal como hicimos en la vista ``current_datetime``, importamos la clase
  ``django.http.HttpResponse`` y el módulo ``datetime``.

* La función de vista ``hours_ahead``, toma *dos* parámetros: ``request`` y
  ``offset``.

* ``request`` es un objeto ``HttpRequest``, al igual que en
    ``current_datetime``. Lo diremos nuevamente: cada vista *siempre*
    toma un objeto ``HttpRequest`` como primer parámetro.

* ``offset`` es la cadena de caracteres capturada por los paréntesis en
  el patrón URL. Por ejemplo, si la petición URL fuera
  ``/time/plus/3/``, entonces el ``offset`` debería ser la cadena de
  caracteres ``'3'``. Si la petición URL fuera ``/time/plus/21/``,
  entonces el ``offset`` debería ser la cadena de caracteres ``'21'``.
  Notar que la cadena de caracteres capturada siempre es una cadena de
  caracteres, no un entero, incluso si se compone sólo de dígitos, como
  en el caso ``'21'``.

Decidimos llamar a la variable ``offset``, pero puedes asignarle el
nombre que quieras, siempre que sea un identificador válido para
Python. El nombre de la variable no importa; todo lo que importa es lo
que contiene el segundo parámetro de la función (luego de
``request``).  Es posible también usar untienes que hacer esto.
No es una buena idea poner cualquier código Python en la carpeta 
raíz del servia palabra clave, en lugar de
posición, como argumentos en la URLconf. Eso lo veremos en detalle en
el :doc:`Capítulo 8<chapter08>`.

* Lo primero que hacemos en la función es llamar a ``int()`` sobre
  ``offset``. Esto convierte el valor de la cadena de caracteres a entero.

Tener en cuenta que Python lanzará una excepción ``ValueError`` si se
llama a la función ``int()`` con un valor que no puede convertirse a un
entero, como lo sería la cadena de caracteres ``'foo'``. Sin embargo, en
este ejemplo no debemos preocuparnos de atrapar la excepción, porque
tenemos la certeza que la variable ``offset`` será una cadena de
caracteres conformada sólo por dígitos. Sabemos esto, por el patrón URL
de la expresión regular en el URLconf -- ``(\d{1,2})``-- captura sólo
dígitos. Esto ilustra otra ventaja de tener un URLconf: nos provee un
primer nivel de validación de entrada.

* La siguiente línea de la función muestra la razón por la que se llamó a
  la función ``int()`` con ``offset``. En esta línea, calculamos la hora
  actual más las hora que tiene ``offset``, almacenando el resultado en la
  variable ``dt``. La función ``datetime.timedelta`` requiere que el
  parámetro ``hours`` sea un entero.

* A continuación, construimos la salida HTML de esta función de vista, tal
  como lo hicimos en la vista ``current_datetime``. Una pequeña diferencia
  en esta línea, es que usamos el formato de cadenas de Python con *dos*
  valores, no sólo uno. Por lo tanto, hay dos símbolos ``%s`` en la cadena
  de caracteres y la tupla de valores a insertar sería: ``(offset, dt)``.

* Finalmente, retornamos el ``HttpResponse`` del HTML -- de nuevo, tal como
  hicimos en la vista ``current_datetime``.

Con esta función de vista y la URLconf escrita, ejecuta el servidor de
desarrollo de Django (si no está corriendo), y visita
``http://127.0.0.1:8000/time/plus/3/`` para verificar que lo que hicimos
funciona. Luego prueba ``http://127.0.0.1:8000/time/plus/5/``.  Para terminar
visita ``http://127.0.0.1:8000/time/plus/100/`` para verificar que el patrón en
la URLconf sólo acepta número de uno o dos dígitos, Django debería mostrar un
error en este caso como "Page not found", tal como vimos en la sección "`Errores
404`_" anteriormente. La URL ``http://127.0.0.1:8000/time/plus/`` (*sin* horas
designadas) debería también mostrar un error 404.

Si estás siguiendo el libro y programando al mismo tiempo, notarás que el
archivo ``views.py`` ahora contiene dos vistas. (Omitimos la vista ``current_datetime``
del ejemplo anterior sólo por claridad). Poniéndolas juntas, veríamos algo
similar a esto::

    from django.http import HttpResponse
    import datetime

    def current_datetime(request):
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

    def hours_ahead(request, offset):
        offset = int(offset)
        dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
        html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
        return HttpResponse(html)

Páginas de error bonitas con Django
===================================

Tomémonos un momento para admirar la bonita aplicación web que hemos creado
hasta ahora . . . y ahora ¡rompámosla! Introduzcamos deliberadamente un error de
Python en el archivo ``views.py`` comentando la línea ``offset = int(offset)``
de la vista ``hours_ahead``::

    def hours_ahead(request, offset):
        #offset = int(offset)
        dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
        html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
        return HttpResponse(html)

Ejecuta el servidor de desarrollo y navega a ``/time/plus/3/``. Verás una página
de error con mucha información significativa, incluyendo el mensaje
``TypeError`` mostrado en la parte superior de la página: ``"unsupported type
for timedelta hours component: str"``.

¿Qué ha ocurrido? Bueno, la función ``datetime.timedelta`` espera que el
parámetro ``hours`` sea un entero, y hemos comentado la línea de código que
realiza la conversión del ``offset`` a entero. Eso causa que
``datetime.timedelta`` lance un ``TypeError``. Es el típico pequeño *bug* que
todo programador comete en algún momento.

El punto de este ejemplo fue demostrar la página de error de Django. Dediquemos
un momento a explorar esta página y descubrir las distintas piezas de
información que nos brinda.

Aquí comentamos algunas cosas a destacar:

    * En la parte superior de la página se muestra la información clave de la
      excepción: el tipo y cualquier parámetro de la excepción (el mensaje
      ``"unsupported type"`` en este caso), el archivo en el cuál la excepción
      fue lanzada, y el número de línea que contiene el error.

    * Abajo de la información clave de la excepción, la página muestra el
      ***traceback*** de Python para dicha excepción. Este es el
      ***traceback*** estándar que se obtiene en el interprete de Python, sólo
      que más interactivo. Por cada marco de la pila, Django muestra el nombre
      del archivo, el nombre de la función/método, el número de línea, y el
      código fuente de esa línea.

      Haz click en la línea de código (en gris oscuro) para ver varias líneas
      anteriores y posteriores a la línea errónea, lo que nos brinda un poco de
      contexto.

      Haz click en *"Locals vars"* debajo de cualquier marco de la pila para
      ver la tabla de todas las variables locales y sus valores, en ese marco y
      en la posición exacta de código en el cual fue lanzada la excepción. Esta
      información de depuración es invaluable.

    * Nota el texto *"Switch to copy-and-paste view"* debajo de la cabecera
      *"Traceback"*. Haz click en esas palabras, y el ***traceback*** cambiará a
      una versión que te permitirá fácilmente copiar y pegar. Usando esto para
      cuando necesitemos compartir el traceback de la excepción con otros para
      obtener soporte técnico -- como los amables colegas que encontraremos en
      el canal de IRC o la lista de correo de Django.

    * A continuación, la sección *"Request information"* incluye una gran
      cantidad de información sobre la petición Web que provocó el error:
      información GET y POST, valores de las cookies y meta información como
      las cabeceras CGI. El :doc:`Apéndice H<appendixH>` es una completa referencia sobre toda
      la información que contienen los objetos peticiones.

      Más abajo, la sección *"Settings"* lista la configuración de la
      instalación de Django en particular. El `Apéndice E`, cubre en detalle
      los ajustes de configuración disponibles. Por ahora, sólo mira los
      ajustes para tener una idea de la información disponible.

La página de error de Django es capaz de mostrar más información en ciertos
casos especiales, como por ejemplo, en el caso de error de sintaxis en las
plantillas. Lo abordaremos más tarde, cuando discutamos el sistema de plantillas
de Django. Por ahora, quita el comentario en la línea ``offset = int(offset)``
para que la función de vista funcione normalmente de nuevo.

¿Eres el tipo de programador al que le gusta depurar con la ayuda de sentencias
``print`` cuidadosamente colocadas? Puedes usar la página de error de Django
para hacer eso -- sin la sentencia ``print``. En cualquier punto de la vista,
temporalmente podemos insertar un ``assert False`` para provocar una página de
error. Luego, podremos ver las variables locales y el estado del programa. (Hay
maneras más avanzadas de depurar las vista en Django, lo explicaremos más
adelante, pero esto es la forma más rápida y fácil).

Finalmente, es obvio que la mayor parte de la información es delicada -- expone
las entrañas del código fuente de Python, como también de la configuración de
Django -- y sería una estupidez mostrarla al público en Internet. Una persona
con malas intenciones podría usar esto para intentar aplicar ingeniería inversa
en la aplicación Web y hacer cosas maliciosas. Por esta razón, la página de
error es mostrada sólo cuando el proyecto está en modo depuración. Explicaremos
cómo desactivar este modo más adelante. Por ahora, hay que tener en claro que
todos los proyectos de Django están en modo depuración automáticamente cuando
son creados. (¿Suena familiar? Los errores "Page not found", descriptos en la
sección "`Errores 404`_", trabajan de manera similar.)

¿Qué sigue?
===========

Hasta ahora hemos producido las vistas mediante código HTML dentro del código
Python. Desafortunadamente, esto es casi siempre es una mala idea. Pero por
suerte, con Django podemos hacer esto con un potente motor de plantillas que nos
permite separar el diseño de las páginas del código fuente subyacente. Nos
sumergiremos en el motor de plantillas de Django en el 
:doc:`próximo capitulo<chapter04>`


