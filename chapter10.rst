==============================================
Capítulo 10: Extender el sistema de plantillas
==============================================

Aunque la mayor parte de tu interacción con el sistema de plantillas
(*templates*) de Django será en el rol de autor, probablemente quieras algunas
veces modificar y extender el sistema de plantillas -- así sea para agregar
funcionalidad, o para hacer tu trabajo más fácil de alguna otra manera.

Este capítulo se adentra en el sistema de plantillas de Django, cubriendo todo
lo que necesitas saber, ya sea por si planeas extender el sistema, o por si sólo
eres curioso acerca de su funcionamiento.

Si estás tratando de utilizar el sistema de plantillas de Django como parte de
otra aplicación, es decir, sin el resto del framework, lee la sección
"`Configurando el Sistema de plantillas en modo autónomo`_" luego en este mismo
capítulo.

Revisión del lenguaje de plantillas
===================================

Primero, vamos a recordar algunos términos presentados en el :doc:`Capítulo 4<chapter04>`:

    * Una *plantilla* es un documento de texto, o un string normal de Python
      marcado con la sintaxis especial del lenguaje de plantillas de Django.
      Una plantilla puede contener etiquetas de bloque (*block tags*) y
      variables.

    * Una *etiqueta de bloque* es un símbolo dentro de una plantilla que hace
      algo. Esta definición es así de vaga a propósito. Por ejemplo, una
      etiqueta de bloque puede producir contenido, servir como estructura de
      control (una sentencia ``if`` o un loop ``for``), obtener contenido de la
      base de datos, o habilitar acceso a otras etiquetas de plantilla.

      Las etiquetas de bloque deben ser rodeadas por ``{%`` y ``%}``::
        
          {% if is_logged_in %}
            Thanks for logging in!
          {% else %}
            Please log in.
          {% endif %}

    * Una *variable* es un símbolo dentro de una plantilla que emite un valor.

      Las etiquetas de variable deben ser rodeadas por ``{{`` y ``}}``::

          My first name is {{ first_name }}. My last name is {{ last_name }}.

    * Un *contexto* es un mapeo entre nombres y valores (similar a un diccionario
      de Python) que es pasado a una plantilla.

    * Una plantilla *renderiza* un contexto reemplazando los "huecos" que dejan
      las variables por valores tomados del contexto y ejecutando todas las
      etiquetes de bloque.

Para más detalles acerca de estos términos, referirse al :doc:`Capítulo 4<chapter04>`.

El resto de este capítulo discute las distintas maneras de extender el sistema
de plantillas. Aunque primero, debemos dar una mirada a algunos conceptos
internos que quedaron fuera del :doc:`Capítulo 4<chapter04>` por simplicidad.

Procesadores de contexto
========================

Cuando una plantilla debe ser renderizada, necesita un contexto. Usualmente este
contexto es una instancia de ``django.template.Context``, pero Django también
provee una subclase especial: ``django.template.RequestContext`` que actúa de
una manera levemente diferente. ``RequestContext`` agrega muchas variables al
contexto de nuestra plantilla -- cosas como el objeto ``HttpRequest`` o
información acerca del usuario que está siendo usado actualmente.

Usa ``RequestContext`` cuando no quieras especificar el mismo conjunto de
variables una y otra vez en una serie de plantillas. Por ejemplo, considera
estas cuatro vistas::

    from django.template import loader, Context

    def view_1(request):
        # ...
        t = loader.get_template('template1.html')
        c = Context({
            'app': 'My app',
            'user': request.user,
            'ip_address': request.META['REMOTE_ADDR'],
            'message': 'I am view 1.'
        })
        return t.render(c)

    def view_2(request):
        # ...
        t = loader.get_template('template2.html')
        c = Context({
            'app': 'My app',
            'user': request.user,
            'ip_address': request.META['REMOTE_ADDR'],
            'message': 'I am the second view.'
        })
        return t.render(c)

    def view_3(request):
    # ...
        t = loader.get_template('template3.html')
        c = Context({
            'app': 'My app',
            'user': request.user,
            'ip_address': request.META['REMOTE_ADDR'],
            'message': 'I am the third view.'
        })
        return t.render(c)

    def view_4(request):
        # ...
        t = loader.get_template('template4.html')
        c = Context({
            'app': 'My app',
            'user': request.user,
            'ip_address': request.META['REMOTE_ADDR'],
            'message': 'I am the fourth view.'
        })
        return t.render(c)

A propósito *no* hemos usado el atajo ``render_to_response`` en
estos ejemplos -- manualmente cargamos las plantillas, construimos el contexto y
renderizamos las plantillas. Simplemente por claridad, estamos demostrando todos
los pasos necesarios.

Cada vista pasa las mismas tres variables -- ``app``, ``user`` y ``ip_address``
-- a su plantilla. ¿No sería bueno poder eliminar esa redundancia?

``RequestContext`` y los **procesadores de contexto** fueron creado para
resolver este problema. Los procesadores de contexto te permiten especificar un
número de variables que son incluidas automáticamente en cada contexto --
sin la necesidad de tener que hacerlo manualmente en cada llamada a
``render_to_response()``. El secreto está en utilizar ``RequestContext`` en
lugar de ``Context`` cuando renderizamos una plantilla.

La forma de nivel más bajo de usar procesadores de contexto es crear algunos de
ellos y pasarlos a ``RequestContext``. A continuación mostramos como el ejemplo
anterior puede lograrse utilizando procesadores de contexto::

    from django.template import loader, RequestContext

    def custom_proc(request):
        "A context processor that provides 'app', 'user' and 'ip_address'."
        return {
            'app': 'My app',
            'user': request.user,
            'ip_address': request.META['REMOTE_ADDR']
        }

    def view_1(request):
        # ...
        t = loader.get_template('template1.html')
        c = RequestContext(request, {'message': 'I am view 1.'},
                processors=[custom_proc])
        return t.render(c)

    def view_2(request):
        # ...
        t = loader.get_template('template2.html')
        c = RequestContext(request, {'message': 'I am the second view.'},
                processors=[custom_proc])
        return t.render(c)

    def view_3(request):
        # ...
        t = loader.get_template('template3.html')
        c = RequestContext(request, {'message': 'I am the third view.'},
                processors=[custom_proc])
        return t.render(c)

    def view_4(request):
        # ...
        t = loader.get_template('template4.html')
        c = RequestContext(request, {'message': 'I am the fourth view.'},
                processors=[custom_proc])
        return t.render(c)

