==============================================
Apéndice D: Referencia de las vistas genéricas
==============================================

El :doc:`Capítulo 9<chapter09>` es una introducción a las vistas genéricas, pero pasa
por alto algunos detalles . Este apéndice describe todas las
vistas genéricas, junto con las opciones que cada una de ellas puede
aceptar. Antes de intentar entender este material de referencia es
muy conveniente leer el :doc:`Capítulo 9<chapter09>` . Tampoco viene mal un repaso a
los modelos ``Book``, ``Publisher`` y ``Author`` definidos en dicho
capítulo, ya que serán usados en los ejemplo incluidos en esta apéndice.

Argumentos comunes a todas las vistas genéricas
===============================================

La mayoría de las vistas aceptan varios argumentos que pueden
modificar su comportamiento. Muchos de esos argumentos funcionan
igual para la mayoría de las vistas. La tabla D-1 describe estos
argumentos comunes; cada vez que veas uno de estos argumentos
en la lista de parámetros admitidos por una vista genérica, su
comportamiento será tal y como se describe en esta tabla.

.. tabla:: Tabla D-1. Argumentos comunes de las vistas genéricas.

==========================  ===============================================
  Argumento                   Descripción
==========================  ===============================================
``allow_empty``             Un valor booleano que indica como debe
                            comportarse la vista si no hay objetos
                            disponibles. Si vale ``False`` y no hay
                            objetos, la vista elevará un error 404 en vez
                            de mostrar una página vacía. Su valor por
                            defecto es ``Falsa``.

``context_processors``      Es una lista de procesadores de contexto
                            adicionales (además de los incluidos por
                            el sistema), que se aplican a la plantilla
                            de la vista.
                            En el :doc:`Capítulo 10<chapter10>`
                            se explica con detalle la lista de 
                            procesadores de  contexto adicionales.

``extra_context``           Un diccionario cuyos valores se añaden al
                            contexto de la plantilla. Si se
                            almacena un objeto que sea invocable, la
                            vista genérica lo ejecutará justo antes de
                            representar la plantilla

``mimetype``                El tipo MIME a usar para el documento
                            resultante. Por defecto utiliza el tipo
                            definido en la variable de configuración
                            ``DEFAULT_MIME_TYPE``, cuyo valor inicial
                            es ``text/html``.

``queryset``                Un objeto de tipo ``QuerySet`` (por ejemplo,
                            ``Author.objects.all()``) del cual se
                            leerán los objetos a utilizar por la vista.
                            En el apéndice C hay más información acerca
                            de los objetos ``QuerySet``. La mayoría de
                            las vistas genéricas necesitan este argumento.

``template_loader``         El cargador de plantillas a utilizar. Por
                            defecto es ``django.template.loader``. Véase
                            el `Capítulo 10`_ donde se da más información
                            acerca de los cargadores de plantillas.

``template_name``           El nombre completo de la plantilla a usar
                            para representar la página. Este argumento
                            se puede usar si queremos modificar el
                            nombre que se genera automáticamente a
                            partir del ``QuerySet``.

``template_object_name``    El nombre de la variable principal en el
                            contexto de la plantilla. Por defecto, es
                            ``'object'``. Para las listas que
                            utilizan más de objeto (por ejemplo, las
                            vistas de listados o de archivos por
                            fechas), se añade el sufijo ``'_list'``
                            al valor de este parámetro, así que si
                            no se indica nada y la vista utiliza
                            varios objetos, estos estarán accesibles
                            mediante una variable llamada
                            ``object_list``.
==========================  ===============================================

Vistas genéricas simples
========================

Dentro del módulo ``django.views.generic.simple`` hay varias
vistas sencillas que manejan unos cuantos problemas frecuentes: mostrar
una plantilla que no necesita una vista lógica, y hacer una redirección
de una página.

Representar una plantilla
-------------------------

*Vista a importar*: ``django.views.generic.simple.direct_to_template``

Esta vista representa una plantilla, a la que se le pasa una
variable de plantilla accesible como ``{{ params }}``, y que es un
diccionario que contiene los parámetros capturados de la URL, si
los hubiera.

Ejemplo
~~~~~~~

Dada la siguiente configuración del URLconf::

    from django.conf.urls.defaults import *
    from django.views.generic.simple import direct_to_template

    urlpatterns = patterns('',
        (r'^foo/$',             direct_to_template, {'template': 'foo_index.html'}),
        (r'^foo/(?P<id>\d+)/$', direct_to_template, {'template': 'foo_detail.html'}),
    )

Una petición a ``/foo/`` mostraría la plantilla ``foo_index.html``, y una
solicitud a ``/foo/15/``  mostraría ``foo_detail.html`` con una variable
de contexto ``{{ params.id }}`` cuyo valor sería ``15``.

Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

    * ``template``: El nombre completo de la plantilla a representar.


Redirigir a otra URL
--------------------

*Vista a importar*: ``django.views.generic.simple.redirect_to``

Esta vista redirige a otra URL. La URL que se pasa como parámetro puede
tener secuencias de formato aptas para diccionarios, que serán
interpretadas contra los parámetros capturados desde la URL origen.

Si la URL pasada como parámetro es ``None``, Django retornará un mensaje
de error 410 ("Gone" según el estándar HTTP).

Ejemplo
~~~~~~~

