============================================
Capítulo 13: Generación de contenido no HTML
============================================

Usualmente cuando hablamos sobre desarrollo de sitios Web, hablamos de producir
HTML. Por supuesto, hay mucho más que contenido HTML en la Web; la usamos para
distribuir datos en todo tipo de formatos: RSS, PDFs, imágenes, y así
sucesivamente.

Hasta ahora nos hemos concentrado en el caso común de la producción de HTML,
pero en ese capítulo tomaremos un desvío y veremos **cómo usar Django para
producir otro tipo de contenido**.

Django posee varias herramientas útiles que puedes usar para producir algunos
tipos comunes de contenido no HTML:

* *Feeds* de sindicación RSS/Atom

* Mapas de sitios haciendo uso de *Sitemaps* (un formato XML originalmente
  desarrollado por Google que provee de ayuda a motores de búsqueda)

Examinaremos cada una de esas herramientas un poco más adelante, pero antes
cubriremos los principios básicos.

Lo básico: Vistas y tipos MIME
==============================

¿Recuerdas esto del :doc:`capítulo 3<chapter03>`?

Una función vista, o una *vista* por abreviar, es simplemente una función en
Python que recibe una petición Web y retorna una respuesta Web. Esta
respuesta puede ser el contenido HTML de una página Web, una redirección, un
error 404, un documento XML, una imagen... en realidad, cualquier cosa.

Más formalmente, una función *vista* Django *debe*

* Aceptar una instancia ``HttpRequest`` como primer argumento.

* Retornar una instancia ``HttpRequestsponse`` como respuesta.

La clave para retornar contenido no HTML desde una vista reside en la
clase ``HttpResponse``, específicamente en el argumento ``mimetype`` del
constructor. Cambiando el tipo MIME, podemos indicarle al navegador que hemos
retornado una respuesta en un formato diferente.

Por ejemplo, veamos una vista que devuelve una imagen PNG. Para mantener las
cosas sencillas, simplemente leeremos un fichero desde el disco::

    from django.http import HttpResponse

    def mi_imagen(request):
        datos_imagen = open("/ruta/a/mi/imagen.png", "rb").read()
        return HttpResponse(datos_imagen, mimetype="imagen/png")

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

    Año, Pasajeros problemáticos
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

.. admonition:: Nota:

    El listado anterior,  contiene números reales; cortesía de la
    Administración Federal de Aviación (FAA) de E.E.U.U. Tomados de:
    http://www.faa.gov/data_statistics/passengers_cargo/unruly_passengers/.

Aunque CSV parezca simple, no es un formato que ha sido definido formalmente.
Diferentes programas producen y consumen diferentes variantes de CSV,
haciendo un poco complicado usarlo.  Afortunadamente, Python incluye una
biblioteca estándar para CSV,  llamada ``csv``, que es bastante robusta.

Debido a que el módulo ``csv`` opera sobre objetos de forma similar a como lo
hace con ficheros, es muy fácil usar un ``HttpResponse`` en lugar de un fichero::

    import csv
    from django.http import HttpResponse

    # Numero de pasajeros problemáticos en el periodo 1995-2005. En una
    # aplicacion real estos datos probablemente vendrían de una base de datos
    # o de algún otro tipo de almacenamiento externo.
    PASAJEROS_PROBLEMATICOS = [146,184,235,200,226,251,299,273,281,304,203]

    def pasajeros_problematicos_csv(request):
        # Crea un objeto HttpResponse con las cabeceras del CVS correctas.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=problematicos.csv'

        # Crea el escritor CSV usando un HttpResponse como "archivo."
        writer = csv.writer(response)
        writer.writerow(['Año', 'Pasajeros problemáticos en aerolínea'])
        for (year, num) in zip(range(1995, 2006), PASAJEROS_PROBLEMATICOS):
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
  un "objeto de tipo fichero", y los objetos de tipo ``HttpResponse`` se ajustan
  a ello.