Inspeccionemos paso a paso este código:

    * Primero, definimos una función ``custom_proc``. Este es un procesador de
      contexto -- toma un objeto ``HttpRequest`` y devuelve un diccionario con
      variables a usar en el contexto de la plantilla. Eso es todo lo que hace.

    * Hemos cambiado las cuatro vistas para que usen ``RequestContext``
      en lugar de ``Context``. Hay dos diferencias en cuanto a cómo el
      contexto es construido. Uno, ``RequestContext`` requiere que
      el primer argumento sea una instancia de ``HttpRequest`` -- la cual fue
      pasada a la vista en primer lugar (``request``). Dos, ``RequestContext``
      recibe un parámetro opcional ``processors``, el cual es una lista o
      tupla de funciones procesadoras de contexto a utilizar. En este caso,
      pasamos ``custom_proc``, nuestro procesador de contexto definido
      previamente.

    * Ya no es necesario en cada vista incluir ``app``, ``user`` o
      ``ip_address`` cuando construimos el contexto, ya que ahora estas
      variables son provistas por ``custom_proc``.

    * Cada vista *aún* posee la flexibilidad como para introducir una o más
      variables en el contexto de la plantilla si es necesario. En este
      ejemplo, la variable de plantilla ``message`` es creada de manera
      diferente en cada una de las vistas.

En el :doc:`Capítulo 4<chapter04>`, presentamos el atajo ``render_to_response()``, el cual nos
ahorra tener que llamar a ``loader.get_template()``, luego crear un ``Context``
y ademas, llamar al método ``render()`` en la plantilla. Para demostrar el
funcionamiento a bajo nivel de los procesadores de contexto, en los ejemplos
anteriores no hemos utilizado ``render_to_response()``, pero es posible -- y
preferible -- utilizar los procesadores de contexto junto a
``render_to_response()``. Esto lo logramos mediante el argumento
``context_instance`` de la siguiente manera::

    from django.shortcuts import render_to_response
    from django.template import RequestContext

    def custom_proc(request):
        "A context processor that provides 'app', 'user' and 'ip_address'."
        return {
            'app': 'My app',
            'user': request.user,
            'ip_address': request.META['REMOTE_ADDR']
        }

    def view_1(request):
        # ...
        return render_to_response('template1.html',
            {'message': 'I am view 1.'},
            context_instance=RequestContext(request, processors=[custom_proc]))

    def view_2(request):
        # ...
        return render_to_response('template2.html',
            {'message': 'I am the second view.'},
            context_instance=RequestContext(request, processors=[custom_proc]))

    def view_3(request):
        # ...
        return render_to_response('template3.html',
            {'message': 'I am the third view.'},
            context_instance=RequestContext(request, processors=[custom_proc]))

    def view_4(request):
        # ...
        return render_to_response('template4.html',
            {'message': 'I am the fourth view.'},
            context_instance=RequestContext(request, processors=[custom_proc]))

Aquí, hemos logrado reducir el código para renderizar las plantillas en
cada vista a una sola línea.

Esto es una mejora, pero, evaluando la concisión de este código, debemos
admitir que hemos logrado reducir la redundancia en los datos
(nuestras variables de plantilla), pero aun así, estamos especificando una
y otra vez nuestro contexto. Es decir, hasta ahora usar procesadores de
contexto no nos ahorra mucho código si tenemos que escribir ``processors``
constantemente.

Por esta razón, Django admite el uso de procesadores de contexto *globales*. El
parámetro de configuración ``TEMPLATE_CONTEXT_PROCESSORS`` designa cuales serán
los procesadores de contexto que deberán ser aplicados *siempre* a
``RequestContext``. Esto elimina la necesidad de especificar ``processors`` cada
vez que utilizamos ``RequestContext``.

``TEMPLATE_CONTEXT_PROCESSORS`` tiene, por omisión, el siguiente valor::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
    )

Este parámetro de configuración es una tupla de funciones que utilizan la
misma interfaz que nuestra función ``custom_proc`` utilizada previamente --
funciones que toman un objeto ``HttpRequest`` como primer argumento, y
devuelven un diccionario de items que serán incluidos en el contexto de la
plantilla. Ten en cuenta que los valores en ``TEMPLATE_CONTEXT_PROCESSORS``
son especificados como *strings*, lo cual significa que estos procesadores
deberán estar en algún lugar dentro de tu ``PYTHONPATH`` (para poder referirse
a ellos desde el archivo de configuración)

Estos procesadores de contexto son aplicados en orden, es decir, si uno de
estos procesadores añade una variable al contexto y un segundo procesador
añade otra variable con el mismo nombre, entonces la segunda sobre-escribirá
a la primera.

Django provee un numero de procesadores de contexto simples, entre ellos los que
están activos por defecto.

django.core.context_processors.auth
-----------------------------------

Si ``TEMPLATE_CONTEXT_PROCESSORS`` contiene este procesador, cada
``RequestContext`` contendrá las siguientes variables:

    * ``user``: Una instancia de ``django.contrib.auth.models.User``
      representando al usuario actualmente autenticado (o una instancia de
      ``AnonymousUser`` si el cliente no se ha autenticado aún).

    * ``messages``: Una lista de mensajes (como *string*) para el usuario
      actualmente autenticado. Detrás del telón, esta variable llama a
      ``request.user.get_and_delete_messages()`` para cada *request*. Este
      método colecta los mensajes del usuario, y luego los borra de la base de
      datos.

    * ``perms``: Instancia de ``django.core.context_processors.PermWrapper``,
      la cual representa los permisos que posee el usuario actualmente
      autenticado.

En el :doc:`Capítulo 12<chapter12>` encontrarás más información acerca de usuarios, permisos
y mensajes.

django.core.context_processors.debug
------------------------------------

