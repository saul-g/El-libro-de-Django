========================================
Apéndice H: Objetos Petición y Respuesta
========================================

Django usa los objetos respuesta y petición para pasar información de
estado a través del sistema.

Cuando se peticiona una página, Django crea un objeto ``HttpRequest`` que
contiene metadatos sobre la petición. Luego Django carga la vista apropiada,
pasando el ``HttpRequest`` como el primer argumento de la función de vista. Cada
vista es responsable de retornar un objeto ``HttpResponse``.

Hemos usado estos objetos con frecuencia a lo largo del libro; este apéndice
explica las APIs completas para los objetos ``HttpRequest`` y ``HttpResponse``.

HttpRequest
===========

``HttpRequest`` representa una sola petición HTTP desde algún agente de usuario.

Mucha de la información importante sobre la petición esta disponible como
atributos en la instancia de ``HttpRequest`` (mira la Tabla H-1). Todos los
atributos excepto ``session`` deben considerarse de sólo lectura.

.. tabla:: Tabla H-1. Atributos de los objetos HttpRequest

==================  =======================================================
    Atributo            Descripción
==================  =======================================================
``path``            Un string que representa la ruta completa a la página
                    peticionada, no incluye el dominio -- por ejemplo,
                    ``"/music/bands/the_beatles/"``.

``method``          Un string que representa el método HTTP usado en la
                    petición. Se garantiza que estará en mayúsculas. Por
                    ejemplo::

                            if request.method == 'GET':
                                do_something()
                            elif request.method == 'POST':
                                do_something_else()

