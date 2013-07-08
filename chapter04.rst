==============================================
Capítulo 4: El sistema de plantillas de Django
==============================================

En el capítulo anterior, quizás notaste algo extraño en cómo retornábamos
el texto en nuestras vistas de ejemplos. A saber, el HTML fue codificado [#]_
directamente en nuestro código Python.

Este convenio conduce a problemas severos:

    * Cualquier cambio en el diseño de la página requiere un cambio en el código
      de Python. El diseño de un sitio tiende a cambiar más frecuentemente que
      el código de Python subyacente, por lo que sería conveniente si el diseño
      podría ser cambiado sin la necesidad de modificar el código Python.

    * Escribir código Python y diseñar HTML son dos disciplinas diferentes, y la
      mayoría de los entornos de desarrollo web profesional dividen estas
      responsabilidades entre personas separadas (o incluso en departamento
      separados).  Diseñadores y programadores HTML/CSS no deberían tener que
      editar código Python para conseguir hacer su trabajo; ellos deberían
      tratar con HTML.

    * Asimismo, esto es más eficiente si los programadores pueden trabajar sobre
      el código Python y los diseñadores sobre las plantillas al mismo tiempo,
      más bien que una persona espere por otra a que termine de editar un solo
      archivo que contiene ambos: Python y HTML.

Por esas razones, es mucho más limpio y mantenible separar el diseño de la
página del código Python en sí mismo. Podemos hacer esto con *el sistema de
plantillas* de Django, el cual trataremos en este capítulo.


Sistema básico de plantillas
=============================

Una plantilla de Django es una cadena de texto que pretende separar la
presentación de un documento de sus datos. Una plantilla define rellenos y
diversos bits de lógica básica (esto es, etiquetas de plantillas) que regulan
cómo debe ser mostrado el documento. Normalmente, las plantillas son usadas para
producir HTML, pero las plantillas de Django son igualmente capaces de generar
cualquier formato basado en texto.

Vamos a sumergirnos en una simple plantilla de ejemplo. Esta plantilla describe
una página HTML que agradece a una persona por hacer un pedido de la empresa. Piensa
en esto como un modelo de carta:

.. code-block:: html 

    <html>
    <head><title>Ordering notice</title></head>

    <body>

    <p>Dear {{ person_name }},</p>

    <p>Thanks for placing an order from {{ company }}. It's scheduled to
    ship on {{ ship_date|date:"F j, Y" }}.</p>

    <p>Here are the items you've ordered:</p>

    <ul>
    {% for item in item_list %}
    <li>{{ item }}</li>
    {% endfor %}
    </ul>

    {% if ordered_warranty %}
    <p>Your warranty information will be included in the packaging.</p>
    {% endif %}

    <p>Sincerely,<br />{{ company }}</p>

    </body>
    </html>

Esta plantilla es un HTML básico con algunas variables y etiquetas de plantillas
agregadas. Vamos paso a paso a través de ésta:

    * Cualquier texto encerrado por un par de llaves (por ej.
      ``{{ person_name }}``) es una *variable*. Esto significa "insertar el
      valor de la variable a la que se dio ese nombre". ¿Cómo especificamos el valor
      de las variables?. Vamos a llegar a eso en un momento.

    * Cualquier texto que esté rodeado por llaves y signos de porcentaje (por
      ej. ``{% if ordered_warranty %}``) es una *etiqueta de plantilla*. La
      definición de etiqueta es bastante amplia: una etiqueta sólo le indica
      al sistema de plantilla "haz algo".

      Este ejemplo de plantilla contiene dos etiquetas: la etiqueta
      ``{% for item in item_list %}`` (una etiqueta ``for``) y la etiqueta
      ``{% if ordered_warranty %}`` (una etiqueta ``if``).

      Una etiqueta ``for`` actúa como un simple constructor de bucle, dejándote
      recorrer a través de cada uno de los items de una secuencia. Una etiqueta
      ``if``, como quizás esperabas, actúa como una cláusula lógica "if". En
      este caso en particular, la etiqueta comprueba si el valor de la
      variable ``ordered_warranty`` se evalúa como ``True``. Si lo hace, el sistema
      de plantillas mostrará todo lo que hay entre ``{% if ordered_warranty %}`` y
      ``{% endif %}``. Si no, el sistema de plantillas no mostrará esto. El
      sistema de plantillas también admite ``{% else %}`` y otras varias
      cláusulas lógicas.

    * Finalmente, el segundo párrafo de esta plantilla tiene un ejemplo de un
      *filtro*, con el cual puedes alterar la exposición de una variable. En
      este ejemplo, ``{{ ship_date|date:"F j, Y" }}``, estamos pasando la
      variable ``ship_date`` por el filtro ``date``, tomando el filtro ``date``
      el argumento ``"F j, Y"``. El filtro ``date`` formatea fechas en el
      formato dado, especificado por ese argumento. Los filtros se encadenan
      mediante el uso de un caracter pipe (``|``), como una referencia a las
      tuberías de Unix.

Cada plantilla de Django tiene acceso a varias etiquetas y filtros incorporados, 
algunos de los cuales serán tratados en la sección que sigue. El Apéndice F contiene
la lista completa de etiquetas y filtros, y es una buena idea familiarizarse con
esta lista, de modo que sepas qué es posible. También es posible crear tus propios
filtros y etiquetas, los cuales cubriremos en el :doc:`Capítulo10<chapter10>`.


Empleo del sistema de plantillas
================================

Para usar el sistema de plantillas en el código Python, sólo sigue estos dos
pasos:

    1. Crea un objeto ``Template`` brindando el código en crudo de la plantilla
       como una cadena. Django también ofrece un camino para crear objetos
       ``Template`` especificando la ruta al archivo de plantilla en el
       sistemas de archivos; vamos a examinar esto en un rato.

    2. Llama al método ``render()`` del objeto ``Template`` con un conjunto de
       variables (o sea, el contexto). Este retorna una plantilla totalmente
       renderizada como una cadena de caracteres, con todas las variables y
       etiquetas de bloques evaluadas de acuerdo al contexto.

Las siguientes secciones describen cada uno de los pasos con mayor detalle.

Creación de objetos Template
-----------------------------

La manera fácil de crear objetos ``Template`` es instanciarlos directamente. La
clase ``Template`` se encuentra en el módulo ``django.template``, y el
constructor toma un argumento, el código en crudo de la plantilla. Vamos a
sumergirnos en el intérprete interactivo de Python para ver cómo funciona este
código.

.. admonition:: Ejemplos del Intérprete Interactivo

    Durante todo el libro, hemos expuesto sesiones de ejemplo del intérprete
    Python interactivo. Puedes reconocer estos ejemplos por el triple signo
    mayor-que (``>>>``), el cuál designa el prompt del intérprete. Si estás
    copiando los ejemplos del libro, no copies estos signos mayor-que.

    Las sentencias multilíneas en el intérprete interactivo son rellenadas con
    tres puntos (``...``), por ejemplo:

        >>> print """This is a
        ... string that spans
        ... three lines."""
        This is a
        string that spans
        three lines.
        >>> def my_function(value):
        ...     print value
        >>> my_function('hello')
        hello

    Esos tres puntos al comienzo de una línea adicional son insertados por el
    shell de Python -- no son parte de nuestra entrada. Los incluimos aquí para
    ser fieles a la salida real del intérprete. Si estás copiando nuestros
    ejemplos para seguirlos, no copies esos puntos.

Desde dentro del directorio del proyecto creado por
``django-admin.py startproject`` (como se expuso en el :doc:`Capítulo 2<chapter02>`), escribe
``python manage.py shell`` para comenzar el intérprete interactivo. Aquí hay
un ensayo básico:

    >>> from django.template import Template
    >>> t = Template("My name is {{ name }}.")
    >>> print t

Si lo estás siguiendo interactivamente, verás algo como esto::

    <django.template.Template object at 0xb7d5f24c>

Ese ``0xb7d5f24c`` será distinto cada vez, y realmente no importa; es la forma
simple en que Python "identifica" un objeto de ``Template``.

.. admonition:: Variables de configuración de Django

    Cuando usas Django, necesitas indicarle qué valores usar para sus variables
    de configuración.  Interactivamente, suele usarse ``python manage.py
    shell``, pero tienes otras opciones descriptas en el Apéndice E.

Cuando creas un objeto ``Template``, el sistema de plantillas compila el código
en crudo a uno interno, de forma optimizada, listo para renderizar. Pero si tu
código de plantilla incluye errores de sintaxis, la llamada a ``Template()``
causará una excepción ``TemplateSyntaxError``:

    >>> from django.template import Template
    >>> t = Template('{% notatag %} ')
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      ...
      django.template.TemplateSyntaxError: Invalid block tag: 'notatag'

El sistema lanza una excepción ``TemplateSyntaxError`` por alguno de los
siguientes casos:

    * Bloques de etiquetas inválidos
    * Argumentos inválidos para una etiqueta válida
    * Filtros inválidos
    * Argumentos inválidos para filtros válidos
    * Sintaxis inválida de plantilla
    * Etiquetas de bloque sin cerrar (para etiquetas de bloque que requieran la
      etiqueta de cierre)

Renderizar una plantilla
-------------------------

Una vez que tienes un objeto ``Template``, le puedes pasar datos brindando un
*contexto*. Un contexto es simplemente un conjunto de variables y sus valores
asociados. Una plantilla usa estas variables para llenar y evaluar estas
etiquetas de bloque.

Un contexto es representado en Django por la clase ``Context``, ésta se
encuentra en el módulo ``django.template``. Su constructor toma un argumento
opcional: un diccionario que mapea nombres de variables con valores. Llama
al método ``render()`` del objeto ``Template`` con el contexto para "llenar" la
plantilla:

    >>> from django.template import Context, Template
    >>> t = Template("My name is {{ name }}.")
    >>> c = Context({"name": "Stephane"})
    >>> t.render(c)
    'My name is Stephane.'

.. admonition:: Diccionarios y Contextos

    Un diccionario de Python es un mapeo entre llaves conocidas y valores de
    variables. Un ``Context`` es similar a un diccionario, pero un ``Context``
    provee funcionalidad adicional, como se cubre en el :doc:`Capítulo 10<chapter10>`.

Los nombres de las variables deben comenzar con una letra (A-Z o a-z) y pueden
contener dígitos, guiones bajos y puntos. (Los puntos son un caso especial al que
llegaremos en un momento). Los nombres de variables son sensible a
mayúsculas-minúsculas.

Este es un ejemplo de compilación y renderización de una plantilla, usando la
plantilla de muestra del comienzo de este capítulo:

    >>> from django.template import Template, Context
    >>> raw_template = """<p>Dear {{ person_name }},</p>
    ...
    ... <p>Thanks for ordering {{ product }} from {{ company }}. It's scheduled
    ... to ship on {{ ship_date|date:"F j, Y" }}.</p>
    ...
    ... {% if ordered_warranty %}
    ... <p>Your warranty information will be included in the packaging.</p>
    ... {% endif %}
    ...
    ... <p>Sincerely,<br />{{ company }}</p>"""
    >>> t = Template(raw_template)
    >>> import datetime
    >>> c = Context({'person_name': 'John Smith',
    ...     'product': 'Super Lawn Mower',
    ...     'company': 'Outdoor Equipment',
    ...     'ship_date': datetime.date(2009, 4, 2),
    ...     'ordered_warranty': True})
    >>> t.render(c)
    "<p>Dear John Smith,</p>\n\n<p>Thanks for ordering Super Lawn Mower from
    Outdoor Equipment. It's scheduled \nto ship on April 2, 2009.</p>\n\n\n
    <p>Your warranty information will be included in the packaging.</p>\n\n\n
    <p>Sincerely,<br />Outdoor Equipment</p>"

Vamos paso a paso por este código, de a una sentencia a la vez:

    * Primero, importamos la clase ``Template`` y ``Context``, ambas se
      encuentran en el módulo ``django.template``.

    * Guardamos en texto crudo de nuestra plantilla en la variable
      ``raw_template``.  Note que usamos triple comillas para delimitar la cadena
      de caracteres, debido a que abarca varias líneas; en el código Python,
      las cadenas de caracteres delimitadas con una sola comilla indican que no
      puede abarcar varias líneas.

    * Luego, creamos un objeto plantilla, ``t``, pasándole ``raw_template`` al
      constructor de la clase ``Template``.

    * Importamos el módulo ``datetime`` desde la biblioteca estándar de Python,
      porque lo vamos a necesitar en la próxima sentencia.

    * Entonces, creamos un objeto ``Context`` , ``c``. El constructor de
      ``Context`` toma un diccionario de Python, el cual mapea nombres de
      variables con valores.  Aquí, por ejemplo, especificamos que
      ``person_name`` es ``'John Smith'``, ``product`` es ``'Super Lawn
      Mower'``, y así sucesivamente.

    * Finalmente, llamamos al método ``render()`` sobre nuestro objeto de
      plantilla, pasando a éste el contexto. Este retorna la plantilla
      renderizada -- esto es, reemplaza las variables de la plantilla con los
      valores reales de las variables, y ejecuta cualquier bloque de
      etiquetas.

      Nota que el párrafo de garantía fue mostrado porque la variable
      ``ordered_warranty`` se evalúa como ``True``. También nota que la fecha
      ``April 2, 2009``, es mostrada acorde al formato de cadena de caracteres
      ``F j, Y``. (Explicaremos los formatos de cadenas de caracteres para el
      filtro ``date`` a la brevedad).

      Si eres nuevo en Python, quizás te preguntes por qué la salida incluye los
      caracteres de nueva línea (``'\n'``) en vez de mostrar los saltos de
      línea.  Esto sucede porque es una sutileza del intérprete interactivo de
      Python: la llamada a ``t.render(c)`` retorna una cadena de caracteres, y
      el intérprete interactivo, por omisión, muestra una *representación* de
      ésta, en vez de imprimir el valor de la cadena. Si quieres ver la cadena
      de caracteres con los saltos de líneas como verdaderos saltos de líneas en
      vez de caracteres ``'\n'``, usa la sentencia ``print``:
      ``print t.render(c)``.

Estos son los fundamentos del uso del sistema de plantillas de Django: sólo
escribe una plantilla, crea un objeto ``Template``, crea un ``Context``, y llama
al método ``render()``.

Múltiples contextos, mismas plantillas
----------------------------------------

Una vez que tengas un objeto ``Template``, puedes renderizarlo con múltiples
contextos, por ejemplo:

.. code-block:: python

    >>> from django.template import Template, Context
    >>> t = Template('Hello, {{ name }}')
    >>> print t.render(Context({'name': 'John'}))
    Hello, John
    >>> print t.render(Context({'name': 'Julie'}))
    Hello, Julie
    >>> print t.render(Context({'name': 'Pat'}))
    Hello, Pat

Cuando estés usando la misma plantilla fuente para renderizar múltiples
contextos como este, es más eficiente crear el objeto ``Template`` *una sola
vez* y luego llamar a ``render()`` sobre éste muchas veces:

.. code-block:: python

    # Bad
    for name in ('John', 'Julie', 'Pat'):
        t = Template('Hello, {{ name }}')
        print t.render(Context({'name': name}))

    # Good
    t = Template('Hello, {{ name }}')
    for name in ('John', 'Julie', 'Pat'):
        print t.render(Context({'name': name}))

El análisis sintáctico de las plantillas de Django es bastante rápido. Detrás de
escena, la mayoría de los analizadores pasan con una simple llamada a una
expresión regular corta. Esto es un claro contraste con el motor de plantillas de XML, que
incurre en la excesiva actividad de un analizador XML, y tiende a ser órdenes de
magnitud más lento que el motor de renderizado de Django.

Búsqueda del contexto de una variable
---------------------------------------

En los ejemplos dados hasta el momento, pasamos valores simples a los contextos --en
su mayoría cadena de caracteres, más un ``datetime.date``. Sin embargo, el
sistema de plantillas maneja elegantemente estructuras de datos más complicadas,
como listas, diccionarios y objetos personalizados.

La clave para recorrer estructuras de datos complejas en las plantillas de
Django ese el carácter punto (``.``). Usa un punto para acceder a las claves de
un diccionario, atributos, índices o métodos de un objeto.

Esto es mejor ilustrarlos con algunos ejemplos. Por ejemplo, imagina que pasas un
diccionario de Python a una plantilla. Para acceder al valor de ese diccionario
por su clave, usa el punto:

    >>> from django.template import Template, Context
    >>> person = {'name': 'Sally', 'age': '43'}
    >>> t = Template('{{ person.name }} is {{ person.age }} years old.')
    >>> c = Context({'person': person})
    >>> t.render(c)
    'Sally is 43 years old.'

De forma similar, los puntos te permiten acceder a los atributos de los objetos.
Por ejemplo, un objeto de Python ``datetime.date`` tiene los atributos ``year``,
``month`` y ``day``, y puedes usar el punto para acceder a ellos en las
plantillas de Django:

    >>> from django.template import Template, Context
    >>> import datetime
    >>> d = datetime.date(1993, 5, 2)
    >>> d.year
    1993
    >>> d.month
    5
    >>> d.day
    2
    >>> t = Template('The month is {{ date.month }} and the year is {{ date.year }}.')
    >>> c = Context({'date': d})
    >>> t.render(c)
    'The month is 5 and the year is 1993.'

Este ejemplo usa una clase personalizada::

    >>> from django.template import Template, Context
    >>> class Person(object):
    ...     def __init__(self, first_name, last_name):
    ...         self.first_name, self.last_name = first_name, last_name
    >>> t = Template('Hello, {{ person.first_name }} {{ person.last_name }}.')
    >>> c = Context({'person': Person('John', 'Smith')})
    >>> t.render(c)
    'Hello, John Smith.'

Los puntos también son utilizados para llamar a métodos sobre los objetos. Por
ejemplo, cada cadena de caracteres de Python tiene el métodos ``upper()`` y
``isdigit()``, y puedes llamar a estos en las plantillas de Django usando la
misma sintaxis de punto:

    >>> from django.template import Template, Context
    >>> t = Template('{{ var }} -- {{ var.upper }} -- {{ var.isdigit }}')
    >>> t.render(Context({'var': 'hello'}))
    'hello -- HELLO -- False'
    >>> t.render(Context({'var': '123'}))
    '123 -- 123 -- True'

Nota que no tienes que incluir los paréntesis en las llamadas a los métodos.
Además, tampoco es posible pasar argumentos a los métodos; sólo puedes llamar
los métodos que no requieran argumentos. (Explicaremos esta filosofía luego
en este capítulo).

Finalmente, los puntos también son usados para acceder a los índices de las
listas, por ejemplo:

    >>> from django.template import Template, Context
    >>> t = Template('Item 2 is {{ items.2 }}.')
    >>> c = Context({'items': ['apples', 'bananas', 'carrots']})
    >>> t.render(c)
    'Item 2 is carrots.'

Los índices negativos de las listas no están permitidos. Por ejemplo,
la variable ``{{ items.-1 }}`` causará una ``TemplateSyntaxError``.

.. admonition:: Listas de Python

    Las listas de Python comienzan en cero, entonces el primer elemento
    es el 0, el segundo es el 1 y así sucesivamente.

La búsqueda del punto puede resumirse como esto: cuando un sistema de
plantillas encuentra un punto en una variable, éste intenta la siguiente
búsqueda, en este orden:

    * Diccionario (por ej. ``foo["bar"]``)
    * Atributo (por ej. ``foo.bar``)
    * Llamada de método (por ej. ``foo.bar()``)
    * Índice de lista (por ej. ``foo[bar]``)

El sistema utiliza el primer tipo de búsqueda que funcione. Es la lógica de
cortocircuito.

Los puntos pueden ser anidados a múltiples niveles de profundidad. El siguiente
ejemplo usa ``{{ person.name.upper }}``, el que se traduce en una búsqueda de
diccionario (``person['name']``) y luego en una llamada a un método
(``upper()``):

    >>> from django.template import Template, Context
    >>> person = {'name': 'Sally', 'age': '43'}
    >>> t = Template('{{ person.name.upper }} is {{ person.age }} years old.')
    >>> c = Context({'person': person})
    >>> t.render(c)
    'SALLY is 43 years old.'

Comportamiento de la llamada a los métodos
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La llamada a los métodos es ligeramente más compleja que los otros tipos de
búsqueda. Aquí hay algunas cosas a tener en cuenta:

    * Si, durante la búsqueda de método, un método provoca una excepción, la
      excepción será propagada, a menos que la excepción tenga un atributo
      ``silent_variable_failure`` cuyo valor sea ``True``. Si la excepción
      *tiene* el atributo ``silent_variable_failure``, la variable será
      renderizada como un string vacío, por ejemplo:
      
.. code-block:: python      

            >>> t = Template("My name is {{ person.first_name }}.")
            >>> class PersonClass3:
            ...     def first_name(self):
            ...         raise AssertionError, "foo"
            >>> p = PersonClass3()
            >>> t.render(Context({"person": p}))
            Traceback (most recent call last):
            ...
            AssertionError: foo

            >>> class SilentAssertionError(AssertionError):
            ...     silent_variable_failure = True
            >>> class PersonClass4:
            ...     def first_name(self):
            ...         raise SilentAssertionError
            >>> p = PersonClass4()
            >>> t.render(Context({"person": p}))
            "My name is ."

* La llamada a un método funcionará sólo si el método no requiere
  argumentos. En otro caso, el sistema pasará a la siguiente búsqueda de
  tipo (índice de lista).

* Evidentemente, algunos métodos tienen efectos secundarios, por lo que
  sería absurdo, en el mejor de los casos, y posiblemente un agujero de
  seguridad, permitir que el sistema de plantillas tenga acceso a ellos.

Digamos, por ejemplo, tienes objeto ``BankAccount`` que tiene un método
``delete()``. Una plantilla no debería permitir incluir algo como
``{{ account.delete }}``.

Para prevenir esto, asigna el atributo ``alters_data`` de la función en el
método:

.. code-block:: python

          def delete(self):
              # Delete the account
          delete.alters_data = True

El sistema de plantillas no debería ejecutar cualquier método marcado de
este modo. En otras palabras, si una plantilla incluye
``{{ account.delete }}``, esta etiqueta no ejecutará el método
``delete()``. Este fallará silenciosamente.

¿Cómo se manejan las variables inválidas?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Por omisión, si una variable no existe, el sistema de plantillas renderiza este
como un string vacío, fallando silenciosamente, por ejemplo::

    >>> from django.template import Template, Context
    >>> t = Template('Your name is {{ name }}.')
    >>> t.render(Context())
    'Your name is .'
    >>> t.render(Context({'var': 'hello'}))
    'Your name is .'
    >>> t.render(Context({'NAME': 'hello'}))
    'Your name is .'
    >>> t.render(Context({'Name': 'hello'}))
    'Your name is .'

El sistema falla silenciosamente en vez de levantar una excepción porque intenta
ser flexible a los errores humanos. En este caso, todas las búsquedas fallan
porque los nombres de las variables, o su capitalización es incorrecta. En el
mundo real, es inaceptable para un sitio web ser inaccesible debido a un
error de sintaxis tan pequeño.

Ten en cuenta que es posible cambiar el comportamiento por omisión de Django en
este sentido, ajustando la configuración de Django. Discutiremos esto más
adelante en el :doc:`Capítulo 10<chapter10>`.

Jugando con objetos Context
---------------------------

La mayoría de la veces, instancias un objeto ``Context`` pasando un diccionario
completamente poblado a  ``Context``. Pero puedes agregar y quitar elementos
de un objeto ``Context`` una vez que éste está instanciado, también, usando
la sintaxis estándar de los diccionarios de Python:

    >>> from django.template import Context
    >>> c = Context({"foo": "bar"})
    >>> c['foo']
    'bar'
    >>> del c['foo']
    >>> c['foo']
    ''
    >>> c['newvariable'] = 'hello'
    >>> c['newvariable']
    'hello'

Etiquetas básicas de plantillas y filtros
=========================================

Como hemos mencionamos, el sistema de plantillas se distribuye con etiquetas y
filtros incorporados. Las secciones que siguen proveen un resumen de la mayoría
de las etiquetas y filtros.

Etiquetas
---------

if/else
~~~~~~~

La etiqueta ``{% if %}`` evalúa una variable, y si esta es "true" (esto es,
existe, no está vacía y no es un valor Boolean falso), el sistema mostrará
todo lo que hay entre ``{% if %}`` y ``{% endif %}``, por ejemplo:

.. code-block:: html

    {% if today_is_weekend %}
        <p>Welcome to the weekend!</p>
    {% endif %}

La etiqueta ``{% else %}`` es opcional:

.. code-block:: html

    {% if today_is_weekend %}
        <p>Welcome to the weekend!</p>
    {% else %}
        <p>Get back to work.</p>
    {% endif %}

.. admonition:: Las "verdades" de Python

    En Python, la lista vacía (``[]``), la tupla vacía (``()``), el diccionario
    vacío (``{}``), la cadena vacía (``''``), el cero (``0``), y el objeto especial
    ``None`` son ``False`` en un contexto booleano.  Todo lo demás es ``True``.

La etiqueta ``{% if %}`` acepta ``and``, ``or``, o ``not`` para testear
múltiples variables, o para negarlas. Por ejemplo:

.. code-block:: html

    {% if athlete_list and coach_list %}
        Both athletes and coaches are available.
    {% endif %}

    {% if not athlete_list %}
        There are no athletes.
    {% endif %}

    {% if athlete_list or coach_list %}
        There are some athletes or some coaches.
    {% endif %}

    {% if not athlete_list or coach_list %}
        There are no athletes or there are some coaches. (OK, so
        writing English translations of Boolean logic sounds
        stupid; it's not our fault.)
    {% endif %}

    {% if athlete_list and not coach_list %}
        There are some athletes and absolutely no coaches.
    {% endif %}

Las etiquetas ``{% if %}`` no permiten las cláusulas ``and`` y ``or`` en la
misma etiqueta, porque el orden de evaluación lógico puede ser ambiguo. Por
ejemplo, esto es inválido:

.. code-block:: html

    {% if athlete_list and coach_list or cheerleader_list %}

No se admite el uso de paréntesis para controlar el orden de las operaciones.
Si necesitas paréntesis, considera efectuar la lógica en el código de la
vista para simplificar las plantillas. Aún así, si necesitas combinar
``and`` y ``or`` para hacer lógica avanzada, usa etiquetas
``{% if %}`` anidadas, por ejemplo:

.. code-block:: html


    {% if athlete_list %}
        {% if coach_list or cheerleader_list %}
            We have athletes, and either coaches or cheerleaders!
        {% endif %}
    {% endif %}

Usar varias veces el mismo operador lógico están bien, pero no puedes combinar
diferentes operadores. Por ejemplo, esto es válido:

.. code-block:: html

    {% if athlete_list or coach_list or parent_list or teacher_list %}

Ahí no hay una etiqueta ``{% elif %}``. Usa etiquetas ``{% if %}`` anidadas
para conseguir alguna cosa:

.. code-block:: html

    {% if athlete_list %}
        <p>Here are the athletes: {{ athlete_list }}.</p>
    {% else %}
        <p>No athletes are available.</p>
        {% if coach_list %}
            <p>Here are the coaches: {{ coach_list }}.</p>
        {% endif %}
    {% endif %}

Asegúrate de cerrar cada ``{% if %}`` con un ``{% endif %}``. En otro caso,
Django levantará la excepción ``TemplateSyntaxError``.

for
~~~

La etiqueta ``{% for %}`` permite iterar sobre cada uno de los elementos de una
secuencia. Como en la sentencia ``for`` de Python, la sintaxis es ``for X in
Y``, dónde ``Y`` es la secuencia sobre la que se hace el bucle y ``X`` es el
nombre de la variable que se usará para cada uno de los ciclos del bucle. Cada
vez que atravesamos el bucle, el sistema de plantillas renderizará todo entre
``{% for %}`` y ``{% endfor %}``.

Por ejemplo, puedes usar lo siguiente para mostrar una lista de atletas tomadas
de la variable ``athlete_list``:

.. code-block:: html

    <ul>
    {% for athlete in athlete_list %}
        <li>{{ athlete.name }}</li>
    {% endfor %}
    </ul>

Agrega ``reversed`` a la etiqueta para iterar sobre la lista en orden inverso:

.. code-block:: html

    {% for athlete in athlete_list reversed %}
    ...
    {% endfor %}

Es posible anidar etiquetas ``{% for %}``::

    {% for country in countries %}
        <h1>{{ country.name }}</h1>
        <ul>
        {% for city in country.city_list %}
            <li>{{ city }}</li>
        {% endfor %}
        </ul>
    {% endfor %}

No se admite la "ruptura" de un bucle antes de que termine. Si quieres conseguir
esto, cambia la variable sobre la que estás iterando para que incluya sólo los
valores sobre los cuales quieres iterar. De manera similar, no hay apoyo para la
sentencia "continue" que se encargue de retornar inmediatamente al inicio del
bucle. (Ve a la sección "`Filosofía y limitaciones`_" luego en este capítulo
para comprender el razonamiento detrás de este decisión de diseño.)

La etiqueta ``{% for %}`` asigna la variable ``forloop`` mágica a la plantilla
con el bucle. Esta variable tiene algunos atributos que toman información acerca
del progreso del bucle:

* ``forloop.counter`` es siempre asignada a un número entero representando
  el número de veces que se ha entrado en el bucle. Esta es indexada a
  partir de 1, por lo que la primera vez que se ingresa al bucle,
  ``forloop.counter`` será ``1``. Aquí un ejemplo::

      {% for item in todo_list %}
          <p>{{ forloop.counter }}: {{ item }}</p>
      {% endfor %}

* ``forloop.counter0`` es como ``forloop.counter``, excepto que esta es
  indexada a partir de cero. Contendrá el valor ``0`` la primera vez que se
  atraviese el bucle.

* ``forloop.revcounter`` es siempre asignada a un entero que representa
  el número de iteraciones que faltan para terminar el bucle. La primera vez
  que se ejecuta el bucle ``forloop.revcounter`` será igual al número de
  elementos que hay en la secuencia. La última vez que se atraviese el
  bucle, a ``forloop.revcounter`` se la asignará el valor ``1``.

* ``forloop.revcounter0`` es como ``forloop.revcounter``, a excepción de que
  está indexada a partir de cero. La primera vez que se atraviesa el bucle,
  ``forloop.revcounter0`` es asignada al número de elementos que hay en la
  secuencia menos 1. La última vez que se atraviese el bucle, el valor de
  esta será ``0``.

* ``forloop.first`` es un valor booleano asignado a ``True`` si es la
  primera vez que se pasa por el bucle. Esto es conveniente para ocasiones
  especiales:

      {% for object in objects %}
          {% if forloop.first %}<li class="first">{% else %}<li>{% endif %}
          {{ object }}
          </li>
          {% endfor %}

* ``forloop.last`` es un valor booleano asignado a ``True`` si es la última
  pasada por el bucle. Un uso común es para esto es poner un carácter pipe
  entre una lista de enlaces:
  
.. code-block:: html

{% for link in links %}{{ link }}{% if not forloop.last %} | {% endif %}{% endfor %}

El código de la plantilla de arriba puede mostrar algo parecido a esto::

       Link1 | Link2 | Link3 | Link4

* ``forloop.parentloop`` esta es una referencia al objeto *padre* de
  ``forloop``, en el caso de bucles anidados. Aquí un ejemplo::

          {% for country in countries %}
              <table>
              {% for city in country.city_list %}
                  <tr>
                  <td>Country #{{ forloop.parentloop.counter }}</td>
                  <td>City #{{ forloop.counter }}</td>
                  <td>{{ city }}</td>
                  </tr>
              {% endfor %}
              </table>
          {% endfor %}

La variable mágica ``forloop`` está sólo disponible dentro de bucles. Después de
que el analizados sintáctico encuentra ``{% endfor %}``, ``forloop`` desaparece.

.. admonition:: Contextos y la variable forloop

Dentro de un bloque ``{% for %}``, las variables existentes se
mueven fuera de tal manera de evitar sobreescribir la variable mágica
``forloop``. Django expone ese contexto movido en ``forloop.parentloop``.
Generalmente no necesitas preocuparte por esto, si provees una variable a
la plantilla llamada ``forloop`` (a pesar de que no lo recomendamos), se
llamará ``forloop.parentloop`` mientras esté dentro del bloque
   ``{% for %}``.

ifequal/ifnotequal
~~~~~~~~~~~~~~~~~~

El sistema de plantillas de Django a propósito no es un lenguaje de
programación completo y por lo tanto no permite ejecutar sentencias
arbitrarias de Python. (Más sobre esta idea en la sección "`Filosofía y
limitaciones`_"). Sin embargo, es bastante común que una plantilla requiera
comparar dos valores y mostrar algo si ellos son iguales -- Django provee la
etiqueta ``{% ifequal %}`` para este propósito.

La etiqueta ``{% ifequal %}``  compara dos valores y muestra todo lo que se
encuentra entre ``{% ifequal %}``  y ``{% endifequal %}`` si el valor es igual.

Este ejemplo compara las variables ``user`` y ``currentuser`` de la plantilla:

.. code-block:: html

    {% ifequal user currentuser %}
        <h1>Welcome!</h1>
    {% endifequal %}

Los argumentos pueden ser strings hard-codeados, con simples o dobles comillas,
lo siguiente es válido:

.. code-block:: html

    {% ifequal section 'sitenews' %}
        <h1>Site News</h1>
    {% endifequal %}

    {% ifequal section "community" %}
        <h1>Community</h1>
    {% endifequal %}

Como ``{% if %}``, la etiqueta ``{% ifequal %}`` admite un opcional
``{% else %}``:

.. code-block:: html

    {% ifequal section 'sitenews' %}
        <h1>Site News</h1>
    {% else %}
        <h1>No News Here</h1>
    {% endifequal %}

Sólo las variables de la plantilla, string, enteros y números decimales son
permitidos como argumentos para ``{% ifequal %}``. Estos son ejemplos válidos:

.. code-block:: html

    {% ifequal variable 1 %}
    {% ifequal variable 1.23 %}
    {% ifequal variable 'foo' %}
    {% ifequal variable "foo" %}

Cualquier otro tipo de variables, tales como diccionarios de Python, listas, o
booleanos, no pueden ser comparados en ``{% ifequal %}``. Estos ejemplos son
inválidos:

    {% ifequal variable True %}
    {% ifequal variable [1, 2, 3] %}
    {% ifequal variable {'key': 'value'} %}

Si necesitas comprobar cuando algo es verdadero o falso, usa la etiqueta

.. code-block:: html

``{% if %}`` en vez de ``{% ifequal %}``.

Comentarios
~~~~~~~~~~~

Al igual que en HTML o en un lenguaje de programación como Python, el lenguaje
de plantillas de Django permite comentarios. Para designar un comentario, usa
``{# #}``:

    {# This is a comment #}

Este comentario no será mostrado cuando la plantilla sea renderizada.

Un comentario no puede abarcar múltiples líneas. Esta limitación mejora la
performance del analizador sintáctico de plantillas. En la siguiente plantilla,
la salida del renderizado mostraría exactamente lo mismo que la plantilla
(esto es, la etiqueta comentario no será tomada como comentario)::

    This is a {# this is not
    a comment #}
    test.

Filtros
-------

Como explicamos anteriormente en este capítulo, los filtros de plantillas son
formas simples de alterar el valor de una variable antes de mostrarla. Los
filtros se parecen a esto:

    {{ name|lower }}

Esto muestra el valor de ``{{ name }}`` después de aplicarle el filtro
``lower``, el cual convierte el texto a minúscula. Usa un pipe (``|``)  para
aplicar el filtro.

Los filtros pueden estar en *cadena* -- eso es, la salida del uno de los filtros
puede ser aplicada al próximo. Aquí un modismo común para escapar contenido del
texto, y entonces convertir los saltos de líneas en etiquetas ``<p>``:

    {{ my_text|escape|linebreaks }}

Algunos filtros toman argumentos. Un filtro con argumento se ve de este modo:

    {{ bio|truncatewords:"30" }}

Esto muestra las primeras 30 palabras de la variable ``bio``. Los argumentos de
los filtros están siempre entre comillas dobles.

Los siguientes son algunos de los filtros más importantes; el Apéndice F cubre
el resto.

    * ``addslashes``: Agrega una con contra-barra antes de cualquier
      contra-barra, comilla simple o comilla doble. Esto es útil si el texto
      producido está incluido en un string de JavaScript.

    * ``date``: Formatea un objeto ``date`` o ``datetime`` de acuerdo al formato
      tomado como parámetro, por ejemplo:

          {{ pub_date|date:"F j, Y" }}

      El formato de los strings está definido en el Apéndice F.

    * ``escape``: Escapa ampersands(&), comillas, y corchetes del string tomado.
      Esto es usado para desinfectar datos suministrados por el usuario y
      asegurar que los datos son válidos para XML y XHTML. Específicamente,
      ``escape`` hace estas conversiones:

          * Convierte ``&`` en ``&amp;``
          * Convierte ``<`` en ``&lt;``
          * Convierte ``>`` en ``&gt;``
          * Convierte ``"`` (comilla doble) en ``&quot;``
          * Convierte ``'`` (comilla simple) en ``&#39;``

    * ``length``: Retorna la longitud del valor. Puedes usar este con una lista
      o con un string, o con cualquier objeto Python que sepa como determinar
      su longitud (o sea cualquier objeto que tenga el método ``__len__()``).

Filosofía y Limitaciones
============================

Ahora que tienes una idea del lenguaje de plantillas de Django, debemos señalar
algunas de sus limitaciones intencionales, junto con algunas filosofías detrás
de la forma en que este funciona.

Más que cualquier otro componente de la aplicación web, las opiniones de los
programadores sobre el sistema de plantillas varía extremadamente. El hecho de
que Python no sólo implemente decenas, sino cientos, de lenguajes de plantillas de
código abierto lo dice todo. Cada uno fue creado probablemente porque su
desarrollador estima que todos los existentes son inadecuados. (¡De hecho, se
dice que es un rito para los desarrolladores de Python escribir su propio
lenguaje de plantillas! Si todavía no lo has hecho, tenlo en cuenta. Es un
ejercicio divertido).

Con eso en la cabeza, debes estar interesado en saber que Django no requiere
que uses su lenguaje de plantillas. Pero Django pretende ser un completo
framework que provee todas las piezas necesarias para que el desarrollo web sea
productivo, quizás a veces es *más conveniente* usar el sistema de plantillas
de Django que otras bibliotecas de plantillas de Python, pero no es un
requerimiento estricto en ningún sentido. Como verás en la próxima
sección "`Uso de plantillas en las vistas`_", es muy fácil usar otro lenguaje
de plantillas con Django.

Aún así, es claro que tenemos una fuerte preferencia por el sistema de
plantillas de Django. El sistema de plantillas tiene raíces en la forma en que
el desarrollo web se realiza en World Online y la experiencia combinada de los
creadores de Django. Éstas con algunas de esas filosofías:

    * *La lógica de negocios debe ser separada de la presentación lógica*.
      Vemos al sistema de plantillas como una herramienta que controla la
      presentación y la lógica relacionado a esta -- y eso es todo. El sistema
      de plantillas no debería admitir funcionalidad que vaya más allá de
      este concepto básico.

      Por esta razón, es imposible llamar a código Python directamente dentro
      de las plantillas de Django. Todo "programador" está fundamentalmente
      limitado al alcance de lo que una etiqueta puede hacer. *Es* posible
      escribir etiquetas personalizadas que hagan cosas arbitrarias, pero las
      etiquetas de Django intencionalmente no permiten ejecutar código
      arbitrario de Python.

    * *La sintaxis debe ser independiente de HTML/XML*. Aunque el sistemas de
      plantillas de Django es usado principalmente para producir HTML, este
      pretende ser útil para formatos no HTML, como texto plano. Algunos otros
      lenguajes de plantillas están basados en XML, poniendo toda la lógica de
      plantilla con etiquetas XML o atributos, pero Django evita
      deliberadamente esta limitación. Requerir un XML válido para escribir
      plantillas introduce un mundo de errores humanos y mensajes difícil de
      entender, y usando un motor de XML para parsear plantillas implica un
      inaceptable nivel de overhead en el procesamiento de la plantilla.

    * *Los diseñadores se supone que se sienten más cómodos con el código HTML*.
      El sistema de plantillas no está diseñado para que las plantillas
      necesariamente sean mostradas de forma agradable en los editores WYSIWYG
      [#]_ tales como Dreamweaver. Eso es también una limitación severa y no
      permitiría que la sintaxis sea tan clara como lo es. Django espera las
      plantillas de los autores para estar cómodo editando HTML directamente.

    * *Se supone que los diseñadores no son programadores Python*. El sistema de
      plantillas de los autores reconoce que las plantillas de las páginas web
      son en al mayoría de los casos escritos por *diseñadores*, no por
      *programadores*, y por esto no debería asumir ningún conocimiento de
      Python.

      Sin embargo, el sistema también pretende acomodar pequeños grupos en los
      cuales las plantillas *sean* creadas por programadores de Python. Esto
      ofrece otro camino para extender la sintaxis del sistema escribiendo
      código Python puro. (Más de esto en el :doc:`Capítulo 10<chapter10>`).

    * *El objetivo no es inventar un lenguaje de programación*. El objetivo es
      ofrecer sólo la suficiente funcionalidad de programación, tales como
      ramificación e iteración, que son esenciales para hacer presentaciones
      relacionadas a decisiones.

Como resultado de esta filosofía, el lenguaje de plantillas de Django tiene las
siguientes limitaciones:

    * *Una plantilla no puede asignar una variable o cambiar el valor de esta*.
      Esto es posible escribiendo una etiqueta personalizada para cumplir con
      esta meta (ve el :doc:`Capítulo 10<chapter10>`), pero la pila de etiquetas de Django no
      lo permite.

    * *Una plantilla no puede llamar código Python crudo*. No hay forma de
      ingresar en "modo Python" o usar sentencias puras de Python. De nuevo,
      esto es posible creando plantillas personalizadas, pero la pila de
      etiquetas de Django no lo permiten.

Uso de plantillas en las vistas
================================

Has aprendido el uso básico del sistema de plantillas; ahora vamos a usar este
conocimiento para crear una vista. Recordemos la vista ``current_datetime`` en
``mysite.views``, la que comenzamos en el capítulo anterior. Se veía como
esto:

.. code-block:: python

    from django.http import HttpResponse
    import datetime

    def current_datetime(request):
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return HttpResponse(html)

Vamos a cambiar esta vista usando el sistema de plantillas de Django. Primero,
podemos pensar en algo como esto:

.. code-block:: python

    from django.template import Template, Context
    from django.http import HttpResponse
    import datetime

    def current_datetime(request):
        now = datetime.datetime.now()
        t = Template("<html><body>It is now {{ current_date }}.</body></html>")
        html = t.render(Context({'current_date': now}))
        return HttpResponse(html)

Seguro, esto usa el sistema de plantillas, pero no soluciona el problema que
planteamos en la introducción de este capítulo. A saber, la plantilla sigue
estando embebida en el código Python. Vamos a solucionar esto poniendo la
plantilla en un *archivo separado*, que la vista cargará.

Puedes primer considerar guardar la plantilla en algún lugar del disco y usar
las funcionalidades de Python para abrir y leer el contenido de la plantilla.
Esto puede verse así, suponiendo que la plantilla esté guardada en
``/home/djangouser/templates/mytemplate.html``:

.. code-block:: python

    from django.template import Template, Context
    from django.http import HttpResponse
    import datetime

    def current_datetime(request):
        now = datetime.datetime.now()
        # Simple way of using templates from the filesystem.
        # This doesn't account for missing files!
        fp = open('/home/djangouser/templates/mytemplate.html')
        t = Template(fp.read())
        fp.close()
        html = t.render(Context({'current_date': now}))
        return HttpResponse(html)

Esta aproximación, sin embargo, es poco elegante por estas razones:

    * No maneja el caso en que no encuentre el archivo. Si el archivo
      ``mytemplate.html`` no existe o no es accesible para lectura, la llamada a
      ``open()`` levantará la excepción ``IOError``.

    * Involucra la ruta de tu plantilla. Si vas a usar esta técnica para cada
      una de las funciones de las vistas, estarás duplicando rutas de
      plantillas. ¡Sin mencionar que esto implica teclear mucho más!

    * Incluye una cantidad aburrida de código repetitivo. Tienes mejores cosas
      para hacer en vez de escribir ``open()``, ``fp.read()`` y ``fp.close()``
      cada vez que cargas una plantilla

Para solucionar estos problemas, usamos *cargadores de plantillas* y
*directorios de plantillas*, los cuales son descriptos en las secciones que
siguen.

Cargadores de plantillas
==========================

Django provee una práctica y poderosa API [#]_ para cargar plantillas del
disco, con el objetivo de quitar la redundancia en la carga de la plantilla y
en las mismas plantillas.

Para usar la API para cargar plantillas, primero necesitas indicarle al
framework dónde están guardadas tus plantillas. El lugar para hacer esto es en
el *archivo de configuración*.

El archivo de configuración de Django es el lugar para poner configuraciones
para tu instancia de Django (aka [#]_ tu proyecto de Django). Es un simple
módulo de Python con variables, una por cada configuración.

Cuando ejecutaste ``django-admin.py startproject mysite`` en el :doc:`Capítulo 2<chapter02>`,
el script creó un archivo de configuración por omisión por ti, llamado
``settings.py``. Échale un vistazo al contenido del archivo. Este contiene
variables que se parecen a estas (no necesariamente en este orden):

    * DEBUG = True
    * TIME_ZONE = 'America/Chicago'
    * USE_I18N = True
    * ROOT_URLCONF = 'mysite.urls'

Éstas se explican por sí solas; las configuraciones y sus respectivos valores
son simples variables de Python. Como el archivo de configuración es sólo un
módulo plano de Python, puedes hacer cosas dinámicas como verificar el valor de
una variable antes de configurar otra. (Esto también significa que debes
evitar errores de sintaxis de Python en los archivos de configuración).

Cubriremos el archivo de configuración en profundidad en el :doc:`Apéndice E<appendixE>`, pero por
ahora, veamos la variable de configuración ``TEMPLATE_DIRS``. Esta variable le
indica al mecanismo de carga de plantillas dónde buscar las plantillas. Por
omisión, ésta es una tupla vacía. Elige un directorio en el que desees guardar
tus plantillas y agrega este a ``TEMPLATE_DIRS``, así:

    * TEMPLATE_DIRS = ('/home/django/mysite/templates',)

Hay algunas cosas para notar:

    * Puedes especificar cualquier directorio que quieras, siempre y cuando la
      cuenta de usuario en el cual se ejecuta el servidor web tengan acceso al
      directorio y su contenido. Si no puedes pensar en un lugar apropiado para
      poner las plantillas, te recomendamos crear un directorio ``templates``
      dentro del proyecto de Django (esto es, dentro del directorio ``mysite``
      que creaste en el :doc:`Capítulo 2<chapter02>` , si vienes siguiendo los ejemplos a lo
      largo del libro).

    * ¡No olvides la coma al final del string del directorio de plantillas!
      Python requiere una coma en las tuplas de un solo elemento para
      diferenciarlas de una expresión de paréntesis. Esto es común en los
      usuarios nuevos.

      Si quieres evitar este error, puedes hacer ``TEMPLATE_DIRS`` una lista,
      en vez de una tupla, porque un solo elemento en una lista no requiere
      estar seguido de una coma:

      *TEMPLATE_DIRS = ['/home/django/mysite/templates']

      Una tupla es un poco más correcta semánticamente que una lista (las
      tuplas no pueden cambiar luego de ser creadas, y nada podría cambiar las
      configuraciones una vez que fueron leídas), nosotros recomendamos usar
      tuplas para la variable ``TEMPLATE_DIRS``.

    * Si estás en Windows, incluye tu letra de unidad y usa el estilo de Unix
      para las barras en vez de barras invertidas, como sigue::

          TEMPLATE_DIRS = ('C:/www/django/templates',)

    * Es más sencillo usar rutas absolutas (esto es, las rutas de directorios
      comienzan desde la raíz del sistema de archivos). Si quieres sen un poco
      más flexible e independiente, también, puedes tomar el hecho de que el
      archivo de configuración de Django es sólo código de Python y construir la
      variable ``TEMPLATE_DIRS`` dinámicamente, por ejemplo:
      
      .. code-block:: python

          import os.path

          TEMPLATE_DIRS = (
              os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
          )

      Este ejemplo usa la variable de Python "mágica" ``__file__``, la cual es
      automáticamente asignada al nombre del archivo del módulo de Python en
      el que se encuentra el código.

Con la variable ``TEMPLATE_DIRS`` configurada, el próximo paso es cambiar el
código de vista que usa la funcionalidad de carga de plantillas de Django,
para no incluir la ruta a la plantilla. Volvamos a nuestra vista
``current_datetime``, vamos a cambiar esta como sigue:

.. code-block:: python

    from django.template.loader import get_template
    from django.template import Context
    from django.http import HttpResponse
    import datetime

    def current_datetime(request):
        now = datetime.datetime.now()
        t = get_template('current_datetime.html')
        html = t.render(Context({'current_date': now}))
        return HttpResponse(html)

En este ejemplo, usamos la función ``django.template.loader.get_template()``
en vez de cargar la plantilla desde el sistemas de archivos manualmente. La
función ``get_template()`` toma el nombre de la plantilla como argumento,
se da cuenta de dónde está la plantilla en el sistema de archivos, lo abre, y
retorna un objeto ``Template`` compilado.

Si ``get_template()`` no puede encontrar la plantilla con el nombre pasado, esta
levanta una excepción ``TemplateDoesNotExist``. Para ver que cómo se ve eso,
ejecutar el servidor de desarrollo de Django otra vez, como en el :doc:`Capítulo 3<chapter03>`,
ejecutando ``python manage.py runserver`` en el directorio de tu proyecto de
Django. Luego, escribe en tu navegador la página que activa la vista
``current_datetime`` (o sea, ``http://127.0.0.1:8000/time/``). Asumiendo que tu
variable de configuración ``DEBUG`` está asignada a ``True`` y todavía no has
creado la plantilla ``current_datetime.html``, deberías ver una página de error
de Django resaltando el error ``TemplateDoesNotExist``.

.. image:: graficos/chapter04/missing_template.png
   :alt: Screenshot of a "TemplateDoesNotExist" error.

Figura 4-1: La página de error que se muestra cuando una plantilla no se encuentra

Esta página de error es similar a la que explicamos en el :doc:`Capítulo 3<capitulo03>`, con una
pieza adicional de información de depuración: una sección "Postmortem del
cargador de plantillas". Esta sección te indica qué plantilla intentó cargar
Django acompañado de una razón para cada intento fallido (por ej. "File does not
exist"). Esta información es invaluable cuando hacemos depuración de
errores de carga de plantillas.

Como probablemente puedas distinguir de los mensajes de error de la Figura 4-1,
Django intentó buscar una plantilla combinando el directorio de la variable
``TEMPLATE_DIRS`` con el nombre de la plantilla pasada a ``get_template()``.
Entonces si tu variable ``TEMPLATE_DIRS`` contiene ``'/home/django/templates'``,
Django buscará ``'/home/django/templates/current_datetime.html'``.  Si
``TEMPLATE_DIRS`` contiene más que un directorio, cada uno de estos es
examinado hasta que se encuentre la plantilla o hasta que no haya más
directorios.

Continuando, crea el archivo ``current_datetime.html`` en tu directorio de
plantillas usando el siguiente código:

.. code-block:: html

    <html><body>It is now {{ current_date }}.</body></html>

Refresca la página en tu navegador web, y deberías ver la página completamente
renderizada.

render_to_response()
--------------------

Debido a que es común cargar una plantilla, rellenar un ``Context``, y retornar
un objeto ``HttpResponse`` con el resultado de la plantilla renderizada, Django
provee un atajo que te deja hacer estas cosas en una línea de código.  Este
atajo es la función llamada ``render_to_response()``, la cual se encuentra en el
módulo ``django.shortcuts``. La mayoría de las veces, usarás
``render_to_response()`` en vez de cargar las plantillas y crear los objetos
``Context`` y ``HttpResponse`` manualmente.

Aquí está el ejemplo actual ``current_datetime`` reescrito utilizando
``render_to_response()``:

.. code-block:: python

    from django.shortcuts import render_to_response
    import datetime

    def current_datetime(request):
        now = datetime.datetime.now()
        return render_to_response('current_datetime.html', {'current_date': now})

¡Qué diferencia! Vamos paso a paso a través de los cambios del código:

    * No tenemos que importar ``get_template``, ``Template``, ``Context``, o
      ``HttpResponse``. En vez de esto, importamos
      ``django.shortcuts.render_to_response``.  ``import datetime``  se
      mantiene.

    * En la función ``current_datetime``, seguimos calculando ``now``, pero la
      carga de la plantilla, creación del contexto, renderización de esta, y de
      la creación de ``HttpResponse`` se encarga la llamada a
      ``render_to_response()``.  Como ``render_to_response()`` retorna un objeto
      ``HttpResponse``, podemos simplemente ``retornar`` ese valor en la vista.

El primer argumento de ``render_to_response()`` debe ser el nombre de la
plantilla a utilizar. El segundo argumento, si es pasado, debe ser un
diccionario para usar en la creación de un ``Context`` para esa plantilla. Si
no se le pasa un segundo argumento, ``render_to_response()`` utilizará un
diccionario vacío.


El truco locals()
------------------

Considera nuestra última versión de ``current_datetime``:

.. code-block:: python

    def current_datetime(request):
        now = datetime.datetime.now()
        return render_to_response('current_datetime.html', {'current_date': now})

Muchas veces, como en este ejemplo, buscarás tú mismo calcular algunos valores,
guardando ellos en variables (por ej. ``now`` en el código anterior), y pasando
estas a la plantilla. Particularmente los programadores perezosos notarán que
es ligeramente redundante tener esos nombres en variables temporales *y*
tener nombres para las variables de la plantilla. No sólo que esto es
redundante, sino que también hay que teclear más.

Entonces si eres uno de esos programadores perezosos y quieres ahorrar código
particularmente conciso, puedes tomar la ventaja de la función built-in de
Python llamada ``locals()``. Esta retorna un diccionario mapeando todos los
nombres de variables locales con sus valores. De esta manera, la vista anterior
podría reescribirse como sigue:

.. code-block:: python

    def current_datetime(request):
        current_date = datetime.datetime.now()
        return render_to_response('current_datetime.html', locals())

Aquí, en vez de especificar manualmente el diccionario al contexto como antes,
pasamos el valor de ``locals()``, el cual incluye todas las variables definidas
hasta ese punto en la ejecución de la función. Como una consecuencia,
renombramos el nombre de la variable ``now`` a ``current_date``, porque esta es
la variable que especificamos en la plantilla. En este ejemplo, ``locals()`` no
ofrece una *gran* mejora, pero esta técnica puede ahorrar un poco de tipeo si
tienes plantillas con varias variables definidas -- o si eres perezoso.

Una cosa en la que tiene que tener cuidado cuando usas ``locals()`` es que esta
incluye *todas* las variables locales, con lo cual quizás conste de más
variables de las cuales quieres tener acceso en la plantilla. En el ejemplo
anterior, ``locals()`` también incluirá ``request``. Depende de tu aplicación
saber si esto es de importancia.

La última cosa a considerar es que ``locals()`` provoca un poco sobrecarga,
porque cuando es llamado, Python crea el diccionario dinámicamente. Si
especificas el diccionario al contexto manualmente, evitas esta sobrecarga.

Subdirectorios en get_template()
--------------------------------

Puede ser un poco inmanejable guardar todas las plantillas en un solo
directorio. Quizás quieras guardar las plantillas en subdirectorios del
directorio de tus plantillas, y esto está bien. De hecho, recomendamos hacerlo;
algunas de las características más avanzadas de Django (como las vistas
genéricas del sistema, las cuales veremos en el :doc:`Capítulo 9<chapter09>`) esperan esta
distribución de las plantillas como una convención por omisión.

Guardar las plantillas en subdirectorios de tu directorio de plantilla es
fácil. En tus llamadas a ``get_template()``, sólo incluye el nombre del
subdirectorio y una barra antes del nombre de la plantilla, así:

.. code-block:: python

    t = get_template('dateapp/current_datetime.html')

Debido a que ``render_to_response()`` es un pequeño envoltorio de
``get_template()``, puedes hacer lo mismo con el primer argumento de
``render_to_response()``.

No hay límites para la profundidad del árbol de subdirectorios. Siéntete libre
de usar tantos como quieras.

.. admonition::

    Los usuario de Windows, asegúrense de usar barras comunes en vez de barras
    invertidas. ``get_template()`` asume el estilo de designación de archivos
    de Unix.

La etiqueta de plantilla ``include``
--------------------------------------

Ahora que vimos el mecanismo para cargar plantillas, podemos introducir una
plantilla built-in que tiene una ventaja para esto: ``{% include %}``. Esta
etiqueta te permite incluir el contenido de otra plantilla. El argumento para
esta etiqueta debería ser el nombre de la plantilla a incluir, y el nombre de
la plantilla puede ser una variable string hard-coded (entre comillas), entre
simples o dobles comillas. En cualquier momento que tengas el mismo código en
varias etiquetas, considera utilizar un ``{% include %}`` para eliminar lo
duplicado.

Estos dos ejemplos incluyen el contenido de la plantilla ``nav.html``. Los
ejemplos son equivalentes e ilustran que cualquier modo de comillas está
permitido:

.. code-block:: html

    {% include 'nav.html' %}
    {% include "nav.html" %}

Este ejemplo incluye el contenido de la plantilla ``includes/nav.html``:

.. code-block:: html

    {% include 'includes/nav.html' %}

Este ejemplo incluye el contenido de la plantilla cuyo nombre se encuentra en
la variable ``template_name``:

.. code-block:: html

    {% include template_name %}

Como en ``get_template()``, el nombre del archivo de la plantilla es
determinado agregando el directorio de plantillas tomado de ``TEMPLATE_DIRS``
para el nombre de plantilla solicitado.

Las plantillas incluidas son evaluadas con el contexto de la plantilla en la
cual está incluida.

Si una plantilla no encuentra el nombre tomado, Django hará una de estas dos
cosas:

    * Si ``DEBUG`` es ``True``, verás la excepción ``TemplateDoesNotExist``
      sobre la página de error de Django.

    * Si ``DEBUG`` es ``False``, la etiqueta fallará silenciosamente, sin
      mostrar nada en el lugar de la etiqueta.

Herencia de plantillas
=======================

Nuestras plantillas de ejemplo hasta el momento han sido fragmentos de HTML,
pero en el mundo real, usarás el sistema de plantillas de Django para crear
páginas HTML enteras. Esto conduce a un problema común del desarrollo web:
¿Cómo reducimos la duplicación y redundancia de las áreas comunes de las
páginas, como por ejemplo, los paneles de navegación?

Una forma clásica de solucionar este problema es usar *includes*, insertando
dentro de las páginas HTML a "incluir" una página dentro de otra. Es más,
Django admite esta aproximación, con la etiqueta ``{% include %}``
anteriormente descripta. Pero la mejor forma de solucionar este problema con
Django es usar una estrategia más elegante llamada *herencia de plantillas*.

En esencia, la herencia de plantillas te deja construir una plantilla base
"esqueleto" que contenga todas las partes comunes de tu sitio y definir
"bloques" que los hijos puedan sobreescribir.

Veamos un ejemplo de esto creando una plantilla completa para nuestra vista
``current_datetime``, editando el archivo ``current_datetime.html``:

.. code-block:: html
 
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
    <html lang="en">
    <head>
        <title>The current time</title>
    </head>
    <body>
        <h1>My helpful timestamp site</h1>
        <p>It is now {{ current_date }}.</p>

        <hr>
        <p>Thanks for visiting my site.</p>
    </body>
    </html>

Esto se ve bien, pero ¿Qué sucede cuando queremos crear una plantilla para otra
vista --digamos, ¿La vista ``hours_ahead`` del :doc:`Capítulo 3<chapter03>`? Si queremos
hacer nuevamente una agradable, válida, y completa plantilla HTML, crearíamos
algo como:

.. code-block:: html 

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
    <html lang="en">
    <head>
        <title>Future time</title>
    </head>
    <body>
        <h1>My helpful timestamp site</h1>
        <p>In {{ hour_offset }} hour(s), it will be {{ next_time }}.</p>

        <hr>
        <p>Thanks for visiting my site.</p>
    </body>
    </html>

Claramente, estaríamos duplicando una cantidad de código HTML. Imagina si
tendríamos más sitios típicos, incluyendo barra de navegación, algunas hojas de
estilo, quizás algo de JavaScript -- terminaríamos poniendo todo tipo de HTML
redundante en cada plantilla.

La solución a este problema usando includes en el servidor es sacar
factor común de ambas plantillas y guardarlas en recortes de
plantillas separados, que luego son incluidos en cada plantilla. Quizás
quieras guardar la parte superior de la plantilla en un archivo
llamado ``header.html``:

.. code-block:: html

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
    <html lang="en">
    <head>

Y quizás quieras guardar la parte inferior en un archivo llamado
``footer.html``:

.. code-block:: html

        <hr>
        <p>Thanks for visiting my site.</p>
    </body>
    </html>

Con una estrategia basada en includes, la cabecera y la parte de abajo son
fáciles. Es el medio el que queda desordenado. En este ejemplo, ambas páginas
contienen un título -- ``<h1>My helpful timestamp site</h1>``-- pero ese título
no puede encajar dentro de ``header.html`` porque ``<title>`` en las dos páginas
es diferente. Si incluimos ``<h1>`` en la cabecera, tendríamos que incluir
``<title>``, lo cual no permitiría personalizar este en cada página. ¿Ves a
dónde queremos llegar?

El sistema de herencia de Django soluciona estos problemas. Lo puedes pensar a
esto como la versión contraria a la del lado del servidor. En vez de definir
los pedazos que son *comunes*, defines los pedazos que son *diferentes*.

El primer paso es definir una *plantilla base*-- un "esquelete" de tu página
que las *plantillas hijas* llenaran luego. Aquí hay una platilla para nuestro
ejemplo actual:

.. code-block:: html


    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
    <html lang="en">
    <head>
        <title>{% block title %}{% endblock %}</title>
    </head>
    <body>
        <h1>My helpful timestamp site</h1>
        {% block content %}{% endblock %}
        {% block footer %}
        <hr>
        <p>Thanks for visiting my site.</p>
        {% endblock %}
    </body>
    </html>

Esta plantilla, que llamamos ``base.html``, define un documento esqueleto
HTML simple que usaremos para todas las páginas del sitio. Es trabajo
de las plantillas hijas sobreescribir, agregar, dejar vacío el contenido de los
bloques. (Si estás lo siguiendo desde casa, guarda este archivo en tu
directorio de plantillas).

Usamos una etiqueta de plantilla aquí que no hemos visto antes: la etiqueta
``{% block %}``. Todas las etiquetas ``{% block %}`` le indican al motor de
plantillas que una plantilla hijo quizás sobreescriba esa porción de la
plantilla.

Ahora que tenemos una plantilla base, podemos modificar nuestra plantilla
existente ``current_datetime.html`` para usar esto:

.. code-block:: python

    {% extends "base.html" %}

    {% block title %}The current time{% endblock %}

    {% block content %}
    <p>It is now {{ current_date }}.</p>
    {% endblock %}

Como estamos en este tema, vamos a crear una plantilla para la vista
``hours_ahead`` del :doc:`Capítulo 3<chapter03>`. (Si lo estás siguiendo junto con el código,
te dejamos cambiar ``hours_ahead`` para usar el sistema de plantilla). Así sería
el resultado:

.. code-block:: html

    {% extends "base.html" %}

    {% block title %}Future time{% endblock %}

    {% block content %}
    <p>In {{ hour_offset }} hour(s), it will be {{ next_time }}.</p>
    {% endblock %}

¿No es hermoso? Cada plantilla contiene sólo el código que es *único* para esa
plantilla. No necesita redundancia. Si necesitas hacer un cambio grande en el
diseño del sitio, sólo cambia ``base.html``, y todas las otras plantillas
reflejarán el efecto inmediatamente.

Veamos cómo trabaja. Cuando cargamos una plantilla ``current_datetime.html``,
el motor de plantillas ve la etiqueta ``{% extends %}``, nota que esta
plantilla es la hija de otra. El motor inmediatamente carga la plantilla padre
--en este caso, ``base.html``.

Hasta este punto, el motor de la plantilla nota las tres etiquetas ``{% block %}``
en ``base.html`` y reemplaza estos bloques por el contenido de la plantilla
hija. Entonces, el título que definimos en ``{% block title %}`` será usado,
así como ``{% block content %}``.

Nota que desde la plantilla hija no definimos el bloque ``footer``, entonces
el sistema de plantillas usa el valor desde la plantilla padre. El contenido de
la etiqueta ``{% block %}`` en la plantilla padre es siempre usado como un plan
alternativo.

La herencia no afecta el funcionamiento del contexto, y puedes usar tantos
niveles de herencia como necesites. Una forma común de utilizar la herencia es
el siguiente enfoque de tres niveles:

    1. Crear una plantilla ``base.html`` que contenga el aspecto principal de
       tu sitio. Esto es lo que rara vez cambiará, si es que alguna vez cambia.

    2. Crear una plantilla ``base_SECTION.html`` para cada "sección" de tu
       sitio (por ej. ``base_photos.html`` y ``base_forum.html``). Esas
       plantillas heredan de ``base.html`` e incluyen secciones específicas de
       estilo/diseño.

    3. Crear una plantilla individual para cada tipo de página, tales como
       páginas de formulario o galería de fotos. Estas plantillas heredan de la
       plantilla de la sección apropiada.

Esta aproximación maximiza la reutilización de código y hace fácil el agregado
de elementos para compartir áreas, como puede ser un navegador de sección.

Aquí hay algunos consejos para el trabajo con herencia de plantillas:

    * Si usas ``{% extends %}`` en la plantilla, esta debe ser la primer
      etiqueta de esa plantilla. En otro caso, la herencia no funcionará.

    * Generalmente, cuanto más etiquetas ``{% block %}`` tengas en tus
      plantillas, mejor. Recuerda, las plantillas hijas no tienen que definir
      todos los bloques del padre, entonces puedes rellenar un número razonable
      de bloques por omisión, y luego definir sólo lo que necesiten las
      plantillas hijas. Es mejor tener más conexiones que menos.

    * Si encuentras código duplicado en un número de plantillas, esto
      probablemente signifique que debes mover ese código a un ``{% block %}``
      en la plantilla padre.

    * Si necesitas obtener el contenido de un bloque desde la plantilla padre,
      la variable ``{{ block.super }}`` hará este truco. Esto es útil si
      quieres agregar contenido del bloque padre en vez de sobreescribirlo
      completamente.

    * No puedes definir múltiples etiquetas ``{% block %}`` con el mismo nombre
      en la misma plantilla. Esta limitación existe porque una etiqueta bloque
      trabaja en ambas direcciones. Esto es, una etiqueta bloque no sólo provee
      un agujero a llenar, sino que también define el contenido que llenará ese
      agujero en el *padre*. Si hay dos nombres similares de etiquetas ``{%
      block %}`` en una plantilla, el padre de esta plantilla puede no saber
      cual de los bloques usar.

    * El nombre de plantilla pasado a ``{% extends %}`` es cargado usando el
      mismo método que ``get_template()``. Esto es, el nombre de la plantilla
      es agregado a la variable ``TEMPLATE_DIRS``.

    * En la mayoría de los casos, el argumento para ``{% extends %}`` será un
      string, pero también puede ser una variable, si no sabes el nombre de la
      plantilla padre hasta la ejecución. Esto te permite hacer cosas
      divertidas, dinámicas.


¿Qué sigue?
===========

Los sitios web más modernos son *manejados con una base de datos*: el contenido
de la página web está guardado en una base de datos relacional. Esto permite
una clara separación de los datos y la lógica (de la misma manera que las
vistas y las etiquetas permiten una separación de la lógica y la vista).

El :doc:`próximo capítulo<chapter05>` cubre las herramientas que Django brinda para
interactuar con la base de datos.


.. [#] \N. del T.: hard-coded
.. [#] \N. del T.: WYSIWYG: What you see is what you get (Lo que ves es lo que obtienes)
.. [#] \N. del T.: API: Application Program Interface (Interfaz de programación de aplicaciones)
.. [#] \N. del T.: aka: Also Know As (También conocido como)