Este URLconf redirige desde ``/foo/<id>/`` a ``/bar/<id>/``::

    from django.conf.urls.defaults import *
    from django.views.generic.simple import redirect_to

    urlpatterns = patterns('django.views.generic.simple',
        ('^foo/(?p<id>\d+)/$', redirect_to, {'url': '/bar/%(id)s/'}),
    )

Este ejemplo devuelve una respuesta "Gone" para cualquier petición a ``/bar/``::

    from django.views.generic.simple import redirect_to

    urlpatterns = patterns('django.views.generic.simple',
        ('^bar/$', redirect_to, {'url': None}),
    )

Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

* ``url``: La URL a la que redirigir, en forma de cadena de texto, o ``None``
  si quereremos devolver una respuesta 410 ("Gone" según el estándar HTTP).

Vistas de listado/detalle
=========================

Las vistas genéricas de listados/detalle (que residen en el módulo
``Django.views.generic.list_detail``) se encargan de la habitual
tarea de mostrar una lista de elementos por un lado (el listado) y
una vista individual para cada uno de los elementos (el detalle).

Listas de objetos
-----------------

*Vista a importar*: ``django.views.generic.list_detail.object_list``

Esta vista sirve para representear una lista de objetos.

Ejemplo
~~~~~~~

Si consideramos el objeto ``Author`` tal y como se definió en el capítulo
5, podemos usar la vista ``object_list`` para obtener un listado sencillo
de todos los autores usando el siguiente URLconf::

    from mysite.books.models import Author
    from django.conf.urls.defaults import *
    from django.views.generic import list_detail

    author_list_info = {
        'queryset' :   Author.objects.all(),
        'allow_empty': True,
    }

    urlpatterns = patterns('',
        (r'authors/$', list_detail.object_list, author_list_info)
    )

Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

* ``queryset``: Un ``QuerySet`` de los objetos a listar (Véase la table D-1).

Argumentos opcionales
~~~~~~~~~~~~~~~~~~~~~

* ``paginate_by``: es un número entero que especifica cuantos
  objetos se deben mostrar en cada página. Según se especifique
  en este parámetro, los resultados serán paginados, de forma
  que se distribuirán por varias páginas de resultado. La vista
  determinará que página de resultados debe mostrar o bien
  desde un parámetro ``page`` incluido en la URL (vía ``Get``)
  o mediante una variable ``page`` especificada en el URLconf. En
  cualquiera de los dos casos, el índice comienza en cero. En la
  siguiente sección hay una nota sobre paginación donde se explica
  con un poco más de detalle este sistema.

Además, esta vidta acepta cualquiera de los siguientes argumentos opcionales
descritos en la tabla D-1:

* ``allow_empty``
* ``context_processors``
* ``extra_context``
* ``mimetype``
* ``template_loader``
* ``template_name``
* ``template_object_name``

Nombre de la plantilla
~~~~~~~~~~~~~~~~~~~~~~

Si no se ha especificado el parámetro opcional ``template_name``, la vista
usará una plantilla llamada ``<app_label>/<model_name>_list.html``. Tanto
la etiqueta de la aplicación como la etiqueta del modelo se obtienen
del parámetro ``queryset``. La etiqueta de aplicación es el
nombre de la aplicación en que se ha definido el modelo, y la etiqueta
de modelo es el nombre, en minúsculas, de la clase del modelo.

En el ejemplo anterior, tendriamos que el ``queryset`` sería ``Author.objects.all()``, por
lo que la etiqueta de la aplicación será ``books`` y el nombre del modelo es ``author``. Con
esos datos, el nombre de la plantilla a utilizar por defecto será ``books/author_list.html``.

Contexto de plantilla
~~~~~~~~~~~~~~~~~~~~~

Además de los valores que se puedan haber definido en ``extra_context``, el
contexto de la plantilla tendrá los siguientes valores:

* ``object_list``: La lista de los objetos. El nombre de la variable
  viene determinado por el parámetro ``template_object_name``, y vale
  ``'object'`` por defecto. Si se definiera ``template_object_name``
  como ``'foo'``, el nombre de esta variable sería ``foo_list``.

* ``is_paginated``: Un valor booleano que indicará si los resultados
  serán paginados o no. Concretamente, valdrá ``False`` si el
  número de objetos disponibles es inferior o igual a ``paginate_by``.

Si los resultados están paginados, el contexto dispondrá también de estas variables:

* ``results_per_page``: El número de objetos por página. (Su valor es el mismo
  que el del parámetro ``paginate_by``).

* ``has_next``: Un valor booleano indicando si hay una siguiente página.

* ``has_previous``: Un valor booleano indicando si hay una página previa.

* ``page``: El número de la página actual, siendo 1 la primera página.

* ``next``: El número de la siguiente página. Incluso si no hubiera
   siguiente página, este valor seguirá siendo un numero entero que
   apuntaría a una hipotética siguiente página. También utiliza
   un índice basado en 1, no en cero.

* ``previous``: El número de la anterior página, usando un índice
   basado en 1, no en cero.

* ``pages``: El número total de páginas.

* ``hits``: El número total de objetos en *todas* las páginas, no sólo
  en la actual.

.. admonition:: Una nota sobre paginación

Si se utiliza el parámetro ``paginate_by``, Django paginará los resultados. Puedes
indicar qué pagina visualizar usando dos métodos diferentes:

