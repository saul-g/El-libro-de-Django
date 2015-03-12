==============================================
Apéndice C: Referencia de las vistas genéricas
==============================================

Él :doc:`capítulo 11<chapter11>` es una introducción a las vistas genéricas
basadas en clases, pero pasa por alto algunos detalles importantes. Este
apéndice describe todas las vistas genéricas, junto con las opciones que cada
una de ellas puede aceptar. Antes de intentar entender este material de
referencia es muy conveniente leer el :doc:`capítulo 11<chapter11>` . Tampoco
viene mal un  repaso a los modelos ``Libro``, ``Editor`` y ``Autor`` definidos
en dicho capítulo, ya que serán usados en los ejemplo incluidos en esta apéndice.

Argumentos comunes a las vistas genéricas basadas en clases
===========================================================

La mayoría de las vistas genéricas basadas en clases, aceptan algunos argumentos
que pueden modificar su  comportamiento. Muchos de esos argumentos funcionan
igual para la mayoría de  las vistas (hay sus excepciones). La tabla C-1 describe
algunos de  estos argumentos comunes; cada vez que veas  uno de estos argumentos
en la lista de parámetros admitidos por una vista  genérica, su comportamiento
será tal y como se describe en esta tabla.

.. table:: Tabla C-1. Argumentos comunes a la mayoría de vistas genéricas.

  ==========================  ===============================================
    Argumento                   Descripción
  ==========================  ===============================================
  ``allow_empty``             Un valor booleano que indica cómo debe
                              comportarse la vista si no hay objetos
                              disponibles. Si vale ``False`` y no hay
                              objetos, la vista elevará un error 404 en vez
                              de mostrar una página vacía. Su valor por
                              defecto es ``Falsa``.

  ``context_object_name``     El nombre de la variable principal en el
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

  ``context_processors``      Es una lista de procesadores de contexto
                              adicionales (además de los incluidos por
                              el sistema), que se aplican a la plantilla
                              de la vista.

  ``model``                   El modelo del cual la vista mostrara los datos.
                              Especificar ``model = Foo`` es tan efectivo como
                              especificar ``queryset = Foo.objects.all()``

  ``mimetype``                El tipo MIME a usar para el documento
                              resultante. Por defecto utiliza el tipo
                              definido en la variable de configuración
                              ``DEFAULT_MIME_TYPE``, cuyo valor inicial
                              es ``text/html``.

  ``queryset``                Un objeto de tipo ``QuerySet`` (por ejemplo,
                              ``Autor.objects.all()``) del cual se
                              leerán los objetos a utilizar por la vista.
                              En el apéndice C hay más información acerca
                              de los objetos ``QuerySet``. La mayoría de
                              las vistas genéricas necesitan este argumento.

  ``paginate_by``             El numero máximo de objetos para paginar
                              permitidos en una plantilla (Disponible solo en
                              listas de objetos).

  ``template_name``           El nombre completo de la plantilla a usar
                              para representar la página. Este argumento
                              se puede usar si queremos modificar el
                              nombre que se genera automáticamente a
                              partir del ``QuerySet``.
  ==========================  ===============================================

Vistas genéricas basadas en clases-base
=======================================

