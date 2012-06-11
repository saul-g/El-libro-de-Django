=============================================================
Capítulo 17: Extender la Interfaz de Administración de Django
=============================================================

El :doc:`Capítulo 6<chapter06>` introdujo la interfaz de administración 
de Django, y ya es tiempo de volver atrás y dar una mirada más
minuciosa al asunto.

Como dijimos varias veces antes, la interfaz de administración es una de las características
más sobresalientes de este framework, y la mayoría de los desarrolladores que usan Django
lo encuentran útil y eficiente. Debido a que esta interfaz es tan popular, es comun
que los desarrolladores quieran personalizarlo o extenderlo.

Las ultimas secciones del :doc:`Capítulo 6<chapter06>` ofrecieron algunas maneras simples de personalizar
ciertos aspectos de la interfaz. Antes de continuar con este capítulo, considera revisar
ese material; cubre como personalizar las listas de cambio y los formularios de edición,
asi como una forma fácil de "remarcar" la interfaz para que se indentifique con tu
sitio.

El capitulo 6 discute también cuando y porqué querrías usar la interfaz de administración
y desde hicimos un gran salto desde esos párrafos hasta este punto, lo reproduciremos
nuevamente aquí:

Obviamente, es muy útil para modificar datos (se veía venir). Si tenemos cualquier
tipo de tarea de introducción de datos, el administrador es lo mejor que hay.
Sospechamos que la gran mayoría de lectores de este libro tiene una horda
de tareas de este tipo.

La interfaz de administración de Django brilla especialmente cuando usuarios
no técnicos necesitan ser capaces de ingresar datos; ese es el propósito detrás
de esta caracteristica, después de todo. En el periódico donde Django fue creado
orginalmente, el desarrollo de una característica tipica online --un reporte especial
sobre la calidad del agua del acueducto municipal, pongamos-- implicaba algo así:

* El periodista responsable del artículo se reune con uno de los desarrolladores
  y discuten sobre la información disponible.

* El desarrollador diseña un modelo basado en esta información y luego abre la
  interfaz de administración para el periodista.

* Mientras el periodista ingresa datos a Django, el programador puede enforcarse
  en desarrollar la interfaz accesible publicamente (¡la parte divertida!).

En otras palabras, la razón de ser de la interfaz de administración de Django es
facilitar el trabajo simultáneo de productores de contenido y programadores.

Sin embargo, más allá de estas tareas de entrada de datos obvias, encontramos
que la interfaz de administración es útil en algunos otros casos:

* *Inspeccionar modelos de datos*: La primer cosa que hacemos cuando hemos definido
  un nuevo modelo es llamarlo desde la interfaz de administración e ingresar algunos
  datos de relleno. Esto es usual para encontrar errores de modelado; tener una una
  interfaz gráfica al modelo revela problemas rápidamente.


* *Gestión de datos adquiridos*: Hay una pequeña entrada de datos asociada a un sitio
  como ``http://chicagocrime.org``, puesto que la mayoría de los datos provienen
  de una fuente automática. No obstante, cuando surgen problemas con los datos
  automáticos, es útil poder entrar y editarlos fácilmente.


La interfaz de administración de Django maneja estos casos comunes con algunas o ninguna
personalización. Aunque, como sucede con la mayoría de las generalizaciones en el diseño,
la gestión unificada de todos estos casos significa que la interfaz no maneja igual de bien
otros modos de edición.

Hablaremos de estos casos para los que la interfaz de administración de Django *no está*
diseñada un poquito más adelante, pero primero, vayamos a una breve disgreción para una
discusión filosófica.


El Zen de la aplicación Admin
=============================

En su núcleo, la interfaz de administración de Django está diseñada para una sola actividad:

    Usuarios confiables editando contenido estructurado.

Sí, es extremadamente simple -- pero esa simplicidad se basa en un montón de asunciones importantes.
La entera filosofía de la interfaz de administración de Django sigue directamente estas asunciones,
así que vamos a cavar sobre el subtexto de esta frase en las secciones que siguen.

"Usuarios confiables ..."
-------------------------