* Usar un parámetro ``page`` en el URLconf. Por ejemplo, tu URLconf
  podría parecerse a este::

  (r'^objects/page(?P<page>[0-9]+)/$', 'object_list', dict(info_dict))

* Pasar el número de la página mediante un parámetro ``page`` en la URL: Por ejemplo,
  tus URL se podrían parecer a esto::

            /objects/?page=3


En ambos casos, ``page`` es un índice basado en 1, lo que significa que la primera
página siempre será la número 1, no la número 0.

Vista de detalle
----------------

*Vista a importar*: ``django.views.generic.list_detail.object_detail``

Esta vista proporciona una representación indidual de los "detalles" de un objeto.

Ejemplo
~~~~~~~

Siguiendo con el ejemplo anterior, podemos añadir una vista de detalle de
cada autor modificacando el URLconf de la siguiente manera::

    from mysite.books.models import Author
    from django.conf.urls.defaults import *
    from django.views.generic import list_detail

    author_list_info = {
        'queryset' :   Author.objects.all(),
        'allow_empty': True,
    }
    **author_detail_info = {**
        **"queryset" : Author.objects.all(),**
        **"template_object_name" : "author",**
    **}**

    urlpatterns = patterns('',
        (r'authors/$', list_detail.object_list, author_list_info),
        **(r'^authors/(?P<object_id>\d+)/$', list_detail.object_detail, author_detail_info),**
    )

Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

* ``queryset``: Un ``QuerySet`` que será usado para localizar el objeto a mostrar (véase la Tabla D-1).

y luego hace falta, o un:

* ``object_id``: El valor de la clave primaria del objeto a mostrar.

o bien:

* ``slug``: La etiqueta o *slug* del objeto en cuestión. Si se usa este sistema de
  identificación, hay que emplear obligatoriamente el argumento ``slug_field`` (que
  se explica en la siguiente sección).


Argumentos opcionales
~~~~~~~~~~~~~~~~~~~~~

* ``slug_field``: El nombre del atributo del objeto que contiene el *slug*. Es
  obligatorio si estás usando el argumento ``slug``, y no se debe usar si estás
  usando el argumento ``object_id``.

* ``template_name_field``: El nombre de un atributo del objeto cuyo valor
  se usará como el nombre de la plantilla a utilizar. De esta forma, puedes
  almacenar en tu objeto la plantilla a usar.

  En otras palabras, si tu objeto tiene un atributo ``'the_template'`` que
  contiene la cadena de texto ``'foo.html'``, y defines ``template_name_field``
  para que valga ``'the_template'``, entonces la vista genérica de este
  objeto usará como plantilla ``'foo.html'``.

  Si el atributo indicado por ``template_name_field`` no existe, se usaría
  el indicado por el argumento ``template_name``. Es un mecanismo
  un poco enmarañado, pero puede ser de mucha ayuda en algunos casos.

Esta vista también acepta estos argumentos comunes (Véase la tabla D-1):

* ``context_processors``
* ``extra_context``
* ``mimetype``
* ``template_loader``
* ``template_name``
* ``template_object_name``

Nombre de la plantilla
~~~~~~~~~~~~~~~~~~~~~~

Si no se especifican ``template_name`` ni ``template_name_field``, se
usará la plantilla ``<app_label>/<model_name>_detail.html``.

Contexto de plantilla
~~~~~~~~~~~~~~~~~~~~~

Además de los valores que se puedan haber definido en ``extra_context``, el
contexto de la plantilla tendrá los siguientes valores:

* ``object``: El objeto. El nombre de esta variable puede ser
  distinto si se ha especificado el argumento ``template_object_name``, cuyo
  valor es ``'object'`` por defecto. Si definimos ``template_object_name``
  como ``'foo'``, el nombre de la variable será ``foo``.

Vistas genéricas basadas en fechas
==================================

Estas vistas genéricas basadas en fechas se suelen utilizar para
organizar la parte de "archivo" de nuestro contenido. Los casos típicos son los
archivos por año/mes/día de un periódico, o el archivo
de una bitácora o *blog*.