* Por cada fila en el fichero CSV, invocamos a ``writer.writerow``,
  pasándole un objeto iterable como una lista o una tupla.

* El módulo CSV se encarga de poner comillas por ti, así que no tendrás que
  preocuparte por *escapar* caracteres en las cadenas que tengan comillas o
  comas en su interior. Limítate a pasar la información a ``writerow()``,
  que hará lo correcto.

Este es el patrón general que usarás siempre que necesites retornar contenido no
HTML: crear un objeto ``HttpResponse`` de respuesta (con un tipo MIME especial),
pasárselo a algo que espera un fichero, y luego devolver la respuesta.

Veamos unos cuantos ejemplos más.

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

.. admonition:: Nota:

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

A continuación un ejemplo "Hola Mundo":

.. code-block:: python

  from reportlab.pdfgen import canvas
  from django.http import HttpResponse

  def hola_pdf(request):
      # Crea un objeto HttpResponse  con las cabeceras PDF correctas.
      response = HttpResponse(content_type='application/pdf')
      response['Content-Disposition'] = 'attachment; filename=hello.pdf'

      # Crea un objeto PDF, usando el objeto como un "archivo".
      p = canvas.Canvas(response)

      # Dibuja cosas en el PDF. Aqui se genera el PDF.
      # Consulta la documentación de ReportLab para una lista completa de funcionalidades.
      p.drawString(50, 800, "Hola mundo.")

      # Cierra el objeto PDF limpiamente y termina.
      p.showPage()
      p.save()
      return response

El codigo y los comentarios deberían explicarse por sí mismos, pero son necesarias alguna
notas adicionales:

* Usamos el tipo MIME ``application/pdf``. Esto le indica al navegador que
  el documento es un fichero PDF y no un fichero HTML. Si no incluyes esta
  información, los navegadores web probablemente interpretarán la respuesta
  como HTML, lo que resultará en jeroglíficos en la ventana del navegador.

* La respuesta obtiene una cabecera ``Content-Disposition`` adicional, la
  cual contiene el nombre de el archivo PDF. Este nombre es arbitrario: llámalo
  como quieras. Solo será usado para abrir el cuadro de dialogo en el navegador
  "Guardar como..."

* En el ejemplo le agregamos ``attachment``  a la  respuesta de la cabecera
  ``Content Disposition`` al nombre del archivo. Esto fuerza a los navegadores Web
  a presentar una ventana de diálogo/confirmación para manipular el documento por
  defecto usando un programa externo, sin embargo  si dejamos en blanco ``attachment``
  el navegador manipulará el PDF usando cualquier plugin que haya sido configurada
  para manejar este tipo de archivos dentro del navegador, el codigo es el siguiente::

    response['Content-Disposition'] = 'filename="archivo.pdf"'

* Interactuar con la API ReportLab es sencillo: sólo pasa ``response`` como
  el primer argumento a ``canvas.Canvas``. La clase ``Canvas`` espera un objeto
  tipo archivo, por lo que los objetos ``HttpResponse`` se ajustarán a la norma.

* Todos los métodos de generación de PDF subsecuentes son llamados
  pasándoles el objeto PDF (en este caso ``p``), no ``response``.

* Finalmente, es importante llamar a los métodos ``showPage()`` y ``save()``
  del objeto PDF (de otra manera obtendrás un fichero PDF corrupto).

PDFs complejos
--------------

Si estás creando un documento PDF complejo considera usar la biblioteca
``io`` como un lugar de almacenamiento temporal para tu fichero PDF.
Esta biblioteca provee una interfaz para tratar con archivos tipo objetos
muy eficiente.