La intefaz de administración está diseñada para ser usada por usuarios en lo que tú,
el desarrollador, *confías*. Esto no significa sólo "gente que ha sido autenticada";
significa que Django asume que se puede confiar que tus editores de contenido harán
las cosas correctas.

Significa además que no hay procesos de aprobación para la edición de contenido
-- si confias en tus usuarios, nadie necesita aprobar sus ediciones. Otra
implicancia es que el sistema de permisos, aunque poderoso, no permite (al
momento en el que se escribe esto) limitar accesos basados en objetos
específicos. Si confias en que alguien edite sus propias historias, confias en
que ese usuario no edite las historias de cualquier otro sin permiso.

"... editando ..."
------------------

El propósito primario de la interfaz de administración de Django es dejar que la gente
edite información. Esto parece obvio al principio, pero de nuevo tiene poderosas y
profundas repercusiones.

Por ejemplo, aunque la interfaz es bastante útil para revisar datos (según se ha descripto),
no está diseñada con este propósito en mente. Por caso, nota la ausencia de un permiso
"puede ver" (ve el :doc:`Capítulo 12<chapter12>`). Django asume que si la gente puede ver el contenido
en la interfaz de administraión, entonces tambien tienen permito editarlo.

Otra cosa más importante es la ausencia de cualquier cosa que se aproxime
remotamente a un "flujo de trabajo". Si una tarea dada requiere una serie de
pasos, no existe algo que permita forzar a que estos pasos se realicen en un
determinado orden. La interfaz se concentra en *editar*, no en actividades
alrededor de la edición. Esta supresión de un flujo de trabajo tambien proviene
del principio de confianza: la filosofía de la interfaz es que este flujo es una
decisión personal, no algo que se pueda implementar en código.

Finalmente, nota la ausencia de agregaciones en la interfaz. Esto es, no existe
la infraestructura necesaria para mostrar totales, promedios y esas cosas. De
nuevo, la interfaz es para editar -- y se espera que escribas tus vistas
personalizadas para todo el resto.

"... contenido estructurado"
----------------------------

Como el resto de Django, la interfaz prefiere que trabajes con datos estructurados.
Esto es porque sólo sirve para editar información almacenada en modelos de Django;
para cualquier otra cosa, como datos almacenados en archivos, necesitarás vistas propias.

Parada Completa
---------------

A esta altura debería estar claro que la interfaz de administración de Django *no*
intenta ser todas las cosas para toda la gente; y en cambio, elegimos enfocarnos
en una cosa y hacerla extremadamente bien.

Cuando se va a extender la interfaz de administración, mucha de esa misma filosofía
se sostiene (nota que "extensibilidad" no figura en nuestros objetivos). Debido a que
vistas personalizadas pueden hacer *cualquier cosa*, y debido a que estas puede ser
visualmente integradas a la interfaz de administración muy facilmente (como se describe
en la siguiente sección), las posibilidades de personalización incorporadas están
un poco limitadas por diseño.

Deberías tener en mente que la interfaz de administración es "sólo una aplicación";
y aunque sea una muy compleja, no hace nada que cualquier desarrollador Django
con suficiente tiempo no podría reproducir. Es enteramente posible que en el futuro
alguien desarrolle una interfaz de adminitración diferente que esté basada en un
conjunto de asunciones distintas y que por lo tanto se comportará de otra manera.

Finalmente, debemos destacar que, a la fecha que escribimos esto, los desarrolladores
de Django trabajaban en una nueva versión de la interfaz de administración que permite
mucha más flexibilidad y personalización. Para el momento en que leas esto, esas nuevas
caracteristicas pudieron haberse incorporado a la distribución de Django oficial.
Para averiguar al respecto, preguntale a alguien de la comunidad Django si la rama
"newforms-admin" ha sido integrada.

Pesonalizar las plantillas de la interfaz
=========================================

Como sale de fábrica, Django provee un número de herramientas para personalizar
las plantillas de la interfaz que vienen integradas, las cuales veremos pronto, pero
para las tareas detrás de ellas (por ejemplo, cualquier cosa que requiera
un flujo de trabajo específico o permisos granulares), necesitarás leer la sección
titulada ":doc:`Creando vistas de administración personalizadas<chapter17>`", más adelante en este
capítulo.