``GET``             Un objeto similar a un diccionario que contiene todos
                    los parámetros HTTP GET dados. Mira la documentación
                    de `QueryDict`` que sigue.

``POST``            Un objeto similar a un diccionario que contiene todos
                    los parámetros HTTP POST dados.Mira la documentación de
                    ``QueryDict`` que sigue.

                    Es posible que una petición pueda ingresar vía POST
                    con un diccionario ``POST`` vacío -- si, digamos, un
                    formulario es peticionado a través del método HTTP POST
                    pero que no incluye datos de formulario. Por eso, no
                    deberías usar ``if request.POST`` para verificar el uso
                    del método POST; en su lugar, utiliza
                    ``if request.method == "POST"`` (mira la entrada
                    ``method`` en esta tabla).

                    Nota: ``POST`` *no* incluye información sobre la subida
                    de archivos. Mira ``FILES``.

``REQUEST``         Por conveniencia, un objeto similar a un diccionario
                    que busca en ``POST`` primero, y luego en ``GET``.
                    Inspirado por ``$_REQUEST`` de PHP.
                    Por ejemplo, si ``GET = {"name": "john"}`` y ``POST
                    = {"age": '34'}``, ``REQUEST["name"]`` será
                    ``"john"``, y ``REQUEST["age"]`` será ``"34"``.
                     Se sugiere encarecidamente que uses ``GET`` y ``POST``
                    en lugar de ``REQUEST``, ya que lo primero es más
                    explícito.

``COOKIES``         Un diccionario Python estándar que contiene todas las
                    cookies. Las claves y los valores son strings. Mira el
                    :doc:`Capítulo 12<chapter12>` para saber mas de cookies.
``FILES``           Un objeto similar a un diccionario que contiene todos
                    los archivos subidos. Cada clave de ``FILES`` es el
                    atributo ``name`` de ``<input type="file" name="" />``.
                    Cada valor de ``FILES`` es un diccionario Python
                    estándar con las siguientes tres claves:
                    
                    * ``filename``: El nombre del archivo subido, como
                     un string Python.

                    * ``content-type``: El tipo de contenido del
                     archivo subido.

                    * ``content``: El contenido en crudo del archivo
                     subido.
 
                    Nota que ``FILES`` contendrá datos sólo si el método de
                    la petición fue ``POST`` y el ``<form>`` que realizó la
                    petición contenía ``enctype="multipart/form-data"``.
                    De lo contrario, ``FILES`` será un objeto similar a un
                    diccionario vacío.

``META``            Un diccionario Python estándar que contiene todos los
                    encabezados HTTP disponibles. Los encabezados
                    disponibles dependen del cliente y del servidor, pero
                    estos son algunos ejemplos:

                            * ``CONTENT_LENGTH``
                            * ``CONTENT_TYPE``
                            * ``QUERY_STRING``: La string de consulta en
                              crudo sin analizar.
                            * ``REMOTE_ADDR``: La dirección IP del cliente.
                            * ``REMOTE_HOST``: El nombre host del cliente.
                            * ``SERVER_NAME``: El nombre host del servidor.
                            * ``SERVER_PORT``: El puerto del servidor.

                    Cualquier cabecera HTTP esta disponible en ``META``
                    como claves con el prefijo ``HTTP_``, por ejemplo:

                            * ``HTTP_ACCEPT_ENCODING``
                            * ``HTTP_ACCEPT_LANGUAGE``
                            * ``HTTP_HOST``: La cabecera HTTP ``host`` en
                              viada por el cliente
                            * ``HTTP_REFERER``: La pagina referente,
                              si la hay
                            * ``HTTP_USER_AGENT``: La string de agente de
                              usuario del cliente
                            * ``HTTP_X_BENDER``: El valor de la cabecera
                              ``X-Bender``, si esta establecida.

``user``            Un objeto ``django.contrib.auth.models.User`` que
                    representa el usuario actual registrado. Si el usuario
                    no esta actualmente registrado, ``user`` se fijará a
                    una instancia de
                    ``django.contrib.auth.models.AnonymousUser``.
                    Puedes distinguirlos con ``is_authenticated()``,
                    de este modo::

                            if request.user.is_authenticated():
                                # Do something for logged-in users.
                            else:
                                # Do something for anonymous users.

                    ``user`` esta disponible sólo si tu instalación
                    Django tiene activado ``AuthenticationMiddleware``.

                    Para los detalles completos sobre autenticación y
                    usuarios, mira el `Capítulo 12`_.

``session``         Un objeto similar a un diccionario que se puede leer y
                    modificar, que representa la sesión actual. Éste esta
                    disponible sólo si tu instalación Django tiene
                    activado el soporte para sesiones. Mira el
                    `Capítulo 12`_.

``raw_post_data``   Los datos HTTP POST en crudo. Esto es útil para
                        procesamiento avanzado.
==================  =======================================================

Los objetos request también tienen algunos métodos de utilidad, como se muestra
en la Tabla H-2.

.. tabla:: Tabla H-2. Métodos de HttpRequest

======================  ===================================================
    Método                  Descripción
======================  ===================================================
``__getitem__(key)``    Retorna el valor GET/POST para la clave dada,
                        verificando POST primero, y luego GET. Emite
                        ``KeyError`` si la clave no existe.

                        Esto te permite usar sintaxis de acceso a
                        diccionarios en una instancia ``HttpRequest``.

                        Por ejemplo, ``request["foo"]`` es lo mismo que
                        comprobar ``request.POST["foo"]`` y luego
                        ``request.GET["foo"]``.

``has_key()``           Retorna ``True`` o ``False``, señalando si
                        ``request.GET`` o ``request.POST`` contiene la
                        clave dada.

``get_full_path()``     Retorna la ``ruta``, más un string de consulta
                        agregado. Por ejemplo,
                        ``"/music/bands/the_beatles/?print=true"``

``is_secure()``         Retorna ``True`` si la petición es segura; es decir
                        si fue realizada con HTTPS.
======================  ===================================================

Objetos QueryDict
-----------------

En un objeto ``HttpRequest``, los atributos ``GET`` y ``POST`` son instancias de
``django.http.QueryDict``. ``QueryDict`` es una clase similar a un diccionario
personalizada para tratar múltiples valores con la misma clave. Esto es
necesario ya que algunos elementos de un formulario HTML, en particular
``<select multiple="multiple">``, pasan múltiples valores para la misma clave.

Las instancias ``QueryDict`` son inmutables, a menos que realices una copia de
ellas.
Esto significa que tu no puedes cambiar directamente los atributos de
``request.POST`` y ``request.GET``.

``QueryDict`` implementa todos los métodos estándar de los diccionarios, debido
a que es una subclase de diccionario. Las excepciones se resumen en la
Tabla H-3.

.. tabla:: Tabla H-3. Como se diferencian los QueryDicts de los diccionarios estándar.

==================  ============================================================
    Método              Diferencias con la implementación estándar de dict
==================  ============================================================
  ``__getitem__``      Funciona como en un diccionario. Sin embargo, si la
                       clave tiene más de un valor,
                       ``__getitem__()`` retorna el último valor.

  ``__setitem__``       Establece la clave dada a ``[value]`` (una lista de
                        Python cuyo único elemento es ``value``). Nota que
                        ésta, como otras funciones de diccionario que tienen
                        efectos secundarios, sólo puede ser llamada en un
                        ``QueryDict`` mutable (uno que fue creado vía
                        ``copy()``).

    ``get()``           Si la clave tiene más de un valor, ``get()`` retorna
                        el último valor al igual que ``__getitem__``.

    ``update()``        Recibe ya sea un ``QueryDict`` o un diccionario
                        estándar. A diferencia del método ``update`` de los
                        diccionarios estándar, este método *agrega* elementos
                        al diccionario actual en vez de reemplazarlos::

                            >>> q = QueryDict('a=1')
                            >>> q = q.copy() # to make it mutable
                            >>> q.update({'a': '2'})
                            >>> q.getlist('a')
                            ['1', '2']
                            >>> q['a'] # returns the last
                            ['2']

    ``items()``         Similar al método ``items()`` de un diccionario
                        estándar, excepto que éste utiliza la misma lógica
                        del último-valor de ``__getitem()__``::

                             >>> q = QueryDict('a=1&a=2&a=3')
                             >>> q.items()
                             [('a', '3')]

    ``values()``        Similar al método ``values()`` de un diccionario
                        estándar, excepto que este utiliza la misma lógica
                        del último-valor de ``__getitem()__``.
==================  ============================================================

Además, ``QueryDict`` posee los métodos que se muestran en la Tabla H-4.

.. tabla:: Tabla H-4. Métodos QueryDict Extra (No relacionados con diccionarios)

==========================  ===============================================
    Método                      Descripción
==========================  ===============================================
``copy()``                  Retorna una copia del objeto, utilizando
                            ``copy.deepcopy()`` de la biblioteca estándar
                            de Python. La copia será mutable -- es decir,
                            puedes cambiar sus valores.

``getlist(key)``            Retorna los datos de la clave requerida, como
                            una lista de Python. Retorna una lista vacía
                            si la clave no existe. Se garantiza que
                            retornará una lista de algún tipo.

``setlist(key, list_)``     Establece la clave dada a ``list_`` (a
                            diferencia de ``__setitem__()``).

``appendlist(key, item)``   Agrega un elemento item a la lista interna
                            asociada a ``key``.

``setlistdefault(key, l)``  Igual a ``setdefault``, excepto que toma una
                            lista de valores en vez de un sólo valor.

``lists()``                 Similar a ``items()``, excepto que incluye
                            todos los valores, como una lista, para cada
                            miembro del diccionario. Por ejemplo::

                                 >>> q = QueryDict('a=1&a=2&a=3')
                                 >>> q.lists()
                                 [('a', ['1', '2', '3'])]


``urlencode()``             Retorna un string de los datos en formato
                            query-string (ej., ``"a=2&b=3&b=5"``).
==========================  ===============================================

Un ejemplo completo
-------------------

Por ejemplo, dado este formulario HTML::

    <form action="/foo/bar/" method="post">
    <input type="text" name="your_name" />
    <select multiple="multiple" name="bands">
        <option value="beatles">The Beatles</option>
        <option value="who">The Who</option>
        <option value="zombies">The Zombies</option>
    </select>
    <input type="submit" />
    </form>

Si el usuario ingresa ``"John Smith"`` en el campo ``your_name`` y selecciona
tanto "The Beatles" como "The Zombies" en la caja de selección múltiple, lo
siguiente es lo que contendrá el objeto request de Django::

    >>> request.GET
    {}
    >>> request.POST
    {'your_name': ['John Smith'], 'bands': ['beatles', 'zombies']}
    >>> request.POST['your_name']
    'John Smith'
    >>> request.POST['bands']
    'zombies'
    >>> request.POST.getlist('bands')
    ['beatles', 'zombies']
    >>> request.POST.get('your_name', 'Adrian')
    'John Smith'
    >>> request.POST.get('nonexistent_field', 'Nowhere Man')
    'Nowhere Man'

.. admonition:: Nota de implementación:

    Los atributos ``GET``, ``POST``, ``COOKIES``, ``FILES``, ``META``,
    ``REQUEST``, ``raw_post_data``, y ``user`` son todos cargados tardíamente.
    Esto significa que Django no gasta recursos calculando los valores de estos
    atributos hasta que tu código los solicita.

HttpResponse
============

A diferencia de los objetos ``HttpRequest``, los cuales son creados
automáticamente por Django, los objetos ``HttpResponse`` son tu
responsabilidad. Cada vista que escribas es responsable de instanciar,
poblar, y retornar un ``HttpResponse``.

La clase ``HttpResponse`` esta ubicada en ``django.http.HttpResponse``.

Construcción de HttpResponses
-----------------------------

Típicamente, tu construirás un ``HttpResponse`` para pasar los contenidos de
la pagina, como un string, al constructor de ``HttpResponse``::

    >>> response = HttpResponse("Here's the text of the Web page.")
    >>> response = HttpResponse("Text only, please.", mimetype="text/plain")

Pero si quieres agregar contenido de manera incremental, puedes usar
``response`` como un objeto similar a un archivo::

    >>> response = HttpResponse()
    >>> response.write("<p>Here's the text of the Web page.</p>")
    >>> response.write("<p>Here's another paragraph.</p>")

Puedes pasarle a ``HttpResponse`` un iterador en vez de pasarle strings
codificadas a mano. Si utilizas esta técnica, sigue estas instrucciones:

* El iterador debe retornar strings.

* Si un ``HttpResponse`` ha sido inicializado con un iterador como su
  contenido, no puedes usar la instancia ``HttpResponse`` como un objeto
  similar a un archivo. Si lo haces, emitirá ``Exception``.

Finalmente, nota que ``HttpResponse`` implementa un método ``write()``,
lo cual lo hace apto para usarlo en cualquier lugar que Python espere un
objeto similar a un archivo. Mira el :doc:`Capítulo 11<chapter11>` para ver algunos ejemplos
de la utilización de esta técnica.

Establecer las cabeceras
------------------------

Puedes agregar o eliminar cabeceras usando sintaxis de diccionario::

    >>> response = HttpResponse()
    >>> response['X-DJANGO'] = "It's the best."
    >>> del response['X-PHP']
    >>> response['X-DJANGO']
    "It's the best."

Puedes utilizar también ``has_header(header)`` para verificar la existencia de
una cabecera.

Evita configurar cabeceras ``Cookie`` a mano; en cambio, mira el :doc:`Capítulo 12<chapter12>`
para instrucciones sobre como trabajan las cookies en Django.

Subclases de HttpResponse
-------------------------

Django incluye un numero de subclases ``HttpResponse`` que manejan diferentes
tipos de respuestas HTTP (mira la Tabla H-5). Así como ``HttpResponse``, estas
subclases se encuentran en ``django.http``.

.. tabla:: Tabla H-5. Subclasses de HttpResponse

==================================  =======================================
    Clase                               Descripción
==================================  =======================================
 ``HttpResponseRedirect``           El constructor toma un único argumento:
                                    la ruta a la cual re-dirigir. Esta
                                    puede ser una URL completa (ej.,
                                    ``'http://search.yahoo.com/'``) o
                                    o una URL absoluta sin dominio (ej.,
                                    ``'/search/'``). Ten en cuenta que esto
                                    retorna un código de estado HTTP 302.

``HttpResponsePermanentRedirect``   Como ``HttpResponseRedirect``, pero
                                    esta retorna una re-dirección
                                    permanente (código de estado HTTP 301)
                                    en vez de una re-dirección "found"
                                    (código de estado 302).

``HttpResponseNotModified``         El constructor no tiene ningún
                                    argumento. Utiliza esta para designar
                                    que una página no ha sido modificada
                                    desde la última petición del usuario.

``HttpResponseBadRequest``          Actúa como ``HttpResponse`` pero usa
                                    un código de estado 400.

``HttpResponseNotFound``            Actúa como ``HttpResponse`` pero usa
                                    un código de estado 404.

``HttpResponseForbidden``            Actúa como ``HttpResponse`` pero usa
                                    un código de estado 403.

``HttpResponseNotAllowed``           Como ``HttpResponse``, pero usa un
                                    código de estado 405. Toma un único
                                    argumento: una lista de los métodos
                                    permitidos (ej., ``['GET', 'POST']``).

``HttpResponseGone``                 Actúa como ``HttpResponse`` pero usa
                                    un código de estado 410.

``HttpResponseServerError``          Actúa como ``HttpResponse`` pero usa
                                    un código de estado 500
==================================  =======================================

Puedes, por supuesto, definir tus propias subclases de ``HttpResponse`` para
permitir diferentes tipos de respuestas no admitidas por las clases estándar.

Retornar Errores
----------------

Retornar códigos de error HTTP en Django es fácil. Ya hemos mencionado las
subclases ``HttpResponseNotFound``, ``HttpResponseForbidden``,
``HttpResponseServerError``, y otras. Simplemente retorna una instancia de una
de estas subclases en lugar de una ``HttpResponse`` normal con el fin de
significar un error, por ejemplo::

    def my_view(request):
        # ...
        if foo:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            return HttpResponse('<h1>Page was found</h1>')

Debido a que el error 404 es por mucho el error HTTP más común, hay una manera
más fácil de manejarlo.

Cuando retornas un error tal como ``HttpResponseNotFound``, eres responsable
de definir el HTML de la página de error resultante::

    return HttpResponseNotFound('<h1>Page not found</h1>')

Por consistencia, y porque es una buena idea tener una página de error 404
consistente en todo tu sitio, Django provee una excepción ``Http404``. Si tu
emites una ``Http404`` en cualquier punto de una vista de función, Django la
atrapará y retornará la página de error estándar de tu aplicación, junto con un
código de error HTTP 404.

Éste es un ejemplo::

    from django.http import Http404

    def detail(request, poll_id):
        try:
            p = Poll.objects.get(pk=poll_id)
        except Poll.DoesNotExist:
            raise Http404
        return render_to_response('polls/detail.html', {'poll': p})

Con el fin de usar la excepción ``Http404`` al máximo, deberías crear una
plantilla que se muestra cuando un error 404 es emitido. Esta plantilla debería
ser llamada ``404.html``, y debería colocarse en el nivel superior de tu árbol de
plantillas.

Personalizar la Vista 404 (Not Found)
-------------------------------------

Cuando tu emites una excepción ``Http404``, Django carga una vista especial
dedicada a manejar errores 404. Por omisión, es la vista
``django.views.defaults.page_not_found``, la cual carga y renderiza la
plantilla ``404.html``.

Esto significa que necesitas definir una plantilla ``404.html`` en tu
directorio raíz de plantillas. Esta plantilla será usada para todos los
errores 404.

Esta vista ``page_not_found`` debería ser suficiente para el 99% de las
aplicaciones Web, pero si tu quieres reemplazar la vista 404, puedes
especificar ``handler404`` en tu URLconf, de la siguiente manera::

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        ...
    )

    handler404 = 'mysite.views.my_custom_404_view'

Detrás de escena, Django determina la vista 404 buscando por ``handler404``.
Por omisión, las URLconfs contienen la siguiente línea::

    from django.conf.urls.defaults import *

Esto se encarga de establecer ``handler404`` en el módulo actual. Como puedes
ver en ``django/conf/urls/defaults.py``, ``handler404`` esta fijado a
``'django.views.defaults.page_not_found'`` por omisión.

Hay tres cosas para tener en cuenta sobre las vistas 404:

* La vista 404 es llamada también si Django no encuentra una coincidencia
  después de verificar toda expresión regular en la URLconf.

* Si no defines tu propia vista 404 -- y simplemente usas la predeterminada,
  lo cual es recomendado -- tu aún tienes una obligación: crear una
  plantilla ``404.html`` en la raíz de tu directorio de plantillas. La
  vista 404 predeterminada usará esa plantilla para todos los errores 404.

* Si ``DEBUG`` esta establecido a ``True`` (en tu modulo de configuración),
  entonces tu vista 404 nunca será usada, y se mostrará en su lugar el
  trazado de pila.

Personalizar la Vista 500 (Server Error)
----------------------------------------

De manera similar, Django ejecuta comportamiento de caso especial en el caso
de errores de ejecución en el código de la vista. Si una vista resulta en una
excepción, Django llamará, de manera predeterminada, a la vista
``django.views.defaults.server_error``, la cual carga y renderiza la plantilla
``500.html``.

Esto significa que necesitas definir una plantilla ``500.html`` en el directorio
raíz de plantillas. Esta plantilla será usada para todos los errores de
servidor.

Esta vista ``server_error`` debería ser suficiente para el 99% de las
aplicaciones Web, pero si tu quieres reemplazar la vista, puedes especificar
``handler500`` en tu URLconf, de la siguiente manera::

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        ...
    )

    handler500 = 'mysite.views.my_custom_error_view'