En este ejemplo, obtenemos datos directamente de la base de datos y los
usamos para crear un PDF usando el modulo ``io`` ::

  from io import BytesIO
  from reportlab.pdfgen import canvas
  from django.http import HttpResponse

  from biblioteca.models import Libro

  def crear_pdf(request, pk):
      # Obtenemos un queryset, para un determinado libro usando pk.
      try:
          libro = Libro.objects.get(id=pk)
      except ValueError:
          raise Http404()
      # Creamos un objeto HttpResponse con las cabeceras del PDF correctas.
      response = HttpResponse(content_type='application/pdf')
      # Nos aseguramos que el navegador lo abra directamente.
      response['Content-Disposition'] = 'filename="archivo.pdf"'
      buffer = BytesIO()

      # Creamos el objeto PDF, usando el objeto BytesIO como si fuera un "archivo".
      p = canvas.Canvas(buffer)

      # Dibujamos cosas en el PDF. Aqui se genera el PDF.
      # Consulta la documentación de ReportLab para una lista completa de funcionalidades.
      p.drawString(100, 800, "Titulo: " + str(libro.titulo))
      p.drawString(100, 780, "Editor: " + str(libro.editor))
      p.drawString(100, 760, "Portada " )
      p.drawImage(str(libro.portada.url), 100, 150, width=400, height=600)

      # Cerramos limpiamente el objeto PDF.
      p.showPage()
      p.save()

      # Traemos  el valor de el bufer BytesIO y escribimos la respuesta.
      pdf = buffer.getvalue()
      buffer.close()
      response.write(pdf)
      return response

Ahora solo enlazamos la vista a la ULRconf asi::

    from django.conf.urls import url
    from biblioteca import views

    urlpatterns =[
    #...
    url(r'^exportar/(?P<pk>[0-9]+)/$', views.crear_pdf, name='exportar-pdf'),
    ]

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
siguiente nivel de abstracción. Django incluye algunas herramientas agradables e
ingeniosas para generar cierto tipo de contenido no-HTML.

El Framework de Feeds de Sindicación
====================================

Django incluye un framework para la generación y sindicación de *feeds* de alto
nivel que permite crear feeds RSS_ y Atom_ de manera sencilla.

.. _RSS: http://www.whatisrss.com/
.. _Atom: http://tools.ietf.org/html/rfc4287


.. admonition:: ¿Qué es RSS? ¿Qué es Atom?

    RSS y Atom son formatos basados en XML que se puede utilizar para actualizar
    automáticamente los "feeds" con el contenido de tu sitio. Lee más sobre RSS
    en http://www.whatisrss.com/, y obtén información sobre Atom en
    http://www.atomenabled.org/.

Para crear cualquier feed de sindicación, todo lo que necesitas hacer es escribir una
pequeña clase Python. Puedes crear tantos feeds como desees.

El framework de generación de feeds de alto nivel es una vista enganchada a
``/feeds/`` por convención. Django usa el final de la URL (todo lo que este
después de ``/feeds/``) para determinar qué feed retornar.

Para crear un feed, necesitas escribir una clase ``Feed`` y hacer referencia a
la misma en tu URLconf (Consulta los capítulos 3 y 8 para más información sobre
URLconfs).

Inicialización
--------------

Para activar los feeds de sindicación en tu sitio Django, agrega lo siguiente en
tu URLconf::

    from biblioteca.feeds import UltimosLibros

    urlpatterns =[
        url(r'^feeds/$', UltimosLibros()),
    ]

Esa línea le indica a Django que use el framework RSS para captar las URLs que
comienzan con ``"feeds/"``. (Puedes cambiar ``"feeds/"`` por algo que se adapte
mejor a tus necesidades).

Deves tener en cuenta que:

* El feed es representado por la clase ``UltimosLibros`` el cual por convención  y claridad residirá en un nuevo archivo llamado ``feeds.py``, en el mismo nivel
  que ``models.py``, aunque puede residir en cualquier parte del árbol de código.

* La clase ``Feed`` debe ser una subclase de ``django.contrib.syndication.feeds.Feed``.

* Una vez que este configurada la URL, necesitas definir la propia clase ``Feed``.
  Puedes pensar en una clase Feed como un tipo de clase genérica.