Para ahora, miremos algunas maneras rápidas de modificar el aspecto (y en cierto grado,
el comportamiento) de la interfaz de administración. El :doc:`Capítulo 6<chapter06>` cubre algunas
de las tareas más comunes: "cambiar la marca" de la interfaz de administración
(para todos esos "Jefes Pelopunta" que odian el azul) y proveer un formulario de
administración personalizado.

Pasado ese punto, el objetivo usualmente implica cambiar alguna de las plantillas
para un item en particular. Cada vista de administración -- las listas de cambio,
los formularios de edición, las páginas de confirmación de eliminación y vistas de
historial -- tienen una plantilla asociada que puede ser reescrita de diferentes
maneras.

Primero, puedes reescribir la plantilla globalmente. La vista de administración
busca plantillas utilizando el mecanismo de carga de plantillas estándar, por lo
que si creas tus plantillas en alguno de los directorios declarados para tal fin,
Django cargará esas en vez de las vienen por defecto. Estas plantillas globales
se describen el la Tabla 17-1.

.. tabla:: Tabla 17-1. Plantillas globales de la interfaz de administración

===============================  ===========================================
    Vista                            Nombre de la plantilla base
===============================  ===========================================
 Lista de cambios                 ``admin/change_list.html``
 Formulario para agregar/editar   ``admin/change_form.html``
 Confirmación de eliminación      ``admin/delete_confirmation.html``
 Historial de un objeto           ``admin/object_history.html``
===============================  ===========================================

La mayoría de las veces, sin embargo, querrás cambiar la plantilla sólo para un
único objeto o aplicación (no globalmente). Así, cada vista busca primero plantillas
para modelos y aplicaciones específicas, en el siguiente orden:

    * ``admin/<app_label>/<object_name>/<template>.html``
    * ``admin/<app_label>/<template>.html``
    * ``admin/<template>.html``

Por ejemplo, la vista del formulario de agregar/editar para un modelo ``Libro`` en
la aplicación ``libros`` busca plantillas en este orden:

    * ``admin/books/book/change_form.html``
    * ``admin/books/change_form.html``
    * ``admin/change_form.html``

Plantillas de modelos propios
-----------------------------

La mayoría de las veces querrás usar la primer plantilla para crear una
basada destinada a un modelo específico. Usualmente la mejor forma de realizar
esto es extendiendo y agregando información a uno de los bloques definidos en la
plantilla que se está modificando.

Por ejemplo, supongamos que queremos agregar un pequeño texto de ayuda en la
cabecera de nuestra página de libros. Quizas algo parecido a lo que muestra la
Figura 17-1.


.. image:: graficos/chapter17/book_extra.png
   :alt: Captura de un formulario de edición de libros personalizado


Figura 17-1. Un formulario de edición de libros personalizado

Esta es una manera muy fácil de hacerlo: simplemente crea una plantilla llamada
``admin/libreria/libro/change_form.html`` e inserta este código::

    {% extends "admin/change_form.html" %}

    {% block form_top %}
      <p>Insert meaningful help message here...</p>
    {% endblock %}

Todas estas plantillas definen un número de bloques que puedes sobreescribir.
Como con la mayoría de los programas, la mejor documentación es el propio código,
por lo que te animamos a mirar las plantillas originales (que se encuentran en
``django/contrib/admin/templates/``) para trabajar con la información más actualizada.

JavaScript Personalizado
------------------------

Un uso común para estas plantillas propias para modelos implica agregar código JavaScript
extra a las páginas de la interfáz -- posiblemennte para implementar algún *widget*
especial o un comportamiento del lado del cliente.