Este procesador añade información de depuración a la capa de plantillas.
Si ``TEMPLATE_CONTEXT_PROCESSORS`` contiene este procesador, cada
``RequestContext`` contendrá las siguientes variables:

    * ``debug``: El valor del parámetro de configuración ``DEBUG`` (``True`` o
      ``False``). Esta variable puede usarse en las plantillas para saber si
      estás en modo de depuración o no.

    * ``sql_queries``: Una lista de diccionarios ``{'sql': ..., 'time': ...}``
      representando todas las consultas SQL que se generaron durante la petición
      (*request*) y cuánto duraron. La lista está ordenada respecto a cuándo fue
      ejecutada cada consulta.

Como la información de depuración es sensible, este procesador de contexto
sólo agregará las variables al contexto si las dos siguientes condiciones
son verdaderas.

    * El parámetro de configuración ``DEBUG`` es True

    * La solicitud (*request*) viene de una dirección IP listada en el parámetro
      de configuración ``INTERNAL_IPS``.

django.core.context_processors.i18n
-----------------------------------

Si este procesador está habilitado, cada ``RequestContext`` contendrá las
siguientes variables:

    * ``LANGUAGES``: El valor del parámetro de configuración ``LANGUAGES``.

    * ``LANGUAGE_CODE``: ``request.LANGUAGE_CODE`` si existe; de lo contrario,
      el valor del parámetro de configuración ``LANGUAGE_CODE``.

En el Apéndice E se especifica más información sobre estos parámetros.

django.core.context_processors.request
--------------------------------------

Si este procesador está habilitado, cada ``RequestContext`` contendrá una
variable ``request``, la cual es el actual objeto ``HttpRequest``. Este
procesador no está habilitado por defecto.

Consideraciones para escribir tus propios procesadores de contexto
------------------------------------------------------------------

Algunos puntos a tener en cuenta:

    * Cada procesador de contexto debe ser responsable por la mínima cantidad de
      funcionalidad posible. Usar muchos procesadores es algo sencillo, es por
      eso que dividir la funcionalidad de tu procesador de manera lógica puede
      ser útil para poder reutilizarlos en el futuro.

    * Ten presente que cualquier procesador de contexto en
      ``TEMPLATE_CONTEXT_PROCESSORS`` estará disponible en *cada* plantilla cuya
      configuración esté dictada por ese archivo de configuración, así que trata
      de seleccionar nombres de variables con pocas probabilidades de entrar en
      conflicto con nombre de variables que tus plantillas pudieran usar en
      forma independiente. Como los nombres de variables son sensibles a
      mayúsculas/minúsculas no es una mala idea usar mayúsculas para las
      variables provistas por un procesador.

    * No importa dónde residan en el sistema de archivos, mientras se hallen en
      tu ruta de Python de manera que puedas incluirlos en tu variable de
      configuración ``TEMPLATE_CONTEXT_PROCESSORS``. Habiendo dicho eso, diremos
      también que la convención es grabarlos en un archivo llamado
      ``context_processors.py`` ubicado en tu aplicación o en tu proyecto.

Detalles internos de la carga de plantillas
===========================================

En general las plantillas se almacenan en archivos en el sistema de archivos,
pero puedes usar cargadores de plantillas personalizados (*custom*) para cargar
plantillas desde otros orígenes.

Django tiene dos maneras de cargar plantillas:

    * ``django.template.loader.get_template(template)``: ``get_template``
      retorna la plantilla compilada (un objeto ``Template``) para la plantilla
      con el nombre provisto. Si la plantilla no existe, se generará una
      excepción ``TemplateDoesNotExist``.

    * ``django.template.loader.select_template(template_name_list)``:
      ``select_template`` es similar a ``get-template``, excepto que recibe una
      lista de nombres de plantillas. Retorna la primera plantilla de dicha
      lista que existe. Si ninguna de las plantillas existe se lanzará una
      excepción ``TemplateDoesNotExist``.

Como se vio en el :doc:`Capítulo 4<chapter04>`, cada una de esas funciones usan por omisión el
valor de tu variable de configuración ``TEMPLATE_DIRS`` para cargar las
plantillas. Sin embargo, internamente las mismas delegan la tarea pesada a un
cargador de plantillas.

Algunos de los cargadores están, por omisión, desactivados pero puedes
activarlos editando la variable de configuración ``TEMPLATE_LOADERS``.
``TEMPLATE_LOADERS`` debe ser una tupla de cadenas, donde cada cadena representa
un cargador de plantillas. Estos son los cargadores de plantillas incluidos con
Django:

    * ``django.template.loaders.filesystem.load_template_source``: Este cargador
      carga plantillas desde el sistema de archivos, de acuerdo a
      ``TEMPLATE_DIRS``. Por omisión está activo.

    * ``django.template.loaders.app_directories.load_template_source``: Este
      cargador carga plantillas desde aplicaciones Django en el sistema de
      archivos. Para cada aplicación en ``INSTALLED_APPS``, el cargador busca un
      sub-directorio ``templates``. Si el directorio existe, Django buscará una
      plantilla en el mismo.

      Esto significa que puedes almacenar plantillas en tus aplicaciones
      individuales, facilitando la distribución de aplicaciones Django con
      plantillas por omisión. Por ejemplo si ``INSTALLED_APPS`` contiene
      ``('myproject.polls', 'myproject.music')`` entonces
      ``get_template('foo.html')`` buscará plantillas en el siguiente orden:

            * ``/path/to/myproject/polls/templates/foo.html``
            * ``/path/to/myproject/music/templates/foo.html``

      Notar que el cargador realiza una optimización cuando es importado por
      primera vez: hace caching de una lista de cuales de los paquetes en
      ``INSTALLED_APPS`` tienen un sub-directorio ``templates``.

      Por omisión este cargador está activo.

    * ``django.template.loaders.eggs.load_template_source``: Este cargador es
      básicamente idéntico a ``app_directories``, excepto que carga las
      plantillas desde eggs Python en lugar de hacerlo desde el sistema de
      archivos. Por omisión este cargador está desactivado; necesitarás
      activarlo si estás usando eggs para distribuir tu aplicación.

Django usa los cargadores de plantillas en el orden en el que aparecen en la
variable de configuración ``TEMPLATE_DIRS``. Usará cada uno de los cargadores
hasta que uno de los mismos tenga éxito en la búsqueda de la plantilla.

Extender el sistema de plantillas
=================================

Ahora que entiendes un poco más acerca del funcionamiento interno del sistema de
plantillas, echemos una mirada a cómo extender el sistema con código
propio.