Dentro del módulo ``django.views.generic`` hay varias vistas sencillas que
manejan unos cuantos problemas frecuentes: mostrar una plantilla que no
necesita una vista lógica ``TemplateView``, hacer una redirección de una
página ``RedirectView`` y la más importante de todas, la  clase base maestra,
de la cual todas las demás clases genéricas heredan llamada ``View``. Estas
tres clases implementan muchas de las funcionalidades necesitadas para crear
vistas en Django, puedes pensar en ellas como ```vistas padres`` que pueden
usarse en sí mismas o heredando sus atributos dependiendo de la complejidad
y las necesidades  de tu proyecto.

Muchas de las características incorporadas en la vistas basadas en clases,
heredan de otras clases o de varias clases usando mixins. Debido a que
la cadena de herencia es muy importante, las clases ancestro están documentadas
debajo del título de cada sección de sus ancestros (MRO). MRO es un acrónimo
para el orden de resolución de un método.

Vista base: View
----------------

.. class:: django.views.generic.base.View

  La clase-base maestra de todas las vistas genéricas. Todas las vistas basadas
  en clases genéricas heredan de esta clase base.

  **Flujo de métodos:**

  1. :meth:`dispatch()`
  2. :meth:`http_method_not_allowed()`
  3. :meth:`options()`

  **Ejemplo:**

  Para crear el famoso ``hola mundo`` usando una clase genérica, creamos una vista
  ``View`` importándola del modulo ``django.views.generic`` de la siguiente forma:

  .. snippet::
     :filename: views.py

     from django.http import HttpResponse
     from django.views.generic import View

     class MiVista(View):

         def get(self, request, *args, **kwargs):
             return HttpResponse('¡Hola, Mundo!')

  Luego la enlazamos directamente en la URL:

  .. snippet::
     :filename: urls.py

     from django.conf.urls import url
     from aplicacion.views import MiVista

     urlpatterns = [
         url(r'^hola/$', MiVista.as_view(), name='mi-vista'),
     ]

  **Atributos**

  .. attribute:: http_method_names

    La lista de nombre de métodos HTTP, que esa vista acepta son:

    Default::

        ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

  **Metodos**

  .. classmethod:: as_view(**initkwargs)

    Retorna una vista llamable que toma una petición y retorna una respuesta::

        response = MiVista.as_view()(request)

  .. method:: dispatch(request, *args, **kwargs)

    La ``view`` la vista -- el método que acepta un argumento ``request`` mas
    los argumentos pasados y devuelve una respuesta HTTP.

    La implementación predeterminada inspecciona el método HTTP y trata de delegarlo
    a el método que coincida con la petición HTTP; una petición ``GET`` será delegada
    a un método ``get()``, una ``POST`` a un ``post()`` y así sucesivamente.

    Por omisión una petición a ``HEAD`` será delegada al método ``get()``. Si
    necesitas manejar peticiones ``HEAD`` de diferentes formas usa ``GET`` para
    sobrescribir el método ``head()``.

  .. method:: http_method_not_allowed(request, *args, **kwargs)

    Si la vista es llamada mediante un método HTTP  no soportado, este método
    es llamado en su lugar.

    La implementación predeterminada devuelve ``HttpResponseNotAllowed`` con
    una lista de métodos permitidos en texto plano.

  .. method:: options(request, *args, **kwargs)

    Maneja la respuesta a las peticiones para los verbos OPTIONS HTTP. Devuelve
    una lista de nombres de métodos HTTP permitidos para las vistas.

Renderizar una plantilla con TemplateView
-----------------------------------------

.. class:: django.views.generic.base.TemplateView

  Renderiza una plantilla dada, con el contexto que contiene los parámetros
  capturados en la URL.

  **Ancestros (MRO)**

  Esta vista hereda métodos y atributos de las siguientes vistas:

  * :class:`django.views.generic.base.TemplateResponseMixin`
  * :class:`django.views.generic.base.ContextMixin`
  * :class:`django.views.generic.base.View`

  **Flujo de métodos**

  1. :meth:`~django.views.generic.base.View.dispatch()`
  2. :meth:`~django.views.generic.base.View.http_method_not_allowed()`
  3. :meth:`~django.views.generic.base.ContextMixin.get_context_data()`

  **Ejemplo:**

  Para mostrar una página de bienvenida que muestre los últimos 5 libros
  publicados en la base de datos, usamos la clase ``TemplateView``
  directamente para crear la vista así:

  .. snippet::
     :filename: views.py

      from django.views.generic.base import TemplateView
      from biblioteca.models import Libro

      class PaginaBienvenida(TemplateView):

          template_name = "bienvenida.html"

          def get_context_data(self, **kwargs):
              context = super(PaginaBienvenida, self).get_context_data(**kwargs)
              context['ultimos_libros'] = Libro.objects.all()[:5]
              return context

  Después solo la enlazamos a su respectiva URL:

  .. snippet::
     :filename: urls.py

      from django.conf.urls import url
      from biblioteca.views import PaginaBienvenida

      urlpatterns = [
          url(r'^$', PaginaBienvenida.as_view(), name='bienvenidos'),
      ]

  **Contexto**

  * Rellena (A través de la clase :class:`~django.views.generic.base.ContextMixin`)
    con los argumentos clave,  capturados de el patrón URL que sirve la vista.


Redirigir a otra URL mediante RedirectView
------------------------------------------

.. class:: django.views.generic.base.RedirectView

  Esta vista redirige a otra URL.

  La URL dada puede contener un formato de estilo tipo diccionario, que será
  intercalado contra los parámetros capturados en la URL. Ya que el intercalado
  de palabras claves se hace *siempre*  (incluso si no se le pasan argumentos),
  por lo que cualquier carácter como "%" (un marcador de posición en Python)
  en la  URL debe ser escrito como "%%" de modo que Python lo convierta en un
  simple signo de porcentaje en la salida.

  Si la URL pasada como parámetro es ``None``, Django retornará un mensaje
  de error 410 ("Gone" según el estándar HTTP).

  **Ancestros (MRO)**

  Esta vista hereda métodos y atributos de las siguientes vistas:

  * :class:`django.views.generic.base.View`

  **Flujo de métodos**

  1. :meth:`~django.views.generic.base.View.dispatch()`
  2. :meth:`~django.views.generic.base.View.http_method_not_allowed()`
  3. :meth:`get_redirect_url()`

  **Ejemplo**

  Supongamos que queremos redirecionar a nuestros usuarios a una pagina
  que actualiza un ficticio contador de libros, después de que visiten
  una página de detalles:

  .. snippet::
   :filename: views.py

      from django.shortcuts import get_object_or_404
      from django.views.generic.base import RedirectView

      from biblioteca.models import Article

      class RedirecionarDeContadorLibros(RedirectView):

          permanent = False
          query_string = True
          pattern_name = 'detalles-libro'

          def get_redirect_url(self, *args, **kwargs):
              libro = get_object_or_404(Libro, pk=kwargs['pk'])
              libro.update_counter()
              return super(RedirecionarDeContadorLibros,
                  self).get_redirect_url(*args, **kwargs)

  .. snippet::
   :filename: urls.py

      from django.conf.urls import url
      from django.views.generic.base import RedirectView

      from biblioteca.views import RedirecionarDeContadorLibros, DetalleLibros

      urlpatterns = [
          url(r'^contador/(?P<pk>[0-9]+)/$', RedirecionarDeContadorLibros.as_view(),
              name='contador-libros'),
          url(r'^detalles/(?P<pk>[0-9]+)/$', DetalleLibros.as_view(),
              name='detalles-libro'),
          url(r'^go-to-django/$', RedirectView.as_view(url='http://djangoproject.com'),
              name='go-to-django'),
      ]

  **Atributos**

  .. attribute:: url

      La URL a redirecionar, como una cadena o string. O ``None`` para lanzar un
      error 410(Gone).

  .. attribute:: pattern_name

      El nombre de el patrón URL para redireccionamiento. El redireccionamiento
      puede hacerse usando los mismos argumentos: ``args`` y ``kwargs`` que son
      pasados en la vistas.

  .. attribute:: permanent

      Indica si el redireccionamiento debería ser permanente, La única diferencia
      aquí es el código del estatus HTTP que devuelve. Si es ``True``, el
      redirecionamiento usara un código de estatus 301. Si es ``False``, el código
      de estatus será 302. El valor predeterminado para ``permanent`` es ``True``.

  .. attribute:: query_string

      Indica si se le pasa la cadena de consulta GET a la nueva localización. Si
      es ``True``, la cadena de consulta es agregada a la URL. Si es ``False`` la
      cadena de consulta es descartada. El valor predeterminado para
      ``query_string`` es ``False``.

  **Metodos**

  .. method:: get_redirect_url(*args, **kwargs)

      Construye la URL del objetivo, para el cambio de dirección.

      La implementación predeterminada usa el atributo ``url`` cuando comienza
      como una cadena y optimiza la expansión de los nombres de parámetros ``%``
      capturados en la cadena, usando los nombres de grupos capturados en la URL.

      Si él :attr:`url` no está establecido, ``get_redirect_url()``  trata de usar
      el inverso de :attr:`pattern_name` usando los valores capturados en la URL
      (usando nombres y nombres de grupos)

      Si la petición de :attr:`query_string`, es agregada a la cadena de consulta
      para general la URL.
      La subclase puede implementar cualquier comportamiento que desee, mientras
      que el método devuelva un redireccionamiento listo para una cadena de una URL.

Vistas de listado/detalle
=========================

Las vistas genéricas basadas en clases de listados/detalle (que residen en el
módulo ``django.views.generic``) se encargan de la habitual tarea de mostrar una
lista de elementos por un lado (el listado) y una vista individual para cada uno
de  los elementos (el detalle).

Listas de objetos: ListView
---------------------------

.. class:: django.views.generic.list.ListView

    Una página que representa una lista de objetos.

    Mientras esta vista es ejecutada con ``self.object_list`` contiene una lista
    de objetos (usualmente, pero no necesariamente un ``queryset``) sobre los
    que la vista está operando.

    **Ancestros (MRO)**

    Esta vista hereda métodos y atributos de las siguientes vistas:

    * :class:`django.views.generic.list.MultipleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * :class:`django.views.generic.list.BaseListView`
    * :class:`django.views.generic.list.MultipleObjectMixin`
    * :class:`django.views.generic.base.View`

    **Flujo de métodos**

    1. :meth:`~django.views.generic.base.View.dispatch()`
    2. :meth:`~django.views.generic.base.View.http_method_not_allowed()`
    3. :meth:`~django.views.generic.base.TemplateResponseMixin.get_template_names()`
    4. :meth:`~django.views.generic.list.MultipleObjectMixin.get_queryset()`
    5. :meth:`~django.views.generic.list.MultipleObjectMixin.get_context_object_name()`
    6. :meth:`~django.views.generic.list.MultipleObjectMixin.get_context_data()`
    7. ``get()``
    8. :meth:`~django.views.generic.base.TemplateResponseMixin.render_to_response()`

.. class:: django.views.generic.list.BaseListView

    Una vista base para mostrar una lista de objetos, No está pensada para ser
    usada directamente, pero puede usarse como una clase padre para
    :class:`django.views.generic.list.ListView` u otras vistas que representen
    una lista de objetos.

    **Ancestros (MRO)**

    Esta vista hereda métodos y atributos de las siguientes vistas:

    * :class:`django.views.generic.list.MultipleObjectMixin`
    * :class:`django.views.generic.base.View`

    **Metodos**

    .. method:: get(request, *args, **kwargs)

        Agrega ``object_list`` al contexto. Si el atributo
        :attr:`~django.views.generic.list.MultipleObjectMixin.allow_empty`
        es ``True`` muestra una lista vacía. Si el atributo
        :attr:`~django.views.generic.list.MultipleObjectMixin.allow_empty` es
        ``False`` lanza un error 404.

    **Ejemplo**

    Si consideramos el objeto ``Autor`` tal y como se definió en el capítulo
    5, podemos usar la vista ``ListView`` para obtener un listado sencillo de todos
    los autores usando la siguiente vista genérica (usando una clase ) y su
    respectiva  URLconf:

    .. snippet::
     :filename: biblioteca/views.py

        from django.views.generic import ListView
        from biblioteca.models import Autor

        # El único requerimiento es un queryset o modelo.
        class ListaAutores(ListView):
            model = Autor

    .. snippet::
     :filename: biblioteca/urls.py

        from django.conf.urls import url
        from biblioteca.views import ListaAutores

        # Enlazamos la vista usando el método as_view()
        urlpatterns = [
            url(r'^autores/$', ListaAutores.as_view()),
        ]

    Y la plantilla: 'autor_list.html'

    .. code-block:: html+django

       <h1>Lista de Autores</h1>

        <ul>
        {% for autor in object_list %}
            <li><a href="{% url 'detalles-autores' autor.id %}">{{ autor.nombre }}
                {{ autor.apellidos }}</li>
        {% empty %}
            <li>No hay autores registrados.</li>
        {% endfor %}
        </ul>

    La vista ``ListView`` usa el método interno ``get_absolute_url()`` de el
    modelo para enlazar la url y la vista detallada de un objeto ``DetailView``,
    de la siguiente forma:

    .. snippet:: python
     :filename: biblioteca/models.py

        from django.core.urlresolvers import reverse
        from django.db import models

        # La clase que define al modelo autor
        class Autor(models.Model):
        nombre = models.CharField(max_length=30)
        # ...

            def get_absolute_url(self):
                return reverse('detalles-autores', args=[self.pk])

    **Argumentos obligatorios**

    * ``queryset``: Un ``QuerySet`` de los objetos a listar (Véase la table C-1) o
      ``model``: El modelo del cual la vista mostrara los datos, como en el ejemplo
      anterior, ``model = Autor`` es equivalente a usar ``queryset = Autor.objects.all()``

    **Argumentos opcionales**

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

    **Nombre de la plantilla**

    Si no se ha especificado el parámetro opcional ``template_name``, la vista
    usará una plantilla llamada ``<app_label>/<model_name>_list.html``. Tanto
    la etiqueta de la aplicación como la etiqueta del modelo se obtienen
    del parámetro ``queryset``. La etiqueta de aplicación es el
    nombre de la aplicación en que se ha definido el modelo, y la etiqueta
    de modelo es el nombre, en minúsculas, de la clase del modelo.

    En el ejemplo anterior, tendriamos que el ``queryset`` sería ``Autor.objects.all()``,
    por lo que la etiqueta de la aplicación será ``biblioteca`` y el nombre del
    modelo es ``autor``. Con esos datos, el nombre de la plantilla a utilizar por
    defecto será ``biblioteca/autor_list.html``.

    **Contexto de plantilla**

    Además de los valores que se puedan haber definido en el contexto, la plantilla
    tendrá los siguientes valores:

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

      Si se utiliza el parámetro ``paginate_by``, Django paginará los resultados.
      Puedes indicar qué pagina visualizar usando dos métodos diferentes:

      * Usar un parámetro ``page`` en el URLconf.
      * Pasar el número de la página mediante un parámetro ``page`` en la URL.

      En ambos casos, ``page`` es un índice basado en 1, lo que significa que la primera
      página siempre será la número 1, no la número 0.