Una clase ``Feed`` es una simple clase Python que representa un feed de sindicación.
Un feed puede ser simple (p. ej. "noticias del sitio", o una lista de las
últimas entradas del blog) o más complejo (p. ej. mostrar todas las entradas de
un blog en una categoría en particular, donde la categoría es variable).

Un Feed simple
--------------

Siguiendo con el modelo creado en los capítulos anteriores, veamos ahora como
crear un simple feed, que muestre los últimos cinco libros  agregados a nuestra
aplicacion biblioteca.

Empecemos por escribir la clase::

    class UltimosLibrosFeed(Feed):
        # FEED TYPE -- Opcional. Este debe ser una subclase de la clase
        # django.utils.feedgenerator.SyndicationFeed. Este designa
        # el tipo de feed a usar: RSS 2.0, Atom 1.0, etc. Si no se
        # especifica el tipo de feed (feed_type), se asumirá que el tipo
        # es RSS 2.0. Este debe aparecer en una clase, no en una instancia de
        # una clase.

        feed_type = feedgenerator.Rss201rev2Feed

        title = "Feed libros publicados"
        link = "/ultimos-libros/"
        description = "Ultimos libros publicados en la biblioteca digital."

        def items(self):
            """
            Retorna una lista de items para publicar en este feed.
            """
            return Libro.objects.order_by('-fecha_publicacion')[:5]

        def item_title(self, item):
            """
            Toma un item, retornado por el método items(), y devuelve los item's
            del titulo como cadena normales Python.
            """
            return item.titulo

        def item_description(self, item):
            """
            Toma un item, retornado por el método items(), y devuelve los item's
            con una descripción en forma de cadena normal de Python.
            """
            return item.descripcion

        def item_link(self, item):
            """
            Toma un item, retornado por el método items(), y devuelve la URL de
            los item's. Es usado solo si el modelo no tiene un método
            get_absolute_url() definido.
            """
            return reverse('detalles-libro', args=[item.pk])

        def item_enclosure_url(self, item):
            """
            Toma un item, retornado por el método items(), y devuelve los item's
            adjuntos en la URL.
            """
            return item.portada.url

        def item_enclosure_length(self, item):
            """
            Toma un item, retornado por el método items(), y devuelve el largo
            de los item's  adjuntos.
            """
            return item.portada.size

        item_enclosure_mime_type = "image/jpeg" # Definimos manualmente el tipo MIME.

Para conectar la URL con el feed, usamos una instancia de un objeto Feed en la
URLconf. Por ejemplo::

  from django.conf.urls import url
  from biblioteca.feeds import UltimosLibrosFeed

  urlpatterns = [
      # ...
      url(r'^feeds/$', UltimosLibrosFeed()),
      # ...
  ]

Las cosas importantes a tener en cuenta son:

* La clase ``Feed`` es una subclase de ``django.contrib.syndication.views.Feed``.

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
``<link>``, y ``<description>``. Por lo que es necesario decirle al framework
qué datos debe poner en cada uno de los elementos.

* Para especificar el contenido de ``<title>`` y ``<description>``,  Django
  trata de llamar a los metodos ``item_title()`` e ``item_description()`` en la
  clase Feed. Estos son pasados como simples parámetros item, el cual es el
  objeto en sí mismo. También estos metodos son opcionales; por defecto la
  representación Unicode del objeto es usado en ambos.

* Para especificar contenido con algún formato en especifico para ``<title>`` y
  ``<description>``, crea  plantillas Django (ver :doc:`capítulo 4<chapter04>`)
  Puedes especificar la ruta  con los atributos ``title_template``  y
  ``description_template`` en la clase Feed. El sistema RSS rende riza dicha
  plantilla por cada ítem, pasándole dos  variables de contexto para plantillas:

  * ``{{ obj }}``: El objeto actual (uno de los tantos que retorna en ``items()``).

  * ``{{ site }}``: Un objeto ``django.models.core.sites.Site`` representa el
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

  Ambos metodos: ``get_absolute_url()`` y ``item_link()`` deben retornar la
  URL del ítem como una cadena normal de Python.

