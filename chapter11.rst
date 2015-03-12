=============================
Capitulo 11: Vistas Genéricas
=============================

De nuevo aparece aquí un tema recurrente en este libro: en el peor de los casos,
el desarrollo Web es aburrido y monótono. Hasta aquí, hemos cubierto cómo
Django trata de alejar parte de esa monotonía en las capas del modelo y las
plantillas, pero los desarrolladores Web también experimentan este aburrimiento
al nivel de las vistas.

Las **vistas genéricas basadas en clase** de Django fueron desarrolladas para
aliviar ese dolor. Recogen ciertos estilos y patrones comunes encontrados en
el desarrollo de vistas y los abstraen, de modo que puedas escribir rápidamente
vistas comunes de datos sin que tengas que escribir mucho código. De hecho,
casi todos los ejemplos de vistas en los capítulos precedentes pueden ser
reescritos con la ayuda de vistas genéricas, usando clases.

Él :doc:`capítulo 8<chapter08>`, se refirió brevemente a la forma de crear una
vista “genérica”. Para repasar, podemos empezar por reconocer ciertas tareas
comunes, como mostrar una lista de objetos, y escribir el código que muestra una
lista de *detalle* de cualquier objeto. Por lo tanto el modelo en cuestión
puede ser pasado como un argumento extra a la URLconf.

Django viene con vistas genéricas, basadas en clases para hacer lo siguiente:

* Realizar tareas “sencillas” y comunes: como redirigir a una página diferente y
  renderizar una plantilla dada.

* Mostrar páginas de "listado" y "detalle" para un solo objeto. Por ejemplo una
  vista para presentar una ``Lista_De_Libros`` y una para presentar el
  ``Detalle_Un_Libro``, la primera es una vista de listado, una página de objetos
  simples que muestra la lista de determinado modelo, mientras el segundo es un
  ejemplo de lo que llamamos vista  “detallada”.