La mayor parte de la personalización de plantillas se da en forma de etiquetas
y/o filtros. Aunque el lenguaje de plantillas de Django incluye muchos,
probablemente ensamblarás tus propias bibliotecas de etiquetas y filtros que se
adapten a tus propias necesidades. Afortunadamente, es muy fácil definir tu
propia funcionalidad.

Crear una biblioteca para plantillas
------------------------------------

Ya sea que estés escribiendo etiquetas o filtros personalizados, la primera
tarea a realizar es crear una **biblioteca para plantillas** -- un pequeño
fragmento de infraestructura con el cual Django puede interactuar.

La creación de una biblioteca para plantillas es un proceso de dos pasos:

    * Primero, decidir qué aplicación Django alojará la biblioteca. Si has
      creado una aplicación vía ``manage.py startapp`` puedes colocarla allí, o
      puedes crear otra aplicación con el solo fin de alojar la biblioteca.

      Sin importar cual de las dos rutas tomes, asegúrate de agregar la
      aplicación a tu variable de configuración ``INSTALLED_APPS``.
      Explicaremos esto un poco más adelante.

    * Segundo, crear un directorio ``templatetags`` en el paquete de aplicación
      Django apropiado. Debe encontrarse en el mismo nivel que ``models.py``,
      ``views.py``, etc. Por ejemplo::

          books/
              __init__.py
              models.py
              templatetags/
              views.py

      Crea dos archivos vacíos en el directorio ``templatetags``: un archivo
      ``__init__.py`` (para indicarle a Python que se trata de un paquete que
      contiene código Python) y un archivo que contendrá tus definiciones
      personalizadas de etiquetas/filtros. El nombre del segundo archivo es el
      que usarás para cargar las etiquetas más tarde. Por ejemplo, si tus
      etiquetas/filtros personalizadas están en un archivo llamado
      ``poll_extras.py``, entonces deberás escribir lo siguiente en una
      plantilla::

          {% load poll_extras %}

      La etiqueta ``{% load %}`` examina tu variable de configuración
      ``INSTALLED_APPS`` y sólo permite la carga de bibliotecas para plantillas
      desde aplicaciones Django que estén instaladas. Se trata de una
      característica de seguridad; te permite tener en cierto equipo el código
      Python de varias bibliotecas para plantillas sin tener que activar el
      acceso a todas ellas para cada instalación de Django.

Si escribes una biblioteca para plantillas que no se encuentra atada a ningún
modelo/vista particular es válido y normal el tener un paquete de aplicación
Django que sólo contiene un paquete ``templatetags``. No existen límites en lo
referente a cuántos módulos puedes poner en el paquete ``templatetags``. Sólo
ten presente que una sentencia ``{% load %}`` cargará etiquetas/filtros para el
nombre del módulo Python provisto, no el nombre de la aplicación.

Una vez que has creado ese módulo Python, sólo tendrás que escribir un poquito
de código Python, dependiendo de si estás escribiendo filtros o etiquetas.

Para ser una biblioteca de etiquetas válida, el módulo debe contener una
variable a nivel del módulo llamada ``register`` que sea una instancia de
``template.Library``. Esta instancia de ``template.Library`` es la estructura de
datos en la cual son registradas todas las etiquetas y filtros. Así que inserta
en la zona superior de tu módulo, lo siguiente::

    from django import template

    register = template.Library()

.. admonition::

    Para ver un buen número de ejemplos, examina el código fuente de los filtros
    y etiquetas incluidos con Django. Puedes encontrarlos en
    ``django/template/defaultfilters.py`` y ``django/template/defaulttags.py``,
    respectivamente. Algunas aplicaciones en ``django.contrib`` también
    contienen bibliotecas para plantillas.

Una vez que hayas creado esta variable ``register``, usarás la misma para crear
filtros y etiquetas para plantillas.

Escribir filtros de plantilla personalizados
--------------------------------------------

Los filtros personalizados son sólo funciones Python que reciben uno o dos
argumentos:

    * El valor de la variable (entrada)

    * El valor del argumento, el cual puede tener un valor por omisión o puede
      ser obviado.

Por ejemplo, en el filtro ``{{ var|foo:"bar" }}`` el filtro ``foo`` recibiría el
contenido de la variable  ``var`` y el argumento ``"bar"``.

Las funciones filtro deben siempre retornar algo. No deben arrojar excepciones,
y deben fallar silenciosamente. Si existe un error, las mismas deben retornar la
entrada original o una cadena vacía, dependiendo de qué sea más apropiado.

Esta es un ejemplo de definición de un filtro::

    def cut(value, arg):
        "Removes all values of arg from the given string"
        return value.replace(arg, '')

Y este es un ejemplo de cómo se usaría::

    {{ somevariable|cut:"0" }}

La mayoría de los filtros no reciben argumentos. En ese caso, basta con que
no incluyas el argumento en tu función::

    def lower(value): # Only one argument.
        "Converts a string into all lowercase"
        return value.lower()

Una vez que has escrito tu definición de filtro, necesitas registrarlo en tu
instancia de ``Library``, para que esté disponible para el lenguaje de
plantillas de Django::

    register.filter('cut', cut)
    register.filter('lower', lower)

El método  ``Library.filter()`` tiene dos argumentos:

    * El nombre del filtro (una cadena)

    * La función filtro propiamente dicha

Si estás usando Python 2.4 o más reciente, puedes usar ``register.filter()``
como un decorador::

    @register.filter(name='cut')
    def cut(value, arg):
        return value.replace(arg, '')

    @register.filter
    def lower(value):
        return value.lower()

Si no provees el argumento ``name``, como en el segundo ejemplo, Django usará el
nombre de la función como nombre del filtro.

Veamos entonces el ejemplo completo de una biblioteca para plantillas, que
provee el filtro ``cut``::

    from django import template

    register = template.Library()

    @register.filter(name='cut')
    def cut(value, arg):
        return value.replace(arg, '')

Escribir etiquetas de plantilla personalizadas
----------------------------------------------

Las etiquetas son más complejas que los filtros porque las etiquetas pueden
implementar prácticamente cualquier funcionalidad.