Vista de detalle: DetailView
----------------------------

.. class:: django.views.generic.detail.DetailView

    Esta vista proporciona una representación individual de los "detalles" de un
    objeto.

    Cuando esta vista es ejecutada ``self.object`` contiene un objeto sobre el que
    la vista opera.

    **Ancestros (MRO)**

    Esta vista hereda métodos y atributos de las siguientes vistas:

    * :class:`django.views.generic.detail.SingleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * ``django.views.generic.detail.BaseDetailView``
    * :class:`django.views.generic.detail.SingleObjectMixin`
    * :class:`django.views.generic.base.View`

    **Flujo de métodos**

    1. :meth:`~django.views.generic.base.View.dispatch()`
    2. :meth:`~django.views.generic.base.View.http_method_not_allowed()`
    3. :meth:`~django.views.generic.base.TemplateResponseMixin.get_template_names()`
    4. :meth:`~django.views.generic.detail.SingleObjectMixin.get_slug_field()`
    5. :meth:`~django.views.generic.detail.SingleObjectMixin.get_queryset()`
    6. :meth:`~django.views.generic.detail.SingleObjectMixin.get_object()`
    7. :meth:`~django.views.generic.detail.SingleObjectMixin.get_context_object_name()`
    8. :meth:`~django.views.generic.detail.SingleObjectMixin.get_context_data()`
    9. ``get()``
    10. :meth:`~django.views.generic.base.TemplateResponseMixin.render_to_response()`

    **Ejemplo**

    Siguiendo con el ejemplo anterior, podemos añadir una vista de detalle de
    cada autor modificando el URLconf y pasándole un contexto extra ``ahora``,
    de la  siguiente manera:

    .. snippet::
     :filename: biblioteca/views.py

        from django.views.generic.detail import DetailView
        from django.utils import timezone

        from biblioteca.models import Autor

        class DetalleAutores(DetailView):
            model = Autor

            # Le agregamos un contexto extra 'ahora', que muestra la fecha actual.
            def get_context_data(self, **kwargs):
                context = super(DetalleAutores, self).get_context_data(**kwargs)
                context['ahora'] = timezone.now()
                return context

    .. snippet::
      :filename: biblioteca/urls.py

        from django.conf.urls import url

        from biblioteca.views import DetalleAutores

        urlpatterns = [
            url(r'^detalle/autores/(?P<pk>[0-9]+)/$', DetalleAutores.as_view(),
                name='detalles-autores' ),
        ]

    Y la plantilla: 'biblioteca/autor_detail.html'

    .. code-block:: html+django

        {% extends "base.html" %}

        {% block content %}
          <h1>{{ object.nombre }}{{ object.apellidos}}</h1>
            <ul>
              <li>Email: {{ object.email }}</li>
              <li>Ultimo acceso: {{ object.ultimo_acceso }}</li>
              <li>Fecha: {{ ahora|date }}</li>
           </ul>
        {% endblock %}

    **Argumentos obligatorios**

    * ``queryset``: Un ``QuerySet`` que será usado para localizar el objeto a
      mostrar o un ``model`` (véase la Tabla C-1).

    y luego hace falta un:

    * ``object_id``: El valor de la clave primaria del objeto a mostrar. En el
      ejemplo  anterior usamos ``pk`` para capturar la clave primaria del objeto
      en la URL, para pasársela a la clase vista.

    o bien:

    * ``slug``: La etiqueta o *slug* del objeto en cuestión. Si se usa este sistema de
      identificación, hay que emplear obligatoriamente el argumento ``slug_field`` (que
      se explica en la siguiente sección).

    **Argumentos opcionales**

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

    **Nombre de la plantilla**

    Si no se especifican ``template_name`` ni ``template_name_field``, se
    usará la plantilla ``<app_label>/<model_name>_detail.html``.

    **Contexto de plantilla**

    Además de los valores que se puedan haber definido en el contexto,  la
    plantilla tendrá los siguientes valores:

    * ``object``: El objeto. El nombre de esta variable puede ser
      distinto si se ha especificado el argumento ``context_object_name``, cuyo
      valor es ``'object'`` por defecto. Si definimos ``context_object_name``
      como ``'foo'``, el nombre de la variable será ``foo``.


Vistas genéricas para Crear/Modificar/Borrar
============================================

.. class:: django.views.generic.dates

El módulo :mod:`django.views.generic.edit`, contiene una serie de funciones
para crear, modificar y borrar objetos.

Las vistas son las siguientes:

* :class:`django.views.generic.edit.FormView`
* :class:`django.views.generic.edit.CreateView`
* :class:`django.views.generic.edit.UpdateView`
* :class:`django.views.generic.edit.DeleteView`

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
:doc:`capítulo 11<chapter11>`.

Mostrar formularios con: FormView
---------------------------------

.. class:: django.views.generic.edit.FormView

    Una vista que muestra un formulario. Si existen errores vuelve a mostrar
    el formulario con los errores de validación;  si esta tiene éxito
    redirecciona a la nueva URL.

    **Ancestros (MRO)**

    Esta vista hereda métodos y atributos de las siguientes vistas:

    * :class:`django.views.generic.base.TemplateResponseMixin`
    * ``django.views.generic.edit.BaseFormView``
    * :class:`django.views.generic.edit.FormMixin`
    * :class:`django.views.generic.edit.ProcessFormView`
    * :class:`django.views.generic.base.View`

    **Ejemplo**

    Supongamos que queremos mostrar un sencillo formulario de contactos:

    .. snippet::
     :filename: forms.py

        from django import forms

        class FormularioContactos(forms.Form):
            nombre = forms.CharField()
            mensaje = forms.CharField(widget=forms.Textarea)

            def send_email(self):
                # envia el email usando el diccionario self.cleaned_data
                pass

    .. snippet::
     :filename: views.py

        from django.views.generic.edit import FormView
        from biblioteca.forms import FormularioContactos

        class VistaContactos(FormView):
            template_name = 'contactos.html'
            form_class = FormularioContactos
            success_url = '/gracias/'

            def form_valid(self, form):
                # Este método es llamado cuando el formulario valida los datos
                # a enviar. Debe devolver un HttpResponse
                form.send_email()
                return super(VistaContactos, self).form_valid(form)

    .. snippet:: html+django
     :filename: contactos.html

        <form action="" method="post">{% csrf_token %}
            {{ form.as_p }}
            <input type="enviar" value="Enviar mensaje" />
        </form>

Vista de creación de objetos: CreateView
----------------------------------------

.. class:: django.views.generic.edit.CreateView

    Esta vista presenta un formulario que permite la creación de un objeto. Cuando
    se envían los datos del formulario, la vista se vuelve a mostrar si se produce
    algún error de validación (incluyendo, por supuesto, los mensajes pertinentes)
    o, en  caso de que no se produzca ningún error de validación, guarda el objeto
    en la base de datos.

    **Ancestros (MRO)**

    Esta vista hereda los métodos y atributos de las siguientes vistas:

    * :class:`django.views.generic.detail.SingleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * ``django.views.generic.edit.BaseCreateView``
    * :class:`django.views.generic.edit.ModelFormMixin`
    * :class:`django.views.generic.edit.FormMixin`
    * :class:`django.views.generic.detail.SingleObjectMixin`
    * :class:`django.views.generic.edit.ProcessFormView`
    * :class:`django.views.generic.base.View`

    **Atributos**

    .. attribute:: template_name_suffix

        La pagina ``CreateView``  a mostrar, mediante una petición ``GET``
        que usa como ``template_name_suffix`` a ``_form``. Por ejemplo
        cambiando este atributo por ``_create_form`` para una vista
        para crear objetos, por ejemplo para el modelo ``Autor``
        ocasionara que el valor predeterminado de  ``template_name``  sea
        "biblioteca/autor_create_form.html".

    .. attribute:: object

        Cuando se usa  ``CreateView`` se tiene acceso a ``self.object``, el cual
        es el objeto creado. Si el objeto no ha sido creado, el valor será
        ```None``.

    **Ejemplo**

    Si quisiéramos permitir al usuario que creara nuevos autores en la
    base de datos, podríamos hacer algo como esto:

    .. snippet::
     :filename: views.py

        from django.views.generic.edit import CreateView
        from biblioteca.models import Autor

        class CrearAutor(CreateView):
            model = Autor
            fields = ['nombre, apellidos']

    Plantilla:'biblioteca/author_form.html'

    .. code-block:: html+django

        <form action="" method="post">{% csrf_token %}
            {{ form.as_p }}
            <input type="enviar" value="Crear" />
        </form>

    **Argumentos obligatorios**

    * ``model``: El modelo Django del objeto a crear.

    .. admonition:: Nota:

        Obsérvese que esta vista espera el *modelo* del objeto a crear, y no
        un ``QuerySet`` como el resto de las vistas anteriores que se han visto
        previamente.

    **Nombre de la plantilla**

    Si no se ha especificado ningún valor en ``template_name`` la vista usará
    como plantilla ``<app_label>/<model_name>_form.html``.

    **Contexto de la plantilla**

    Además de los valores que se puedan haber definido en el contexto, la
    plantilla tendrá los siguientes valores:

    * ``form``: Una instancia de la clase ``ModelForm``, que representa
      el formulario a utilizar. Esto te permite referirte de una forma
      sencilla a los campos del formulario desde la plantilla. Por
      ejemplo, si el modelo consta de dos atributos, ``nombre`` y ``direccion``:

    .. code-block: html+django

          <form action="" method="post">{% csrf_token %}
            <p><label for="id_name">Nombre:</label> {{ form.nombre }}</p>
            <p><label for="id_address">Direccion:</label> {{ form.direccion }}</p>
          </form>


Vista para modificar objetos: UpdateView
----------------------------------------

.. class:: django.views.generic.edit.UpdateView

    Esta vista muestra un formulario para editar un objeto existente, vuelve a
    mostrar el formulario en caso de errores de validación (si los hay) y
    permite guardar los cambios en el objeto. Usa un formulario generado
    automáticamente por el modelo de la clase del objeto (A menos que se
    especifique manualmente una clase para el formulario ).

    **Ancestros (MRO)**

    Esta vista hereda los métodos y atributos de las siguientes vistas:

    * :class:`django.views.generic.detail.SingleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * ``django.views.generic.edit.BaseUpdateView``
    * :class:`django.views.generic.edit.ModelFormMixin`
    * :class:`django.views.generic.edit.FormMixin`
    * :class:`django.views.generic.detail.SingleObjectMixin`
    * :class:`django.views.generic.edit.ProcessFormView`
    * :class:`django.views.generic.base.View`

    **Atributos**

    .. attribute:: template_name_suffix

      La pagina ``UpdateView``  a mostrar, mediante una petición ``GET``
      que usa como ``template_name_suffix`` a ``_form``. Por ejemplo
      cambiando este atributo por ``_create_form`` para una vista
      para actualizar objetos, por ejemplo para el modelo ``Autor``
      ocasionara que el valor predeterminado de  ``template_name``  sea
      'biblioteca/autor_create_form.html'.

    .. attribute:: object

      Cuando se usa ``UpdateView` se tiene acceso a ``self.object``, el cual
      es el objeto modificado.

    **Ejemplo**

    Siguiendo con el ejemplo, podemos proporcionar al usuario una interfaz de
    modificación de los datos de un autor con el siguiente código en el
    URLconf:

    .. snippet::
      :filename: biblioteca/views.py

        from django.views.generic.edit import UpdateView
        from biblioteca.models import Autor

        class ModificarAutor(UpdateView):
            model = Autor
            fields = ['nombre', 'apellidos']
            template_name_suffix = '_update_form'

    Y por supuesto la plantilla: 'autor_update_form.html'

    .. code-block:: html+django

        <form action="" method="post">{% csrf_token %}
            {{ form.as_p }}
            <input type="submit" value="Update" />
        </form>

    **Argumentos obligatorios**

    * ``model``: El modelo Django a editar. Hay que prestar atención a que es
      el *modelo* en sí, y no un objeto tipo ``QuerySet``.

    Y, o bien un:

    * ``object_id``: El valor de la clave primaria del objeto a modificar.

    o bien un:

    * ``slug``: El *slug* del objeto a modificar. Si se pasa este argumento, es
      obligatorio también el argumento ``slug_field``.

    **Argumentos opcionales**

    * ``slug_field``: El nombre del campo en el que se almacena el
      valor del *slug* del sujeto. Es obligado usar este argumento
      si se ha indicado el argumento ``slug``, pero no debe
      especificarse si hemos optado por identificar el objeto
      mediante su clave primaria, usando el argumento ``object_id``.

      Esta vista acepta los mismos argumentos opcionales que la vista
      de creación y, además, el argumento común ``template_object_name``,
      explicado en la tabla C-1.

    **Nombre de la plantilla**

    Esta vista utiliza el mismo nombre de plantilla por defecto que la
    vista de creación (``<app_label>/<model_name>_form.html``).

    **Contexto de la plantilla**

    Además de los valores que se puedan haber definido en el contexto,
    la plantilla tendrá los siguientes valores:

    * ``form``: Una instancia de ``ModelForm`` que representa el formulario
      de edición del objeto.

    * ``object``: El objeto a editar (El nombre de esta variable puede ser
      diferente si se ha especificado el argumento ``template_object_name``).

Vista de borrado de objetos: DeleteView
---------------------------------------

.. class:: django.views.generic.edit.DeleteView

    Una vista que muestra una página de confirmación  y borrado de un objeto
    existente. Esta vista es muy similar a la dos anteriores: crear y modificar
    objetos. El  propósito de esta vista es, sin embargo, permitir el borrado
    de objetos.

    Si la vista es alimentada mediante ``GET``, se mostrará una pantalla de
    confirmación (del tipo "¿Realmente quieres borrar este objeto?"). Si
    la vista se alimenta con ``POST``, el objeto será borrado sin
    conformación.

    Los argumentos son los mismos que los de la vista de modificación, así
    como las variables de contexto. El nombre de la plantilla por defecto
    para esta vista es ``<app_label>/<model_name>_confirm_delete.html``.

    **Ancestros (MRO)**

    Esta vista hereda los métodos y atributos de las siguientes vistas:

    * :class:`django.views.generic.detail.SingleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * ``django.views.generic.edit.BaseDeleteView``
    * :class:`django.views.generic.edit.DeletionMixin`
    * ``django.views.generic.detail.BaseDetailView``
    * :class:`django.views.generic.detail.SingleObjectMixin`
    * :class:`django.views.generic.base.View`

    .. attribute:: template_name_suffix

        La pagina ``DeleteView``  a mostrar, mediante una peticion ``GET``
        que usa como ``template_name_suffix`` a ``_confirm_delete``.
        Por ejemplo cambiando este atributo por ``_check_delete`` para
        una vista para actualizar objetos, por ejemplo para el modelo ``Autor``
        ocasionara que el valor predeterminado de  ``template_name``  sea
        ``biblioteca/autor__check_delete.html``.

    **Ejemplo**

    Supongamos que queremos borrar un objeto ``Autor``, esta es la forma en la
    que lo podemos hacer.

    .. snippet::
     :filename: biblioteca/views.py

        from django.views.generic.edit import DeleteView
        from django.core.urlresolvers import reverse_lazy
        from biblioteca.models import Author

        class BorrarAutor(DeleteView):
            model = Autor
            success_url = reverse_lazy('lista-autores')

    Y la plantilla: 'biblioteca/author_confirm_delete.html'

    .. code-block:: html+django

        <form action="" method="post">{% csrf_token %}
            <p>¿Realmente quieres borrar este {{ object }}"?</p>
            <input type="enviar" value="Confirmar" />
        </form>