* Presentar objetos basados en fechas en páginas de archivo de tipo día/mes/año,
  su detalle asociado, y las páginas “más recientes”. Los archivos por día, mes,
  año del Weblog de Django (http://www.djangoproject.com/weblog/) están
  construidos con ellas, como lo estarían los típicos archivos de un periódico.

* Permitir a los usuarios crear, actualizar y borrar objetos – con o sin
  autorización.

Agrupadas, estas vistas proveen interfaces fáciles para realizar las tareas más
comunes que encuentran los desarrolladores.

Introducción a las clases genéricas
===================================

Las vistas genéricas basadas en clases, proveen  una forma alternativa de
implementar vistas como objetos Python en lugar de funciones. No remplazan
a las funciones basadas en vista, pero poseen ciertas ventajas y diferencias
si las comparamos con las vistas basadas en funciones:

* Organizan el código relacionado en métodos específicos HTTP (GET, POST, etc)
  para que pueda ser tratado por métodos específicos en lugar de tener que tratar
  cada uno  por separado.

* Usan la técnica de orientación a objetos para crear "mixins" (herencia
  múltiple) que puede ser usado para factorizar el código en componentes
  comunes y reusables.

Como mencionamos en capítulos anteriores un vista es un llamable que toma
una petición y retorna una respuesta. Pero una vista puede ser más que una
función, Y Django provee ejemplos de algunas clases que pueden ser utilizadas
como vistas. Estas permiten estructurar  las vistas y rehusar el código
aprovechando los mixins y la herencia. Existen vistas genéricas para realizar
tareas simples, que veremos más adelante, sin embargo también sirven
para diseñar estructuras personalizables y  reutilizables que fácilmente se
pueden adaptar a la mayoría de caso de uso.

Un poco de historia
-------------------

La conexión y la historia de las vistas genéricas, vistas basadas en clase y las
vistas genéricas basadas en clases-base, puede ser un poco confusa, sobre todo
si es la primera vez que escuchas sobre ellas.

Inicialmente solo existían funciones de vista genéricas, Django pasaba la
función en una petición ``HttpRequest`` y esperaba de vuelta una respuesta
``HttpResponse``. Ese era todo el alcance que Django ofrecía.

El problema con las funciones genéricas basadas en vistas es que solo cubren
los casos simples, pero no permiten extenderlas y personalizarlas mas allá de
la simple configuración de opciones, limitando su utilidad en muchas
aplicaciones del mundo real.

Las vistas genéricas basadas en clases, fueron creadas con el mismo objetivo que
las basadas en funciones, ``hacer el desarrollo más sencillo``. Por lo que la
solución se implemento a través del uso de "mixins", que proveen un conjunto
de herramientas, que dieron como resultado que las vistas genéricas se basaran
en clases-base, para que fueran más extensibles y flexibles que su contraparte
basadas en funciones.

Si usaste las funciones genéricas para crear vistas en el pasado y las
encontraste limitadas y deficientes, *no* debes pensar que las vistas basadas en
clases son su equivalente, ya que funcionan de modo diferente, piensa más en
ellas, como un acercamiento fresco para solucionar el problema original, que la
vistas genéricas tratan de solucionar, "hacer de el desarrollo aburrido, una
tarea divertida".

El conjunto de herramientas que proveen las clases base y los "mixins" que
Django usa para crear clases basadas en vistas genéricas, nos ayudan  a
realizar los trabajos comunes con una máxima flexibilidad, para situaciones
simples y complejas.

Usando vistas basadas en clases
===============================

En su núcleo, una vista basada en una clase-base (class-based) permite responder
a  diferentes métodos de petición HTTP, con diversos métodos de la instancia de
una clase, en lugar de condicionalmente ramificar el código dentro de una simple
función de vista.

Por lo que el código para manipular HTTP en una petición ``GET``, en una
función de vista sería algo como esto::

    from django.http import HttpResponse

    def mi_vista(request):
        if request.method == 'GET':
            # <la logica de la vista>
            return HttpResponse('resultado')

Mientras que en una vista basada en una clase-base, haríamos esto::

    from django.http import HttpResponse
    from django.views.generic import View

    class MiVista(View):
        def get(self, request):
            # <la logica de la vista>
            return HttpResponse('resultado')

Debido a que el resolvedor de URL de Django espera enviar la petición y los
argumentos asociados a una función llamable no a una clase, la vistas basadas
en clases provén un método interno llamado ``as_view()``, que sirve como punto
de entrada para enlazar la clase a la URL. El punto de entrada ``as_view()``
crea una instancia de la clase y llama al método ``dispatch()``, (el despachador
o resolvedor de URL) que  busca la petición para determinar si es un GET, POST,
etc, y releva la petición a un método que coincida con uno definido, o levante
una excepción ``HttpResponseNotAllowed`` si no encuentra coincidencias.

Y así es como enlazamos la clase a la URL, usando el método ``as_view()`` ::

    # urls.py
    from django.conf.urls import url
    from myapp.views import MiVista

    urlpatterns = [
        url(r'^indice/', MiVista.as_view()),
    ]

Vale la pena observar que el  método  que devuelve es idéntico al que devuelve
una vista basada en una función, a saber una cierta forma de ``HttpResponse``.
Esto significa que los atajos para los objetos ``shortcuts`` o
``TemplateResponse`` son válidos para usar dentro de una vista basada en clases.

También vale la pena mencionar que mientras que una vista mínima basada en clases,
no requiere ningún atributos de clase para realizar su trabajo, los atributos de
una clase son útiles en muchos de los diseños de las clases-base, por lo que hay
dos maneras de configurar o de fijar los atributos de una clase.

El primero está basado en la forma estándar de Python de sobrescribir atributos
y métodos en las subclases. De modo que si una clase padre tiene un
atributo ``saludo`` tal como este::

    from django.http import HttpResponse
    from django.views.generic import View

    class VistaSaludo(View):
        saludo= "Buenos Dias"

        def get(self, request):
            return HttpResponse(self.saludo)

Puede sobrescribirse en una subclase así::

    class VistaSaludoInformal(VistaSaludo):
        saludo= "Que onda"

La segunda opción  es configurar los atributos de la clase como argumentos
clave para el método ``as_view`` de ``django.views.generic.base.View.as_view``,
llamándolos en la URLconf::

    urlpatterns = [
        url(r'^acerca/', VistaSaludo.as_view(saludo="Que tal")),
    ]

.. admonition:: Nota:

    Mientras que una clase es instanciada en cada petición enviada a ella, los
    atributos de la clase fijados a través del punto de entrada del método
    ``as_view ()`` se configuran solamente una vez; cuando se importa la URLs.

Vista Base
==========

Django proporciona varias vistas basadas en clases,  las cuales se adaptan a
una gran variedad de aplicaciones. Todas las vista heredan de la clase-base
``View`` la cual maneja las conexiones de la vista y las URLs, a través del uso
de métodos HTTP y otras características simples. Algunas de estas vistas son:
``RedirectView`` usada para simple redirecionamiento HTTP, ``TemplateView`` la
cual extiende la clases base para poder renderizar una plantilla cualqueira.

Estas tres clases: ``View``, ``TemplateView`` y ```RedirectView`` proveen muchas
de las funcionalidades  necesaria para crear vistas genéricas en Django.
Puedes pensar en ellas como si fueran vista padre o superclases, las cuales
pueden ser usadas en sí mismo o heredar de ellas. Sin embargo no puede
proveer todas las capacidades requeridas para un proyecto en general, en cuyo
caso puedes usar los mixins y las vistas basadas en clases genéricas.

Muchas de las vistas construidas sobre clases basadas en vistas heredan de
otras vistas genéricas también basadas en clases o de varios mixins. Debido a
que esta cadena de herencia es muy importante, el manejo de ancestros de una
clases se denomina (MRO). MRO por sus siglas en ingles para ``Method Resolution
Orden``, se encarga de resolver el orden que siguen los métodos en una clase.

View
-----

``View`` es la clase base maestra, las demás vistas heredan de esta clase base,
que pertenece al paquete ``class django.views.generic.base.View``.

Flujo de los métodos:

1. :meth:`dispatch()`: El resolvedor de URL´s de la vista -- es decir el método
   que valida el argumento de la petición, más los argumentos recibidos y devuelve
   la respuesta correcta HTTP.

   Por defecto es la implementación que inspecciona el método HTTP y
   tentativamente la  delega al método que coincida con la petición HTTP; por
   ejemplo una petición GET será delegado a un método get(), un POST a un post(),
   y así sucesivamente.

2. :meth:`http_method_not_allowed()`: Si la vista es  llamada con un método
   HTTP no soportado, este método es llamado en su lugar.

   La implementación por defecto retorna un ``HttpResponseNotAllowed``  con una
   lista de métodos permitidos en texto plano.

3. :meth:`options()`: Manejadores que responden a las peticiones ``OPTIONS HTTP``.
   Retorna una lista de nombres permitidos al método HTTP para la vista

Ejemplo views.py:::

    from django.http import HttpResponse
    from django.views.generic import View

    class MiVista(View):

        def get(self, request, *args, **kwargs):
            return HttpResponse('Hola, Mundo')

Ejemplo urls.py::

    from django.conf.urls import url

    from myapp.views import MiVista

    urlpatterns = [
        url(r'^hola/$', MiVista.as_view(), name='mi-vista'),
    ]

Por defecto la lista de nombres de métodos HTTP que la vista ```View`` puede
aceptar son: 'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'.

TemplateView
-------------

La clase ``TemplateView`` renderiza una plantilla dada, con el contexto que
contiene los parámetros capturados en la URL, esta clase pertenece al paquete
``class django.views.generic.base.TemplateView``

**Ancestros (MRO)**

Esta vista hereda atributos y métodos de las siguientes vistas:

* django.views.generic.base.TemplateResponseMixin
* django.views.generic.base.ContextMixin
* django.views.generic.base.View

Flujo de los métodos:

1. :meth:`~django.views.generic.base.View.dispatch()`: Valida la petición
   (ver arriba).
2. :meth:`~django.views.generic.base.View.http_method_not_allowed()`: Verifica
   los métodos soportados.
3. :meth:`~django.views.generic.base.ContextMixin.get_context_data()`: Se
   encarga de pasar el contexto (context) a la vista.

Ejemplo views.py:

.. code-block:: python

    from django.views.generic.base import TemplateView

    from biblioteca.models import Libro

    class PaginaInicio(TemplateView):

        template_name = "bienvenidos.html"

        def get_context_data(self, **kwargs):
            context = super(PaginaInicio, self).get_context_data(**kwargs)
            context['ultimos_libros'] = Libro.objects.all()[:5]
            return context

Ejemplo urls.py:

.. code-block:: python

    from django.conf.urls import url

    from biblioteca.views import PaginaInicio

    urlpatterns = [
        url(r'^$', PaginaInicio.as_view(), name='bienvenidos'),
    ]

La clase ``TemplateView`` rellena el **contexto** (a través de la clase
``django.views.generic.base.ContextMixin``) con los argumentos clave capturados
en el patrón URL, que sirve a la vista.

RedirectView
------------

La clase ``RedirectView`` tal como su nombre lo indica, simplemente redirecciona
una vista con la URL dada.

La URL dada puede contener un formato de estilo tipo diccionario, que será
intercalado contra los parámetros capturados en la URL. Ya que el intercalado
de palabras claves se hace *siempre*  (incluso si no se le pasan argumentos),
por lo que cualquier carácter como ``"%"`` (un marcador de posición en Python)
en la  URL debe ser escrito como ``%%"`` de modo que Python lo convierta en un
simple signo de porcentaje en la salida.

Si la URL dada es ``None``, Django retornara una respuesta ``HttpResponseGone`` (410).

**Ancestros (MRO)**

Esta vista hereda los métodos y los atributos de:

* :class:`django.views.generic.base.View`

Flujo de los métodos:

1. :meth:`~django.views.generic.base.View.dispatch()`
2. :meth:`~django.views.generic.base.View.http_method_not_allowed()`
3. :meth:`get_redirect_url()`: Construye el URL del objetivo para el redireccionamiento.

La implementación por defecto usa la ``url`` como la cadena de inicio
para realizar la expansión mediante el marcador de posición ``%`` en
la cadena usando el grupo de nombres capturados en la URL.

Si no se configura el atributo ``url``, mediante el método ``get_redirect_url()``
entonces Django intenta invertir el nombre del patrón, usando  los argumentos
capturados en la URL (usando los grupos con y sin nombre).

Si es una petición de un atributo ``query_string`` también se agregara a la cadena
de consulta generada por la URL.  Las subclases pueden ejecutar cualquier
comportamiento que deseen, mientras que el método devuelva una cadena de
redireccionamiento a una URL.

Los atributos de esta clase son:

.. attribute:: url

  La URL para redireccionar la vista, en formato de cadena o un valor ``None``
  para lanzar un error ``HTTP 410``.

.. attribute:: pattern_name

  El nombre de el patrón URL para redirecionar la vista. El redireccionamiento
  puede ser hecho usando los mismos ``args`` y ``kwargs`` que se pasan a las
  vistas.

.. attribute:: permanent

  Se usa solo si el redireccionamiento debe ser permanente. La única diferencia
  aquí  es el código de estado devuelto por la petición HTTP. Si  es ``True``,
  entonces el  redireccionamiento utiliza el código de estado ``301``. Si es
  ``False``, entonces el redireccionamiento utiliza el código de estado ``302``.
  Por defecto, ``permanent`` es ``True``.

.. attribute:: query_string

  Cualquier cosa que se le pase a la consulta usando el método GET a la nueva
  localización. Si es ``True``, entonces la consulta se añade al final de la URL.
  Si es ``False``, entonces la consulta se desecha. Por defecto, ``query_string``
  es ``False``.

Ejemplo views.py:

.. code-block:: python

  from django.shortcuts import get_object_or_404
  from django.views.generic.base import RedirectView

    from biblioteca.models import Libro

    class ContadorLibrosRedirectView(RedirectView):

        permanent = False
        query_string = True
        pattern_name = 'detalle-libro'

        def get_redirect_url(self, *args, **kwargs):
            libro = get_object_or_404(Libro, pk=kwargs['pk'])
            libro.update_counter()
            return super(ContadorLibrosRedirectView, self).get_redirect_url(*args, **kwargs)

Ejemplos urls.py:
::

  from django.conf.urls import url
  from django.views.generic.base import RedirectView

  from biblioteca.views import ContadorLibrosRedirectView, DetalleLibro

  urlpatterns = [
      url(r'^contador/(?P<pk>[0-9]+)/$', ContadorLibrosRedirectView.as_view(), name='contador-libros'),
      url(r'^detalles/(?P<pk>[0-9]+)/$', DetalleLibro.as_view(), name='detalles-libro'),
      url(r'^ir-a-django/$', RedirectView.as_view(url='http://djangoproject.com'), name='ir-a-django'),
  ]

Vistas genéricas basadas en clases usando URLconfs
--------------------------------------------------

La manera más simple de utilizar las vistas genéricas es creándolas directamente
en la URLconf. Si únicamente quieres cambiar algunos atributos en una vista
basada en clases-base, puedes simplemente pasarle los atributos que quieres
sobrescribir dentro del método ``as_view``, ya que este es un llamable en si
mismo.

Por ejemplo, ésta es una URLconf simple que podrías usar para presentar una
página estática "acerca de", usando una vista genérica creada con una
clase-base:::

    from django.conf.urls import url
    from django.views.generic import TemplateView

    urlpatterns = [
        url(r'^acerca/', TemplateView.as_view(template_name="acerca_de.html")),
    ]

Cualquier argumento pasado al método ``as_view`` sobrescribirá los atributos
fijados en la clase. En este ejemplo, hemos configurado el nombre de la plantilla
con la variable ``template_name`` en la URLconf, de la vista ``TemplateView``.
Un patrón similar se puede utilizar para sobrescribir atributos en la clase
``RedirectView``.

Aunque esto podría parecer un poco “mágico” a primera vista, en realidad solo
estamos usando la clase ``TemplateView``, la cual renderiza una plantilla dada,
con el contexto dado,  sobrescribiendo el nombre de la plantilla y los atributos
predefinidos en la clase base ``TemplateView``.

Vistas genéricas basadas en clases usando subclases
---------------------------------------------------

La segunda forma más poderosa de usar las vistas genéricas es hacer que estas
hereden de una vista  sobrescribiendo sus atributos (tal como el nombre de la
plantilla) o sus métodos (como ``get_context_data`` ) en una subclase que
proporcione nuevos valores o métodos. Considera por ejemplo una vista que
muestre una plantilla ``acerca_de.html``.  Django posee una vista genérica que
hace este trabajo, como lo vimos en el ejemplo anterior -- ``TemplateView`` solo
es necesario crear una subclase que  sobrescriba el nombre de la plantilla así:

.. snippet:: python
    :filename: biblioteca/views.py

    from django.views.generic import TemplateView

    class VistaAcercaDe(TemplateView):
        template_name = "acerca_de.html"

Después lo único que necesitamos es agregar la nueva vista al URLConf. La clase
``TemplateView`` no es una función, así que apuntamos la URL usando un  método
interno ``as_view()`` de la clase en su lugar, el cual provee una entrada como
si fuera una función a la vista basada en una clases-base.

.. snippet:: python
    :filename: biblioteca/urls.py

    from django.conf.urls import url
    from aplicacion.views import AboutView

    urlpatterns = [
        url(r'^acerca/', VistaAcercaDe.as_view()),
    ]

Cualquier argumento pasado al método ``as_view()`` sobrescribira los definidos
en la clase recién creada.

Vistas genéricas de objetos
===========================

La vista genérica ``TemplateView`` ciertamente es útil, pero las vistas
genéricas de Django brillan realmente cuando se trata de presentar vistas del
contenido de tu base de datos. Ya que es una tarea tan común, Django viene con
un puñado de vistas genéricas incluidas que hacen la generación de vistas de
listado y detalle de objetos increíblemente fácil.

Comenzaremos observado algunos ejemplos basicos, sobre como mostrar una lista
de objetos usando la vista generica basada en clases llamada ``ListView`` y
como mostrar objetos de forma individual, usando la clase generica ``DetailView``.

Usaremos el modelo Editor creado en capítulos anteriores:

.. snippet:: python
    :filename: biblioteca/models.py

    from django.db import models

    class Editor(models.Model):
        nombre = models.CharField(max_length=30)
        domicilio = models.CharField(max_length=50)
        ciudad = models.CharField(max_length=60)
        estado = models.CharField(max_length=30)
        pais = models.CharField(max_length=50)
        website = models.URLField()

        class Meta:
            ordering = ["nombre"]
            verbose_name_plural = 'editores'

        def __str__(self):            # __unicode__ en Python 2
            return self.nombre

Primero definimos una vista, para crear una lista de editores, usando una clase
genérica llamada ``ListView``:

.. snippet:: python
    :filename: biblioteca/views.py

    from django.views.generic import ListView
    from biblioteca.models import Editor

    class ListaEditores(ListView):
        model = Editor

Como puedes ver la clase ``ListView`` pertenece a la clase ``django.views.generic.list.ListView``
la cual se encarga de presentar un listado de todos los objetos de un modelo,
piensa en ``ListView`` como una consulta del tipo ``Editor.objets.all().``
Cuando esta vista es ejecutada llama al método ``self.object_list`` el
cual contiene una lista de objetos(usualmente, pero no necesariamente un
``queryset``)

Después importamos la vista y la enlazamos directamente a la urls, usando el
método ``as_view()``, es como decirle a Django: esta clase es una vista:

.. snippet:: python
    :filename: biblioteca/urls.py

    from django.conf.urls import url
    from biblioteca.views import ListaEditores

    urlpatterns = [
        url(r'^editores/$', ListaEditores.as_view()),
    ]

Ese es todo el código Python que necesitamos escribir, para presentar un listado
de objetos de un modelo. Sin embargo, todavía necesitamos escribir una plantilla.
Podríamos decirle explícitamente a la vista que plantilla debe usar incluyendo
un atributo ``template_name``, pero en la ausencia de una plantilla explícita
Django inferirá una del nombre del objeto. En este caso, la plantilla inferida
será ``"biblioteca/editorlist.html"`` – la parte “biblioteca” proviene del
nombre de la aplicación que define el modelo, mientras que la parte “editor” es
sólo la versión en minúsculas del nombre del modelo.

.. admonition:: Nota

    Así, cuando (por ejemplo) la clase ``django.template.loaders.app_directories.Loader``
    esta activada en el archivo de configuración,  en la variable
    ``TEMPLATE_LOADERS`` el directorio predeterminado donde Django buscara, las
    plantillas será: en /ruta/a/proyecto/biblioteca/templates/biblioteca/editorlist.html

    Django por omisión busca un directorio con el nombre de la aplicación dentro
    del directorio de plantillas llamado ```templates``.


Esta plantilla será renderizada con un contexto que contiene una variable
llamada ``object_list`` la cual contiene todos los objetos editor del modelo.

Una plantilla muy simple podría verse de la siguiente manera:

.. snippet:: html+django
    :filename: libros/templates/editorlist.html

    {% extends "base.html" %}

    {% block content %}
        <h2>Editores</h2>
        <ul>
            {% for editores in object_list %}
                <li>{{ editores.nombre }}</li>
            {% endfor %}
        </ul>
    {% endblock %}

(Observa que esta plantilla asume que existe una plantilla base ``base.html``,
de la cual hereda,  tal y como vimos en los ejemplos del :doc:`capítulo 4<chapter04>`)

Ciertamente obtener una lista de objetos con la clase genérica ``ListView`` es
siempre muy útil, pero que pasa si queremos mostrar un solo objeto, por ejemplo
los detalles de un determinado editor, en ese caso usamos la vista genérica
``DetailView``, que se encarga de presentar los ``detalles`` de un objeto,
ejecutando ``self.object`` el cual  contendrá el objeto sobre el que la vista
está operando.

Por ejemplo si quisiéramos mostrar un editor en particular, usaríamos la clase:
``DetailView``, de esta manera::

    from django.views.generic.detail import DetailView

    from biblioteca.models import Editor

    class DetalleEditores(DetailView):
        model = Editor

AL igual que con la vista anterior, solo necesitamos importar y enlazar la vista
a su respectiva URL así::

    from django.conf.urls import url

    from biblioteca.views import DetalleEditores

    urlpatterns = [
        url(r'^detalle/editores/(?P<pk>[0-9]+)/$', DetalleEditores.as_view(),
            name='detalles-editores' ),

    ]

Y por ultimo creamos la plantilla con el nombre por defecto que le asigna Django
que es ``editor_detail.html``:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
      <h2>editor.nombre</h2>
        <ul>
          <li>Domicilio: {{ editor.domicilio }}</li>
          <li>Ciudad: {{ editor.ciudad }}</li>
          <li>Estado: {{ editor.estado }}</li>
          <li>Pais: {{ editor.pais }}</li>
          <li>Sitio web: {{ editor.website }}</li>
       </ul>
    {% endblock %}

``ListView`` y ``DetailView`` son las dos vistas basadas en clases genéricas que
probablemente se usen mas en el diseño de proyectos.

Eso es realmente todo en lo referente al tema. Todas las geniales
características de las vistas genéricas provienen de cambiar los atributos
fijados en la vista genérica.  El Apéndice C documenta todas las vistas
genéricas y todas sus opciones en detalle; el resto de este capítulo
considerará algunas de las maneras más comunes en que puedes personalizar y
extender las vistas genéricas basadas en clases base.

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

Crear contextos de plantilla “amistosos”
----------------------------------------

Tal vez hayas notado que el ejemplo de la plantilla editores almacena la lista
de todos los editores en una variable llamada ``object_list``. Aunque esto
funciona bien, no es una forma “amistosa” para los autores de plantillas: ellos
sólo tienen que “saber” que están trabajando con una lista de editores.

Bien, si estas tratando con un objeto de un modelo,  el trabajo está hecho.
Cuando estas tratando con un objeto o queryset, Django es capaz de rellenar
el contexto usando el nombre de la clase en minúsculas de un modelo. Esto es
provisto además de la entrada predeterminada ``object_list``, pero
conteniendo exactamente los mismos datos, por ejemplo ``lista_editores``.

Si el nombre no es una buena idea, puedes manualmente cambiarlo en el contexto
de la variable. El atributo ``context_object_name`` en una vista genérica
especifica el contexto de las variables a usar:

.. snippet:: python
    :filename: biblioteca/views.py

    from django.views.generic import ListView
    from biblioteca.models import Editor

    class ListaEditores(ListView):
        model = Editor
        context_object_name = 'lista_editores'

Proporcionar útiles nombres de contexto (``context_object_name``) es siempre
una buena idea. Tus compañeros de trabajo que diseñan las plantillas te lo
agradecerán.

Agregar un contexto extra
-------------------------

A menudo simplemente necesitas presentar alguna información extra aparte de la
proporcionada por la vista genérica. Por ejemplo, piensa en mostrar una lista
de todos los libros en cada una de las páginas de detalle de un editor.

La vista genérica  ``DetailView``, que pertenece a la clase
``django.views.generic.detail.DetailView``  provee el contexto a editores,
¿Pero cómo obtener información adicional en la plantilla?

La respuesta está en la misma clase ``DetailView``, que provee su propia
implementación de el método ``get_context_data``, la implementación por
defecto simplemente agrega un objeto para mostrar en la plantilla, pero
puede sobrescribirse aun mas::

    from django.views.generic import DetailView
    from biblioteca.models import Editor, Libro

    class DetallesEditor(DetailView):

        model = Editor
        context_object_name = 'lista_editores'

        def get_context_data(self, **kwargs):
            # Llama primero a la implementación para traer un contexto
            context = super(DetallesEditor, self).get_context_data(**kwargs)
            # Agrega un QuerySet para obtener todos los libros
            context['lista_libros'] = Libro.objects.all()
            return context

.. admonition:: Nota

    Por lo general ``get_context_data`` combina los datos del contexto de
    todas las clases padres con los de la clase actual. Para conservar este
    comportamiento en las clases donde se quiera alterar el comportamiento del
    contexto, asegúrate de llamar a ``get_context_data`` en la súper clase.
    Cuando ninguna de las dos clases trate de definir la misma clave, esto
    dará los resultados esperados. Sin embargo si cualquiera de las clases
    trata de sobrescribir la clave después de que la clase padre la ha fijado
    (después de llamar a súper) cualquiera de las clases hija necesitara
    explícitamente fijarla y asegurarse de sobrescribir todas las clases padres.
    Si tienes problemas, revisa el orden de resolución del método de una vista.

Vista para subconjuntos de objetos
----------------------------------

Ahora echemos un vistazo más de cerca al argumento  ``model`` que hemos venido
usando hasta aquí.  El argumento ``model`` especifica el modelo de la base de
datos que usara la vista genérica, la mayoría de las vistas genéricas usan uno de
estos argumentos para operar sobre un simple objeto o una colección de objetos.
Sin embargo  El argumento ``model`` no es la única forma de especificar los
objetos que se mostraran en la vista, puedes especificar una lista de objetos
usando como argumentos  un ``queryset`` ::

    from django.views.generic import DetailView
    from biblioteca.models import Editor

    class DetallesEditor(DetailView):

        context_object_name = 'editores'
        queryset = Editor.objects.all()

Especificando ``model = Editor`` es realmente un atajo para decir:
``queryset = Editor.objects.all()``. Sin embargo, usando un ``queryset``
puedes filtrar una lista de objetos y puedes especificar los objetos que quieres
que se muestren en la vista.

Para escoger un ejemplo simple, puede ser que quieras ordenar una lista de
libros por fecha de publicación, con los libros más reciente al inicio::

    from django.views.generic import ListView
    from biblioteca.models import Libro

    class LibrosRecientes(ListView):
        queryset = Libro.objects.order_by('-fecha_publicacion')
        context_object_name = 'libros_recientes'

Este es un ejemplo bastante simple, pero ilustra bien la idea. Por supuesto,
tú usualmente querrás hacer más que sólo reordenar objetos. Si quieres presentar
una lista de libros de un editor en particular, puedes usar la misma técnica::

    from django.views.generic import ListView
    from biblioteca.models import Libro

    class LibroAcme(ListView):

        context_object_name = 'lista_libros_acme'
        queryset = Libro.objects.filter(editor__nombre='Editores Acme')
        template_name = 'biblioteca/lista_libros_acme.html'

Nota que además de filtrar un ``queryset``, también estamos usando un nombre de
plantilla personalizado. Si no lo hiciéramos, la vista genérica usaría la misma
plantilla que la lista de objetos “genérica” [4], que puede no ser lo que
queremos.

También observa que ésta no es una forma muy elegante de hacer una lista
de editores-específicos de libros.  Si queremos agregar otra página de editores,
necesitamos otro puñado de líneas en la URLconf, y más de unos cuantos editores
no será razonable. Enfrentaremos este problema en la siguiente sección.

.. admonition:: Nota

    Si obtienes un error 404 cuando solicitas /libros/acme/, para estar seguro,
    verifica que en realidad tienes un Editor con el nombre 'Editores Acme'.
    Las vistas genéricas proveen un parámetro extra ``allow_empty`` para estos
    casos. Mira el Apéndice D para mayores detalles.

Filtrado Dinámico
-----------------

Otra necesidad muy común es filtrar los objetos que se muestran en una página
de listado por alguna clave en la URLconf. Anteriormente codificamos [5] el nombre
de los editores en la URLconf, pero ¿qué pasa si queremos escribir una vista
que muestre todos los libros por algún editor arbitrario?.

Podemos “usar” la vista genérica ``ListView`` que posee un método ``get_queryset``
que pertenece a la clase ``django.views.generic.list.MultipleObjectMixin.get_queryset``
el cual sobrescribimos anteriormente, el cual retornaba el valor del  atributo
``queryset``, pero ahora le agregaremos más lógica.

La parte crucial para hacer este trabajo está en llamar a las vistas basadas en
clases-base, ya que guardan algunas cosa útiles con ``self``; tal como
la petición (``self.request``) esta incluye la posición (``self.args``) el
nombre base (``self.kwargs``) los argumentos capturados acorde a la URLconf.

Esta es la URLconf con un único grupo capturado:

.. snippet:: python
   :filename: biblioteca/urls.py

    from django.conf.urls import url
    from biblioteca.views import ListaDeEditores

    urlpatterns = [
        url(r'^libros/([\w-]+)/$', ListaDeEditores.as_view()),
    ]

A continuación, actualizamos la vista ``ListaDeEditores`` anterior:

.. snippet:: python
   :filename: biblioteca/views.py

    from django.shortcuts import get_object_or_404
    from django.views.generic import ListView
    from biblioteca.models import Libro, Editor

    class ListaDeEditores(ListView):

        template_name = 'biblioteca/lista_de_editores.html'

        def get_queryset(self):
            self.editor = get_object_or_404(Editor, nombre=self.args[0])
            return Libro.objects.filter(editor=self.editor)

Como puedes ver, es sencillo agregar más lógica a la selección del queryset; si
quieres, puedes usar  ``self.request.user`` para filtrar usando el usuario
actual  o realizar otra  lógica más compleja.

También puedes agregar un editor dentro del contexto, así puedes utilizarlos en
la plantilla al mismo tiempo::

        # ...

        def get_context_data(self, **kwargs):
            # Llama primero a la implementación para traer el contexto
            context = super(ListaDeEditores, self).get_context_data(**kwargs)
            # Se agregan  los editores
            context['editores'] =self.editor
            return context

Realizar trabajo extra
----------------------

El último patrón común que veremos involucra realizar algún trabajo extra antes
o después de llamar a la vista genérica.

Imagina que tenemos un campo ``ultimo_acceso`` en nuestro modelo ``Autor``
que usamos para tener un registro de la última vez que alguien vio
ese autor.

.. snippet:: python
    :filename: biblioteca/models.py

    from django.db import models

    class Autor(models.Model):
        nombre = models.CharField(max_length=30)
        apellidos = models.CharField(max_length=40)
        email = models.EmailField(blank=True, verbose_name='e-mail')
        ultimo_acceso = models.DateTimeField()

La vista genérica basada en la clase ``DetailView``, por supuesto, no sabría
nada sobre este campo, pero una vez más, fácilmente podríamos escribir una
vista personalizada para mantener ese campo actualizado.

Primero, necesitamos agregar una pequeña parte de detalle sobre el autor en la
URLconf para que apunte a una vista personalizada:::

    from django.conf.urls import url
    from biblioteca.views import VistaDetallesAutor

    urlpatterns = [
        #...
        url(r'^autores/(?P<pk>[0-9]+)/$', VistaDetallesAutor.as_view(), name='detalles-autor'),
    ]

.. admonition:: Nota:

    La URLconf aquí usa un nombre de grupo ``pk`` -- este nombre, es el nombre
    predeterminado que ``DetailView`` usa para encontrar el valor de una clave
    primaria que se usa para filtrar el queryset (que no es mas que la clave
    primaria o ``primary key``.)

    Si quieres llamar esta vista con otro nombre de grupo, puedes fijarlo a
    ``pk_url_kwarg`` en la vista.

Después  escribimos la vista -- ``get_object``  es un método que recupera un
objeto, simplemente sobreescribe y envuelve la llamada.::

    from django.views.generic import DetailView
    from django.utils import timezone
    from biblioteca.models import Autor

    class VistaDetallesAutor(DetailView):

        queryset = Autor.objects.all()

        def get_object(self):
            # LLama a la superclase
            objeto = super(VistaDetallesAutor, self).get_object()
            # Graba el último dato de acceso
            objeto.ultimo_acceso = timezone.now()
            objeto.save()
            # Retorna el objeto
            return objeto

Introducción a los mixins
=========================

Los ``mixins`` son una forma de herencia múltiple, donde los comportamientos y
los atributos de múltiples clases padre, pueden ser combinados en una única clase .

Por ejemplo en las vistas genéricas basadas en clases existe un mixin llamado
``TemplateResponseMixin `` cuyo propósito central es definir el método
``render_to_response()``. Cuando se combina con el comportamiento de la clase
base ```View``, el resultado es una clase ``TemplateView``  que enviara
peticiones a los métodos que coincidan con la petición del patrón (un
comportamiento definido en la clase base ```View``) en el método
``render_to_response()`` y que utiliza un atributo como el nombre de una
plantilla para retornar un objeto mediante ``TemplateResponse``
(un comportamiento definido en el mixin ``TemplateResponseMixin``.)

Los mixins son una excelente manera de reutilizar el código a través de
múltiples clases, pero vienen con un cierto costo. Cuanto más los utilizas mas
se dispersa el código, lo que dificulta leer lo que hace exactamente una clase
hija y  complica aún más saber qué métodos remplazan los ``mixins`` si es que
estas usando la herencia en subclases con una cierta profundidad.

Observa también que puedes heredar solamente de una vista genérica - es decir,
sólo una clase padre puede heredar de una vista y el resto (eventualmente)
deben ser mixins. Si intentas heredar de más de una clase que herede de ```View``
-- por ejemplo, tratando de usar una formulario  en la cima de una lista y
combinándola con ``ProcessFormView`` y ``ListView`` -- no trabajará según lo
esperado.

Usando un mixin y una vistas genérica
-------------------------------------

Veamos ahora como usar un simple mixin llamado ``SingleObjectMixin`` que se
encarga de recuperar un solo objeto, con  una vista genérica ``ListView`` que
como vimos anteriormente presenta una lista de objetos de un determinado
modelo.

La vista genérica ``ListView`` ofrece paginación incorporada, para la lista
de objetos de un modelo, usando el atributo ``paginate_by``, pero a lo mejor
lo que quieres paginar es una lista de objetos que están enlazados (por una
clave foránea por ejemplo) a otro objeto. En el modelo ``Editor`` que vimos
anteriormente, para paginar una lista de libros por un editor en especifico,
podríamos hacerlo de la siguiente forma.

Combinando una vista ``ListView`` con un mixin ``SingleObjectMixin``, a fin de
que el ``queryset`` para la lista paginada de libros cuelgue de un simple objeto
editor. Para hacer esto necesitamos primero obtener dos querysets diferentes:

Libro: queryset para usar en ``ListView``

    Puesto que tenemos acceso a la lista de libros de un editor que queremos
    listar, podemos simplemente  sobrescribir el método ``get_queryset ()`` y utilizar
    el manejador para usar los editores del campo foráneo Libro en relación inversa.

Editores: un queryset para usar con get_object()

   Confiaremos en la implementación predeterminada del método ``get_object()``
   para traer el objeto correcto ``Editor``. Sin embargo, necesitamos
   explícitamente pasarle un argumento al queryset porque de otra manera la
   implementación predeterminada de ``get_object()`` llamara al método
   ``get_queryset()``  el cual sobrescribirá los objetos Libro devueltos en
   lugar de el Editor.

.. admonition:: Nota

  Pensemos cuidadosamente acerca de ``get_context_data ()``. Ya que
  ``SingleObjectMixin`` y ``ListView`` pueden poner cosas en los datos del
  contexto bajo el valor de ``context_object_name`` si se configuran,  en lugar
  de eso nos aseguraremos explícitamente que ``Editor`` este en los datos del
  contexto. La vista ``ListView`` agregará convenientemente ``page_obj`` y
  ``paginator`` para usar en la paginación por nosotros, siempre que recordemos
  llamar a la superclase().

Con esto en mente, ahora podemos escribir la vista:

.. code-block:: python

    from django.views.generic import ListView
    from django.views.generic.detail import SingleObjectMixin
    from biblioteca.models import Editor

    class DetalleEditores(SingleObjectMixin, ListView):
        paginate_by = 2
        template_name = "biblioteca/detalles_editores.html"

        def get(self, request, *args, **kwargs):
            self.object = self.get_object(queryset=Editor.objects.all())
            return super(DetalleEditores, self).get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            context = super(DetalleEditores, self).get_context_data(**kwargs)
            context['editor'] = self.object
            return context

        def get_queryset(self):
            return self.object.libro_set.all()

Fíjate cómo colocamos ``self.object`` dentro del método ``get()``  para usarlo
más adelante dentro del método  ``get_context_data()`` y obtener un ``get_queryset()``.
Si no usamos el atributo ``template_name`` para configurar el nombre de la
plantilla, Django usara el valor por defecto para ``ListView`` la cual en este
caso es "biblioteca/libro_list.html" porque es una lista de libros; ``ListView``
no sabe nada acerca de el mixin ``SingleObjectMixin``, así que no tiene ninguna
pista sobre que esta vista es una lista de libros de acuerdo a un editor
predeterminado.

Observa que el atributo ``paginate_by`` es deliberadamente pequeño en este
ejemplo, para que no tengas que crear un buen lote de libros para ver en
funcionamiento la paginación.

Esta es la plantilla que usa:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}
        <h2>Editor {{ editor.nombre }}</h2>

        <ol>
          {% for libro in page_obj %}
            <li>{{ libro.titulo }}</li>
          {% endfor %}
        </ol>

        <div class="pagination">
            <span class="step-links">
                {% if page_obj.has_previous %}
                    <a href="?page={{ page_obj.previous_page_number }}">anterior</a>
                {% endif %}

                <span class="current">
                    Pagina {{ page_obj.number }} de {{ paginator.num_pages }}.
                </span>

                {% if page_obj.has_next %}
                    <a href="?page={{ page_obj.next_page_number }}">siguiente</a>
                {% endif %}
            </span>
        </div>
    {% endblock %}

El uso de mixins y vistas genéricas es una buena forma de extender las vistas
basadas en clases, en el ejemplo anterior observamos en acción un simple mixins
llamado ``SingleObjectMixin``  que se encarga de traer un objeto, sin embargo
Django cuenta con una conveniente cantidad de mixins repartidos en las siguientes
categorías:

* Simple mixins
* Single object mixins
* Multiple object mixins
* Editing mixins
* Date-based mixins

Envolviendo el método as_view() con mixins
------------------------------------------

Una forma de aplicar un comportamiento común a muchas clases es escribir un
``mixin`` que envuelva el método ``as_view ()``.

Por ejemplo, si tienes muchas vistas genéricas que necesites decorar con un
método ``login_required ()``  lo podrías implementar usando un mixin como este:::

    from django.contrib.auth.decorators import login_required

    class RequiereLogin(object):
        @classmethod
        def as_view(cls, **initkwargs):
            vista = super(RequiereLogin, cls).as_view(**initkwargs)
            return login_required(vista)

    class MiVista(RequiereLogin, ...):
        # Esta es la vista genérica
        ...

Manejando formularios con vistas basadas en clases genéricas
-------------------------------------------------------------

Una vista basada en una función que maneja un formulario, luce así::

    from django.http import HttpResponseRedirect
    from django.shortcuts import render

    from .forms import MyForm

    def mivista(request):
        if request.method == "POST":
            form = MyForm(request.POST)
            if form.is_valid():
                # <proceso el formulario con cleaned data>
                return HttpResponseRedirect('/success/')
        else:
            form = MyForm(initial={'key': 'value'})

        return render(request, 'formulario.html', {'form': form})

De igual forma una vista basada en una clase base, se ve así::

    from django.http import HttpResponseRedirect
    from django.shortcuts import render
    from django.views.generic import View

    from .forms import MyForm

    class MiFormulario(View):
        form_class = MyForm
        initial = {'key': 'value'}
        template_name = 'formulario.html'

        def get(self, request, *args, **kwargs):
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})

        def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)
            if form.is_valid():
                # <proceso el formulario con cleaned data>
                return HttpResponseRedirect('/success/')

            return render(request, self.template_name, {'form': form})