Por suerte, esto no podría ser más fácil. Cada plantilla del administrador define
un ``{% block extrahead %}``, el cual puedes usar para incluir contenido extra dentro
del elemento ``<head>``. Por ejemplo, incluir la biblioteca jQuery (http://jquery.com/)
en tu página de historia de objetos, es tan simple como esto::

    {% extends "admin/object_history.html" %}

    {% block extrahead %}
        <script src="http://media.ejemplo.com/javascript/jquery.js" type="text/javascript"></script>
        <script type="text/javascript">

            // code to actually use jQuery here...

        </script>
    {% endblock %}


.. admonition:: Nota

    No estamos seguros porqué necesitarías jQuery en la página de historia de
    objetos, pero, por supuesto, este ejemplo es válido para cualquier plantilla
    de la interfaz de administración.

Puedes usar esta técnica para incluir cualquier tipo de controladores JavaScript
que puedas necesitar en tus formularios.

Crear vistas de administración personalizadas
=============================================

Hasta ahora, cualquiera que haya buscando agregar *comportamientos* personalizados
a la interfaz de administración probablemente esté un poco frustrado. "Todo lo que
han dicho es cómo cambiar la interfaz *visualmente*", los escuchamos llorar.
"¿Pero como puedo cambiar la forma en que la interfaz de administración *funciona*?"

La primer cosa para entender es que *esto no es mágico*. Esto es, nada de lo que
la interfaz hace es *especial* de manera alguna -- ya que se trata simplemente de
un conjunto de vistas (que se encuentran en ``django.contrib.admin.views``) que
manipulan datos como cualquier otra vista.

Seguro, hay bastante código allí, y se debe a que tienen que lidear con todas las
opciones, diferentes tipos de campos, y configuraciones que influyen en el
comportamiento. No obstante, cuando te das cuenta que la intefaz de administración
es sólo un juego de vistas, agregar las tuyas propias es más fácil de entender.

A modo de ejemplo, agreguemos una vista "reporte de editores" a nuestra aplicación
de libros del :doc:`Capítulo 6<chapter06>`. Construiremos una vista de administración que muestre
la lista de libros en función de los editores -- un ejemplo bastante típico de
vista de "reporte" que puedes necesitar construir.

Primero, actualicemos nuestro archivo URLconf. Necesitamos insertar esta línea::

    (r'^admin/books/report/$', 'mysite.books.admin_views.report'),

*antes* de la línea que incluye las vistas del administrador. Un esqueleto del
URLconf puede parecerse a algo así::

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^admin/libreria/reporte/$', 'libreria.admin_views.reporte'),
        (r'^admin/', include('django.contrib.admin.urls')),
    )

¿Por qué ponemos la vista personalizada *antes* de incluir las del administrador?
Recuerda que Django procesa los patrones de URL en orden. La inclusión de los
patrones de urls del administrador coincide con casi cualquier cosa que llega a
su punto de inclusión, por lo que si invertimos el orden de esas lineas,
Django encontrará una vista por omisión para ese patrón y no funcionará como queremos.
En este caso particular, intentará cargar un un lista de cambios para un modelo
"Reporte" en la aplicación "libros", que no existe.

Ahora escribamos nuestra vista. Para hacer honor a la simplicidad, sólo cargaremos
todos los libros dentro del contexto, y dejaremos que la plantilla maneje el
agrupamiento con la etiqueta ``{% regroup %}``. Crea un archivo ``books/admin_views.py``,
con este código::

    from mysite.books.models import Book
    from django.template import RequestContext
    from django.shortcuts import render_to_response
    from django.contrib.admin.views.decorators import staff_member_required


    def report(request):
        return render_to_response(
            "admin/books/report.html",
            {'book_list' : Book.objects.all()},
            RequestContext(request, {}),
        )
    report = staff_member_required(report)


Debido a que dejamos el agrupamiento a la plantilla, esta vista es bastante simple.
Sin embargo, hay algunos fragmentos sutiles dignos de explicitar:


* Usamos el decorador ``staff_member_required`` de ``django.contrib.admin.views.decorators``.
  Esto es similar a ``login_required`` discutido en el :doc:`Capítulo 12<chapter12>`,
  pero este decorador también verifica que el usuario esté marcado como un
  mientro del "staff", y tenga en consecuencia acceso a la interfaz de administración
  
  Este decorador protege todos las vistas predefinidas del administrador, y
  hace que la lógica de autenticación para tus vistas coincida con la del resto
  de la interfaz.