También es posible pasarle información adicional a ``title`` y a ``description``
en las plantillas, si es que necesitas suministrar más información a las dos
variables anteriores. Para hacerlo solo necesitas implementar el  método
``get_context_data`` en la subclase Feed. Por ejemplo:

.. code-block:: python

  from django.contrib.syndication.views import Feed
  from biblioteca.models import Libro

  class UltimosLibrosFeed(Feed):

      # NOMBRES PLANTILLAS -- Opcionales. Estas deben de ser cadenas de texto
      # que representan el nombre de las plantillas que Django usara para
      # renderizar el titulo y la descripción del los items del Feed.
      # Ambos son opcionales. Si no se especifica una plantilla, se usara
      # el método item_title() o item_description() en su lugar.

      title = "Mis Libros" # Hard-coded titulo.
      description_template = "feeds/libros.html" # La plantilla

      def items(self):
          """
          Retorna una lista de items para publicar en este feed.
          """
          return Libro.objects.order_by('-fecha_publicacion')[:5]

      def get_context_data(self, **kwargs):
          """
          Toma la petición actual y los argumentos de la URL, y
          devuelve un objeto que representa este feed. Levanta una
          excepción del tipo django.core.exceptions.ObjectDoesNotExist
          si existe algún error.
          """
          context = super(UltimosLibros, self).get_context_data(**kwargs)
          context['foo'] = 'bar'
          return context

Y en la plantilla:

.. code-block:: python

    Algo como {{ foo }}: {{ obj.description }}

Este método será llamado una vez por cada item en la lista de libros devuelta
por items() con los siguientes argumentos clave:

``item`` El actual item. Por razones de compatibilidad, el nombre de esta
variable de contexto es ``{{ obj }}.``

``obj`` El objeto devuelto por el método ``get_object()``. Por defecto este no
es expuesto en las plantillas para evitar confusión con ``get_object()``. (ver
arriba), pero se puede usar en la implementacion de el método

``get_context_data()``.

``site``  El sitio actual, descrito anteriormente.

``request`` La petición actual o ``request``.

Como puedes ver el comportamiento de  ``get_context_data()`` es muy similar al
de las vistas genéricas - solo llamas a la super clase() para extraer datos del
contexto de la clase padre, agregas datos y devuelves el diccionario modificado.

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
que retornan items basados en la información de la URL del feed.

En chicagocrime.org, los feed por departamento de policía son accesibles mediante
URLs como estas:

* ``/beats/613/rss/`` : Retorna los crímenes más recientes para el departamento 0613
* ``/beats/1424/rss/``: Retorna los crímenes más  recientes para el departamento 1424

Estas funcionan con una URLconf parecida a esta::

    url(r'^beats/(?P<beat_id>[0-9]+)/rss/$', BeatFeed()),

El slug aquí es ``"beats"``. El framework de sindicación ve las partes extra en
la URL tras el slug -- ``0613`` y ``1424`` -- y te provee un gancho (*hook*)
para que le indiques qué significa cada uno de esas partes y cómo influyen en
los items que serán publicados en el feed.

Tal como en una vista, los argumentos en la URL son pasados mediante el método
``get_object()``  junto con el objeto de la petición.

Un ejemplo aclarará esto. Este es el código para los feeds por departamento::

  from django.contrib.syndication.views import FeedDoesNotExist
  from django.shortcuts import get_object_or_404

  class BeatFeed(Feed):
      description_template = 'feeds/beat_description.html'

      def get_object(self, request, beat_id):
          return get_object_or_404(Beat, pk=beat_id)

      def title(self, obj):
          return "Police beat central: Crimes for beat %s" % obj.beat

      def link(self, obj):
          return obj.get_absolute_url()

      def description(self, obj):
          return "Crimes recently reported in police beat %s" % obj.beat

      def items(self, obj):
          return Crime.objects.filter(beat=obj).order_by('-crime_date')[:30]