El :doc:`Capítulo 4<chapter04>` describe cómo el sistema de plantillas funciona como un proceso de
dos etapas: compilación y renderizado. Para definir una etiqueta de plantilla
personalizada, necesitas indicarle a Django cómo manejar ambas etapas cuando
llega a tu etiqueta.

Cuando Django compila una plantilla, divide el texto crudo de la plantilla en
*nodos*. Cada nodo es una instancia de ``django.template.Node`` y tiene un
método ``render()``. Por lo tanto, una plantilla compilada es simplemente una
lista de objetos ``Node``.

Cuando llamas a ``render()`` en una plantilla compilada, la plantilla llama a
``render()`` en cada ``Node()`` de su lista de nodos, con el contexto
proporcionado. Los resultados son todos concatenados juntos para formar la
salida de la plantilla. Por ende, para definir una etiqueta de plantilla
personalizada debes especificar cómo se debe convertir la etiqueta en crudo en
un ``Node`` (la función de compilación) y qué hace el método ``render()`` del
nodo.

En las secciones que siguen, explicaremos todos los pasos necesarios para
escribir una etiqueta propia.

Escribir la función de compilación
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para cada etiqueta de plantilla que encuentra, el intérprete (*parser*) de
plantillas llama a una función de Python pasándole el contenido de la etiqueta y
el objeto parser en sí mismo. Esta función tiene la responsabilidad de retornar
una instancia de ``Node`` basada en el contenido de la etiqueta.