.. admonition:: Truco:

    En principio, estas vistas ignoran las fechas que estén situadas en el futuro.

    Esto significa que si intentas visitar una página del archivo que esté en
    el futuro, Django mostrará automáticamente un error 404 ("Página no
    encontrada"), incluso aunque hubiera objetos con esa fecha en el sistema.

    Esto te permite publicar objetos por adelantado, que no se mostrarán
    públicamente hasta que se llegue a la fecha de publicación deseada.

    Sin embargo, para otros tipos de objetos con fechas, este comportamiento
    no es el deseable (por ejemplo, un calendario de próximos eventos). Para
    estas vistas, podemos definir el argumento ``allow_future`` como ``True``  y
    de esa manera conseguir que los objetos con fechas futuras aparezcan (o permitir
    a los usuarios visitar páginas de archivo "en el futuro").

Índice de archivo
-----------------

*Vista a importar*: ``django.views.generic.date_based.archive_index``

Esta vista proporciona un índice donde se mostraría los
"últimos" objetos (es decir, los más recientes) según la fecha.

Ejemplo
~~~~~~~

Supongamos el típico editor que desea una página con la lista de sus
últimos libros publicados. Suponiendo que tenemos un objeto ``Book``
con un atributo de fecha de publicación, ``publication_date``, podemos
usar la vista ``archive_index`` para resolver este problema::


    from mysite.books.models import Book
    from django.conf.urls.defaults import *
    from django.views.generic import date_based

    book_info = {
        "queryset"   : Book.objects.all(),
        "date_field" : "publication_date"
    }

    urlpatterns = patterns('',
        (r'^books/$', date_based.archive_index, book_info),
    )

Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

* ``date_field``: El nombre de un campo ``DateField`` o ``DateTimeField`` de los
  objetos que componen el ``QuerySet``. La vista usará los valores de ese campo
  como referencia para obtener los últimos objetos.

* ``queryset``: El ``QuerySet`` de objetos que forman el archivo.

Argumentos opcionales
~~~~~~~~~~~~~~~~~~~~~

* ``allow_future``: Un valor booleano que indica si los objetos
  "futuros" (es decir, con fecha de referencia en el futuro) deben
  aparecer o no.

* ``num_latest``: El número de objetos que se deben enviar a la
  plantilla. Su valor por defecto es 15.

Esta vista también acepta estos argumentos comunes (Véase la tabla D-1):

* ``allow_empty``
* ``context_processors``
* ``extra_context``
* ``mimetype``
* ``template_loader``
* ``template_name``

Nombre de la plantilla
~~~~~~~~~~~~~~~~~~~~~~

Si no se ha especificado ``template_name``, se
usará la plantilla ``<app_label>/<model_name>_archive.html``.

Contexto de la plantilla
~~~~~~~~~~~~~~~~~~~~~~~~

Además de los valores que se puedan haber definido en ``extra_context``, el
contexto de la plantilla tendrá los siguientes valores:

* ``date_list``: Una lista de objetos de tipo ``datetime.date`` que representarían
  todos los años en los que hay objetos, de acuerdo al ``queryset``. Vienen ordenados
  de forma descendente, los años mas recientes primero.

  Por ejemplo, para un blog que tuviera entradas desde el año 2003 hasta el
  2006, la lista contendrá cuatro objetos de tipo ``datetime.date``, uno
  para cada uno se esos años.

* ``latest``: Los últimos ``num_latest`` objetos en el sistema, considerándolos
  ordenados de forma descendiente por el campo ``date_field`` de referencia. Por
  ejemplo, si ``num_latest`` vale ``10``, entonces ``latest`` será una lista de
  los últimos 10 objetos contenidos en el ``queryset``.

Archivos anuales
----------------

*Vista a importar*: ``django.views.generic.date_based.archive_year``

Esta vista sirve para presentar archivos basados en años. Poseen una lista
de los meses en los que hay algún objeto, y pueden mostrar opcionalmente todos
los objetos publicados en un año determinado.

Ejemplo
~~~~~~~

Vamos a ampliar el ejemplo anterior incluyendo una vista que muestre todos los libros
publicados en un determinado año::


    from mysite.books.models import Book
    from django.conf.urls.defaults import *
    from django.views.generic import date_based

    book_info = {
        "queryset"   : Book.objects.all(),
        "date_field" : "publication_date"
    }

    urlpatterns = patterns('',
        (r'^books/$', date_based.archive_index, book_info),
        **(r'^books/(?P<year>\d{4})/?$', date_based.archive_year, book_info),**
    )

Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

* ``date_field``: Igual que en ``archive_index`` (Véase la sección previa).

* ``queryset``: El ``QuerySet`` de objetos archivados.

* ``year``: El año, con cuatro dígitos, que la vista usará para
  mostrar el archivo (Como se ve en el ejemplo, normalmente
  se obtiene  de un parámetro en la URL).

Argumentos opcionales
~~~~~~~~~~~~~~~~~~~~~

* ``make_object_list``: Un valor booleano que indica si se debe
  obtener la lista completa de objetos para este año y pasársela
  a la plantilla. Si es ``True``, la lista de objetos estará disponible
  para la plantilla con el nombre de ``object_list`` (Aunque este nombre
  podría ser diferente; véase la información sobre ``object_list``
  en la siguiente explicación sobre "Contexto de plantilla"). Su
  valor por defecto es ``False``.

* ``allow_future``: Un valor booleano que indica si deben incluirse
  o no en esta vista las fechas "en el futuro".

Esta vista también acepta los siguientes argumentos comunes (Véase la Tabla D-1):

* ``allow_empty``
* ``context_processors``
* ``extra_context``
* ``mimetype``
* ``template_loader``
* ``template_name``
* ``template_object_name``

Nombre de la plantilla
~~~~~~~~~~~~~~~~~~~~~~

Si no se especifica ningún valor en ``template_name``, la vista usará
la plantilla ``<app_label>/<model_name>_archive_year.html``.

Contexto de la plantilla
~~~~~~~~~~~~~~~~~~~~~~~~

Además de los valores que se puedan haber definido en ``extra_context``, el
contexto de la plantilla tendrá los siguientes valores:

* ``date_list``: Una lista de objetos de tipo ``datetime.date``, que
  representan todos los meses en los que hay disponibles objetos
  en un año determinado, de acuerdo al contenido del ``queryset``, en
  orden ascendente.

* ``year``: El año a mostrar, en forma de cadena de texto con cuatro dígitos.

* ``object_list``: Si el parámetro ``make_object_list`` es ``True``, esta
  variable será una lista de objetos cuya fecha de referencia cae en
  en año a mostrar, ordenados por fecha. El nombre de la variable depende
  del parámetro ``template_object_name``, que es ``'object'`` por
  defecto. Si ``template_object_name`` fuera ``'foo'``, el nombre de esta
  variable sería ``foo_list``.

Si ``make_object_list`` es ``False``, ``object_list`` será una lista vacía.

Archivos mensuales
------------------

*Vista a importar*: ``django.views.generic.date_based.archive_month``

Esta vista proporciona una representación basada en meses, en la que
se muestran todos los objetos cuya fecha de referencia caiga en
un determinado mes y año.

Ejemplo
~~~~~~~

Siguiendo con nuestro ejemplo, añadir una vista mensual debería
ser algo sencillo::

    urlpatterns = patterns('',
        (r'^books/$', date_based.archive_index, book_info),
        (r'^books/(?P<year>\d{4})/?$', date_based.archive_year, book_info),
        **(**
            **r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',**
            **date_based.archive_month,**
            **book_info**
        **),**
    )

Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

* ``year``: El año a mostrar, en forma de cadena de texto con cuatro dígitos.

* ``month``: El mes a mostrar, formateado de acuerdo con el argumento
  ``month_format``.

* ``queryset``: El ``QuerySet`` de objetos archivados.

* ``date_field``: El nombre del campo de tipo ``DateField`` o ``DateTimeField``
   en el modelo usado para el ``QuerySet`` que se usará como fecha de referencia.

Argumentos opcionales
~~~~~~~~~~~~~~~~~~~~~

* ``month_format``: Una cadena de texto que determina el formato que
  debe usar el parámetro ``month``. La sintaxis a usar debe coincidir
  con la de la función ``time.strftime`` (La documentación de esta
  función se puede consultar en http://www.djangoproject.com/r/python/strftime/).
  Su valor por defecto es ``"%b"``, que significa el nombre del mes, en inglés, y
  abreviado a tres letras (Es decir, "jan", "feb", etc.). Para cambiarlo de forma
  que se usen números, hay que utilizar como cadena de formato ``"%m"``.

* ``allow_future``: Un valor booleano que indica si deben incluirse
  o no en esta vista las fechas "en el futuro", igual al que hemos
  visto en otras vistas anteriores.

Esta vista también acepta los siguientes argumentos comunes (Véase la Tabla D-1):

* ``allow_empty``
* ``context_processors``
* ``extra_context``
* ``mimetype``
* ``template_loader``
* ``template_name``
* ``template_object_name``

Nombre de la plantilla
~~~~~~~~~~~~~~~~~~~~~~

Si no se especifica ningún valor en ``template_name``, la vista usará como
plantilla ``<app_label>/<model_name>_archive_month.html``.

Contexto de la plantilla
~~~~~~~~~~~~~~~~~~~~~~~~

Además de los valores que se puedan haber definido en ``extra_context``, el
contexto de la plantilla tendrá los siguientes valores:

* ``month``: Un objeto de tipo ``datetime.date`` que representa el mes y año
  de referencia.

* ``next_month``: Un objeto de tipo ``datetime.date`` que representa el primer
  día del siguiente mes. Si el siguiente mes cae en el futuro, valdrá ``None``.

* ``previous_month``: Un objeto de tipo ``datetime.date`` que representa el primer
  día del mes anterior. Al contrario que ``next_month``, su valor nunca será ``None``.

* ``object_list``: Una lista de objetos cuya fecha de referencia cae en
  en año y mes a mostrar. El nombre de la variable depende
  del parámetro ``template_object_name``, que es ``'object'`` por
  defecto. Si ``template_object_name`` fuera ``'foo'``, el nombre de esta
  variable sería ``foo_list``.

Archivos semanales
------------------

*Vista a importar*: ``django.views.generic.date_based.archive_week``

Esta vista muestra todos los objetos de una semana determinada.

.. admonition:: Nota:

    Por consistencia con las bibliotecas de manejo de fechas de Python, Django
    asume que el primer día de la semana es el domingo.

Ejemplo
~~~~~~~

.. code-block:: python

    urlpatterns = patterns('',
        # ...
        **(**
            **r'^(?P<year>\d{4})/(?P<week>\d{2})/$',**
            **date_based.archive_week,**
            **book_info**
        **),**
    )


Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

    * ``year``: El año, con cuatro dígitos (Una cadena de texto).

    * ``week``: La semana del año (Una cadena de texto).

    * ``queryset``: El ``QuerySet`` de los objetos archivados.

    * ``date_field``: El nombre del campo de tipo ``DateField`` o ``DateTimeField``
      en el modelo usado para el ``QuerySet`` que se usará como fecha de referencia.

Argumentos opcionales
~~~~~~~~~~~~~~~~~~~~~

    * ``allow_future``: Un valor booleano que indica si deben incluirse
      o no en esta vista las fechas "en el futuro".

Esta vista también acepta los siguientes argumentos comunes (Véase la Tabla D-1):

* ``allow_empty``
* ``context_processors``
* ``extra_context``
* ``mimetype``
* ``template_loader``
* ``template_name``
* ``template_object_name``

Nombre de la plantilla
~~~~~~~~~~~~~~~~~~~~~~

Si no se ha especificado ningún valor en ``template_name`` la vista usará como plantilla
``<app_label>/<model_name>_archive_week.html``.

Contexto de la plantilla
~~~~~~~~~~~~~~~~~~~~~~~~

Además de los valores que se puedan haber definido en ``extra_context``, el
contexto de la plantilla tendrá los siguientes valores:

* ``week``: Un objeto de tipo ``datetime.date``, cuyo valor es el primer
  día de la semana considerada.

* ``object_list``: Una lista de objetos disponibles para la semana
  en cuestión. El nombre de esta variable depende del parámetro
  ``template_object_name``, que es ``'object'`` por defecto. Si
  ``template_object_name`` fuera ``'foo'``, el nombre de esta
  variable sería ``foo_list``.

Archivos diarios
----------------

*Vista a importar*: ``django.views.generic.date_based.archive_day``

esta vista muestra todos los objetos para un día determinado.

Ejemplo
~~~~~~~

.. code-block:: python

    urlpatterns = patterns('',
        # ...
        **(**
            **r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$',**
            **date_based.archive_day,**
            **book_info**
        **),**
    )


Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

* ``year``: El año, con cuatro dígitos (Una cadena de texto).

* ``month``: El mes, formateado de acuerdo a lo indicado por el
  argumento ``month_format``

* ``day``: El día, formateado de acuerdo al argumento ``day_format``.

* ``queryset``: El ``QuerySet`` de los objetos archivados.

* ``date_field``: El nombre del campo de tipo ``DateField`` o ``DateTimeField``
  en el modelo usado para el ``QuerySet`` que se usará como fecha de referencia.

Argumentos opcionales
~~~~~~~~~~~~~~~~~~~~~

* ``month_format``: Una cadena de texto que determina el formato que
  debe usar el parámetro ``month``. Hay una explicación más detallada
  en la seccion de "Archivos mensuales", incluida anteriormente.

* ``day_format``: Equivalente a ``month_format``, pero para el día. Su
  valor por defecto es ``"%d"`` (que es el día del mes como número
  decimal y relleno con ceros de ser necesario; 01-31).

* ``allow_future``: Un valor booleano que indica si deben incluirse
  o no en esta vista las fechas "en el futuro".

Esta vista también acepta los siguientes argumentos comunes (Véase la Tabla D-1):

* ``allow_empty``
* ``context_processors``
* ``extra_context``
* ``mimetype``
* ``template_loader``
* ``template_name``
* ``template_object_name``

Nombre de la plantilla
~~~~~~~~~~~~~~~~~~~~~~

Si no se ha especificado ningún valor en ``template_name`` la vista usará como plantilla
``<app_label>/<model_name>_archive_day.html``.

Contexto de la plantilla
~~~~~~~~~~~~~~~~~~~~~~~~

Además de los valores que se puedan haber definido en ``extra_context``, el
contexto de la plantilla tendrá los siguientes valores:

* ``day``: Un objeto de tipo ``datetime.date`` cuyo valor es el del día en cuestión.

* ``next_day``: Un objeto de tipo ``datetime.date`` que representa el
      siguiente día. Si cae en el futuro, valdrá ``None``.

* ``previous_day``: Un objeto de tipo ``datetime.date`` que representa el
  día  anterior. Al contrario que ``next_day``, su valor nunca será ``None``.

* ``object_list``: Una lista de objetos disponibles para el día
  en cuestión. El nombre de esta variable depende del parámetro
  ``template_object_name``, que es ``'object'`` por defecto. Si
  ``template_object_name`` fuera ``'foo'``, el nombre de esta
  variable sería ``foo_list``.

Archivo para hoy
----------------

La vista ``django.views.generic.date_based.archive_today`` muestra todos
los objetos cuya fecha de referencia sea *hoy*. Es exactamente igual a
``archive_day``, excepto que no se utilizan los argumentos
``year``, ``month`` ni ``day``, ya que esos datos se obtendrán
de la fecha actual.

Ejemplo
~~~~~~~

.. code-block:: python

    urlpatterns = patterns('',
        # ...
        **(r'^books/today/$', date_based.archive_today, book_info),**
    )

Páginas de detalle basadas en fecha
-----------------------------------

*Vista a importar*: ``django.views.generic.date_based.object_detail``

Se usa esta vista para representar un objeto individual.

Esta vista tiene una URL distinta de la vista ``object_detail``; mientras
que la última usa una URL como, por ejemplo, ``/entries/<slug>/``, esta
usa una URL en la forma ``/entries/2006/aug/27/<slug>/``.

.. admonition:: Nota:

    Si estás usando páginas de detalle basadas en la fecha con *slugs* en
    la URL, lo más probable es que quieras usar la opción ``unique_for_date``
    en el campo *slug*, de forma que se garantice que los *slugs* nunca se
    duplican para una misma fecha. Lee el apéndice F para más detalles sobre
    la opción ``unique_for_date``.

Ejemplo
~~~~~~~

Esta vista tiene una (pequeña) diferencia con las demás vistas basadas en
fechas que hemos visto anteriormente, y es que necesita que le especifiquemos
de forma inequívoca el objeto en cuestión; esto lo podemos hacer con el
identificador del objeto o con un campo de tipo *slug*.

Como el objeto que estamos usando en el ejemplo no tiene ningún campo
de tipo *slug*, usaremos el identificador para la URL. Normalmente
se considera una buena práctica usar un campo *slug*, pero no lo
haremos en aras de simplificar el ejemplo.

.. code-block:: python

    urlpatterns = patterns('',
        # ...
        **(**
            **r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/(?P<object_id>[\w-]+)/$',**
            **date_based.object_detail,**
            **book_info**
        **),**
    )

Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

* ``year``: El año, con cuatro dígitos (Una cadena de texto).

* ``month``: El mes, formateado de acuerdo a lo indicado por el
  argumento ``month_format``

* ``day``: El día, formateado de acuerdo al argumento ``day_format``.

* ``queryset``: El ``QuerySet`` que contiene el objeto.

* ``date_field``: El nombre del campo de tipo ``DateField`` o ``DateTimeField``
  en el modelo usado para el ``QuerySet`` que se usará como fecha de referencia.

Y también habrá que especificar, o bien un:

* ``object_id``: El valor de la clave primaria del objeto.

o bien un:

* ``slug``: El *slug* del objeto. Si se utiliza este argumento, es obligatorio
  especificar un valor para el argumento ``slug_field`` (que describiremos en la
  siguiente sección).

Argumentos opcionales
~~~~~~~~~~~~~~~~~~~~~

* ``allow_future``: Un valor booleano que indica si deben incluirse
  o no en esta vista las fechas "en el futuro".

* ``day_format``: Equivalente a ``month_format``, pero para el día. Su
  valor por defecto es ``"%d"`` (que es el día del mes como número
  decimal y relleno con ceros de ser necesario; 01-31).

* ``month_format``: Una cadena de texto que determina el formato que
  debe usar el parámetro ``month``. Hay una explicación más detallada
  en la seccion de "Archivos mensuales", incluida anteriormente.

* ``slug_field``: El  nombre del atributo que almacena el valor del
  slug*. Es obligatorio incluirlo si se ha usado el argumento ``slug``, y
  no debe aparecer si se ha especificado el argumento ``object_id``.

* ``template_name_field``: El nombre de un atributo del objeto cuyo valor
  se usará como el nombre de la plantilla a utilizar. De esta forma, puedes
  almacenar en tu objeto la plantilla a usar.

  En otras palabras, si tu objeto tiene un atributo ``'the_template'`` que
  contiene la cadena de texto ``'foo.html'``, y defines ``template_name_field``
  para que valga ``'the_template'``, entonces la vista genérica de este
  objeto usará como plantilla ``'foo.html'``.

Esta vista también acepta los siguientes argumentos comunes (Véase la Tabla D-1):

* ``context_processors``
* ``extra_context``
* ``mimetype``
* ``template_loader``
* ``template_name``
* ``template_object_name``

Nombre de la plantilla
~~~~~~~~~~~~~~~~~~~~~~

Si no se ha especificado ningún valor en ``template_name`` la vista usará como plantilla
``<app_label>/<model_name>_detail.html``.

Contexto de la plantilla
~~~~~~~~~~~~~~~~~~~~~~~~

Además de los valores que se puedan haber definido en ``extra_context``, el
contexto de la plantilla tendrá los siguientes valores:

* ``object``: El object. El nombre de esta variable depende del parámetro
  ``template_object_name``, que es ``object`` por defecto. Si ``template_object_name``
  fuera ``foo``, el nombre de esta variable sería ``foo``.

Vistas genericas para Crear/Modificar/Borrar
============================================

El módulo ``Django.views.generic.create_update`` contiene una serie de funciones
para crear, modificar y borrar objetos.

.. admonition:: Nota:
 
    Estas vistas pueden cambiar ligeramente en la nueva revisión
    de la arquitectura de formularios de Django (que está en fase
    de desarrollo con el nombre ``django.newforms``).

Todas estas vistas presenta formularios si se acceden con ``GET`` y
realizan la operación solicitada (crear/modificar/borrar) si se acceden
con ``POST``.

Estas vistas tienen un concepto muy simple de la seguridad. Aunque
aceptan un argumento llamado ``login_required``, que restringe el
acceso sólo a usuarios identificados, no hacen nada más. Por ejemplo,
no comprueban que el usuario que está modificando un objeto sea
el  mismo usuario que lo creo, ni validarán ningún tipo de
permisos.

En cualquier caso, la mayor parte de las veces se puede conseguir esta
funcionalidad simplemente escribiendo un pequeño recubrimiento alrededor de
la vista genérica. Para más información sobre esta técnica, véase el
:doc:`Capítulo 9<chapter09>`.

Vista de creación de objetos
----------------------------

*Vista a importar*: ``django.views.generic.create_update.create_object``

Esta vista presenta un formulario que permite la creación de un objeto. Cuando
se envían los datos del formulario, la vista se vuelve a mostrar si se produce
algún error de validación (incluyendo, por supuesto, los mensajes pertinentes) o, en
caso de que no se produzca ningún error de validación, guarda el objeto en la
base de datos.

Ejemplo
~~~~~~~

Si quisiéramos permitir al usuario que creara nuevos libros en la
base de datos, podríamos hacer algo como esto::

    from mysite.books.models import Book
    from django.conf.urls.defaults import *
    from django.views.generic import create_update

    book_info = {'model' : Book}

    urlpatterns = patterns('',
        (r'^books/create/$', create_update.create_object, book_info),
    )

Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

* ``model``: El modelo Django del objeto a crear.

.. admonition:: Nota:

    Obsérvese que esta vista espera el *modelo* del objeto a crear, y no
    un ``QuerySet`` como el resto de las vistas anteriores que se han visto
    previamente.

Argumentos opcionales
~~~~~~~~~~~~~~~~~~~~~

* ``post_save_redirect``: Una URL, a la cual la vista redirigirá después de haber
  guardado el objeto. Si no se especifica, se tomará de ``object.get_absolute_url()``

  ``post_save_redirect``: puede contener cadenas de formato para diccionarios, cuyos
  valores se interpolarán usando los nombres de los atributos del objeto. Por ejemplo, se
  podría usar: ``post_save_redirect="/polls/%(slug)s/"``.

* ``login_required``: Un valor booleano que obliga a que la operación la realice
  un usuario identificado, ya sea para ver el formulario o para realizar la
  operación de creación del objeto. Utiliza el subsistema de autentificación
  y seguridad de Django. Por defecto, su valor es ``False``.

  En caso de que se defina como ``True``, si un usuario no identificado intentase
  acceder a esta página o guardar los datos, Django le redirigiría a
  ``/accounts/login/``

Esta vista también acepta los siguientes argumentos comunes (Véase la Tabla D-1):

* ``context_processors``
* ``extra_context``
* ``template_loader``
* ``template_name``

Nombre de la plantilla
~~~~~~~~~~~~~~~~~~~~~~

Si no se ha especificado ningún valor en ``template_name`` la vista usará como plantilla
``<app_label>/<model_name>_form.html``.

Contexto de la plantilla
~~~~~~~~~~~~~~~~~~~~~~~~

Además de los valores que se puedan haber definido en ``extra_context``, el
contexto de la plantilla tendrá los siguientes valores:

* ``form``: Una instancia de la clase ``FormWrapper``, que representa
  el formulario a utilizar. Esto te permite referirte de una forma
  sencilla a los campos del formulario desde la plantilla. Por
  ejemplo, si el modelo consta de dos atributos, ``name`` y ``address``::

          <form action="" method="post">
            <p><label for="id_name">Name:</label> {{ form.name }}</p>
            <p><label for="id_address">Address:</label> {{ form.address }}</p>
          </form>

Hay que hacer notar que ``form`` es un  FormWrapper definido en *oldforms*, y
que no está contemplado en este libro. Véase http://www.djangoproject.com/documentation/0.96/forms/
par más información.

Vista de modificación de objetos
--------------------------------

*Vista a importar*: ``django.views.generic.create_update.update_object``

Esta vista es prácticamente igual al anterior, siendo la única diferencia
que esta permite la modificación de los atributos del objeto, en vez de su creación.

Ejemplo
~~~~~~~

Siguiendo con el ejemplo, podemos proporcionar al usuario una interfaz de
modificación de los datos de un libro con el siguiente código en el
URLconf:

.. code-block:: python

    from mysite.books.models import Book
    from django.conf.urls.defaults import *
    from django.views.generic. import create_update

    book_info = {'model' : Book}

    urlpatterns = patterns('',
        (r'^books/create/$', create_update.create_object, book_info),
        **(**
            **r'^books/edit/(?P<object_id>\d+)/$',**
            **create_update.update_object,**
            **book_info**
        **),**
    )

Argumentos obligatorios
~~~~~~~~~~~~~~~~~~~~~~~

* ``model``: El modelo Django a editar. Hay que prestar atención a que es
  el *modelo* en sí, y no un objeto tipo ``QuerySet``.

Y, o bien un:

* ``object_id``: El valor de la clave primaria del objeto a modificar.

o bien un:

* ``slug``: El *slug* del objeto a modificar. Si se pasa este argumento, es
  obligatorio también el argumento ``slug_field``.

Argumentos opcionales
~~~~~~~~~~~~~~~~~~~~~

* ``slug_field``: El nombre del campo en el que se almacena el
  valor del *slug* del sujeto. Es obligado usar este argumento
  si se ha indicado el argumento ``slug``, pero no debe
  especificarse si hemos optado por identificar el objeto
  mediante su calve primaria, usando el argumento ``object_id``.

Esta vista acepta los mismos argumentos opcionales que la vista
de creación y, además, el argumento común ``template_object_name``, explicado
en la tabla D-1.

Nombre de la plantilla
~~~~~~~~~~~~~~~~~~~~~~

Esta vista utiliza el mismo nombre de plantilla por defecto que la
vista de creación (``<app_label>/<model_name>_form.html``).

Contexto de la plantilla
~~~~~~~~~~~~~~~~~~~~~~~~

Además de los valores que se puedan haber definido en ``extra_context``, el
contexto de la plantilla tendrá los siguientes valores:

* ``form``: Una instancia de ``FormWrapper`` que representa el formulario
  de edición del objeto. Véase la sección "`Vista de creación de objetos`_"
  para obtener más información de esta variable.

* ``object``: El objeto a editar (El nombre de esta variable puede ser
  diferente si se ha especificado el argumento ``template_object_name``).

Vista de borrado de objetos
---------------------------

*Vista a importar*: ``django.views.generic.create_update.delete_object``

Esta vista es muy similar a la dos anteriores: crear y modificar objetos. El
propósito de esta es, sin embargo, permitir el borrado de objetos.

Si la vista es alimentada mediante ``GET``, se mostrará una pantalla de
confirmación (del tipo "¿Realmente quieres borrar este objeto?"). Si
la vista se alimenta con ``POST``, el objeto será borrado sin
conformación.

Los argumentos son los mismos que los de la vista de modificación, así
como las variables de contexto. El nombre de la plantilla por defecto
para esta vista es ``<app_label>/<model_name>_confirm_delete.html``.