Para generar los feed’s <title>, <link> y <description>, Django usa los metodos
title(), link() y description(). En el ejemplo anterior, estos eran atributos
simples de una clase, pero este ejemplo ilustra que estos pueden ser tanto
métodos o cadenas.  Por cada ``title``, ``link`` y ``description``, Django sigue
el siguiente algoritmo.

#. Primero trata de llamar al método, pasando el argumento ``obj``, donde
   ``obj`` es el objeto retornado por ``get_object()``.

#. Si eso falla, trata de llamar al método sin argumentos.

#. Si eso falla, usa los atributos de clase.

Nota que ``items()`` en el ejemplo también toma como argumento a ``obj``. El
algoritmo para ``items`` es el mismo que se describe en el paso anterior
-- primero prueba ``items(obj)``, después ``items()``, y finalmente un atributo
de clase ``items`` (que debe ser una lista).

Estamos usando una plantilla muy simple para las descripciones de los ``ìtems``,
como esta::

    {{ obj.description }}

Especificar el tipo de Feed
---------------------------

Por omisión, el framework de feeds de sindicación produce RSS 2.0. Para cambiar
eso, agrega un atributo ``feed_type`` a la clase ``Feed``::

    from django.utils.feedgenerator import Atom1Feed

    class MiFeed(Feed):
        feed_type = Atom1Feed

Observa que asignas como valor de ``feed_type`` una clase, no una instancia.
Los tipos de feeds disponibles actualmente se muestran en la siguiente tabla.

.. table:: Tabla 13-1. Tipos de Feeds disponibles en Django.

    ===================================================  ======================
        Clase Feed                                           Formato
    ===================================================  ======================
    ``django.utils.feedgenerator.Rss201rev2Feed``        RSS 2.01 (por defecto)

    ``django.utils.feedgenerator.RssUserland091Feed``    RSS 0.91

    ``django.utils.feedgenerator.Atom1Feed``             Atom 1.0
    ===================================================  ======================

Adjuntos
--------

Para especificar archivos adjuntos o *enclosures* (p. ej. recursos multimedia
asociados al ítem del feed tales como feeds de podcasts MP3, imagenes), usa los
metodos ``item_enclosure_url``, ``item_enclosure_length``, e
``item_enclosure_mime_type``,  por ejemplo:

.. code-block:: python

    from django.contrib.syndication.views import Feed
    from biblioteca.models import Libro

    class UltimosLibrosConAdjuntos(Feed):
        title = "Ultimas portadas de Libros"
        link = "/feeds/ejemplo-con-adjuntos/"

        def items(self):
            return Libro.objects.all()[:30]

        def item_enclosure_url(self, item):
            return item.portada.url

        def item_enclosure_length(self, item):
            return item.portada.size

        item_enclosure_mime_type = "image/jpeg" # Definimos un mime-type

Esto asume, por supuesto que estamos usando el modelo ``Libro`` el cual contiene
un campo llamado portada (que es una imagen), al cual se accede a su URL
mediante ``portada.url`` y mediante ``portada.size`` obtenemos el tamaño en
bytes.

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
para agregar una versión extra. Aquí un ejemplo usando completo::

    from django.contrib.syndication.views import Feed
    from django.utils.feedgenerator import Atom1Feed

    from biblioteca.models import Libro

    class UltimosLibrosFeed(Feed):
        title = "Feed libros publicados"
        link = "/ultimos-libros/"
        description = "Ultimos libros publicados en la biblioteca digital."

        def items(self):
            return Libro.objects.order_by('-fecha_publicacion')[:5]

    class UltimosLibrosAtom(UltimosLibrosFeed):
        feed_type = Atom1Feed
        subtitle = UltimosLibrosFeed.description

.. test ok!

