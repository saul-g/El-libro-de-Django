============================
Capítulo 9: Vistas genéricas
============================

De nuevo aparece aquí un tema recurrente en este libro: en el peor de los casos,
el desarrollo Web es aburrido y monótono. Hasta aquí, hemos cubierto cómo Django
trata de alejar parte de esa monotonía en las capas del modelo y las plantillas,
pero los desarrolladores Web también experimentan este aburrimiento al nivel de
las vistas.

Las *vistas genéricas* de Django fueron desarrolladas para aliviar ese dolor.
Éstas recogen ciertos estilos y patrones comunes encontrados en el desarrollo de
vistas y los abstraen, de modo que puedas escribir rápidamente vistas comunes de
datos sin que tengas que escribir mucho código. De hecho, casi todos los
ejemplos de vistas en los capítulos precedentes pueden ser reescritos con la
ayuda de vistas genéricas.

El Capítulo 8 refirió brevemente sobre cómo harías para crear una vista
"genérica". Para repasar, podemos reconocer ciertas tareas comunes, como mostrar
una lista de objetos, y escribir código que muestra una lista de *cualquier*
objeto. Por lo tanto el modelo en cuestión puede ser pasado como un argumento
extra a la URLconf.

Django viene con vistas genéricas para hacer lo siguiente:

    * Realizar tareas "sencillas" comunes: redirigir a una página diferente y
      renderizar una plantilla dada.

    * Mostrar páginas de listado y detalle para un solo objeto. Las vistas
      ``event_list`` y ``entry_list`` del :doc:`Capítulo 8<chapter08>`
      son ejemplos de vistas de listado. Una página de evento simple 
      es un ejemplo de lo que llamamos vista "detallada".

    * Presentar objetos basados en fechas en páginas de archivo de tipo
      día/mes/año, su detalle asociado, y las páginas "más recientes". Los
      archivos por día, mes, año del Weblog de Django
      (http://www.djangoproject.com/weblog/) están construidos con ellas, como
      lo estarían los típicos archivos de un periódico.

    * Permitir a los usuarios crear, actualizar y borrar objetos -- con o sin
      autorización.

Agrupadas, estas vistas proveen interfaces fáciles para realizar las tareas más
comunes que encuentran los desarrolladores.

Usar vistas genéricas
=====================

Todas estas vistas se usan creando diccionarios de configuración en tus archivos
URLconf y pasando estos diccionarios como el tercer miembro de la tupla URLconf
para un patrón dado.

Por ejemplo, ésta es una URLconf simple que podrías usar para presentar una
página estática "about" (acerca de)::

    from django.conf.urls.defaults import *
    from django.views.generic.simple import direct_to_template

    urlpatterns = patterns('',
        ('^about/$', direct_to_template, {
            'template': 'about.html'
        })
    )

Aunque esto podría verse un poco "mágico" a primera vista -- ¡mira, una vista
sin código! --, es en realidad exactamente lo mismo que los ejemplos en el
:doc:`Capítulo 8<chapter08>`: la vista ``direct_to_template`` 
simplemente toma información del diccionario de parámetros extra
y usa esa información cuando renderiza la vista.

Ya que esta vista genérica -- y todas las otras -- es una función de vista
regular como cualquier otra, podemos reusarla dentro de nuestras propias vistas.
Como ejemplo, extendamos nuestro ejemplo "about" para mapear URLs de la forma
``/about/<cualquiercosa>/`` para renderizar estáticamente
``/about/<cualquiercosa>.html``. Haremos esto primero modificando la URLconf
para que apunte a una función de vista:

.. code-block: python  

    from django.conf.urls.defaults import *
    from django.views.generic.simple import direct_to_template
    **from mysite.books.views import about_pages**

    urlpatterns = patterns('',
        ('^about/$', direct_to_template, {
            'template': 'about.html'
        }),
        **('^about/(\w+)/$', about_pages),**
    )

A continuación, escribimos la vista ``about_pages``::


    from django.http import Http404
    from django.template import TemplateDoesNotExist
    from django.views.generic.simple import direct_to_template

    def about_pages(request, page):
        try:
            return direct_to_template(request, template="about/%s.html" % page)
        except TemplateDoesNotExist:
            raise Http404()

Aquí estamos tratando ``direct_to_template`` como cualquier otra función. Ya que
esta devuelve una ``HttpResponse``, podemos retornarlo así como está. La única
ligera dificultad aquí es ocuparse de las plantillas perdidas. No queremos que
una plantilla inexistente cause un error de servidor, por lo tanto atrapamos las
excepciones ``TemplateDoesNotExist`` y en su lugar devolvemos errores 404.

.. admonition:: ¿Hay una vulnerabilidad de seguridad aquí?

    Los lectores atentos pueden haber notado un posible agujero de seguridad:
    estamos construyendo el nombre de la plantilla usando contenido interpolado
    proveniente del navegador (``template="about/%s.html" % page``). A primera
    vista, esto parece como una clásica vulnerabilidad de *recorrido de
    directorio* [#]_ (discutida en detalle en el :doc:`Capítulo 19<chapter19>`). ¿Pero es
    realmente una vulnerabilidad?

    No exactamente. Sí, un valor creado maliciosamente de ``page`` podría causar
    un recorrido de directorio, pero aunque ``page`` *es* tomado de la URL
    solicitada, no todos los valores serán aceptados. La clave esta en la
    URLconf: estamos usando la expresión regular ``\w+`` para verificar la parte
    ``page`` de la URL y ``\w`` sólo acepta letras y números. Por lo tanto,
    cualquier caracter malicioso (puntos y barras, en este caso) serán
    rechazadas por el sistema de resolución de URLs antes de alcanzar la vista en sí.

Vistas genéricas de objetos
===========================

La vista genérica ``direct_to_template`` ciertamente es útil, pero las vistas
genéricas de Django brillan realmente cuando se trata de presentar vistas del
contenido de tu base de datos. Ya que es una tarea tan común, Django viene con
un puñado de vistas genéricas incluidas que hacen la generación de vistas de
listado y detalle de objetos increíblemente fácil.

Demos un vistazo a una de estas vistas genéricas: la vista "object list".
Usaremos el objeto ``Publisher`` del :doc:`Capítulo 5<chapter05>`::

    class Publisher(models.Model):
        name = models.CharField(maxlength=30)
        address = models.CharField(maxlength=50)
        city = models.CharField(maxlength=60)
        state_province = models.CharField(maxlength=30)
        country = models.CharField(maxlength=50)
        website = models.URLField()

        def __unicode__(self):
            return self.name

        class Meta:
            ordering = ["-name"]

        class Admin:
            pass


Para construir una página listado de todos los books, usaremos la URLconf bajo
estas líneas::

    from django.conf.urls.defaults import *
    from django.views.generic import list_detail
    from mysite.books.models import Publisher

    publisher_info = {
        "queryset" : Publisher.objects.all(),
    }

    urlpatterns = patterns('',
        (r'^publishers/$', list_detail.object_list, publisher_info)
    )

Ese es todo el código Python que necesitamos escribir. Sin embargo, todavía
necesitamos escribir una plantilla. Podríamos decirle explícitamente a la vista
``object_list`` que plantilla debe usar incluyendo una clave ``template_name``
en el diccionario de argumentos extra, pero en la ausencia de una plantilla
explícita Django inferirá una del nombre del objeto. En este caso, la plantilla
inferida será ``"books/publisher_list.html"`` -- la parte "books" proviene del
nombre de la aplicación que define el modelo, mientras que la parte "publisher"
es sólo la versión en minúsculas del nombre del modelo.

Esta plantilla será renderizada en un contexto que contiene una variable llamada
``object_list`` la cual contiene todos los objetos book. Una plantilla muy
simple podría verse como la siguiente:

.. code-block:: html 

    {% extends "base.html" %}

    {% block content %}
        <h2>Publishers</h2>
        <ul>
            {% for publisher in object_list %}
                <li>{{ publisher.name }}</li>
            {% endfor %}
        </ul>
    {% endblock %}

Eso es realmente todo en lo referente al tema. Todas las geniales
características de las vistas genéricas provienen de cambiar el diccionario
"info" pasado a la vista genérica. El Apéndice D documenta todas las vistas
genéricas y todas sus opciones en detalle; el resto de este capítulo considerará
algunas de las maneras comunes en que tú puedes personalizar y extender las
vistas genéricas.

Extender las vistas genéricas
=============================

No hay duda de que usar las vistas genéricas puede acelerar el desarrollo
sustancialmente. En la mayoría de los proyectos, sin embargo, llega un momento
en el que las vistas genéricas no son suficientes. De hecho, la pregunta más
común que se hacen los nuevos desarrolladores de Django es cómo hacer que las
vistas genéricas manejen un rango más amplio de situaciones.

Afortunadamente, en casi cada uno de estos casos, hay maneras de simplemente
extender las vistas genéricas para manejar un conjunto más amplio de casos de
uso. Estas situaciones usualmente recaen en un puñado de patrones que se tratan
en las secciones que siguen.

Crear contextos de plantilla "amistosos"
----------------------------------------

Tal vez hayas notado que el ejemplo de la plantilla publisher list almacena
todos los books en una variable llamada ``object_list``. Aunque que esto
funciona bien, no es una forma "amistosa" para los autores de plantillas: ellos
sólo tienen que "saber" aquí que están trabajando con books. Un nombre mejor
para esa variable sería ``publisher_list``; el contenido de esa variable es
bastante obvio.

Podemos cambiar el nombre de esa variable fácilmente con el argumento
``template_object_name``:

.. code-block:: python  
 
    publisher_info = {
        "queryset" : Publisher.objects.all(),
        **"template_object_name" : "publisher",**
    }

    urlpatterns = patterns('',
        (r'^publishers/$', list_detail.object_list, publisher_info)
    )

Proveer un ``template_object_name`` útil es siempre una buena idea. Tus
compañeros de trabajo que diseñan las plantillas te lo agradecerán.

Agregar un contexto extra
-------------------------

A menudo simplemente necesitas presentar alguna información extra aparte de la
proporcionada por la vista genérica. Por ejemplo, piensa en mostrar una lista
de todos los otros publisher en cada página de detalle de un publisher. La vista
genérica ``object_detail`` provee el publisher al contexto, pero parece que no
hay forma de obtener una lista de *todos* los publishers en esa plantilla.

Pero sí la hay: todas las vistas genéricas toman un parámetro opcional extra,
``extra_context``. Este es un diccionario de objetos extra que serán agregados
al contexto de la plantilla. Por lo tanto, para proporcionar la lista de todos
los publishers en la vista de detalles, usamos un diccionario info como el que
sigue:

.. code-block:: python  

    publisher_info = {
        "queryset" : Publisher.objects.all(),
        "template_object_name" : "publisher",
        **"extra_context" : {"book_list" : Book.objects.all()}**
    }

Esto llenaría una variable ``{{ book_list }}`` en el contexto de la plantilla.
Este patrón puede ser usado para pasar cualquier información hacia la plantilla
para la vista genérica. Es muy práctico.

Sin embargo, en realidad hay un error sutil aquí -- ¿puedes detectarlo?

El problema aparece cuando las consultas en ``extra_context`` son evaluadas.
Debido a que este ejemplo coloca ``Publisher.objects.all()`` en la URLconf, sólo
se evaluará una vez (cuando la URLconf se cargue por primera vez). Una vez que
agregues o elimines publishers, notarás que la vista genérica no refleja estos
cambios hasta que reinicias el servidor Web (mira "Almacenamiento en caché y
QuerySets" en el Apéndice C para mayor información sobre cuándo los QuerySets
son almacenados en la cache y evaluados).

Este problema no se aplica al argumento ``queryset`` de las vistas
genéricas. Ya que Django sabe que ese QuerySet en particular *nunca* debe 
ser almacenado en la caché, la vista genérica se hace cargo de limpiar la
caché cuando cada vista es renderizada.

La solución es usar un callback [#]_ en ``extra_context`` en vez de un valor.
Cualquier callable [#]_ (por ejemplo, una función) que sea pasado a
``extra_context`` será evaluado cuando su vista sea renderizada (en vez de sólo
la primera vez). Puedes hacer esto con una función explícitamente definida:

.. code-block:: python  

    def get_books():
        return Book.objects.all()

    publisher_info = {
        "queryset" : Publisher.objects.all(),
        "template_object_name" : "publisher",
        "extra_context" : **{"book_list" : get_books}**
    }

o puedes usar una versión menos obvia pero más corta que se basa en el hecho de
que ``Publisher.objects.all`` es en sí un callable:

.. code-block:: python  

    publisher_info = {p
        "queryset" : Publisher.objects.all(),
        "template_object_name" : "publisher",
        "extra_context" : **{"book_list" : Book.objects.all}**
    }

Nota la falta de paréntesis después de ``Book.objects.all``; esto hace
referencia a la función sin invocarla realmente (cosa que hará la vista genérica
luego).

Mostrar subconjuntos de objetos
-------------------------------

Ahora echemos un vistazo más de cerca a esta clave ``queryset`` que hemos venido
usando hasta aquí. La mayoría de las vistas genéricas usan uno de estos
argumentos ``queryset`` -- es la manera en que la vista conoce qué conjunto de
objetos mostrar (mira "Seleccionando objetos" en el :doc:`Capítulo 5<chapter05>` para una
introducción a los QuerySets, y mira el Apéndice C para los detalles completos).

Para tomar un ejemplo simple, tal vez querríamos ordenar una lista de books por
fecha de publicación, con el más reciente primero.

.. code-block:: python  

    book_info = {
        "queryset" : Book.objects.all().order_by("-publication_date"),
    }

    urlpatterns = patterns('',
        (r'^publishers/$', list_detail.object_list, publisher_info),
        **(r'^books/$', list_detail.object_list, book_info),**
    )


Este es un muy lindo y simple ejemplo, pero ilustra bien la idea. Por supuesto,
tú usualmente querrás hacer más que sólo reordenar objetos. Si quieres presentar
una lista de books de un publisher particular, puedes usar la misma técnica:

.. code-block:: python  

    **apress_books = {**
        **"queryset": Book.objects.filter(publisher__name="Apress Publishing"),**
        **"template_name" : "books/apress_list.html"**
    **}**

    urlpatterns = patterns('',
        (r'^publishers/$', list_detail.object_list, publisher_info),
        **(r'^books/apress/$', list_detail.object_list, apress_books),**
    )

Nota que además de un ``queryset`` filtrado, también estamos usando un nombre de
plantilla personalizado. Si no lo hiciéramos, la vista genérica usaría la misma
plantilla que la lista de objetos "genérica" [#]_, que puede no ser lo que
queremos.

También nota que ésta no es una forma muy elegante de hacer publisher-specific
books. Si queremos agregar otra página publisher, necesitamos otro puñado de
líneas en la URLconf, y más de unos pocos publishers no será razonable.
Enfrentaremos este problema en la siguiente sección.

Si obtienes un error 404 cuando solicitas ``/books/apress/``, para estar
seguro, verifica que en realidad tienes un Publisher con el nombre 'Apress
Publishing'. Las vistas genéricas tienen un parámetro ``allow_empty`` para
este caso. Mira el Apéndice D para mayores detalles.

Filtrado complejo con funciones adaptadoras
-------------------------------------------

Otra necesidad común es filtrar los objetos que se muestran en una página
listado por alguna clave en la URLconf. Anteriormente codificamos [#]_ el nombre
del publisher en la URLconf, pero ¿qué pasa si queremos escribir una vista que
muestre todos los books por algún publisher arbitrario?. Podemos "encapsular" [#]_
la vista genérica ``object_list`` para evitar escribir mucho código a mano. Como
siempre, empezamos escribiendo una URLconf.

.. code-block:: python  

    urlpatterns = patterns('',
        (r'^publishers/$', list_detail.object_list, publisher_info),
        **(r'^books/(\w+)/$', books_by_publisher),**
    )

A continuación, escribiremos la vista ``books_by_publisher``:

.. code-block:: python  

    from django.http import Http404
    from django.views.generic import list_detail
    from mysite.books.models import Book, Publisher

    def books_by_publisher(request, name):

        # Look up the publisher (and raise a 404 if it can't be found).
        try:
            publisher = Publisher.objects.get(name__iexact=name)
        except Publisher.DoesNotExist:
            raise Http404

        # Use the object_list view for the heavy lifting.
        return list_detail.object_list(
            request,
            queryset = Book.objects.filter(publisher=publisher),
            template_name = "books/books_by_publisher.html",
            template_object_name = "books",
            extra_context = {"publisher" : publisher}
        )

Esto funciona porque en realidad no hay nada en especial sobre las vistas
genéricas -- son sólo funciones Python. Como cualquier función de vista,
las vistas genéricas esperan un cierto conjunto de argumentos y retornan objetos
``HttpResponse``. Por lo tanto, es increíblemente fácil encapsular una pequeña
función sobre una vista genérica que realiza trabajo adicional antes (o después;
mira la siguiente sección) de pasarle el control a la vista genérica.

.. admonition::

    Nota que en el ejemplo anterior pasamos el publisher que se está mostrando
    actualmente en el ``extra_context``. Esto es usualmente una buena idea en
    wrappers de esta naturaleza; le permite a la plantilla saber qué objeto
    "padre" esta siendo navegado en ese momento.

Realizar trabajo extra
----------------------

El último patrón común que veremos involucra realizar algún trabajo extra antes
o después de llamar a la vista genérica.

Imagina que tenemos un campo ``last_accessed`` en nuestro objeto ``Author`` que
estuvimos usando para tener un registro de la última vez que alguien vio ese
author. La vista genérica ``object_detail``, por supuesto, no sabría nada sobre
este campo, pero una vez más fácilmente podríamos escribir una vista
personalizada para mantener ese campo actualizado.

Primero, necesitamos agregar una pequeña parte de detalle sobre el author en la
URLconf para que apunte a una vista personalizada:

.. code-block:: python  

    from mysite.books.views import author_detail

    urlpatterns = patterns('',
        #...
        **(r'^authors/(?P<author_id>\d+)/$', author_detail),**
    )

Luego escribiremos nuestra función wrapper:

.. code-block:: python  

    import datetime
    from mysite.books.models import Author
    from django.views.generic import list_detail
    from django.shortcuts import get_object_or_404

    def author_detail(request, author_id):
        # Look up the Author (and raise a 404 if she's not found)
        author = get_object_or_404(Author, pk=author_id)

        # Record the last accessed date
        author.last_accessed = datetime.datetime.now()
        author.save()

        # Show the detail page
        return list_detail.object_detail(
            request,
            queryset = Author.objects.all(),
            object_id = author_id,
        )
.. admonition:: 
    Este código en realidad no funcionará a menos que agregues un campo
    ``last_accessed`` a tu modelo ``Author`` y agregues una plantilla
    ``books/author_detail.html``.

Podemos usar un método similar para alterar la respuesta devuelta por la vista
genérica. Si quisiéramos proporcionar una versión en texto plano [#]_ que se pueda
descargar desde la lista de autores, podríamos usar una vista como esta:

.. code-block:: python  

    def author_list_plaintext(request):
        response = list_detail.object_list(
            request,
            queryset = Author.objects.all(),
            mimetype = "text/plain",
            template_name = "books/author_list.txt"
        )
        response["Content-Disposition"] = "attachment; filename=authors.txt"
        return response

Esto funciona porque la vista genérica devuelve simplemente objetos
``HttpResponse`` que pueden ser tratados como diccionarios para establecer las
cabeceras HTTP. Este arreglo de ``Content-Disposition``, por otro lado,
instruye al navegador a descargar y guardar la página en vez de mostrarla en
pantalla.

¿Qué sigue?
===========

En este capítulo hemos examinado sólo un par de las vistas genéricas que incluye
Django, pero las ideas generales presentadas aquí deberían aplicarse a cualquier
vista genérica. El Apéndice D cubre todas las vistas disponibles en detalle, y
es de lectura obligada si quieres sacar el mayor provecho de esta
característica.

En el :doc:`próximo capítulo<chapter10>` ahondamos profundamente en el funcionamiento interno
de las plantillas de Django, mostrando todas las maneras geniales en que pueden
ser extendidas. Hasta ahora, hemos tratado el sistema de plantillas meramente
como una herramienta estática que puedes usar para renderizar tu contenido.


.. [#] \N. del T.: directory traversal vulnerability.
.. [#] \N. del T.: llamada a función.
.. [#] \N. del T.: en Python cualquier objeto puede ser llamado como función.
.. [#] \N. del T.: "vanilla" object list.
.. [#] \N. del T.: hard-coded.
.. [#] \N. del T.: "wrap".
.. [#] \N. del T.: en texto plano.