Por ejemplo, escribamos una etiqueta ``{% current_time %}`` que visualice la
fecha/hora actuales con un formato determinado por un parámetro pasado a la
etiqueta, usando la sintaxis de ``strftime`` (ver
``http://www.djangoproject.com/r/python/strftime/``). Es una buena idea definir
la sintaxis de la etiqueta previamente. En nuestro caso, supongamos que la
etiqueta deberá ser usada de la siguiente manera::

    <p>The time is {% current_time "%Y-%m-%d %I:%M %p" %}.</p>

.. admonition::

    Si, esta etiqueta de plantilla es redundante -- La etiqueta ``{% now %}``
    incluida en Django por defecto hace exactamente lo mismo con una sintaxis
    más simple. Sólo mostramos esta etiqueta a modo de ejemplo.


Para evaluar esta función, se deberá obtener el parámetro y crear el objeto
``Node``::

    from django import template

    def do_current_time(parser, token):
        try:
            # split_contents() knows not to split quoted strings.
            tag_name, format_string = token.split_contents()
        except ValueError:
            msg = '%r tag requires a single argument' % token.split_contents()[0]
            raise template.TemplateSyntaxError(msg)
        return CurrentTimeNode(format_string[1:-1])

Hay muchas cosas en juego aquí:

    * ``parser`` es la instancia del *parser*. No lo necesitamos
      en este ejemplo.

    * ``token.contents`` es un *string* con los contenidos crudos de la
      etiqueta, en nuestro ejemplo sería: ``'current_time "%Y-%m-%d %I:%M
      %p"'``.

    * El método ``token.split_contents()`` separa los argumentos en sus
      espacios, mientras deja unidas a los *strings*. Evite utilizar
      ``token.contents.split()`` (el cual usa la semántica natural de Python
      para dividir *strings*, y por esto no es tan robusto, ya que divide en
      todos los espacios, incluyendo aquellos dentro de cadenas entre comillas.

    * Esta función es la responsable de generar la excepción
      ``django.template.TemplateSyntaxError`` con mensajes útiles, ante
      cualquier caso de error de sintaxis.

    * No escribas el nombre de la etiqueta en el mensaje de error, ya que eso
      acoplaría innecesariamente el nombre de la etiqueta a la función. En
      cambio, ``token.split_contents()[0]`` siempre contendrá el nombre de tu
      etiqueta -- aún cuando la etiqueta no lleve argumentos.

    * La función devuelve ``CurrentTimeNode`` (el cual mostraremos en
      un momento) conteniendo todo lo que el nodo necesita saber sobre esta
      etiqueta. En este caso, sólo pasa el argumento ``"%Y-%m-%d %I:%M %p"``.
      Las comillas son removidas con ``format_string[1:-1]``.

    * Las funciones de compilación de etiquetas de plantilla *deben* devolver
      una subclase de ``Nodo``; cualquier otro valor es un error.


Escribir el nodo de plantilla
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El segundo paso para escribir etiquetas propias, es definir una subclase de
``Node`` que posea un método ``render()``. Continuando con el ejemplo previo,
debemos definir ``CurrentTimeNode``::

    import datetime

    class CurrentTimeNode(template.Node):

        def __init__(self, format_string):
            self.format_string = format_string

        def render(self, context):
            now = datetime.datetime.now()
            return now.strftime(self.format_string)

Estas dos funciones (``__init__`` y ``render``) se relacionan directamente
con los dos pasos para el proceso de la plantilla (compilación y renderizado).
La función de inicialización sólo necesitará almacenar el string con el formato
deseado, el trabajo real sucede dentro de la función ``render()``

Del mismo modo que los filtros de plantilla, estas funciones de renderización
deberían fallar silenciosamente en lugar de generar errores. En el único momento
en el cual se le es permitido a las etiquetas de plantilla generar errores es en
tiempo de compilación.

Registrar la etiqueta
~~~~~~~~~~~~~~~~~~~~~

Finalmente, deberás registrar la etiqueta con tu objeto ``Library`` dentro del
módulo. Registrar nuevas etiquetas es muy similar a registrar nuevos filtros
(como explicamos previamente). Sólo deberás instanciar un objeto
``template.Library`` y llamar a su método ``tag()``. Por ejemplo::

    register.tag('current_time', do_current_time)

El método ``tag()`` toma dos argumentos:

    * El nombre de la etiqueta de plantilla (*string*). Si esto se omite, se
      utilizará el nombre de la función de compilación.

    * La función de compilación.

De manera similar a como sucede con el registro de filtros, también es posible utilizar
``register.tag`` como un decorador en Python 2.4 o posterior::

    @register.tag(name="current_time")
    def do_current_time(parser, token):
        # ...

    @register.tag
    def shout(parser, token):
        # ...

Si omitimos el argumento ``name``, así como en el segundo ejemplo, Django
usará el nombre de la función como nombre de la etiqueta.

Definir una variable en el contexto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El ejemplo en la sección anterior simplemente devuelve un valor. Muchas veces es
útil definir variables de plantilla en vez de simplemente devolver valores. De
esta manera, los autores de plantillas podrán directamente utilizar las
variables que esta etiqueta defina.

Para definir una variable en el contexto, asignaremos a nuestro objeto
``context`` disponible en el método ``render()`` nuestras variables, como si de
un diccionario se tratase. Aquí mostramos la versión actualizada de
``CurrentTimeNode`` que define una variable de plantilla, ``current_time``, en
lugar de devolverla::

    class CurrentTimeNode2(template.Node):

        def __init__(self, format_string):
            self.format_string = format_string

        def render(self, context):
            now = datetime.datetime.now()
            context['current_time'] = now.strftime(self.format_string)
            return ''

Devolvemos un *string* vacío, debido a que ``render()`` siempre debe devolver
un string. Entonces, si todo lo que la etiqueta hace es definir una variable,
``render()`` debe al menos devolver un *string* vacío.

De esta manera usaríamos esta nueva versión de nuestra etiqueta::

    {% current_time2 "%Y-%M-%d %I:%M %p" %}
    <p>The time is {{ current_time }}.</p>

Pero hay un problema con ``CurrentTimeNode2``: el nombre de la variable
``current_time`` está definido dentro del código. Esto significa que tendrás que
asegurar que ``{{ current_time }}`` no sea utilizado en otro lugar dentro de la
plantilla, ya que ``{% current_time %}`` sobreescribirá el valor de esa otra
variable.

Una solución más limpia, es poder recibir el nombre de la variable en la
etiqueta de plantilla así::

    {% get_current_time "%Y-%M-%d %I:%M %p" as my_current_time %}
    <p>The current time is {{ my_current_time }}.</p>

Para hacer esto, necesitaremos modificar tanto la función de compilación
como la clase ``Node`` de esta manera::

    import re

    class CurrentTimeNode3(template.Node):

        def __init__(self, format_string, var_name):
            self.format_string = format_string
            self.var_name = var_name

        def render(self, context):
            now = datetime.datetime.now()
            context[self.var_name] = now.strftime(self.format_string)
            return ''

    def do_current_time(parser, token):
        # This version uses a regular expression to parse tag contents.
        try:
            # Splitting by None == splitting by spaces.
            tag_name, arg = token.contents.split(None, 1)
        except ValueError:
            msg = '%r tag requires arguments' % token.contents[0]
            raise template.TemplateSyntaxError(msg)

        m = re.search(r'(.*?) as (\w+)', arg)
        if m:
            fmt, var_name = m.groups()
        else:
            msg = '%r tag had invalid arguments' % tag_name
            raise template.TemplateSyntaxError(msg)

        if not (fmt[0] == fmt[-1] and fmt[0] in ('"', "'")):
            msg = "%r tag's argument should be in quotes" % tag_name
            raise template.TemplateSyntaxError(msg)

        return CurrentTimeNode3(fmt[1:-1], var_name)

Ahora, ``do_current_time()`` pasa el *string* de formato junto al nombre de la
variable a ``CurrentTimeNode3``.

Evaluar hasta otra etiqueta de bloque
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Las etiquetas de plantilla pueden funcionar como bloques que contienen otras
etiquetas (piensa en ``{% if %}``, ``{% for %}``, etc.). Para crear una
etiqueta como esta, usa ``parser.parse()`` en tu función de compilación.

Aquí vemos como está implementada la etiqueta estándar ``{% coment %}``::

    def do_comment(parser, token):
        nodelist = parser.parse(('endcomment',))
        parser.delete_first_token()
        return CommentNode()

    class CommentNode(template.Node):
        def render(self, context):
            return ''

``parser.parse()`` toma una tupla de nombres de etiquetas de bloque para
evaluar y devuelve una instancia de ``django.template.NodeList``, la cual es una
lista de todos los objetos ``Nodo`` que el *parser* encontró *antes* de haber
encontrado alguna de las etiquetas nombradas en la tupla.

Entonces, en el ejemplo previo, ``nodelist`` es una lista con todos los nodos
entre ``{% comment %}`` y ``{% endcomment %}``, excluyendo a los mismos ``{%
comment %}`` y ``{% endcomment %}``.

Luego de que ``parser.parse()`` es llamado el *parser* aún no ha "consumido" la
etiqueta ``{% endcomment %}``, es por eso que en el código se necesita llamar
explícitamente a ``parser.delete_first_token()`` para prevenir que esta
etiqueta sea procesada nuevamente.

Luego, ``CommentNode.render()`` simplemente devuelve un *string* vacío.
Cualquier cosa entre ``{% comment %}`` y ``{% endcomment %}`` es ignorada.

Evaluar hasta otra etiqueta de bloque y guardar el contenido
````````````````````````````````````````````````````````````

En el ejemplo anterior, ``do_comment()`` desechó todo entre ``{% comment %}`` y
``{% endcomment %}``, pero también es posible hacer algo con el código entre
estas etiquetas.

Por ejemplo, presentamos una etiqueta de plantilla, ``{% upper %}``, que
convertirá a mayúsculas todo hasta la etiqueta ``{% endupper %}``::

    {% upper %}
        This will appear in uppercase, {{ your_name }}.
    {% endupper %}

Como en el ejemplo previo, utilizaremos ``parser.parse()`` pero esta vez
pasamos el resultado en ``nodelist`` a ``Node``::

    @register.tag
    def do_upper(parser, token):
        nodelist = parser.parse(('endupper',))
        parser.delete_first_token()
        return UpperNode(nodelist)

    class UpperNode(template.Node):

        def __init__(self, nodelist):
            self.nodelist = nodelist

        def render(self, context):
            output = self.nodelist.render(context)
            return output.upper()

El único concepto nuevo aquí es ``self.nodelist.render(context)`` en
``UpperNode.render()``. El mismo simplemente llama a ``render()`` en cada
``Node`` en la lista de nodos.

Para más ejemplos de renderizado complejo, examina el código fuente para las
etiquetas ``{% if %}``, ``{% for %}``, ``{% ifequal %}`` y ``{% ifchanged %}``.
Puedes encontrarlas en ``django/template/defaulttags.py``.

Un atajo para etiquetas simples
-------------------------------

Muchas etiquetas de plantilla reciben un único argumento--una cadena o una
referencia a una variable de plantilla-- y retornan una cadena luego de hacer
algún procesamiento basado solamente en el argumento de entrada e información
externa. Por ejemplo la etiqueta ``current_time`` que escribimos antes es de
este tipo. Le pasamos una cadena de formato, y retorna la hora como una cadena.

Para facilitar la creación de esos tipos de etiquetas, Django provee una función
auxiliar: ``simple_tag``. Esta función, que es un método de
``django.template.Library``, recibe una función que acepta un argumento, lo
encapsula en una función ``render`` y el resto de las piezas necesarias que
mencionamos previamente y lo registra con el sistema de plantillas.

Nuestra función ``current_time`` podría entonces ser escrita de la siguiente
manera::

    def current_time(format_string):
        return datetime.datetime.now().strftime(format_string)

    register.simple_tag(current_time)

En Python 2.4 la sintaxis de decorador también funciona::

    @register.simple_tag
    def current_time(token):
        ...

Un par de cosas a tener en cuenta acerca de la función auxiliar ``simple_tag``:

    * Sólo se pasa un argumento a nuestra función.

    * La verificación de la cantidad requerida de argumentos ya ha sido
      realizada para el momento en el que nuestra función es llamada, de manera
      que no es necesario que lo hagamos nosotros.

    * Las comillas alrededor del argumento (si existieran) ya han sido quitadas,
      de manera que recibimos una cadena común.

Etiquetas de inclusión
----------------------

Otro tipo de etiquetas de plantilla común es aquel que visualiza ciertos datos
renderizando *otra* plantilla. Por ejemplo la interfaz de administración de
Django usa etiquetas de plantillas personalizadas (*custom*) para visualizar los
botones en la parte inferior de la páginas de formularios "agregar/cambiar".
Dichos botones siempre se ven igual, pero el destino del enlace  cambia
dependiendo del objeto que se está modificando. Se trata de un caso perfecto
para el uso de una pequeña plantilla que es llenada con detalles del objeto
actual.

Ese tipo de etiquetas reciben el nombre de *etiquetas de inclusión*. Es
probablemente mejor demostrar cómo escribir una usando un ejemplo. Escribamos
una etiqueta que produzca una lista de opciones para un simple objeto ``Poll``
con múltiples opciones. Usaremos una etiqueta como esta::

    {% show_results poll %}

El resultado será algo como esto::

    <ul>
      <li>First choice</li>
      <li>Second choice</li>
      <li>Third choice</li>
    </ul>

Primero definimos la función que toma el argumento y produce un diccionario de
datos con los resultados. Nota que nos basta un diccionario y no necesitamos
retornar nada más complejo. Esto será usado como el contexto para el fragmento
de plantilla::

    def show_books_for_author(author):
        books = author.book_set.all()
        return {'books': books}

Luego creamos la plantilla usada para renderizar la salida de la etiqueta.
Siguiendo con nuestro ejemplo, la plantilla es muy simple::

    <ul>
    {% for book in books %}
        <li> {{ book }} </li>
    {% endfor %}
    </ul>

Finalmente creamos y registramos la etiqueta de inclusión invocando el método
``inclusion_tag()`` sobre un objeto ``Library``.

Continuando con nuestro ejemplo, si la plantilla se encuentra en un archivo
llamado ``polls/result_snippet.html``, registraremos la plantilla de la
siguiente manera::

    register.inclusion_tag('books/books_for_author.html')(show_books_for_author)

Como siempre, la sintaxis de decoradores de Python 2.4 también funciona, de
manera que en cambio podríamos haber escrito::

    @register.inclusion_tag('books/books_for_author.html')
    def show_books_for_author(show_books_for_author):
        ...

A veces tus etiquetas de inclusión necesitan tener acceso a valores del contexto
de la plantilla padre. Para resolver esto Django provee una opción
``takes_context`` para las etiquetas de inclusión. Si especificas
``takes_context`` cuando creas una etiqueta de plantilla, la misma no tendrá
argumentos obligatorios y la función Python subyacente tendrá un argumento: el
contexto de la plantilla en el estado en el que se encontraba cuando la etiqueta
fue invocada.

Por ejemplo supongamos que estás escribiendo una etiqueta de inclusión que será
siempre usada en un contexto que contiene variables ``home_link`` y
``home_title`` que apuntan a la página principal. Así es como se vería la
función Python::

    @register.inclusion_tag('link.html', takes_context=True)
    def jump_link(context):
        return {
            'link': context['home_link'],
            'title': context['home_title'],
        }

.. nota::

    El primer parámetro de la función *debe* llamarse ``context``.

La plantilla ``link.html`` podría contener lo siguiente::

    Jump directly to <a href="{{ link }}">{{ title }}</a>.

Entonces, cada vez que desees usar esa etiqueta personalizada, carga su
biblioteca y ejecútala sin argumentos, de la siguiente manera::

    {% jump_link %}

Escribir cargadores de plantillas personalizados
================================================

Los cargadores de plantillas incluidos con Django (descriptos en la sección
"`Etiquetas de inclusión`_" más arriba) cubrirán usualmente todas tus necesidades
de carga de plantillas, pero es muy sencillo escribir el tuyo propio si
necesitas alguna lógica especial en dicha carga. Por ejemplo podrías cargar
plantillas desde una base de datos, o directamente desde un repositorio
Subversion usando las librerías (*bindings*) Python de Subversion, o (como
veremos) desde un archivo ZIP.

Un cargador de plantillas --esto es, cada entrada en la variables de
configuración ``TEMPLATE_LOADERS``--  debe ser un objeto invocable (*callable*)
con la siguiente interfaz::

    load_template_source(template_name, template_dirs=None)

El argumento ``template_name`` es el nombre de la plantilla a cargar (tal como
fue pasado a ``loader.get_template()`` o ``loader.select_template()``) y
``template_dirs`` es una lista opcional de directorios en los que se buscará en
lugar de ``TEMPLATE_DIRS``.

Si un cargador es capaz de cargar en forma exitosa una plantilla, debe retornar
una tupla: ``(template_source, template_path)``. Donde ``template_source`` es la
cadena de plantilla que será compilada por la maquinaria de plantillas, y
``template_path`` es la ruta desde la cual fue cargada la plantilla. Dicha ruta
podría ser presentada al usuario para fines de depuración así que debe
identificar en forma rápida desde dónde fue cargada la plantilla.

Si al cargador no le es posible cargar una plantilla, debe lanzar
``django.template.TemplateDoesNotExist``.

Cada función del cargador debe también poseer un atributo de función
``is_usable``. Este es un Booleano que le informa a la maquinaria de plantillas
si este cargador está disponible en la instalación de Python actual. Por ejemplo
el cargador desde eggs (que es capaz de cargar plantillas desde eggs Python)
fija ``is_usable`` a ``False`` si el módulo ``pkg_resources`` no se encuentra
instalado, porque ``pkg_resources`` es necesario para leer datos desde eggs.

Un ejemplo ayudará a clarificar todo esto. Aquí tenemos una función cargadora de
plantillas que puede cargar plantillas desde un archivo ZIP. Usa una variable
de configuración personalizada ``TEMPLATE_ZIP_FILES`` como una ruta
de búsqueda en lugar de ``TEMPLATE_DIRS`` y espera que cada ítem en dicha ruta
sea un archivo ZIP contiendo plantillas::

    import zipfile
    from django.conf import settings
    from django.template import TemplateDoesNotExist

    def load_template_source(template_name, template_dirs=None):
        """Template loader that loads templates from a ZIP file."""

        template_zipfiles = getattr(settings, "TEMPLATE_ZIP_FILES", [])

        # Try each ZIP file in TEMPLATE_ZIP_FILES.
        for fname in template_zipfiles:
            try:
                z = zipfile.ZipFile(fname)
                source = z.read(template_name)
            except (IOError, KeyError):
                continue
            z.close()
            # We found a template, so return the source.
            template_path = "%s:%s" % (fname, template_name)
            return (source, template_path)

        # If we reach here, the template couldn't be loaded
        raise TemplateDoesNotExist(template_name)

    # This loader is always usable (since zipfile is included with Python)
    load_template_source.is_usable = True

El único paso restante si deseamos usar este cargador es agregarlo a la variable
de configuración ``TEMPLATE_LOADERS``. Si pusiéramos este código en un paquete
llamado ``mysite.zip_loader`` entonces agregaremos
``mysite.zip_loader.load_template_source`` a ``TEMPLATE_LOADERS``.

Usar la referencia de plantillas incorporadas
=============================================

La interfaz de administración de Django incluye una referencia completa de todas
las etiquetas y filtros de plantillas disponibles para un sitio determinado.
Está designada para ser una herramienta que los programadores Django proveen a
los desarrolladores de plantillas. Para verla, ve a la interfaz de
administración y haz click en el enlace Documentación en la zona superior
derecha de la página.

La referencia está dividida en cuatro secciones: etiquetas, filtros, modelos y
vistas. Las secciones *etiquetas* y *filtros* describen todas las etiquetas
incluidas (en efecto, las referencias de etiquetas y filtros del :doc:`Capítulo 4<chapter04>` han
sido extraídas directamente de esas páginas) así como cualquier biblioteca de
etiquetas o filtros personalizados disponible.

La página *views* es la más valiosa. Cada URL en tu sitio tiene allí una entrada
separada. Si la vista relacionada incluye una docstring, haciendo click en la
URL te mostrará lo siguiente:

    * El nombre de la función de vista que genera esa vista.

    * Una breve descripción de qué hace la vista.

    * El contexto, o una lista de variables disponibles en la plantilla de la
      vista.

    * El nombre de la plantilla o plantillas usados para esa vista.

Para un ejemplo detallado de la documentación de vistas, lee el código fuente de
la vista genérica de Django ``object_list`` la cual se encuentra en
``django/views/generic/list_detail.py``.

Debido a que los sitios implementados con Django generalmente usan objetos de
bases de datos, las páginas *models* describen cada tipo de objeto en el sistema
así como todos los campos disponibles en esos objetos.

En forma conjunta, las páginas de documentación deberían proveerte cada
etiqueta, filtro, variable y objeto disponible para su uso en una plantilla
arbitraria.

Configurar el sistema de plantillas en modo autónomo
====================================================

.. nota::

    Esta sección es sólo de interés para aquellos que intentan usar el sistema
    de plantillas como un componente de salida en otra aplicación. Si estás
    usando el sistema como parte de un aplicación Django, la información aquí
    presentada no es relevante para ti.

Normalmente Django carga toda la información de configuración que necesita desde
su propio archivo de configuración por omisión, combinado con las variables de
configuración en el módulo indicado en la variable de entorno
``DJANGO_SETTINGS_MODULE``.  Pero si estás usando el sistema de plantillas
independientemente del resto de Django, el esquema de la variable de entorno no
es muy conveniente porque probablemente quieras configurar el sistema de
plantillas en una manera acorde con el resto de tu aplicación en lugar de tener
que vértelas con archivos de configuración e indicando los mismos con variables
de entorno.

Para resolver este problema necesitas usar la opción de configuración manual
descripta en forma completa en el Apéndice E. En resumen, necesitas importar las
partes apropiadas del sistema de plantillas y entonces, *antes* de invocar
alguna de las funciones de plantillas, invoca
``django.conf.settings.configure()`` con cualquier valor de configuración que
desees especificar.

Podrías desear considerar fijar al menos ``TEMPLATE_DIRS`` (si vas a usar
cargadores de plantillas), ``DEFAULT_CHARSET`` (aunque el valor por omisión
``utf-8`` probablemente sea adecuado) y ``TEMPLATE_DEBUG``. Todas las variables
de configuración están descriptas en el Apéndice E y todos las variables cuyos
nombres comienzan con ``TEMPLATE_`` son de obvio interés.

¿Qué sigue?
===========

Hasta ahora este libro ha asumido que el contenido que estás visualizando es
HTML. Esta no es una suposición incorrecta para un libro sobre desarrollo Web,
pero en algunas ocasiones querrás usar Django para generar otros formatos de
datos.

El :doc:`próximo capítulo<chapter11>` describe cómo puedes usar Django para producir imágenes,
PDFs y cualquier otro formato de datos que puedas imaginar.