Y este es el URLconf asociado::

    from django.conf.urls import url
    from biblioteca.feeds import UltimosLibrosFeed, UltimosLibrosAtom

    urlpatterns = [
        # ...
        url(r'^feeds/$', UltimosLibrosFeed()),
        url(r'^atom/$', UltimosLibrosAtom()),
        # ...
    ]

.. test ok!

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
   ``'django.template.loaders.app_directories.Loader'`` está en
   tu variable de configuración ``TEMPLATE_LOADERS``. Por omisión se encuentra
   activado, por lo que los cambios son necesarios solamente si modificaste
   dicha variable de configuración.

#. Asegúrate de que tienes instalado el framework sites

.. Admonition:: Nota:

    La aplicación sitemap no instala tablas en la base de datos. La única razón
    de que esté en ``INSTALLED_APPS`` es que el cargador de plantillas
    ``Loader()`` pueda encontrar las plantillas incluidas.

Inicialización
--------------

Para activar la generación del sitemap en tu sitio Django, agrega la siguiente
línea a tu URLconf::

    from django.contrib.sitemaps.views import sitemap

    urlpatterns =[
        url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap')
    ]

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
ej. ``blog`` o ``consulta``) a tu clase ``Sitemap`` (p.e., ``BlogSitemap`` o
``NewsSitemap``).

También puede mapear una *instancia* de una clase ``Sitemap`` (p. ej.
``GenericSitemap(alguna_var)``) en el mismo archivo ``urls.py``.

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

Por ejemplo, asumamos que posees un sistema llamado biblioteca (si haz seguido
los ejemplos ya tienes uno), con un modelo ``Autor``, y quieres que tu sitemap
incluya todos los enlaces a los autores.

Tu clase ``Sitemap`` debería verse así:

.. code-block:: python

    from django.contrib.sitemaps import Sitemap
    from biblioteca.models import Autor

    class SitemapAutores(Sitemap):
        changefreq = "monthly"
        priority = 0.5

        def items(self):
            return Autor.objects.all()

        def lastmod(self, items):
            return items.ultimo_acceso

Y solo necesitas anclar la clase ``SitemapAutores``  creada a la URLconf,  asi:

.. code-block:: python

    from django.conf.urls import url
    from django.contrib.sitemaps.views import sitemap

    from biblioteca.sitemap import SitemapAutores

    urlpatterns =[
        url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'sitemaps': SitemapAutores}}),
        ]

Declarar un ``Sitemap`` debería verse muy similar a declarar un ``Feed``; esto
es justamente un objetivo del diseño.

De forma similar a las clases ``Feed``, los miembros de ``Sitemap`` pueden ser
métodos o atributos. Consulta la sección "`Un feed más complejo`_" para obtener
más información sobre cómo funciona.

Una clase ``Sitemap`` puede definir los siguientes métodos/atributos:

* ``items`` (**requerido**): Provee una lista de objetos. Al framework no le
  importa que *tipo* de objeto es; todo lo que importa es que los objetos
  sean pasados a los métodos ``location()``, ``lastmod()``,
  ``changefreq()``, y ``priority()``.

* ``location`` (opcional): Provee la URL absoluta para el objeto dado. La "URL
  absoluta" significa una URL que no incluye el protocolo o el dominio.

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

Para más información sobre Páginas Planas  o "flatpages" consulta el
:doc:`capítulo 14<chapter14>`.

Sitemap Genérico
~~~~~~~~~~~~~~~~

La clase ``GenericSitemap`` trabaja de forma bastante sencilla.

Para usarla, solo crea una instancia pasándola en una variable a ``sitemap`` en
forma de diccionario. El único requerimiento es que el diccionario tenga una
entrada ``queryset``. También debe poseer una entrada ``date_field`` que
especifica un campo fecha para los objetos obtenidos del ``queryset``. Esto será
usado por el atributo ``lastmod`` en el sitemap generado. También puedes pasar
los argumentos palabra clave (*keyword*) ``priority`` y ``changefreq`` al
constructor ``GenericSitemap`` para especificar dichos atributos para todas las
URLs.

