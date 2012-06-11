============================================
Capítulo 11: Generación de contenido no HTML
============================================

Usualmente cuando hablamos sobre desarrollo de sitios Web, hablamos de producir
HTML. Por supuesto, hay mucho más que contenido HTML en la Web; la usamos para
distribuir datos en todo tipo de formatos: RSS, PDFs, imágenes, y así
sucesivamente.

Hasta ahora nos hemos concentrado en el caso común de la producción de HTML,
pero en ese capítulo tomaremos un desvío y veremos cómo usar Django para
producir otro tipo de contenido.

Django posee varias herramientas útiles que puedes usar para producir algunos
tipos comunes de contenido no HTML:

    * *Feeds* de sindicación RSS/Atom

    * Mapas de sitios haciendo uso de *Sitemaps* (un formato XML originalmente
      desarrollado por Google que provee de ayuda a motores de búsqueda)

Examinaremos cada una de esas herramientas un poco más adelante, pero antes
cubriremos los principios básicos.

Lo básico: Vistas y tipos MIME
==============================

¿Recuerdas esto del :doc:`Capítulo 3<chapter03>`?

    Una función vista, o una *vista* por abreviar, es simplemente una función en
    Python que recibe una petición Web y retorna una respuesta Web. Esta
    respuesta puede ser el contenido HTML de una página Web, una redirección, un
    error 404, un documento XML, una imagen... en realidad, cualquier cosa.

Más formalmente, una función *vista* Django *debe*

    * Aceptar una instancia ``HttpRequest`` como primer argumento.

    * Retornar una instancia ``HttpResponse``.

La clave para retornar contenido no HTML desde una vista reside en la
clase ``HttpResponse``, específicamente en el argumento ``mimetype`` del
constructor. Cambiando el tipo MIME, podemos indicarle al navegador que hemos
retornado una respuesta en un formato diferente.

Por ejemplo, veamos una vista que devuelve una imagen PNG. Para mantener las
cosas sencillas, simplemente leeremos un fichero desde el disco::

    from django.http import HttpResponse

    def my_image(request):
        image_data = open("/path/to/my/image.png", "rb").read()
        return HttpResponse(image_data, mimetype="image/png")

¡Eso es todo! Si sustituimos la ruta de la imagen en la llamada a ``open()`` con
la ruta a una imagen real, podemos usar esta vista bastante sencilla para servir
una imagen, y el navegador la mostrará correctamente.

La otra cosa importante a tener presente es que los objetos ``HttpResponse``
implementan el API estándar de Python para ficheros.  Esto significa que podemos
usar una instancia de ``HttpResponse`` en cualquier lugar donde Python (o
biblioteca de terceros) espera un fichero.

Como un ejemplo de cómo funciona esto, veamos la producción de CSV con Django.

Producción de CSV
=================

CSV es un formato de datos sencillo que suele ser usada por programas de hojas de
cálculo. Básicamente es una serie de filas en una tabla, cada celda en la fila
está separada por comas (CSV significa *comma-separated values*). Por ejemplo,
aquí tienes una lista de pasajeros "problemáticos" en líneas aéreas en formato
CSV::

    Year,Unruly Airline Passengers
    1995,146
    1996,184
    1997,235
    1998,200
    1999,226
    2000,251
    2001,299
    2002,273
    2003,281
    2004,304
    2005,203
    
.. admonition::

    El listado precedente contiene números reales; cortesía de la
    Administración Federal de Aviación (FAA) de E.E.U.U. Vea
    http://www.faa.gov/data_statistics/passengers_cargo/unruly_passengers/.

Aunque CSV parezca simple, no es un formato que ha sido definido formalmente.
Diferentes programas producen y consumen diferentes variantes de CSV,
haciendo un poco complicado usarlo.  Afortunadamente, Python incluye una
biblioteca estándar para CSV, ``csv``, que es bastante robusta.

Debido a que el módulo ``csv`` opera sobre objetos similares a ficheros, es muy
fácil usar un ``HttpResponse`` en lugar de un fichero::

    import csv
    from django.http import HttpResponse

    # Número de pasajeros problematicos por año entre 1995 - 2005. En una aplicación real
    # esto vendría desde una base de datos o cualquier otro medio de almacenamiento.
    UNRULY_PASSENGERS = [146,184,235,200,226,251,299,273,281,304,203]

    def unruly_passengers_csv(request):
        # Creamos el objeto Httpresponse con la cabecera CSV apropiada.
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=unruly.csv'

        # Creamos un escritor CSV usando a HttpResponse como "fichero"
        writer = csv.writer(response)
        writer.writerow(['Year', 'Unruly Airline Passengers'])
        for (year, num) in zip(range(1995, 2006), UNRULY_PASSENGERS):
            writer.writerow([year, num])

        return response