Como puedes observar, este es un caso muy simple del uso de clases genéricas
para el manejo de formularios, pero te darás cuenta enseguida de las ventajas
de usar este enfoque basado en clases, ya que tendrías la opción de modificar
esta vista para requisitos particulares, personalizando y sobrescribiendo los
atributos de la vista, por ejemplo ``form_class``,``template_name`` a través
de la configuración de la URLconf, o de una subclase y también podrías
reemplazar uno o más métodos (¡o todos!).

Ejemplo de un formulario y una clase genérica
---------------------------------------------

Como se menciona anteriormente las vistas genéricas de Django brillan realmente
cuando se necesitan presentar datos, sin embargo tambien brillan cuando es
necesario guardar  y procesar datos mediante formularios Web.

Al trabajar con modelos  podemos crear automáticamente formularios a partir de
un modelo, usando vistas genericas basadas en clases.

Esta es la forma en que las puedes utilizar:

* Si se da el atributo de un modelo, ese modelo de clase será utilizada.
* Si ``get_object ()`` devuelve un objeto, la clase de ese objeto será utilizada.
* Si se da un ``queryset``, el modelo para ese queryset será utilizado.

Las vistas para los modelos de un formulario  proveen un método ``form_valid``
que  sobrescribe el modelo automáticamente. Puedes reemplazar esto si necesitas
algún requisito en especial.