Este es un ejemplo de URLconf parecido al anterior, solo que aquí estamos
usando la clase genérica ``GenericSiteMap`` usando el mismo modelo ``Autor``.

.. code-block::python

    from django.conf.urls import url
    from django.contrib.sitemaps import GenericSitemap
    from django.contrib.sitemaps.views import sitemap

    from biblioteca.models import Autor

    consulta = {
        'queryset': Autor.objects.all(), # Un queryset con todos los objetos del modelo.
        'date_field': 'ultimo_acceso', # Un campo fecha.
    }

    sitemaps = {
        'autores': GenericSitemap(consulta, priority=0.6, changefreq= 'always'),
    }

    urlpatterns =[
        url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap')
    ]


Crear un índice Sitemap
-----------------------

El framework sitemap también tiene la habilidad de crear índices sitemap que
hagan referencia a ficheros sitemap individuales, uno por cada sección definida
en tu diccionario ``sitemaps``. Las única diferencias de uso son:

* Usas dos vistas en tu URLconf:
  ``django.contrib.sitemaps.views.index`` y
  ``django.contrib.sitemaps.views.sitemap``.

* La vista ``django.contrib.sitemaps.views.sitemap`` debe tomar un parámetro
  que corresponde a una palabra clave, llamado ``section``. Por ejemplo:

Así deberían verse las líneas relevantes en tu URLconf para el ejemplo anterior::

    urlpatterns =[
        #...

        url(r'^sitemap3\.xml$','django.contrib.sitemaps.views.index',
            {'sitemaps': sitemaps}),
        url(r'^sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap',
            {'sitemaps': sitemaps})
    ]

Esto genera automáticamente un fichero ``sitemap.xml`` que hace referencia a
ambos ficheros ``sitemap-flatpages.xml`` y ``sitemap-autores.xml``. La clase
``Sitemap`` y el diccionario ``sitemaps`` no cambian en absoluto.

.. http://localhost:9000/sitemap-autores.xml

Hacer ping a Google
-------------------

Puedes desear hacer un "ping" a Google cuando tu sitemap cambia, para hacerle
saber que debe reindexar tu sitio. El framework provee una función para hacer
justamente eso: ``django.contrib.sitemaps.ping_google()``.

.. admonition:: ¡Primero regístrate con Google!

    El comando ``ping_google()`` únicamente trabaja si haz registrado tu sitio
    con ``Google Webmaster Tools``.

``ping_google()`` toma un argumento opcional, ``sitemap_url``, que debe ser la
URL absoluta de tu sitemap (por ej., ``'/sitemap.xml'``). Si este argumento no es
provisto, ``ping_google()`` tratará de generar un sitemap realizando una
búsqueda reversa en tu URLconf.

``ping_google()`` lanza la excepción
``django.contrib.sitemaps.SitemapNotFound`` si no puede determinar la URL de tu
sitemap.

Una forma útil de llamar a ``ping_google()`` es desde el método ``save()``::

    from django.contrib.sitemaps import ping_google

    class Libro(models.Model):
        # ...
        def save(self, force_insert=False, force_update=False):
            super(Libro, self).save(force_insert, force_update)
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

Hacer pin a Google mediante manage.py
-------------------------------------

Una vez que la aplicacion ``sitemap``  es agregada a tu proyecto, puedes hacer
ping a Google usando el comando ``ping_google``  mediante la línea de comandos
as::

    python manage.py ping_google [/sitemap.xml]

¿Qué sigue?
===========

A continuación, seguiremos indagando más profundamente en las herramientas
internas que Django nos ofrece. Él :doc:`capítulo 14<chapter12>` examina todas las
herramientas que necesitas para proveer sitios personalizados: sesiones, usuarios, y
autenticación.