El código y los comentarios deberían ser bastante claros, pero hay unas pocas
cosas que merecen mención especial:

    * Se le da a la respuesta el tipo MIME ``text/csv`` (en lugar del tipo
      predeterminado ``text/html``). Esto le dice a los navegadores que el
      documento es un fichero CSV.

    * La respuesta obtiene una cabecera ``Content-Disposition`` adicional, la
      cual contiene el nombre del fichero CSV. Esta cabecera (bueno, la parte
      "adjunta") le indicará al navegador que solicite la ubicación donde
      guardará el fichero (en lugar de simplemente mostrarlo). El nombre de
      fichero es arbitrario; llámalo como quieras. Será usado por los navegadores
      en el cuadro de diálogo "Guardar como..."

    * Usar el API de generación de CSV es sencillo: basta pasar ``response``
      como primer argumento a ``csv.writer``. La función ``csv.writer`` espera
      un objeto de tipo fichero, y los de tipo ``HttpResponse`` se ajustan.

    * Por cada fila en el fichero CSV, invocamos a ``writer.writerow``,
      pasándole un objeto iterable como una lista o una tupla.

    * El módulo CSV se encarga de poner comillas por ti, así que no tendrás que
      preocuparte por *escapar* caracteres en las cadenas que tengan comillas o
      comas en su interior. Limítate a pasar la información a ``writerow()``,
      que hará lo correcto.

Este es el patrón general que usarás siempre que necesites retornar contenido no
HTML: crear un objeto ``HttpResponse`` de respuesta (con un tipo MIME especial),
pasárselo a algo que espera un fichero, y luego devolver la respuesta.

Veamos unos cuántos ejemplos más.

Generar PDFs
============

El Formato Portable de Documentos (PDF, por Portable Document Format) es un
formato desarrollado por Adobe que es usado para representar documentos
imprimibles, completos con formato perfecto hasta un nivel de detalle medido en
pixels, tipografías empotradas y gráficos de vectores en 2D. Puedes pensar en un
documento PDF como el equivalente digital de un documento impreso;
efectivamente, los PDFs se usan normalmente cuando se necesita entregar un
documento a alguien para que lo imprima.

Puedes generar PDFs fácilmente con Python y Django gracias a la excelente
biblioteca open source ReportLab (http://www.reportlab.org/rl_toolkit.html).
La ventaja de generar ficheros PDFs dinámicamente es que puedes crear PDFs a
medida para diferentes propósitos -- supongamos, para diferentes usuarios u
diferentes contenidos.

Por ejemplo, hemos usado Django y ReportLab en KUSports.com para generar
programas de torneos de la NCAA personalizados, listos para ser impresos.

Instalar ReportLab
------------------

Antes de que puedas generar ningún PDF, deberás instalar ReportLab.
Esto es usualmente muy simple: sólo descarga e instala la biblioteca desde
http://www.reportlab.org/downloads.html.

La guía del usuario (naturalmente sólo disponible en formato PDF) en
http://www.reportlab.org/rsrc/userguide.pdf contiene instrucciones de
instalación adicionales.

.. admonition::

    Si estás usando una distribución moderna de Linux, podrías desear comprobar
    con la utilidad de manejo de paquetes de software antes de instalar
    ReportLab. La mayoría de los repositorios de paquetes ya incluyen ReportLab.

    Por ejemplo, si estás usando la (excelente) distribución Ubuntu, un simple
    ``apt-get install python-reportlab`` hará la magia necesaria.

Prueba tu instalación importando la misma en el intérprete interactivo Python::

    >>> import reportlab

Si ese comando no lanza ningún error, la instalación funcionó.

Escribir tu Vista
-----------------

Del mismo modo que CSV, la generación de PDFs en forma dinámica con Django es
sencilla porque la API ReportLab actúa sobre objetos similares a ficheros
(*file-like* según la jerga Python).

A continuación un ejemplo "Hola Mundo"::

    from reportlab.pdfgen import canvas
    from django.http import HttpResponse

    def hello_pdf(request):
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=hello.pdf'

        # Create the PDF object, using the response object as its "file."
        p = canvas.Canvas(response)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 100, "Hello world.")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        return response

Son necesarias alguna notas:

    * Usamos el tipo MIME ``application/pdf``. Esto le indica al navegador que
      el documento es un fichero PDF y no un fichero HTML. Si no incluyes esta
      información, los navegadores web probablemente interpretarán la respuesta
      como HTML, lo que resultará en jeroglíficos en la ventana del navegador.

    * Interactuar con la API ReportLab es sencillo: sólo pasa ``response`` como
      el primer argumento a ``canvas.Canvas``. La clase ``Canvas`` espera un
      objeto *file-like*, y los objetos ``HttpResponse`` se ajustarán a la norma.

    * Todos los métodos de generación de PDF subsecuentes son llamados
      pasándoles el objeto PDF (en este caso ``p``), no ``response``.

    * Finalmente, es importante llamar a los métodos ``showPage()`` y ``save()``
      del objeto PDF (de otra manera obtendrás un fichero PDF corrupto).

PDFs complejos
--------------