No necesitas proveer un método ``success_url`` para una vista tipo ``CreateView``
o ``UpdateView`` ya que usan el método ``get_absolute_url()`` de el modelo, si
este está disponible.

Si quieres usar un  formulario personalizado con la clase ```ModelForm`` (como
una instancia para agregar validación) simplemente fija el valor ``form_class``
en la vista.

.. admonition:: Nota

    Cuando especifiques una clase de un formulario personalizada, todavía debemos
    especificar el modelo, aunque ``form_class`` sea una clase de  ``ModelForm``

Para ver las clase genéricas en acción, lo primero que necesitamos es agregar
un método ``get_absolute_url()`` a la clase ``Autor`` del modelo, para así
usarlo como redirecionamiento por defecto:

.. snippet:: python
    :filename: biblioteca/models.py

    from django.db import models
    from django.core.urlresolvers import reverse

    class Autor(models.Model):
        nombre = models.CharField(max_length=30)
        # Omitimos los demas campos y métodos.

        def get_absolute_url(self):
            return reverse('detalles-autor', kwargs={'pk': self.pk})

Ahora podemos llamar a la clase ``CreateView`` y a sus amigos para que hagan el
trabajo duro. Observa que lo único que necesitamos es configurar las vistas
genéricas basadas en clases-base aquí; no tenemos que escribir ninguna lógica
nosotros mismos:

.. snippet:: python
    :filename: biblioteca/views.py

    from django.views.generic.edit import CreateView, UpdateView, DeleteView
    from django.core.urlresolvers import reverse_lazy
    from biblioteca.models import Autor

    class CrearAutor(CreateView):
        model = Autor
        fields = ['nombre', 'apellidos', 'email',]

    class ActualizarAutor(UpdateView):
        model = Autor
        fields = ['nombre', 'apellidos', 'email',]

    class BorrarAutor(DeleteView):
        model = Autor
        success_url = reverse_lazy('lista-autor')

.. admonition:: Nota

    Observa que usamos el método ``reverse_lazy()`` en la ultima clase, el cual
    es útil para cuando se necesita utilizar una url inversa, antes de que se
    cargue la URLConf de el proyecto.

El atributo ``fields`` trabaja de la misma forma que un atributo ``fields`` en
una clase interna Meta dentro de una clase ``ModelForm``. A menos que definas un
formulario de otra forma el atributo es requerido y la vista lanzara una excepción
``ImproperlyConfigured`` si no lo encuentra.

Finalmente enlazamos las nuevas vistas basadas en clases para Crear, Actualizar
y Borrar objetos, (``CRUD`` por sus siglas en ingles: Create, Update y Delete)
en la URLconf:

.. snippet:: python
    :filename: biblioteca/urls.py

    from django.conf.urls import url
    from biblioteca.views import CrearAutor, ActualizarAutor, BorrarAutor

    urlpatterns = [
      # ...
      url(r'autor/agregar/$', CrearAutor.as_view(), name='agregar-autor'),
      url(r'autor/(?P<pk>[0-9]+)/$', ActualizarAutor.as_view(), name='actualizar-autor'),
      url(r'autor/(?P<pk>[0-9]+)/borrar/$', BorrarAutor.as_view(), name='borrar-autor'),
    ]

Esta vistas heredan del mixin ``SingleObjectTemplateResponseMixin`` el cual
usa el método ``template_name_suffix`` para construir el nombre de la plantilla
con el atributo ``template_name`` basado en el nombre del modelo.

En este ejemplo:

* ``CreateView`` y ``UpdateView`` usan la misma plantilla: "biblioteca/autor_form.html"
* ``DeleteView`` usa la plantilla "biblioteca/autor_confirm_delete.html"

Si quieres especificar nombres diferentes para cada plantilla de la clase
``CreateView`` y ``UpdateView``, puedes configurarlos mediante el atributo
``template_name`` como en cualquier vista basada en clases.

.. Como crear un CRUD con Django

Decorando vistas de una clase-base
==================================

La extensión de  vistas basadas en clases  no se limita a usar solamente mixins.
También puedes utilizar decoradores. Puesto que las vistas basadas en clases
no son funciones, necesitas  decorarlas de forma diferente dependiendo de si
estás utilizando el método ``as_view`` o está creando una subclase.

Decorando una URLconf
---------------------

La forma más simple de decorar una vista basada en una clase, es decorar el
resultado de el método ``as_view()``. El lugar más sencillo para hacer esto es
en la URLconf donde se despliega la vista:

.. code-block:: python

    from django.contrib.auth.decorators import login_required, permission_required
    from django.views.generic import TemplateView

    from .views import VoteView

    urlpatterns = [
        url(r'^acerca/', login_required(TemplateView.as_view(template_name="acerca.html"))),
        url(r'^votar/', permission_required('libros.votar')(VistaVotar.as_view())),
    ]

Esta aproximación aplica únicamente a decoradores por-instancia. Si quieres que
cada instancia de una vista sea decorada, necesitas usar un acercamiento
diferente

Decorando una clase
-------------------

Para decorar cada instancia de una vista basada en clases, necesitas decorar la
definición de la clase misma. Para hacer esto aplica el decorador a el método
``dispatch()`` de la clase.

Un método sobre una clase no equivale realmente a una función independiente,
así que solo puedes aplicar un decorador a un método de una función –- por lo
que necesitas transformarlo en un decorador primero. El decorador ``@method_decorator``
transforma un decorador de una función en un decorador de un método a fin de
que puede ser usado sobre una instancia de un método. Por ejemplo:

.. code-block:: python

    from django.contrib.auth.decorators import login_required
    from django.utils.decorators import method_decorator
    from django.views.generic import TemplateView

    class Vista Protegida(TemplateView):
        template_name = 'secret.html'

        @method_decorator(login_required)
        def dispatch(self, *args, **kwargs):
            return super(Vista Protegida, self).dispatch(*args, **kwargs)

En este ejemplo, cada instancia de Vista Protegida, tendrá protección de login.

.. admonition:: Nota:

    El ``method_decorator`` pasa  ``*args``  y ``**kwargs`` como parámetros
    al método del decorador de la clase.  Si el método no valida el conjunto
    de parámetros compatibles levantará una excepción del tipo ``TypeError``.


Soporte para Apis
-----------------

Supongamos que alguien acceder a nuestra librería de libros sobre HTTP, usando
la vista como una API. La API del cliente se conectaría de vez en cuando y
descargaría la lista de libros publicados desde su última visita. Pero
si no se ha publicado ningún libro desde la última vez, sería una pérdida de
CPU y de ancho de banda obtener los libros de la base de datos, renderizar
una respuesta completa y enviársela al cliente. No sería preferible preguntarle
a la API  cuales son los libros recientemente publicados.

Mapeamos la URL a la lista de libros en la URLconf:

.. code-block:: python

    from django.conf.urls import url
    from biblioteca.views import ListaLibros

    urlpatterns = [
        url(r'^libros/$', VistaLibrosRecientes.as_view()),
    ]

Y creamos la clase-base para la vista:

.. code-block:: python

    from django.http import HttpResponse
    from django.views.generic import ListView
    from biblioteca.models import Libro

    class VistaLibrosRecientes(ListView):
        model = Libro
        template_name = 'lista_libros.html'

        def head(self, *args, **kwargs):
            ultimos_libros = self.get_queryset().latest('fecha_publicacion')
            response = HttpResponse('')
            # Formato de datos RFC 1123
            response['modificados'] = ultimos_libros.fecha_publicacion.strftime('%a, %d %b %Y
                %H:%M:%S GMT')
            return response

Si la vista es accesada por una petición  ``GET`` una simple lista de objetos
será devuelta como respuesta (usando  la plantilla "lista_libros.html")
Pero si el cliente nos envía una petición HEAD, la respuesta tendrá un cuerpo
vacio  y la cabecera de la última modificación indicara los libros que se
publicaron recientemente. Basados en esta información, el cliente puede o no
descargar la lista completa de objetos.

¿Qué sigue?
===========

En este capítulo hemos examinado sólo un par de las vistas genéricas que
incluye Django, pero las ideas generales presentadas aquí deberían aplicarse a
cualquier vista genérica basada en clases-base. El Apéndice C cubre todas las
vistas disponibles en detalle, y es de lectura obligada si quieres sacar el
mayor provecho de esta poderosa característica.

Aquí concluye la sección del libro dedicada al "uso avanzado de Django". En el
:doc:`proximo capítulo<chapter12>` cubriremos el despliegue de aplicaciones
en Django.