* Renderizamos una plantilla que se encuntra bajo ``admin/``. Aunque esto no
  es estrictamente requerido, se considera una buena practica para mantener todas
  tus plantillas de administración agrupadas en un directorio ``admin/``.
  También pusimos la plantilla en un directorio llamado ``books`` luego de
  nuestra aplicación -- lo que es también una buena práctica.

* Usamos ``RequestContext`` como el tercer parámetro (``context_instance``)
  para ``render_to_response``. Esto asegura que la información sobre el usuario
  en curso está disponible para la plantilla.
  
  Mira el :doc:`Capítulo 10<chapter10>` para saber más sobre ``RequestContext``.

Finalmente, haremos una plantilla para esta vista. Extenderemos una plantilla
de la administración para que lograr que nuestra vista coincida visualmente con
el resto de la interfaz:

.. code-block:: html

    {% extends "admin/base_site.html" %}

    {% block title %}List of books by publisher{% endblock %}

    {% block content %}
    <div id="content-main">
      <h1>List of books by publisher:</h1>
      {% regroup book_list|dictsort:"publisher.name" by publisher as books_by_publisher %}
      {% for publisher in books_by_publisher %}
        <h3>{{ publisher.grouper }}</h3>
        <ul>
          {% for book in publisher.list|dictsort:"title" %}
            <li>{{ book }}</li>
          {% endfor %}
        </ul>
      {% endfor %}
    </div>
    {% endblock %}

Al extender ``admin/base_site.html``, conseguimos el *look and feel* de la interfaz
de administración de Django "gratis". La Figura 17-2 muestra como luce el resultado.

.. image:: chapter17/books_by_publisher.png
   :alt: Captura de una vista personalizada "libros por editor".

Figura 17-2. Una vista personalizada "libros por editor".

Puedes usar esta técnica para agregar cualquier cosa que sueñes para la interfaz
de administración. Recuerda que las llamadas vistas de administración personalizadas
en realidad son sólo vistas comunes de Django; por lo que puedes usar todas las
técnicas aprendidas en el resto de este libro para proveer una interfaz con tanta
complejidad como necesites.

Cerraremos este capítulo con algunas ideas para vistas de administración personalizadas.

Sobreescribir vistas incorporadas
=================================

Algunas veces las vistas de administración por omisión simplemente no te sirven.
Fácilmente puedes reemplazarlas por las tuyas propias en cualquier etapa de la
interfaz de administración; simplemente haz que tu URL "haga sombra" sobre la
incorporada. Es decir, si tu vista viene antes que la vista incorporada de la
aplicación en URLconf, tu vista será invocada por sobre la de omisión.

Por ejemplo, podriamos reemplazar la vista incorporada "para crear" libros con
un formulario que permita a los usuarios ingresar simplemente un código ISBN.
Luego podriamos buscar la información del libro desde http://isbn.nu y crear el
objeto automáticamente.

El código para esa vista te lo dejamos como ejercicio, pero la parte importante
esta partecita del URLconf::

    (r'^admin/bookstore/book/add/$', 'mysite.books.admin_views.add_by_isbn'),

Si esta linea aparece antes que las URLs de administracion en tu URLconf, la
vista ``agregar_por_isbn`` reemplazará completamente a la vista estándar para ese
modelo.

Podriamos seguir un truco similar para reemplazar la página de confirmación de
eliminación, la de edición o cualquier otra parte de la interfaz.

¿Qué sigue?
===========

Si tu idioma nativo es el inglés --cosa que gracias a los traductores ya no es
necesaria para leer este libro-- quizas no te hayas enterado de una las más
fantásticas características de la interfaz de administracion: ¡está disponible en
casi 40 idiomas distintos! Esto es posible gracias al framework de
internacionalización de Django (y el duro trabajo de los traductores voluntarios
de Django). El :doc:`próximo capítulo<chapter18>` explica como usar este framework para crear
sitios Django localizados.

¡Avanti!