Si estás creando un documento PDF complejo (o cualquier pieza de datos de gran
tamaño), considera usar la biblioteca ``cStringIO`` como un lugar de
almacenamiento temporario para tu fichero PDF. La biblioteca ``cStringIO``
provee una interfaz vía objetos *file-like* que está escrita en C para máxima
eficiencia.

Ese es el ejemplo "Hola Mundo" anterior modificado para usar ``cStringIO``::

    from cStringIO import StringIO
    from reportlab.pdfgen import canvas
    from django.http import HttpResponse

    def hello_pdf(request):
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=hello.pdf'

        temp = StringIO()

        # Create the PDF object, using the StringIO object as its "file."
        p = canvas.Canvas(temp)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 100, "Hello world.")

        # Close the PDF object cleanly.
        p.showPage()
        p.save()

        # Get the value of the StringIO buffer and write it to the response.
        response.write(temp.getvalue())
        return response

Otras posibilidades
===================

Hay infinidad de otros tipos de contenido que puedes generar en Python.
Aquí tenemos algunas otras ideas y las bibliotecas que podrías usar para
implementarlas:

    * *Archivos ZIP*: La biblioteca estándar de Python contiene el módulo
      ``zipfile``, que puede escribir y leer ficheros comprimidos en formato ZIP.
      Puedes usarla para guardar ficheros bajo demanda, o quizás comprimir
      grandes documentos cuando lo requieran. De la misma manera puedes generar
      ficheros en formato TAR usando el módulo de la biblioteca estándar ``tarfile``.

    * *Imágenes Dinámicas*: Biblioteca Python de procesamiento de Imágenes
      (Python Imaging Library, PIL; http://www.pythonware.com/products/pil/) es
      una herramienta fantástica para producir imágenes (PNG, JPEG, GIF, y
      muchas más). Puedes usarla para escalar automáticamente imágenes para
      generar miniaturas, agrupar varias imágenes en un solo marco e incluso
      realizar procesamiento de imágenes directamente en la web.

    * *Ploteos y Gráficos*: Existe un número importante de increíblemente
      potentes bibliotecas de Python para Ploteo y Gráficos, que se pueden
      utilizar para generar mapas, dibujos, ploteos y gráficos. Es imposible
      listar todas las bibliotecas, así que resaltamos algunas de ellas:

        * ``matplotlib`` (http://matplotlib.sourceforge.net/) puede usarse para
          generar ploteos de alta calidad al estilo de los generados con MatLab
          o Mathematica.

        * ``pygraphviz`` (https://networkx.lanl.gov/wiki/pygraphviz), una
          interfaz con la herramienta Graphviz (http://graphviz.org/), puede
          usarse para generar diagramas estructurados de grafos y redes.

En general, cualquier biblioteca Python capaz de escribir en un fichero puede ser
utilizada dentro de Django. Las posibilidades son realmente interminables.

Ahora que hemos visto lo básico de generar contenido no-HTML, avancemos al
siguiente nivel de abstracción. Django incluye algunas herramientas bonitas e
ingeniosas para generar cierto tipo de contenido no-HTML.

El Framework de Feeds de Sindicación
====================================

Django incluye un framework para la generación y sindicación de *feeds* de alto
nivel que permite crear feeds RSS y Atom de manera sencilla.

.. exhortacion:: ¿Qué es RSS? ¿Qué es Atom?

    RSS y Atom son formatos basados en XML que se puede utilizar para actualizar
    automáticamente los "feeds" con el contenido de tu sitio. Lee más sobre RSS
    en http://www.whatisrss.com/, y obtén información sobre Atom en
    http://www.atomenabled.org/.

Para crear cualquier feed de sindicación, todo lo que debes hacer es escribir una
corta clase Python. Puedes crear tantos feeds como desees.

El framework de generación de feeds de alto nivel es una vista enganchada a
``/feeds/`` por convención. Django usa el final de la URL (todo lo que este
después de ``/feeds/``) para determinar qué feed retornar.

Para crear un feed, necesitas escribir una clase ``Feed`` y hacer referencia a
la misma en tu URLconf (ver los Capítulos 3 y 8 para más información sobre
URLconfs).

Inicialización
--------------

Para activar los feeds de sindicación en tu sitio Django, agrega lo siguiente en
tu URLconf::

    (r'^feeds/(?P<url>.*)/$',
     'django.contrib.syndication.views.feed',
     {'feed_dict': feeds}
    ),

Esa línea le indica a Django que use el framework RSS para captar las URLs que
comienzan con ``"feeds/"``. (Puedes cambiar ``"feeds/"`` por algo que se adapte
a tus necesidades).

Esta línea de URLconf tiene un argumento extra: ``{'feed_dict': feeds}``. Usa
este argumento extra para pasar al framework de feeds de sindicación los feeds
que deben ser publicados en dicha URL.

Específicamente, ``feed_dict`` debe ser un diccionario que mapee el *slug*
(etiqueta corta de URL) de un feed a la clase Feed. Puedes definir el
``feed_dict`` en el mismo URLconf. Este es un ejemplo completo de URLconf::

    from django.conf.urls.defaults import *
    from myproject.feeds import LatestEntries, LatestEntriesByCategory

    feeds = {
        'latest': LatestEntries,
        'categories': LatestEntriesByCategory,
    }

    urlpatterns = patterns('',
        # ...
        (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
            {'feed_dict': feeds}),
        # ...
    )

El ejemplo anterior registra dos feeds:

    * El feed representado por ``LatestEntries`` residirá en ``feeds/latest/``.

    * El feed representado por ``LatestEntriesByCategory`` residirá en
      ``feeds/categories/``.

Una vez que este configurado, necesitas definir la propia clase ``Feed``.

Una clase ``Feed`` es una simple clase Python que representa un feed de sindicación.
Un feed puede ser simple (p. ej. "noticias del sitio", o una lista de las
últimas entradas del blog) o más complejo (p. ej. mostrar todas las entradas de
un blog en una categoría en particular, donde la categoría es variable).

La clase ``Feed`` debe ser una subclase de ``django.contrib.syndication.feeds.Feed``.
Esta puede residir en cualquier parte del árbol de código.

Un Feed simple
--------------

Este ejemplo simple, tomado de http://chicagocrime.org, describe un feed que muestra
los últimos cinco items agregados::

    from django.contrib.syndication.feeds import Feed
    from chicagocrime.models import NewsItem

    class LatestEntries(Feed):
        title = "Chicagocrime.org site news"
        link = "/sitenews/"
        description = "Updates on changes and additions to chicagocrime.org."

        def items(self):
            return NewsItem.objects.order_by('-pub_date')[:5]

Las cosas importantes a tener en cuenta son:

    * La clase es subclase de ``django.contrib.syndication.feeds.Feed``.

    * ``title``, ``link``, y ``description`` corresponden a los elementos RSS
      estándar ``<title>``, ``<link>``, y ``<description>`` respectivamente.

    * ``items()`` es simplemente un método que retorna una lista de objetos que
      deben incluirse en el feed como elementos ``<item>``.  Aunque este ejemplo
      retorna objetos ``NewsItem`` usando la API de base de datos de Django, no
      es un requerimiento que ``items()`` deba retornar instancias de modelos.

      Obtienes unos pocos bits de funcionalidad "gratis" usando los modelos de
      Django, pero ``items()`` puede retornar cualquier tipo de objeto que
      desees.

Hay solamente un paso más. En un feed RSS, cada ``<item>`` posee ``<title>``,
``<link>``, y ``<description>``. Necesitamos decirle al framework qué datos
debe poner en cada uno de los elementos.

    * Para especificar el contenido de ``<title>`` y ``<description>``, crea
      plantillas Django (ver `Capítulo 4`_) llamadas ``feeds/latest_title.html`` y
      ``feeds/latest_description.html``, donde ``latest`` es el ``slug``
      especificado en URLconf para el feed dado. Notar que la extensión ``.html``
      es requerida.

      El sistema RSS renderiza dicha plantilla por cada ítem, pasándole dos
      variables de contexto para plantillas:

          * ``obj``: El objeto actual (uno de los tantos que retorna en ``items()``).

          * ``site``: Un objeto ``django.models.core.sites.Site`` representa el
            sitio actual. Esto es útil para ``{{ site.domain }}`` o ``{{
            site.name }}``.

      Si no creas una plantilla para el título o la descripción, el framework
      utilizará la plantilla por omisión ``"{{ obj }}"`` -- exacto, la cadena
      normal de representación del objeto.

      También puedes cambiar los nombres de estas plantillas especificando
      ``title_template`` y ``description_template`` como atributos de tu clase
      ``Feed``.

    * Para especificar el contenido de ``<link>``, hay dos opciones. Por cada
      ítem en ``items()``, Django primero tratará de ejecutar el método
      ``get_absolute_url()`` en dicho objeto. Si dicho método no existe, entonces
      trata de llamar al método ``item_link()`` en la clase ``Feed``, pasándole
      un único parámetro, ``item``, que es el objeto en sí mismo.

      Ambos ``get_absolute_url()`` y ``item_link()`` deben retornar la URL del
      ítem como una cadena normal de Python.

    * Para el ejemplo anterior ``LatestEntries``, podemos usar plantillas de
      feed muy simples. ``latest_title.html`` contiene::

            {{ obj.title }}

      y ``latest_description.html`` contiene::

            {{ obj.description }}

      Es casi demasiado fácil...

Un Feed más complejo
--------------------

El framework también permite la creación de feeds más complejos mediante el uso
de parámetros.

Por ejemplo, http://chicagocrime.org ofrece un feed RSS de los crímenes recientes de
cada departamento de policía en Chicago. Sería tonto crear una clase ``Feed``
separada por cada departamento; esto puede violar el principio "No te repitas a
ti mismo" (DRY, por "Do not repeat yourself") y crearía acoplamiento entre los
datos y la lógica de programación.

En su lugar, el framework de feeds de sindicación te permite crear feeds genéricos
que retornan items basados en la información en la URL del feed.

En chicagocrime.org, los feed por departamento de policía son accesibles mediante
URLs como estas:

    * ``http://www.chicagocrime.org/rss/beats/0613/``: Retorna los crímenes más
      recientes para el departamento 0613

    * ``http://www.chicagocrime.org/rss/beats/1424/``: Retorna los crímenes más
      recientes para el departamento 1424

El slug aquí es ``"beats"``. El framework de sindicación ve las partes extra en
la URL tras el slug -- ``0613`` y ``1424`` -- y te provee un gancho (*hook*)
para que le indiques qué significa cada uno de esas partes y cómo influyen en
los items que serán publicados en el feed.

Un ejemplo aclarará esto. Este es el código para los feeds por departamento::

    from django.core.exceptions import ObjectDoesNotExist

    class BeatFeed(Feed):
        def get_object(self, bits):
            # In case of "/rss/beats/0613/foo/bar/baz/", or other such
            # clutter, check that bits has only one member.
            if len(bits) != 1:
                raise ObjectDoesNotExist
            return Beat.objects.get(beat__exact=bits[0])

        def title(self, obj):
            return "Chicagocrime.org: Crimes for beat %s" % obj.beat

        def link(self, obj):
            return obj.get_absolute_url()

        def description(self, obj):
            return "Crimes recently reported in police beat %s" % obj.beat

        def items(self, obj):
            crimes =  Crime.objects.filter(beat__id__exact=obj.id)
            return crimes.order_by('-crime_date')[:30]

Aquí tenemos el algoritmo básico del framework RSS, asumiendo esa clase y un
requerimiento a la URL ``/rss/beats/0613/``:

    #. El framework toma la URL ``/rss/beats/0613/`` y nota que la URL contiene
       una parte extra tras el slug. Separa esa cadena remanente por el carácter
       ``"/"`` y llama al método ``get_object()`` de la clase ``Feed`` pasándole
       los trozos (*bits*) resultantes.

       En este caso, los trozos "son" ``['0613']``. Para un requerimiento a
       ``/rss/beats/0613/foo/bar/``, serán ``['0613', 'foo', 'bar']``.

    #. ``get_object()`` es el responsable de obtener el departamento requerido,
       a partir del ``bits`` dado.

       En este caso, usa la API de base de datos de Django para obtener el
       departamento. Notar que ``get_object()`` debe capturar la excepción
       ``django.core.exceptions.ObjectDoesNotExist`` si recibe parámetros
       inválidos. No hay ``try``/``except`` abarcando la llamada a
       ``Beat.objects.get()`` porque no es necesario. Esa función, ante una falla
       lanza la excepción ``Beat.DoesNotExist``, y ``Beat.DoesNotExist`` es una
       subclase de ``ObjectDoesNotExist``. Lanzar la excepción ``ObjectDoesNotExist``
       en ``get_object()`` le dice a Django que produzca un error 404 para
       el requerimiento en curso.

    #. Para generar los campos ``<title>``, ``<link>``, y ``<description>`` del
       feed, Django usa los métodos ``title()``, ``link()``, y ``description()``.
       En el ejemplo anterior, se utilizaron atributos simples de clase string,
       pero este ejemplo muestra que estos pueden ser strings o métodos.
       Por cada ``title``, ``link``, y ``description``, Django sigue este
       algoritmo:

          #. Trata de llamar al método, pasando el argumento ``obj``, donde
             ``obj`` es el objeto retornado por ``get_object()``.

          #. Si eso falla, trata de llamar al método sin argumentos.

          #. Si eso falla, usa los atributos de clase.

    #. Finalmente, nota que ``items()`` en el ejemplo también toma como argumento
       a ``obj``. El algoritmo para ``items`` es el mismo que se describe en el
       paso anterior -- primero prueba ``items(obj)``, después ``items()``, y
       finalmente un atributo de clase ``items`` (que debe ser una lista).

La documentación completa de todos los métodos y atributos de las clases ``Feed``
siempre esta disponible en la documentación oficial de Django
(http://www.djangoproject.com/documentation/0.96/syndication_feeds/).

Especificar el tipo de Feed
---------------------------

Por omisión, el framework de feeds de sindicación produce RSS 2.0. Para cambiar
eso, agrega un atributo ``feed_type`` a tu clase ``Feed``::

    from django.utils.feedgenerator import Atom1Feed

    class MyFeed(Feed):
        feed_type = Atom1Feed

Nota que asignas como valor de ``feed_type`` una clase, no una instancia.
Los tipos de feeds disponibles actualmente se muestran en la Tabla 11-1.

.. tabla:: Tabla 11-1. Tipos de Feeds

===================================================  ======================
    Clase Feed                                           Formato
===================================================  ======================
``django.utils.feedgenerator.Rss201rev2Feed``        RSS 2.01 (por defecto)

  ``django.utils.feedgenerator.RssUserland091Feed``    RSS 0.91

    ``django.utils.feedgenerator.Atom1Feed``             Atom 1.0
===================================================  ======================

Enclosures
----------

Para especificar *enclosures* (p. ej. recursos multimedia asociados al ítem del
feed tales como feeds de podcasts MP3), usa los ganchos ``item_enclosure_url``,
``item_enclosure_length``, y ``item_enclosure_mime_type``, por ejemplo::

    from myproject.models import Song

    class MyFeedWithEnclosures(Feed):
        title = "Example feed with enclosures"
        link = "/feeds/example-with-enclosures/"

        def items(self):
            return Song.objects.all()[:30]

        def item_enclosure_url(self, item):
            return item.song_url

        def item_enclosure_length(self, item):
            return item.song_length

        item_enclosure_mime_type = "audio/mpeg"

Esto asume, por supuesto, que has creado un objeto ``Song`` con los campos
``song_url`` y ``song_length`` (p. ej. el tamaño en bytes).

Idioma
------

Los Feeds creados por el framework de sindicación incluyen automáticamente la
etiqueta ``<language>`` (RSS 2.0) o el atributo ``xml:lang`` apropiados (Atom).
Esto viene directamente de tu variable de configuración ``LANGUAGE_CODE``.

URLs
----

El método/atributo ``link`` puede retornar tanto una URL absoluta (p. ej.
``"/blog/"``) como una URL con el nombre completo de dominio y protocolo (p. ej.
``"http://www.example.com/blog/"``). Si ``link`` no retorna el dominio,
el framework de sindicación insertará el dominio del sitio actual, acorde a
la variable de configuración ``SITE_ID``.

Los feeds Atom requieren un ``<link rel="self">`` que define la ubicación actual
del feed. El framework de sindicación completa esto automáticamente, usando el
dominio del sitio actual acorde a la variable de configuración ``SITE_ID``.

Publicar feeds Atom y RSS conjuntamente
---------------------------------------

Algunos desarrolladores prefieren ofrecer ambas versiones Atom *y*
RSS de sus feeds. Esto es simple de hacer con Django: solamente crea una subclase de tu clase
``feed`` y asigna a ``feed_type`` un valor diferente. Luego actualiza tu URLconf
para agregar una versión extra. Aquí un ejemplo completo::

    from django.contrib.syndication.feeds import Feed
    from chicagocrime.models import NewsItem
    from django.utils.feedgenerator import Atom1Feed

    class RssSiteNewsFeed(Feed):
        title = "Chicagocrime.org site news"
        link = "/sitenews/"
        description = "Updates on changes and additions to chicagocrime.org."

        def items(self):
            return NewsItem.objects.order_by('-pub_date')[:5]

    class AtomSiteNewsFeed(RssSiteNewsFeed):
        feed_type = Atom1Feed

Y este es el URLconf asociado::

    from django.conf.urls.defaults import *
    from myproject.feeds import RssSiteNewsFeed, AtomSiteNewsFeed

    feeds = {
        'rss': RssSiteNewsFeed,
        'atom': AtomSiteNewsFeed,
    }

    urlpatterns = patterns('',
        # ...
        (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
            {'feed_dict': feeds}),
        # ...
    )

El framework Sitemap
====================

Un *sitemap* es un fichero XML en tu sitio web que le indica a los indexadores
de los motores de búsqueda cuan frecuentemente cambian tus páginas así como la
"importancia" relativa de ciertas páginas en relación con otras (siempre
hablando de páginas de tu sitio). Esta información ayuda a los motores de
búsqueda a indexar tu sitio.

Por ejemplo, esta es una parte del sitemap del sitio web de Django
(http://www.djangoproject.com/sitemap.xml):

.. code-block:: html 

    <?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url>
        <loc>http://www.djangoproject.com/documentation/</loc>
        <changefreq>weekly</changefreq>
        <priority>0.5</priority>
      </url>
      <url>
        <loc>http://www.djangoproject.com/documentation/0_90/</loc>
        <changefreq>never</changefreq>
        <priority>0.1</priority>
      </url>
      ...
    </urlset>

Para más información sobre sitemaps, vea http://www.sitemaps.org/.

El framework sitemap de Django automatiza la creación de este fichero XML si
lo indicas expresamente en el código Python. Para crear un sitemap, debes
simplemente escribir una clase ``Sitemap`` y hacer referencia a la misma en tu
URLconf.

Instalación
-----------

Para instalar la aplicación sitemap, sigue los siguientes pasos:

    #. Agrega ``'django.contrib.sitemaps'`` a tu variable de configuración
       ``INSTALLED_APPS``.

    #. Asegúrate de que
       ``'django.template.loaders.app_directories.load_template_source'`` está en
       tu variable de configuración ``TEMPLATE_LOADERS``. Por omisión se encuentra
       activado, por lo que los cambios son necesarios solamente si modificaste
       dicha variable de configuración.

    #. Asegúrate de que tienes instalado el framework sites (ver `Capítulo 14`_).

.. nota::

    La aplicación sitemap no instala tablas en la base de datos. La única razón
    de que esté en ``INSTALLED_APPS`` es que el cargador de plantillas
    ``load_template_source`` pueda encontrar las plantillas incluídas.

Inicialización
--------------

Para activar la generación del sitemap en tu sitio Django, agrega la siguiente
línea a tu URLconf::

    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})

Esta línea le dice a Django que construya un sitemap cuando un cliente accede
a ``/sitemap.xml``.

El nombre del fichero sitemap no es importante, pero la ubicación sí lo es. Los
motores de búsqueda solamente indexan los enlaces en tu sitemap para el nivel de
URL actual y anterior. Por ejemplo, si ``sitemap.xml`` reside en tu directorio
principal, el mismo puede hacer referencia a cualquier URL en tu sitio. Pero si
tu sitemap reside en ``/content/sitemap.xml``, solamente podrá hacer referencia
a URLs que comiencen con ``/content/``.

La vista sitemap toma un argumento extra: ``{'sitemaps': sitemaps}``.
``sitemaps`` debe ser un diccionario que mapee una etiqueta corta de sección (p.
ej. ``blog`` o ``news``) a tu clase ``Sitemap`` (p.e., ``BlogSitemap`` o
``NewsSitemap``).  También mapea hacia una *instancia* de una clase ``Sitemap``
(p. ej. ``BlogSitemap(some_var)``).

Clases Sitemap
--------------

Una clase ``Sitemap`` es simplemente una clase Python que representa una
"sección" de entradas en tu sitemap. Por ejemplo, una clase ``Sitemap`` puede
representar todas las entradas de tu weblog, y otra puede representar todos los
eventos de tu calendario.

En el caso más simple, todas estas secciones se unen en un único ``sitemap.xml``,
pero también es posible usar el framework para generar un índice sitemap que
haga a referencia ficheros sitemap individuales, uno por sección (describiéndolo
sintéticamente).

Las clases ``Sitemap`` debe ser una subclase de ``django.contrib.sitemaps.Sitemap``.
Estas pueden residir en cualquier parte del árbol de código.

Por ejemplo, asumamos que posees un sistema de blog, con un modelo ``Entry``, y
quieres que tu sitemap incluya todos los enlaces a las entradas individuales
de tu Blog. Tu clase ``Sitemap`` debería verse así::

    from django.contrib.sitemaps import Sitemap
    from mysite.blog.models import Entry

    class BlogSitemap(Sitemap):
        changefreq = "never"
        priority = 0.5

        def items(self):
            return Entry.objects.filter(is_draft=False)

        def lastmod(self, obj):
            return obj.pub_date

Declarar un ``Sitemap`` debería verse muy similar a declarar un ``Feed``; esto
es justamente un objetivo del diseño.

En manera similar a las clases ``Feed``, los miembros de ``Sitemap`` pueden ser
métodos o atributos.  Ver los pasos en la sección "`Un feed más complejo`_" para
más información sobre cómo funciona esto.

Una clase ``Sitemap`` puede definir los siguientes métodos/atributos:

    * ``items`` (**requerido**): Provee una lista de objetos. Al framework no le
      importa que *tipo* de objeto es; todo lo que importa es que los objetos
      sean pasados a los métodos ``location()``, ``lastmod()``,
      ``changefreq()``, y ``priority()``.

    * ``location`` (opcional): Provee la URL absoluta para el objeto dado. Aquí
      "URL absoluta" significa una URL que no incluye el protocolo o el dominio.
      Estos son algunos ejemplos:

            * Bien: ``'/foo/bar/'``
            * Mal: ``'example.com/foo/bar/'``
            * Mal: ``'http://example.com/foo/bar/'``

      Si ``location`` no es provisto, el framework llamará al método
      ``get_absolute_url()`` en cada uno de los objetos retornados por ``items()``.

    * ``lastmod`` (opcional): La fecha de "última modificación" del objeto, como
      un objeto ``datetime`` de Python.

    * ``changefreq`` (opcional): Cuán a menudo el objeto cambia. Los valores
      posibles (según indican las especificaciones de Sitemaps) son:

            * ``'always'``
            * ``'hourly'``
            * ``'daily'``
            * ``'weekly'``
            * ``'monthly'``
            * ``'yearly'``
            * ``'never'``

    * ``priority`` (opcional): Prioridad sugerida de indexado entre ``0.0``
      y ``1.0``. La prioridad por omisión de una página es ``0.5``; ver la
      documentación de http://sitemaps.org para más información de cómo
      funciona ``priority``.

Accesos directos
----------------

El framework sitemap provee un conjunto de clases para los casos más comunes.
Describiremos estos casos en las secciones a continuación.

FlatPageSitemap
~~~~~~~~~~~~~~~

La clase ``django.contrib.sitemaps.FlatPageSitemap`` apunta a todas las páginas
planas definidas para el sitio actual y crea una entrada en el sitemap. Estas
entradas incluyen solamente el atributo ``location`` -- no ``lastmod``,
``changefreq``, o ``priority``.

Para más información sobre Páginas Planas ver el :doc:`Capítulo 14<chapter14>`_.

Sitemap Genérico
~~~~~~~~~~~~~~~~

La clase ``GenericSitemap`` trabaja con cualquier vista genérica (ver `Capítulo 9`_)
que pudieras poseer con anterioridad.

Para usarla, crea una instancia, pasándola en el mismo ``info_dict`` que se pasa
a la vista genérica. El único requerimiento es que el diccionario tenga una
entrada ``queryset``. También debe poseer una entrada ``date_field`` que
especifica un campo fecha para los objetos obtenidos del ``queryset``. Esto será
usado por el atributo ``lastmod`` en el sitemap generado. También puedes pasar
los argumentos palabra clave (*keyword*) ``priority`` y ``changefreq`` al
constructor ``GenericSitemap`` para especificar dichos atributos para todas las
URLs.

Este es un ejemplo de URLconf usando tanto, ``FlatPageSitemap`` como
``GenericSiteMap`` (con el anterior objeto hipotético ``Entry``)::

    from django.conf.urls.defaults import *
    from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
    from mysite.blog.models import Entry

    info_dict = {
        'queryset': Entry.objects.all(),
        'date_field': 'pub_date',
    }

    sitemaps = {
        'flatpages': FlatPageSitemap,
        'blog': GenericSitemap(info_dict, priority=0.6),
    }

    urlpatterns = patterns('',
        # some generic view using info_dict
        # ...

        # the sitemap
        (r'^sitemap.xml$',
         'django.contrib.sitemaps.views.sitemap',
         {'sitemaps': sitemaps})
    )

Crear un índice Sitemap
-----------------------

El framework sitemap también tiene la habilidad de crear índices sitemap que
hagan referencia a ficheros sitemap individuales, uno por cada sección definida
en tu diccionario ``sitemaps``. Las única diferencias de uso son:

    * Usas dos vistas en tu URLconf:
      ``django.contrib.sitemaps.views.index`` y
      ``django.contrib.sitemaps.views.sitemap``.

    * La vista ``django.contrib.sitemaps.views.sitemap`` debe tomar un parámetro
      que corresponde a una palabra clave, llamado ``section``.

Así deberían verse las líneas relevantes en tu URLconf para el ejemplo anterior::

    (r'^sitemap.xml$',
     'django.contrib.sitemaps.views.index',
     {'sitemaps': sitemaps}),

    (r'^sitemap-(?P<section>.+).xml$',
     'django.contrib.sitemaps.views.sitemap',
     {'sitemaps': sitemaps})

Esto genera automáticamente un fichero ``sitemap.xml`` que hace referencia a
ambos ficheros ``sitemap-flatpages.xml`` y ``sitemap-blog.xml``. La clase
``Sitemap`` y el diccionario ``sitemaps`` no cambian en absoluto.

Hacer ping a Google
-------------------

Puedes desear hacer un "ping" a Google cuando tu sitemap cambia, para hacerle
saber que debe reindexar tu sitio. El framework provee una función para hacer
justamente eso: ``django.contrib.sitemaps.ping_google()``.

.. admonition::

    Hasta el momento en que este libro se escribió, únicamente Google responde a
    los pings de sitemap. Pero es muy probable que pronto Yahoo y/o MSN también
    admitan estos pings.

    Cuando eso suceda, cambiaremos el nombre de ``ping_google()`` a algo como
    ``ping_search_engines()``, así que asegúrate de verificar la ultima
    documentación de sitemap en
    http://www.djangoproject.com/documentation/.

``ping_google()`` toma un argumento opcional, ``sitemap_url``, que debe ser la
URL absoluta de tu sitemap (por ej., ``'/sitemap.xml'``). Si este argumento no es
provisto, ``ping_google()`` tratará de generar un sitemap realizando una
búsqueda reversa en tu URLconf.

``ping_google()`` lanza la excepción
``django.contrib.sitemaps.SitemapNotFound`` si no puede determinar la URL de tu
sitemap.

Una forma útil de llamar a ``ping_google()`` es desde el método ``save()``::

    from django.contrib.sitemaps import ping_google

    class Entry(models.Model):
        # ...
        def save(self):
            super(Entry, self).save()
            try:
                ping_google()
            except Exception:
                # Bare 'except' because we could get a variety
                # of HTTP-related exceptions.
                pass

Una solución más eficiente, sin embargo, sería llamar a ``ping_google()`` desde
un script ``cron`` o un manejador de tareas. La función hace un pedido HTTP a
los servidores de Google, por lo que no querrás introducir esa demora asociada a
la actividad de red cada vez que se llame al método ``save()``.

¿Qué sigue?
===========

A continuación, seguiremos indagando más profundamente en las herramientas
internas que Django nos ofrece. El :doc:`Capítulo 12<chapter12>` examina todas las herramientas
que necesitas para proveer sitios personalizados: sesiones, usuarios, y
autenticación.

¡Adelante!