Vistas genéricas basadas en fechas
==================================

Estas vistas genéricas basadas en fechas se suelen utilizar para
organizar la parte de "archivo" de nuestro contenido. Los casos típicos son los
archivos por año/mes/día de un periódico, o el archivo de una bitácora o *blog*.

.. admonition:: Truco:

    En principio, estas vistas ignoran las fechas que estén situadas en el futuro.

    Esto significa que si intentas visitar una página de un archivo que esté en
    el futuro, Django mostrará automáticamente un error 404 ("Página no
    encontrada"), incluso aunque hubiera objetos con esa fecha en el sistema.

    Esto te permite publicar objetos por adelantado, que no se mostrarán
    públicamente hasta que se llegue a la fecha de publicación deseada.

    Sin embargo, para otros tipos de objetos con fechas, este comportamiento
    no es el deseable (por ejemplo, un calendario de próximos eventos). Para
    estas vistas, podemos definir el argumento ``allow_future`` como ``True``  y
    de esa manera conseguir que los objetos con fechas futuras aparezcan (o
    permitir a los usuarios visitar páginas de archivo "en el futuro").

Índice de archivo: ``ArchiveIndexView``
---------------------------------------

.. class:: django.views.generic.dates.ArchiveIndexView

    Esta vista proporciona un índice a nivel-superior donde se muestran los
    "últimos" objetos  (es decir, los más recientes) según la fecha. Los objetos
    con fechas en el futuro no están incluidos, a menos que se establezca el
    atributo ``allow_future`` en ``True``.

    **Ancestros (MRO)**

    * :class:`django.views.generic.list.MultipleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * :class:`django.views.generic.dates.BaseArchiveIndexView`
    * :class:`django.views.generic.dates.BaseDateListView`
    * :class:`django.views.generic.list.MultipleObjectMixin`
    * :class:`django.views.generic.dates.DateMixin`
    * :class:`django.views.generic.base.View`

    **Contexto**

    Además del contexto ofrecido por:
    :class:`django.views.generic.list.MultipleObjectMixin` (via
    :class:`django.views.generic.dates.BaseDateListView`), el contexto de
    las plantillas será:

    * ``date_list``: Un objeto
      :meth:`DateQuerySet<django.db.models.query.QuerySet.dates>` que contiene
      todos las años según los cuales tengan objetos disponibles de acuerdo al
      ``queryset``, representado como un objeto
      :class:`datetime.datetime<python:datetime.datetime>` en orden descendiente.

    **Notas**

    * Usa de forma predeterminada ``latest`` para el ``context_object_name``.
    * Usa de forma predeterminada ``_archive`` para el sufijo ``template_name_suffix``.
    * Usa de forma predeterminada ``date_list`` por año, pero puede ser
      sobrescrito  a mes o día usando el atributo ``date_list_period``.  Esto
      también se aplica a las vistas de las subclases.

    **Ejemplo**


    Supongamos el típico editor que desea una página con la lista de sus
    últimos libros publicados. Suponiendo que tenemos un objeto ``Libro``
    con un atributo tipo, ``fecha_publicacion``, podemos usar la vista
    ``ArchiveIndexView`` para resolver este problema:

    .. snippet::
     :filename: biblioteca/urls.py

        from django.conf.urls import url
        from django.views.generic.dates import ArchiveIndexView

        from biblioteca.models import Libro

        urlpatterns = [
            url(r'^ultimos-libros/$',
                ArchiveIndexView.as_view(model=Libro, date_field="fecha_publicacion"),
                    name="ultimos_libros"),
        ]

    La plantilla: 'biblioteca/libro_archive.html'

    .. code-block:: html+django

        <ul>
            {% for libros in latest %}
                <li>{{ libros.fecha_publicacion }}: {{ libros.titulo }}</li>
            {% endfor %}
        </ul>

    **Argumentos obligatorios**

    * ``date_field``: El nombre de un campo tipo ``DateField`` o ``DateTimeField``
      de los objetos que componen el ``QuerySet``. La vista usará los valores de
      ese campo como referencia para obtener los últimos objetos.

    * ``queryset``: El ``QuerySet`` de objetos que forman el archivo o el ``model``.

    **Argumentos opcionales**

    * ``allow_future``: Un valor booleano que indica si los objetos
      "futuros" (es decir, con fecha de referencia en el futuro) deben
      aparecer o no.

    **Nombre de la plantilla**

    Si no se ha especificado ``template_name``, se
    usará la plantilla ``<app_label>/<model_name>_archive.html``.

    **Contexto de la plantilla**

    Además de los valores que se puedan haber definido en el contexto de la
    plantilla tendrá los siguientes valores:

    * ``date_list``: Una lista de objetos de tipo ``datetime.date`` que representarían
      todos los años en los que hay objetos, de acuerdo al ``queryset``. Vienen ordenados
      de forma descendente, los años más recientes primero.

      Por ejemplo, para un blog que tuviera entradas desde el año 2003 hasta el
      2006, la lista contendrá cuatro objetos de tipo ``datetime.date``, uno
      para cada uno se esos años.

    * ``latest``: Los últimos ``num_latest`` objetos en el sistema, considerándolos
      ordenados de forma descendiente por el campo ``date_field`` de referencia.

Archivos anuales: ``YearArchiveView``
-------------------------------------

.. class:: django.views.generic.dates.BaseYearArchiveView

    Esta vista sirve para presentar archivos basados en años. Poseen una lista
    de los meses en los que hay algún objeto, y pueden mostrar opcionalmente todos
    los objetos publicados en un año determinado. Los objetos con fechas en el
    futuro no están incluidos, a menos que se establezca el  atributo
    ``allow_future`` en ``True``.

    **Ancestros (MRO)**

    * :class:`django.views.generic.list.MultipleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * :class:`django.views.generic.dates.BaseYearArchiveView`
    * :class:`django.views.generic.dates.YearMixin`
    * :class:`django.views.generic.dates.BaseDateListView`
    * :class:`django.views.generic.list.MultipleObjectMixin`
    * :class:`django.views.generic.dates.DateMixin`
    * :class:`django.views.generic.base.View`

    **Atributos**

    .. attribute:: make_object_list

    Un valor booleano que especifica si debe recuperar la lista completa de
    objetos para este año y pasársela a la plantilla. Si es ``True`` la lista
    de objetos estará disponible en el contexto. Si es ```False``, el queryset
    usara el valor ``None`` como la lista de objetos. De forma predeterminada
    esta es ``False``.

    .. method:: get_make_object_list()

    Determina si un objeto de la lista, debe devolverse como parte de el
    contexto. Devuelve de forma predeterminada
    :attr:`~YearArchiveView.make_object_list`

    **Contexto**

    Además del contexto ofrecido por:
    :class:`django.views.generic.list.MultipleObjectMixin` (a través de
    :class:`django.views.generic.dates.BaseDateListView`), el contexto de la
    plantilla contendrá:

    * ``date_list``: Un objeto
      :meth:`DateQuerySet<django.db.models.query.QuerySet.dates>` que contiene
      todos los meses en los que hay objetos disponibles,  de acuerdo al
      ``queryset``, representado como un objeto
      :class:`datetime.datetime<python:datetime.datetime>` en orden ascendente.

    * ``year``: Un objeto  :class:`~datetime.date` que representa el año dado.

    * ``next_year``: Un objeto :class:`~datetime.date` que representa el primer
      día de el siguiente año, de acuerdo al :attr:`~BaseDateListView.allow_empty` y
      :attr:`~DateMixin.allow_future`.

    * ``previous_year``: Un objeto :class:`~datetime.date` que representa el primer
      día del año previo, de acuerdo al :attr:`~BaseDateListView.allow_empty` y
      :attr:`~DateMixin.allow_future`.

    **Notas**

    * Usa de forma predeterminada ``_archive_year`` como el nombre del sufijo
      de plantilla para  ``template_name_suffix``.

    **Ejemplo**

    Vamos a ampliar el ejemplo anterior incluyendo una vista que muestre todos los
    libros publicados en un determinado año:

    .. snippet::
      :filename: biblioteca/views.py

        from django.views.generic.dates import YearArchiveView

        from biblioteca.models import Libro

        class LibrosAnuales(YearArchiveView):
            queryset = Libro.objects.all()
            date_field = "fecha_publicacion"
            make_object_list = True
            allow_future = True

    .. snippet::
     :filename: biblioteca/urls.py

        from django.conf.urls import url
        from biblioteca.views import LibrosAnuales

        urlpatterns = [
            url(r'^(?P<year>[0-9]{4})/$',
                LibrosAnuales.as_view(),
                    name="libros_anuales"),
        ]

    La plantilla: 'biblioteca/libros_archive_year.html'

    .. code-block:: html+django

        <ul>
            {% for fecha in date_list %}
                <li>{{ fecha|date }}</li>
            {% endfor %}
        </ul>

        <div>
            <h1>Todos los libros del {{ year|date:"Y" }}</h1>
               {% for libros in object_list %}
                   <p>
                       {{ libros.titulo }} - {{ libros.fecha_publicacion|date:"F j, Y" }}
                   </p>
               {% endfor %}
        </div>

    **Argumentos obligatorios**

    * ``date_field``: Igual que en ``ArchiveIndexView`` (Véase la sección previa).

    * ``queryset``: El ``QuerySet`` de objetos archivados.

    * ``year``: El año, con cuatro dígitos, que la vista usará para
      mostrar el archivo (Como se ve en el ejemplo, normalmente
      se obtiene  de un parámetro en la URL).

    **Argumentos opcionales**

    * ``make_object_list``: Un valor booleano que indica si se debe
      obtener la lista completa de objetos para este año y pasársela
      a la plantilla. Si es ``True``, la lista de objetos estará disponible
      para la plantilla con el nombre de ``object_list`` (Aunque este nombre
      podría ser diferente; véase la información sobre ``object_list``
      en la siguiente explicación sobre "Contexto de plantilla"). Su
      valor por defecto es ``False``.

    * ``allow_future``: Un valor booleano que indica si deben incluirse
      o no en esta vista las fechas "en el futuro".

    **Nombre de la plantilla**

    Si no se especifica ningún valor en ``name``, la vista usará
    la plantilla ``<app_label>/<model_name>_archive_year.html``.

    **Contexto de la plantilla**

    Además de los valores que se puedan haber definido en  el contexto de la
    plantilla,  tendrá los siguientes valores:

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

.. class:: django.views.generic.dates.BaseMonthArchiveView

    Esta vista proporciona una representación basada en meses, en la que se
    muestran todos los objetos cuya fecha de referencia caiga en un determinado
    mes y año. Los objetos con fechas en el futuro no están incluidos, a menos
    que se establezca el  atributo   ``allow_future`` en ``True``.

    **Ancestros (MRO)**

    * :class:`django.views.generic.list.MultipleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * :class:`django.views.generic.dates.BaseMonthArchiveView`
    * :class:`django.views.generic.dates.YearMixin`
    * :class:`django.views.generic.dates.MonthMixin`
    * :class:`django.views.generic.dates.BaseDateListView`
    * :class:`django.views.generic.list.MultipleObjectMixin`
    * :class:`django.views.generic.dates.DateMixin`
    * :class:`django.views.generic.base.View`

    **Contexto**

    Además del contexto ofrecido por:
    :class:`~django.views.generic.list.MultipleObjectMixin` (a través de
    :class:`~django.views.generic.dates.BaseDateListView`), el contexto de la
    plantilla contendrá:

    * ``date_list``: Un objeto
      :meth:`DateQuerySet<django.db.models.query.QuerySet.dates>` que contiene
      todos los días que contienen objetos disponibles en el mes dado, de
      acuerdo  al ``queryset`` representado por el objeto
      :class:`datetime.datetime<python:datetime.datetime>` en orden ascendente.

    * ``month``:Una objeto de la clase :class:`~datetime.date` que representa
      en mes dado.

    * ``next_month``: Un objeto de la clase :class:`~datetime.date` que
      representa el primer día de el siguiente mes, de acuerdo al atributo
      :attr:`~BaseDateListView.allow_empty` y
      :attr:`~DateMixin.allow_future`.

    * ``previous_month``: Un objeto de la clase :class:`~datetime.date` que
      representa el primer día del mes anterior, de acuerdo al atributo
      :attr:`~BaseDateListView.allow_empty` y :attr:`~DateMixin.allow_future`.

    **Notas**

    * Usa de forma predeterminada ``_archive_month`` como el nombre del sufijo
      de plantilla para  ``template_name_suffix``.

    **Ejemplo**

    Siguiendo con nuestro ejemplo, añadir una vista mensual a nuestra aplicación,
    debería ser algo sencillo:

    .. snippet::
     :filename: biblioteca/views.py

        from django.views.generic.dates import MonthArchiveView
        from biblioteca.models import Libro

        class LibrosPorMes(MonthArchiveView):
            queryset = Libro.objects.all()
            date_field = "fecha_publicacion"
            make_object_list = True
            allow_future = True

    .. snippet::
     :filename: biblioteca/urls.py

        from django.conf.urls import url
        from biblioteca.views import LibrosPorMes

        urlpatterns = [
            # Ejemplo: /2012/agosto/
            url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
                LibrosPorMes.as_view(),
               name="libros_mes"),
            # Ejemplo: /2012/08/
            url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',
                LibrosPorMes.as_view(month_format='%m'),
                name="libros_mes_numerico"),
        ]

    La plantilla: 'libro_archive_month.html'

    .. code-block:: html+django

        <ul>
            {% for libro in object_list %}
                <li>{{ libro.fecha_publicacion|date:"F j, Y" }}: {{ libro.titulo }}</li>
            {% endfor %}
        </ul>

        <p>
            {% if previous_month %}
                Mes anterior: {{ previous_month|date:"F Y" }}
            {% endif %}
            {% if next_month %}
                Mes siguiente: {{ next_month|date:"F Y" }}
            {% endif %}
        </p>

    **Argumentos obligatorios**

    * ``year``: El año a mostrar, en forma de cadena de texto con cuatro dígitos.

    * ``month``: El mes a mostrar, formateado de acuerdo con el argumento
      ``month_format``.

    * ``queryset``: El ``QuerySet`` de objetos archivados.

    * ``date_field``: El nombre del campo de tipo ``DateField`` o ``DateTimeField``
      en el modelo usado para el ``QuerySet`` que se usará como fecha de referencia.

    **Argumentos opcionales**

    * ``month_format``: Una cadena de texto que determina el formato que
      debe usar el parámetro ``month``. La sintaxis a usar debe coincidir
      con la de la función ``time.strftime`` (La documentación de esta
      función se puede consultar en http://www.djangoproject.com/r/python/strftime/).
      Su valor por defecto es "%b", que significa el nombre del mes, en inglés, y
      abreviado a tres letras (Es decir, "jan", "feb", etc.). Para cambiarlo de forma
      que se usen números, hay que utilizar como cadena de formato "%m".

    * ``allow_future``: Un valor booleano que indica si deben incluirse
      o no en esta vista las fechas "en el futuro", igual al que hemos
      visto en otras vistas anteriores.

    **Nombre de la plantilla**

    Si no se especifica ningún valor en ``template_name``, la vista usará como
    plantilla ``<app_label>/<model_name>_archive_month.html``.

    **Contexto de la plantilla**

    Además de los valores que se puedan haber definido en el contexto,
    la plantilla contendrá los siguientes valores:

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

Archivos semanales: ``WeekArchiveView``
---------------------------------------

.. class:: django.views.generic.dates.BaseWeekArchiveView

    Esta vista muestra todos los objetos de una semana determinada. Los objetos
    con fechas en el futuro no están incluidos, a menos  que se establezca el
    atributo ``allow_future`` en ``True``.

    **Ancestros (MRO)**

    * :class:`django.views.generic.list.MultipleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * :class:`django.views.generic.dates.BaseWeekArchiveView`
    * :class:`django.views.generic.dates.YearMixin`
    * :class:`django.views.generic.dates.WeekMixin`
    * :class:`django.views.generic.dates.BaseDateListView`
    * :class:`django.views.generic.list.MultipleObjectMixin`
    * :class:`django.views.generic.dates.DateMixin`
    * :class:`django.views.generic.base.View`

    **Contexto**

    Además del contexto ofrecido por:
    :class:`~django.views.generic.list.MultipleObjectMixin` (a través de
    :class:`~django.views.generic.dates.BaseDateListView`), el contexto de la
    plantilla contendrá:

    * ``week``: Una objeto  :class:`~datetime.date` que representa el primer
      día de la semana dada.

    * ``next_week``: Un objeto :class:`~datetime.date` que representa el primer
      día de la siguiente semana, de acuerdo al atributo
      :attr:`~BaseDateListView.allow_empty` y :attr:`~DateMixin.allow_future`.

    * ``previous_week``: Un objeto :class:`~datetime.date` que representa el
      primer día de la semana previa, de acuerdo a
      :attr:`~BaseDateListView.allow_empty` y
      :attr:`~DateMixin.allow_future`.

    **Notas**

    * Usa de forma predeterminada ``_archive_week`` como el nombre del sufijo
      de plantilla para  ``template_name_suffix``.

    .. admonition:: Nota:

        Por consistencia con las Librerías de manejo de fechas de Python, Django
        asume que el primer día de la semana es el domingo.

    **Ejemplo**

    Siguiendo con nuestro ejemplo, añadir una vista semanal a nuestra aplicación,
    no debería ser muy complicado.

    .. snippet::
     :filename: biblioteca/views.py.html

        from django.views.generic.dates import WeekArchiveView

        from biblioteca.models import Libro

        class LibrosSemanales(WeekArchiveView):
            queryset = Libro.objects.all()
            date_field = "fecha_publicacion"
            make_object_list = True
            week_format = "%W"
            allow_future = True

    .. snippet::
     :filename: biblioteca/urls.py

        from django.conf.urls import url

        from biblioteca.views import LibrosSemanales

        urlpatterns = [
            # Example: /2012/week/23/
            url(r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$',
                LibrosSemanales.as_view(),
                name="libros-semanales"),
        ]

    La plantilla 'article_archive_week.html'

    .. code-block:: html+django

        <h1>Semana {{ week|date:'W' }}</h1>

        <ul>
            {% for libros in object_list %}
                <li>{{ libros.fecha_publicacion|date:"F j, Y" }}: {{ libro.titulo }}</li>
            {% endfor %}
        </ul>

        <p>
            {% if previous_week %}
                Semana anterior: {{ previous_week|date:"F Y" }}
            {% endif %}
            {% if previous_week and next_week %}--{% endif %}
            {% if next_week %}
                Semana siguiente: {{ next_week|date:"F Y" }}
            {% endif %}
        </p>

    En este ejemplo, mostramos la salida de el número de semanas. El valor
    predeterminado  para ``week_format`` en la vista ``WeekArchiveView`` usa
    '%U' el cual está basado en el sistema de semanas manejado en los
    Estados Unidos, cuyo inicio de semana es el domingo.  El formato ISO
    usa el formato de semanas '%W', en este formato la semana comienza el
    Lunes. El formato '%W' es el mismo en ambas funciones:
    :func:`~time.strftime` y en el filtro  :tfilter:`date`.

    Sin embargo el  filtro :tfilter:`date` del el sistema de plantillas
    no tiene un equivalente, para la salida en el formato que soporta el
    sistema de semanas US. El filtro :tfilter:`date` '%U', muestra por
    salida el numero  de segundos desde la época Unix.

    **Argumentos obligatorios**

    * ``year``: El año, con cuatro dígitos (Una cadena de texto).

    * ``week``: La semana del año (Una cadena de texto).

    * ``queryset``: El ``QuerySet`` de los objetos archivados.

    * ``date_field``: El nombre del campo de tipo ``DateField`` o ``DateTimeField``
      en el modelo usado para el ``QuerySet`` que se usará como fecha de referencia.

    **Argumentos opcionales**

    * ``allow_future``: Un valor booleano que indica si deben incluirse
      o no en esta vista las fechas "en el futuro".

    **Nombre de la plantilla**

    Si no se ha especificado ningún valor en ``template_name`` la vista usará
    como plantilla  ``<app_label>/<model_name>_archive_week.html``.

    **Contexto de la plantilla**

    Además de los valores que se puedan haber definido en el contexto, la
    plantilla contendrá los siguientes valores:

    * ``week``: Un objeto de tipo ``datetime.date``, cuyo valor es el primer
      día de la semana considerada.

    * ``object_list``: Una lista de objetos disponibles para la semana
      en cuestión. El nombre de esta variable depende del parámetro
      ``template_object_name``, que es 'object' por defecto. Si
      ``template_object_name`` fuera 'foo', el nombre de esta
      variable sería ``foo_list``.

Archivos diarios: ``DayArchiveView``
------------------------------------

.. class:: django.views.generic.dates.BaseDayArchiveView

    Esta vista muestra todos los objetos para un día determinado. Los objetos
    con fechas en el futuro muestran un error 404, no importa si existen objetos
    a menos que se establezca el  atributo ``allow_future`` en ``True``.

    **Ancestros (MRO)**

    * :class:`django.views.generic.list.MultipleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * :class:`django.views.generic.dates.BaseDayArchiveView`
    * :class:`django.views.generic.dates.YearMixin`
    * :class:`django.views.generic.dates.MonthMixin`
    * :class:`django.views.generic.dates.DayMixin`
    * :class:`django.views.generic.dates.BaseDateListView`
    * :class:`django.views.generic.list.MultipleObjectMixin`
    * :class:`django.views.generic.dates.DateMixin`
    * :class:`django.views.generic.base.View`

    **Contexto**

    Además del contexto ofrecido por:
    :class:`~django.views.generic.list.MultipleObjectMixin` (a través de
    :class:`~django.views.generic.dates.BaseDateListView`), el contexto de la
    plantilla contendrá:

    * ``day``: Un objeto :class:`~datetime.date` que representa el día dado.

    * ``next_day``: Un objeto :class:`~datetime.date` object que representa el
      día siguiente, de acuerdo al :attr:`~BaseDateListView.allow_empty` y
      :attr:`~DateMixin.allow_future`.

    * ``previous_day``: Un objeto :class:`~datetime.date` que representa el día
      anterior, de acuerdo al atributo :attr:`~BaseDateListView.allow_empty` y
      :attr:`~DateMixin.allow_future`.

    * ``next_month``: Un objeto de la clase :class:`~datetime.date` que
      representa el primer día de el siguiente mes, de acuerdo al atributo
      :attr:`~BaseDateListView.allow_empty` y
      :attr:`~DateMixin.allow_future`.

    * ``previous_month``: Un objeto de la clase :class:`~datetime.date` que
      representa el primer día del mes anterior, de acuerdo al atributo
      :attr:`~BaseDateListView.allow_empty` y :attr:`~DateMixin.allow_future`.

    **Notas**

    * Usa de forma predeterminada ``_archive_day`` como el nombre del sufijo
      de plantilla para  ``template_name_suffix``.

    **Ejemplo**

    Siguiendo con nuestro ejemplo, añadir una vista diaria de objetos a nuestra
    aplicación, no debería ser más complicada que las anteriores.

    .. snippet::
     :filename: biblioteca/views.py

        from django.views.generic.dates import DayArchiveView
        from biblioteca.models import Libro

        class LibrosDiarios(DayArchiveView):
            queryset = Libro.objects.all()
            date_field = "fecha_publicacion"
            make_object_list = True
            allow_future = True

    .. snippet::
     :filename: biblioteca/biblioteca/urls.py

        from django.conf.urls import url
        from biblioteca.views import LibrosDiarios

        urlpatterns = [
            # Ejemplo: /2012/nov/10/
            url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/$',
                LibrosDiarios.as_view(),
                name="libros-día"),

    La plantilla 'biblioteca/libro_archive_day.html'

    .. code-block:: html+django

        <h1>{{ day }}</h1>

        <ul>
            {% for libros in object_list %}
                <li>{{ libros.fecha_publicacion|date:"F j, Y" }}: {{ libro.titulo }}</li>
            {% endfor %}
        </ul>

        <p>
            {% if previous_day %}
                Dia anterior: {{ previous_day }}
            {% endif %}
            {% if previous_day and next_day %}--{% endif %}
            {% if next_day %}
                Siguiente dia: {{ next_day }}
            {% endif %}
        </p>

    **Argumentos obligatorios**

    * ``year``: El año, con cuatro dígitos (Una cadena de texto).

    * ``month``: El mes, formateado de acuerdo a lo indicado por el
      argumento ``month_format``.

    * ``day``: El día, formateado de acuerdo al argumento ``day_format``.

    * ``queryset``: El ``QuerySet`` de los objetos archivados.

    * ``date_field``: El nombre del campo de tipo ``DateField`` o ``DateTimeField``
      en el modelo usado para el ``QuerySet`` que se usará como fecha de referencia.

    **Argumentos opcionales**

    * ``month_format``: Una cadena de texto que determina el formato que
      debe usar el parámetro ``month``. Hay una explicación más detallada
      en la sección de "Archivos mensuales", incluida anteriormente.

    * ``day_format``: Equivalente a ``month_format``, pero para el día. Su
      valor por defecto es ``"%d"`` (que es el día del mes como número
      decimal y relleno con ceros de ser necesario; 01-31).

    * ``allow_future``: Un valor booleano que indica si deben incluirse
      o no en esta vista las fechas "en el futuro".

    **Nombre de la plantilla**

    Si no se ha especificado ningún valor en ``template_name`` la vista usará como
    plantilla ``<app_label>/<model_name>_archive_day.html``.

    **Contexto de la plantilla**

    Además de los valores que se puedan haber definido en el contexto,  la
    plantilla tendrá los siguientes valores:

    * ``day``: Un objeto de tipo ``datetime.date`` cuyo valor es el del día en cuestión.

    * ``next_day``: Un objeto de tipo ``datetime.date`` que representa el
          siguiente día. Si cae en el futuro, valdrá ``None``.

    * ``previous_day``: Un objeto de tipo ``datetime.date`` que representa el
      día  anterior. Al contrario que ``next_day``, su valor nunca será ``None``.

    * ``object_list``: Una lista de objetos disponibles para el día  en cuestión.
      El nombre de esta variable depende del parámetro ``template_object_name``,
      que es ``object`` por defecto. Si ``template_object_name`` fuera ``foo``,
      el nombre de esta  variable sería ``foo_list``.

Archivo para hoy: ``TodayArchiveView``
--------------------------------------

.. class:: django.views.generic.dates.BaseTodayArchiveView

    Esta  vista  muestra todos los objetos cuya fecha de referencia sea *hoy*.
    Es parecida a :class:`django.views.generic.dates.DayArchiveView`, excepto
    que no se utilizan los argumentos *year/month/day*,  ya que esos datos se
    obtendrán de la fecha actual.

    **Ancestros (MRO)**

    * :class:`django.views.generic.list.MultipleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * :class:`django.views.generic.dates.BaseTodayArchiveView`
    * :class:`django.views.generic.dates.BaseDayArchiveView`
    * :class:`django.views.generic.dates.YearMixin`
    * :class:`django.views.generic.dates.MonthMixin`
    * :class:`django.views.generic.dates.DayMixin`
    * :class:`django.views.generic.dates.BaseDateListView`
    * :class:`django.views.generic.list.MultipleObjectMixin`
    * :class:`django.views.generic.dates.DateMixin`
    * :class:`django.views.generic.base.View`

    **Notas**

    * Usa de forma predeterminada ``_archive_today`` como el nombre del sufijo
      de plantilla para  ``template_name_suffix``.

    **Ejemplo**

    Siguiendo con ejemplo anterior, podemos añadir una vista para mostrar los objetos
    del día de hoy de la siguiente forma.

    .. snippet::
     :filename: biblioteca/views.py

        from django.views.generic.dates import TodayArchiveView

        from biblioteca.models import Libro

        class LibrosPublicadosHoy(TodayArchiveView):
            queryset = Libro.objects.all()
            date_field = "pub_date"
            make_object_list = True
            allow_future = True

    .. snippet::
     :filename: biblioteca/urls.py

        from django.conf.urls import url

        from myapp.views import LibrosPublicadosHoy

        urlpatterns = [
            url(r'^hoy/$',
                LibrosPublicadosHoy.as_view(),
                name="libros-publicados-hoy"),
        ]

    .. admonition:: ¿Donde está la plantilla para ``TodayArchiveView``?

        Esta vista usa de forma predeterminada la misma plantilla que la clase
        :class:`~DayArchiveView`, como en el ejemplo anterior. Si necesitas
        una plantilla diferente, establece el atributo  ``template_name`` para
        utilizar el nombre de la nueva plantilla.

Páginas de detalle basadas en fecha: ``DateDetailView``
-------------------------------------------------------

.. class:: django.views.generic.dates.BaseDateDetailView


    Esta vista se usa para representar un objeto individual. Los objetos
    con fechas en el futuro muestran un error 404, no importa si existen los
    objetos a menos que se establezca el  atributo ``allow_future`` en ``True``.

    **Ancestors (MRO)**

    * :class:`django.views.generic.detail.SingleObjectTemplateResponseMixin`
    * :class:`django.views.generic.base.TemplateResponseMixin`
    * :class:`django.views.generic.dates.BaseDateDetailView`
    * :class:`django.views.generic.dates.YearMixin`
    * :class:`django.views.generic.dates.MonthMixin`
    * :class:`django.views.generic.dates.DayMixin`
    * :class:`django.views.generic.dates.DateMixin`
    * ``django.views.generic.detail.BaseDetailView``
    * :class:`django.views.generic.detail.SingleObjectMixin`
    * :class:`django.views.generic.base.View`

    **Contexto**

    * Incluye el único objeto asociado al ``modelo`` especificado en
      ``DateDetailView``.

    **Notas**

    * Usa de forma predeterminada ``_detail`` como el nombre del sufijo
      de plantilla para  ``template_name_suffix``.

    * Esta vista tiene una URL distinta de la vista ``DetailView``; mientras
      que la última usa una URL como, por ejemplo, ``/entradas/<slug>/``, esta
      usa una URL en la forma ``/entradas/2006/aug/27/<slug>/``.

    .. admonition:: Nota:

        Si estás usando páginas de detalle basadas en fechas con *slugs* en
        la URL, lo más probable es que quieras usar la opción ``unique_for_date``
        en el campo *slug*, de forma que se garantice que los *slugs* nunca se
        duplican para una misma fecha.

    **Ejemplo**

    Esta vista tiene una (pequeña) diferencia con las demás vistas basadas en
    fechas que hemos visto anteriormente, y es que necesita que le especifiquemos
    de forma inequívoca el objeto en cuestión; esto lo podemos hacer con el
    identificador del objeto *pk* o con un campo de tipo *slug*.

    Como el objeto que estamos usando en el ejemplo no tiene ningún campo
    de tipo *slug*, usaremos el identificador para la URL. Normalmente
    se considera una buena práctica usar un campo *slug*, pero no lo
    haremos en aras de simplificar el ejemplo.

    .. snippet::
     :filename: biblioteca/urls.py

        from django.conf.urls import url
        from django.views.generic.dates import DateDetailView
        from biblioteca.models import Libro

        urlpatterns = [
            url(r'^(?P<year>[0-9]+)/(?P<month>[-\w]+)/(?P<day>[0-9]+)/(?P<pk>[0-9]+)/$',
                DateDetailView.as_view(model=Libro, date_field="fecha_publicacion"),
                name="libros-detalle-por-fecha"),
        ]

    Plantilla: 'biblioteca/libro_detail.html'

    code-block:: html+django

        <h1>{{ object.titulo }}</h1>

    **Argumentos obligatorios**

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

    **Argumentos opcionales**

    * ``allow_future``: Un valor booleano que indica si deben incluirse
      o no en esta vista las fechas "en el futuro".

    * ``day_format``: Equivalente a ``month_format``, pero para el día. Su
      valor por defecto es ``"%d"`` (que es el día del mes como número
      decimal y relleno con ceros de ser necesario; 01-31).

    * ``month_format``: Una cadena de texto que determina el formato que
      debe usar el parámetro ``month``. Hay una explicación más detallada
      en la sección de "Archivos mensuales", incluida anteriormente.

    * ``slug_field``: El  nombre del atributo que almacena el valor del
      slug*. Es obligatorio incluirlo si se ha usado el argumento ``slug``, y
      no debe aparecer si se ha especificado el argumento ``object_id``.

    * ``template_name_field``: El nombre de un atributo del objeto cuyo valor
      se usará como el nombre de la plantilla a utilizar. De esta forma, puedes
      almacenar en tu objeto la plantilla a usar.

    **Nombre de la plantilla**

    Si no se ha especificado ningún valor en ``template_name`` la vista usará
    como plantilla ``<app_label>/<model_name>_detail.html``.

    **Contexto de la plantilla**

    Además de los valores que se puedan haber definido en el contexto,  la
    plantilla contendrá los siguientes valores:

    * ``object``: El object. El nombre de esta variable depende del parámetro
      ``template_object_name``, que es ``object`` por defecto. Si ``template_object_name``
      fuera ``foo``, el nombre de esta variable sería ``foo``.

Todas las vistas genéricas basadas en clases listadas anteriormente,
corresponden y heredan de la vista ``Base``, únicamente difieren de ella en que
no incluyen la clase :class:`~django.views.generic.list.
MultipleObjectTemplateResponseMixin` (para las vistas de archivos) o
:class:`~django.views.generic.detail.SingleObjectTemplateResponseMixin`
(para la clase :class:`DateDetailView`).

