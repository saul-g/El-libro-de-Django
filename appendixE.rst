=========================================================
Apéndice E: Etiquetas de plantilla y filtros predefinidos
=========================================================


En él :doc:`capítulo 4<chapter04>` se hace una introducción a las etiquetas de
plantilla y filtros más utilizados, pero Django incorpora muchos más. En este
apéndice se listan todas las que estaban incluidas en el momento en que se
escribió el libro, pero se añaden nuevas etiquetas y filtros de forma regular.

La mejor referencia de todas las etiquetas y filtros disponibles se encuentra
en la propia página de administración. Allí se incluye una referencia completa
de todas las etiquetas y filtros que hay disponibles para una determinada
aplicación.  Para verla, sólo tienes que pulsar con el ratón en el enlace de
documentación que está en la esquina superior derecha de la página.

Las secciones de **etiquetas y filtros** de esta documentación incluirán tanto las
etiquetas y filtros predefinidos (de hecho, las referencias de este apéndice
vienen directamente de ahí) como aquellas etiquetas y filtros que se hayan
incluido o escrito para la aplicación.

Este apéndice será más útil, por tanto, para aquellos que no dispongan de acceso
a la interfaz de administración. Como Django es altamente configurable, las
indicaciones de la interfaz de administración deben ser consideradas como la
documentación más actualizada y, por tanto, la de mayor autoridad.

Etiquetas predefinidas
======================

.. templatetag:: autoescape

autoescape
----------

Controla el comportamiento actual del auto-escape. Esta etiqueta toma como
argumento tanto  a:  ``on`` y ``off`` y determina si el auto-escapeo están dentro
del bloque.

Cuando el auto-escapeo esta activado, todas las variables contenidas que contenga
HTML serán escapadas antes de mostrar el resultado de la salida (pero después de
que cualquier filtro se haya aplicado). Esto es equivalente a manualmente
aplicar el filtro ``escape`` a cada variable.

La única excepción son las variables que están marcadas como "safe" para
autoescape, ya sea por la clave que pobló la variable, o porque se ha aplicado
el filtro ``safe`` o ``escape``.

Forma de usarlo:

.. code-block:: html+django

    {% autoescape on %}
        {{ body }}
    {% endautoescape %}

.. templatetag:: block

block
-----

Define un bloque que puede ser sobrescrito por las plantillas derivadas. Véase
la sección acerca de herencia de plantillas en él :doc:`capítulo 4<chapter04>`
para más información.

.. templatetag:: comment

comment
-------

Ignora todo lo que aparece entre ``{% comment %}`` y ``{% endcomment %}``.
Como nota opcional,  se puede insertar en la primera etiqueta. Por ejemplo,
es útil para comentar fuera del código para documentar, porqué el código fue
deshabilitado.

Ejemplo de su uso:

.. code-block:: html+django

    <p>Renderizar texto con {{ fecha_publicacion|date:"c" }}</p>

    {% comment "Nota opcional" %}
        <p>Comentado fuera del texto {{ creado|date:"c" }}</p>
    {% endcomment %}

.. templatetag:: csrf_token

csrf_token
-----------

Esta etiqueta es usada para protección  CSRF.

.. templatetag:: cycle

cycle
-----

Rota una cadena de texto entre diferentes valores, cada vez que
aparece la etiqueta.

Dentro de un bucle, el valor rota entre los distintos valores
disponibles en cada iteración del bucle:

.. code-block:: html+django

    {% for o in some_list %}
        <tr class="{% cycle row1,row2 %}">
            ...
        </tr>
    {% endfor %}

Fuera de un bucle, hay que asignar un nombre único la primera vez que se usa
la etiqueta, y luego hay que incluirlo ese nombre en las sucesivas llamadas:

.. code-block:: html+django

        <tr class="{% cycle row1,row2,row3 as rowcolors %}">...</tr>
        <tr class="{% cycle rowcolors %}">...</tr>
        <tr class="{% cycle rowcolors %}">...</tr>

Se pueden usar cualquier número de valores, separándolos por comas. Asegúrate
de no poner espacios entre los valores, sólo comas.

.. templatetag:: debug

debug
-----

Muestra un montón de información para depuración de errores, incluyendo el
contexto actual y los módulos importados.

.. templatetag:: extends

extends
-------

Sirve para indicar que esta plantilla extiende una plantilla padre.

Esta etiqueta se puede usar de dos maneras:

* ``{% extends "base.html" %}`` (Con las comillas) interpreta literalmente
  ``"base.html"`` como el nombre de la plantilla  a extender.

* ``{% extends variable %}`` usa el valor de ``variable``. Si
  la variable apunta a una cadena de texto, Django usará
  dicha cadena como el nombre de la plantilla padre. Si la variable
  es un objeto de tipo ``Template``, se usará ese mismo objeto como
  plantilla base.

En él :doc:`capítulo 4<chapter04>` podrás encontrar muchos ejemplo de uso de esta
etiqueta.

.. templatetag:: filter

filter
------

Filtra el contenido de una variable.

Los filtros pueden ser encadenados sucesivamente (La salida
de uno es la entrada del siguiente), y pueden tener argumentos, como
en la sintaxis para variables

He aquí un ejemplo:

.. code-block:: html+django

    {% filter escape|lower %}
        Este texto será escapado y aparecerá en minúsculas
    {% endfilter %}

.. templatetag:: firstof

firstof
-------

Presenta como salida la primera de las variables que se le pasen
que evalúe como no falsa. La salida será nula si todas las
variables pasadas valen ``False``.

He aquí un ejemplo:

.. code-block:: html+django

    {% firstof var1 var2 var3 %}

Equivale a:

.. code-block:: html+django

    {% if var1 %}
        {{ var1 }}
    {% else %}{% if var2 %}
        {{ var2 }}
    {% else %}{% if var3 %}
        {{ var3 }}
    {% endif %}{% endif %}{% endif %}

.. templatetag:: for

for
---

Itera sobre cada uno de los elementos de un lista o *array*. Por ejemplo, para
mostrar una lista de libros, cuyos  títulos estén en la ``lista_libros``,
podríamos hacer esto:

.. code-block:: html+django

    <ul>
    {% for libro in lista_libros %}
        <li>{{ libro.titulo }}</li>
    {% endfor %}
    </ul>

También se puede iterar la lista en orden inverso usando
``{% for obj in list reversed %}``.

Dentro de un bucle, la propia sentencia ``for`` crea una serie de
variables. A estas variables se puede acceder únicamente dentro del
bucle. Las distintas variables se explican en la Tabla F-1.

.. table:: Variables accesibles dentro de bucles {% for %}

    ==========================  ====================================================
        Variable                    Descripción
    ==========================  ====================================================
    ``forloop.counter``         El número de vuelta o iteración actual (usando
                                un índice basado en 1).
    ``forloop.counter0``        El número de vuelta o iteración actual (usando
                                un índice basado en 0).
    ``forloop.revcounter``      El número de vuelta o iteración contando desde
                                el fin del bucle  (usando un índice basado en 1).
    ``forloop.revcounter0``     El número de vuelta o iteración contando desde
                                el fin del bucle  (usando un índice basado en 0).
    ``forloop.first``
                                ``True`` si es la primera iteración.
    ``forloop.last``
                                ``True`` si es la última iteración.
    ``forloop.parentloop``      Para bucles anidados, es una referencia al bucle
                                externo.
    ==========================  ====================================================


for ... empty
^^^^^^^^^^^^^

La etiqueta  ``for`` toma una cláusula  opcional ``{% empty %}`` cuando el
texto es mostrado,  si el *array* esta vacio o no puede ser encontrado.

.. code-block:: html+django

    <ul>
    {% for atleta in lista_atletas %}
        <li>{{ atleta.nombre }}</li>
    {% empty %}
        <li>Lo sentimos, no hay atletas en esta lista.</li>
    {% endfor %}
    </ul>

El ejemplo anterior es equivalente a (pero más corto, limpio y posiblemente
mas rápido) a lo siguiente:

.. code-block:: html+django

    <ul>
      {% if lista_atletas %}
        {% for atleta in lista_atletas %}
          <li>{{ atleta.nombre }}</li>
        {% endfor %}
      {% else %}
        <li>Lo sentimos, no hay atletas en esta lista.</li>
      {% endif %}
    </ul>

.. templatetag:: if

if
--

La etiqueta ``{% if %}`` evalúa una variable. Si dicha variable se evalúa como
una expresión "verdadera" (Es decir, que el valor exista, no esté vacía y no
es el valor booleano ``False``), se muestra el contenido del bloque:

.. code-block:: html+django

    {% if lista_atletas %}
        Número de atletas: {{ lista_atletas|length }}
    {% else %}
        No hay atletas.
    {% endif %}

Si la lista ``lista_atletas`` no está vacía, podemos mostrar el
número de atletas con la expresión ``{{ lista_atletas|length }}``

Además, como se puede ver en el ejemplo, la etiqueta ``if`` puede
tener un bloque opcional ``{% else %}`` que se mostrará en el
caso de que la evaluación de falso.

Operadores booleanos
--------------------

Las etiquetas ``if`` pueden usar operadores lógicos como
``and``, ``or`` y ``not`` para evaluar expresiones más
complejas:

.. code-block:: html+django

    {% if lista_atletas and lista_entrenadores %}
       Los atletas y los entrenadores están disponibles
    {% endif %}

    {% if not lista_atletas %}
        No hay atletas.
    {% endif %}

    {% if lista_atletas or lista_entrenadores %}
        Hay algunos atletas o algunos entrenadores.
    {% endif %}

    {% if not lista_atletas or lista_entrenadores %}
        No hay atletas o hay algunos entrenadores
    {% endif %}

    {% if lista_atletas and not lista_entrenadores %}
        Hay algunos atletas y absolutamente ningún entrenador.
    {% endif %}

La etiqueta ``if`` no admite, sin embargo, mezclar los operadores
``and`` y ``or`` dentro de la misma comprobación, porque la orden
de aplicación de los operadores lógicos sería ambigua. Por ejemplo,
el siguiente código es inválido::

    {% if lista_atletas and lista_entrenadores or lista_animadoras %}

Para combinar operadores ``and`` y ``or``, puedes usar sentencias
``if`` anidadas, como en el siguiente ejemplo:

.. code-block:: html+django

    {% if lista_atletas %}
        {% if lista_entrenadores or lista_animadoras %}
            ¡Tenemos atletas, y ya sea entrenadores o porristas!
        {% endif %}
    {% endif %}

Es perfectamente posible usar varias veces un operador lógico, siempre
que sea el mismo siempre. Por ejemplo, el siguiente código es válido::

    {% if lista_atletas or lista_entrenadores or lista_animadoras or lista_profesores %}

Las etiquetas ``if`` pueden usarse con operadores ``==``, ``!=``, ``<``, ``>``,
``<=``, ``>=`` e ``in``, los cuales funcionan de la siguiente forma:


operador: ``==``
^^^^^^^^^^^^^^^^

Igualdad. Por ejemplo:

.. code-block:: html+django

    {% if mivariable == "x" %}
        Esta variable aparece si ``mivariable`` es igual a la cadena "x"
    {% endif %}

operador: ``!=``
^^^^^^^^^^^^^^^^

Desigualdad. Por ejemplo:

.. code-block:: html+django

    {% if mi_variable != "x" %}
      Esta cadena aparece si mi ``mi_variable`` no es igual a la cadena "x",
      o si ``mi_variable`` no se encuentra en el contexto.
    {% endif %}

operador:  ``<``
^^^^^^^^^^^^^^^^

Menor que. Por ejemplo:

.. code-block:: html+django

    {% if mi_variable < 100 %}
      Esta cadena aparece si ``mi_variable`` es menor que 100.
    {% endif %}

operador: ``>``
^^^^^^^^^^^^^^^

Mayor que. Por ejemplo:

.. code-block:: html+django

    {% if mi_variable > 0 %}
      Esta cadena aparece si ``mi_variable```es mayor que 0.
    {% endif %}

operador: ``<=``
^^^^^^^^^^^^^^^^

Menor o igual a. Por ejemplo:

.. code-block:: html+django

    {% if ``mi_variable`` <= 100 %}
    Esta cadena aparece si ``mi_variable`` es menor o igual a 100.
    {% endif %}

operador: ``>=``
^^^^^^^^^^^^^^^^

Mayor o igual a. Por ejemplo:

.. code-block:: html+django

    {% if ``mi_variable`` >= 1 %}
      Esta cadena aparece si ``mi_variable`` es mayor o igual que 1.
    {% endif %}

operador: ``in``
^^^^^^^^^^^^^^^^

Contenido dentro. Este operador es soportado por muchos contenedores Python
para probar si el valor dado está en el contenedor. Los siguientes son algunos
ejemplos sobre como ``x in y`` son interpretados.

.. code-block:: html+django

    {% if "bc" in "abcdef" %}
        Esto aparece si "bc" es una subcadena de "abcdef"
    {% endif %}

    {% if "hola" in saludos %}
        Si saludos es una lista o un conjunto de elementos, donde uno de los
        elementos de la cadena es "hola", entonces aparecerá.
    {% endif %}

    {% if usuario in usuarios %}
        Si usuarios es un  QuerySet, éste aparecerá si el usuario es un instancia
        que pertenece a el QuerySet.
    {% endif %}

operador: ``not in``
^^^^^^^^^^^^^^^^^^^^

No contenido dentro. Ésta es la negación de el operador ``in``.

El operador de comparación no puede 'encadenar' como en Python  en notación
Matemática. Por ejemplo en lugar de usar esto::

    {% if a > b > c %}  (MAL)

debes hacer esto::

    {% if a > b and b > c %}

Filtros
^^^^^^^

Puedes usar filtros en las expresiones :ttag:`if`.

Por ejemplo:

.. code-block:: html+django

    {% if messages|length >= 100 %}
       ¡Hoy tienes montones de mensajes!
    {% endif %}

Expresiones complejas
^^^^^^^^^^^^^^^^^^^^^^

Todo lo anterior se puede combinar para formar expresiones complejas. Para tales
expresiones, puede ser importante saber cómo  agrupar los operadores cuando se
evalúan las expresiones - es decir, conocer las reglas de prioridad. La
precedencia de los operadores, desde lo más bajo a lo más alto posible,
es como sigue:

* ``or``
* ``and``
* ``not``
* ``in``
* ``==``, ``!=``, ``<``, ``>``, ``<=``, ``>=``

(Esto funciona exactamente como en Python). Por ejemplo, la siguiente etiqueta
:ttag:`if` en Django:

.. code-block:: html+django

    {% if a == b or c == d and e %}

En Python se escribiría así:

.. code-block:: python

    (a == b) or ((c == d) and e)

Si necesitas usar diferentes prioridades, necesitas jerarquizar las etiquetas
:ttag:`if`.  Algunas veces eso es mejor para obtener mayor claridad, de
cualquier manera, es necesario conocer las reglas de precedencia o prioridad.

.. templatetag:: ifchanged

ifchanged
^^^^^^^^^

Comprueba si el valor ha cambiado desde la ultima iteración al bucle.

El bloque de etiqueta ``{% ifchanged %}`` es usado con bucles. Tiene dos
posibles usos:

Comprueba el contenido dado contra el estado previo y sólo exhibe el
contenido si ha cambiado. Por ejemplo, esto muestra una lista de días,
únicamente si cambia el mes.

.. code-block:: html+django

    <h1>Archivos del {{ year }}</h1>

    {% for date in days %}
        {% ifchanged %}<h3>{{ date|date:"F" }}</h3>{% endifchanged %}
        <a href="{{ date|date:"M/d"|lower }}/">{{ date|date:"j" }}</a>
    {% endfor %}

Si se le pasan una o más variables, verifica cualquier variable que haya
cambiado. El siguiente ejemplo muestra la fecha cada vez que cambia, mientras
que muestra la hora si la fecha y la hora cambian:

.. code-block:: html+django

    {% for date in days %}
        {% ifchanged date.date %} {{ date.date }} {% endifchanged %}
        {% ifchanged date.hour date.date %}
            {{ date.hour }}
        {% endifchanged %}
   {% endfor %}

También puede aceptar opcionalmente  una cláusula ``{% else %}`` que muestra
si el valor no ha cambiado.

.. code-block:: html+django

    {% for match in matches %}
        <div style="background-color:
            {% ifchanged match.ballot_id %}
                {% cycle "red" "blue" %}
            {% else %}
                gray
            {% endifchanged %}
        ">{{ match }}</div>
    {% endfor %}

.. templatetag:: ifequal

ifequal
-------

Muestra el contenido del bloque si los dos argumentos suministrados
son iguales.

He aquí un ejemplo:

.. code-block:: html+django

    {% ifequal user.id comment.user_id %}
        ...
    {% endifequal %}

Al igual que con la etiqueta ``{% if %}``, existe una cláusula ``{% else %}`` opcional.

Los argumentos pueden ser cadenas de texto, así que el siguiente código es
válido:

.. code-block:: html+django

    {% ifequal user.username "adrian" %}
        ...
    {% endifequal %}

Un uso alternativo para la etiqueta ``ifequal`` es usarlo con la etiqueta
:ttag:`if` y el operador ``==``.

.. templatetag:: ifnotequal

ifnotequal
----------

Es igual que ``ifequal``, excepto que comprueba que los dos parámetros
suministrados *no* sean iguales.


Una alternativa para usar la etiqueta  ``ifnotequal`` es usándola con la
etiqueta :ttag:`if`  y el operador ``!=``.

.. templatetag:: include

include
-------

Carga una plantilla y la representa usando el contexto actual. Es
una forma de "incluir" una plantilla dentro de otra.

El nombre de la plantilla puede o bien ser el valor de una variable
o estar escrita en forma de cadena de texto, rodeada ya sea con comillas
simples o comillas dobles, a gusto del lector.

El siguiente ejemplo incluye el contenido de la
plantilla ``"foo/bar.html"``::

    {% include "foo/bar.html" %}

Este otro ejemplo incluye el contenido de la plantilla cuyo nombre sea
el valor de la variable ``template_name``::

    {% include template_name %}

.. templatetag:: load

load
----

Carga una biblioteca de plantillas. En el capítulo 9 puedes encontrar
más información acerca de las bibliotecas de plantillas.

Por ejemplo, la siguiente plantilla carga todas las etiquetas y filtros
registrados en un ``unalibreria`` y ``otralibreira`` localizada en el
paquete ``package``.::

    {% load unalibreria package.otralibreira %}

También se pueden cargar selectivamente filtros de forma individual o etiquetas
de alguna libreria usando el argumento ``from``. En este ejemplo las plantillas
de etiquetas/filtros llamada ``foo`` y ``bar``  serán cargados de
``algunalibreria``::

    {% load foo bar from algunalibreria %}

.. templatetag:: lorem

lorem
-----

Muestra en orden aleatorio el texto en Latin "lorem ipsum". Esto puede ser útil
para proveer datos en las plantillas.

Uso::

    {% lorem [count] [method] [random] %}

La etiqueta ``{% lorem %}`` puede usarse con cero, uno, dos o tres argumentos.
Los argumentos son:

.. table:: Argumentos de la etiqueta lorem.

    ===========  ==============================================================
    Argumento     Descripción
    ===========  ==============================================================
    ``count``    Un numero (o variable) que contiene el numero de párrafos
                 o palabras para generar (el valor predeterminado es 1).
    ``method``   Usa ``w`` para palabras, ``p`` para párrafos en HTML o ``b``
                 para bloques de texto (el valor predeterminado es ``b``).
    ``random``   La palabra ``random``, la cual si es dada, no usa  el común
                 párrafo ("Lorem ipsum dolor sit amet...") cuando genera texto.
    ===========  ==============================================================

Ejemplos:

* ``{% lorem %}`` la salida con el común párrafo: "lorem ipsum".
* ``{% lorem 3 p %}``la salida con el común párrafo: "lorem ipsum"
  y dos párrafos al azar en HTML y con etiquetas ``<p>``.
* ``{% lorem 2 w random %}`` la salida serán dos palabras en latín al azar.

.. templatetag:: now

now
---

Muestra la fecha, escrita de acuerdo a un formato indicado.

Esta etiqueta fue inspirada por la función ``date()`` de PHP(), y
utiliza el mismo formato que esta (http://php.net/date). La versión
Django tiene, sin embargo, algunos extras.

He aquí un ejemplo::

    It is {% now "jS F Y H:i" %}

Se pueden escapar los caracteres de formato con una barra invertida, si se
quieren incluir de forma literal. En el siguiente ejemplo, se escapa el
significado de la letra "f" con la barra invertida, ya que de otra manera
se interpretaría como una indicación de incluir la hora. La "o", por otro
lado, no necesita ser escapada, ya que no es un carácter de formato::

    It is the {% now "jS o\f F" %}

El ejemplo mostraría: "It is the 4th of September".

.. templatetag:: regroup

regroup
-------

Reagrupa una lista de objetos similares usando un atributo común.

Para comprender esta etiqueta, es mejor recurrir a un ejemplo. Digamos
que ``gente`` es una lista de objetos de tipo ``Persona``, y que dichos
objetos tienen los atributos ``nombre``, ``apellido`` y ``genero``. Queremos
mostrar un listado como el siguiente:

* Hombre:
    * George Bush
    * Bill Clinton
* Mujeres:
    * Margaret Thatcher
    * Condoleezza Rice
* Desconocido:
    * Pat Smith

El siguiente fragmento de plantilla mostraría como realizar esta
tarea:

.. code-block:: html+django

    {% regroup gente by genero as grouped %}
    <ul>
    {% for group in grouped %}
        <li>{{ group.grouper }}
        <ul>
            {% for item in group.list %}
            <li>{{ item }}</li>
            {% endfor %}
        </ul>
        </li>
    {% endfor %}
    </ul>

Como puedes ver, ``{% regroup %}`` crea una nueva variable, que es una
lista de objetos que tienen dos tributos, ``grouper`` y ``list``. En
``grouper`` se almacena el valor de agrupación, ``list`` contiene una lista
de los objetos que tenían en común al valor de agrupación. En este
caso, ``grouper`` podría valer ``Male``, ``Female`` y ``Unknown``, y
``list`` sería una lista con las personas correspondientes a cada uno
de estos sexos.

Hay que destacar que ``{% regroup %}`` **no** funciona correctamente
cuando la lista no está ordenada por el mismo atributo que se quiere
agrupar. Esto significa que si la lista del ejemplo no está ordenada
por el sexo, debes asegurarte de que se ordene antes correctamente, por
ejemplo con el siguiente código::

    {% regroup gente|dictsort:"genero" by genero as grouped %}

.. templatetag:: spaceless

spaceless
---------

Elimina los espacios en blanco entre etiquetas HTML Esto incluye
tabuladores y saltos de línea.

El siguiente ejemplo:

.. code-block:: html+django

    {% spaceless %}
        <p>
            <a href="foo/">Foo</a>
        </p>
    {% endspaceless %}

Retornaría el siguiente código HTML::

    <p><a href="foo/">Foo</a></p>

Sólo se eliminan los espacios *entre* las etiquetas, no los espacios
entre la etiqueta y el texto. En el siguiente ejemplo, no se quitan
los espacios que rodean la palabra ``Hello``:

.. code-block:: html+django

    {% spaceless %}
        <strong>
            Hola
        </strong>
    {% endspaceless %}

.. templatetag:: ssi

ssi
---

Muestra el contenido de un fichero determinado dentro de la página.

Al igual que la etiqueta "include", ``{% ssi %}`` incluye el contenido
de otro fichero (que debe ser especificado usando una ruta absoluta)
en la página actual::

    {% ssi /home/html/ljworld.com/includes/right_generic.html %}

Si se le pasa el parámetro opcional "parsed", el contenido del fichero
incluido se evalúa como si fuera código de plantilla, usando el contexto
actual::

    {% ssi /home/html/ljworld.com/includes/right_generic.html parsed %}

Para poder usar la etiqueta ``{% ssi %}``, hay que definir el
valor `ALLOWED_INCLUDE_ROOTS` en los ajustes de Django, como
medida de seguridad.

La mayor parte de las veces, ``{% include %}`` funcionará mejor que
``{% ssi %}``; esta se ha incluido sólo para garantizar compatibilidad
hacia atrás.

.. templatetag:: templatetag

templatetag
-----------

Permite representar los caracteres que están definidos como
parte del sistema de plantillas.

Como el sistema de plantillas no tiene el concepto de "escapar" el significado
de las combinaciones de símbolos que usa internamente, tenemos que recurrir
a la etiqueta ``{% templatetag %}`` si nos vemos obligados a representarlos.

Se le pasa un argumento que indica que combinación de símbolos debe
producir. Los valores posibles del argumento se muestran en la
tabla F-3.

.. table:: Argumentos válidos de templatetag

    ==================  =======
    Argumento           Salida
    ==================  =======
    ``openblock``       ``{%``
    ``closeblock``      ``%}``
    ``openvariable``    ``{{``
    ``closevariable``   ``}}``
    ``openbrace``       ``{``
    ``closebrace``      ``}``
    ``opencomment``     ``{#``
    ``closecomment``    ``#}``
    ==================  =======

Ejemplo de su uso::

    {% templatetag openblock %} url 'lista_entradas' {% templatetag closeblock %}

.. templatetag:: url

url
---

Devuelve una URL absoluta (Es decir, una URL sin la parte del dominio) que
coincide con una determinada vista, incluyendo sus parámetros opcionales. De
esta forma se posibilita realizar enlaces sin violar el principio DRY,
codificando las direcciones en las plantillas::

    {% url 'algun-nombre-de-url' v1 v2 %}

El primer argumento es el nombre del patrón URL o ``name``. El resto de
parámetros son opcionales y deben ir separados con comas, convirtiéndose en
parámetros  posicionales o por nombre que se incluirán en la URL. Deben estar
presentes  todos los argumentos que se hayan definido como obligatorios en el
URLconf. No es posible mezclar argumentos posicionales y argumentos.

Por ejemplo, supongamos que tenemos una vista, ``VistaDetallesCliente``, y que
en el URLconf se la indica que acepta un parámetro, el identificador
del cliente. La línea del URL podría ser algo así:

.. code-block:: python

    url(r'^cliente/(?P<pk>[0-9]+)/$', VistaDetallesCliente.as_view(),
        name='detalles-cliente'),

Si este URLconf fuera incluido en el URLconf del proyecto bajo un
directorio, como en este ejemplo:

.. code-block:: python

    ('^clientes/', include('project_name.app_name.urls'))

Podríamos crear un enlace a esta vista, en nuestra plantilla, con la
siguiente etiqueta::

    {% url 'detalles-cliente' cliente.id %}

La salida de esta etiqueta será ``/clientes/cliente/123/``.

.. warning::

    No olvides poner comillas alrededor del ``name`` del patrón, o el valor
    será interpretado como el contexto de una variable.

Si solo quieres extraer la URL sin mostrarla, puedes usar una llamada un poco
diferente:

.. code-block:: html+django

    {% url 'algun-nombre_patron' arg arg2 as the_url %}

    <a href="{{ the_url }}">Estoy enlazando a {{ the_url }}</a>

El alcance de la variable creada por la sintaxis ``as var`` es el ``{% block %}``
en el cual la etiqueta ``{% url %}`` aparece.

Si quieres extraer el ``namespaced`` de una URL, especifica la ruta completa
a ``name`` así::

    {% url 'miaplic:nombre-url' %}

.. templatetag:: verbatim

verbatim
--------

Detiene el motor de plantillas que renderiza el contenido de esta etiqueta de
bloque.

Un uso muy común es para permitir que  Javascript y la capa de plantillas
no colisiones con la sintaxis de Django. Por ejemplo:

.. code-block:: html+django

    {% verbatim %}
        {{if dying}}Still alive.{{/if}}
    {% endverbatim %}

También se puede llamar específicamente a una etiqueta de cierre ``{% endverbatim %}``
como parte del contenido no renderizado.

.. code-block:: html+django

    {% verbatim myblock %}
        Evita la renderizacion a través de {% verbatim %}{% endverbatim %} block.
    {% endverbatim myblock %}

.. templatetag:: widthratio

widthratio
----------

Esta etiqueta es útil para presentar gráficos de barras y similares. Calcula
la proporción entre un valor dado y un máximo predefinido, y luego multiplica ese
cociente por una constante.

Veamos un ejemplo:

.. code-block:: html+django

    <img src="bar.png" alt="Bar"
         height="10" width="{% widthratio this_valor max_valor max_width %}" />

Si ``this_valor`` vale 175 y ``max_valor`` es 200, la imagen resultante
tendrá un ancho de 88 pixels (porque 175/200 = 0.875 y 0.875 * 100 = 87.5,
que se redondea a 88).

En algunos casos es necesario capturar el valor de el resultado de ``widthratio``
en una variable. Puede ser útil en instancias,  en  :ttag:`blocktrans` tal como:

.. code-block:: html+django

    {% widthratio this_valor max_valor max_width as width %}
    {% blocktrans %}The width is: {{ width }}{% endblocktrans %}


.. templatetag:: with

with
^^^^

Cachea  una variable complicada bajo un nombre más simple. Esto es útil al
acceder a un método "costoso" (e.g., uno que 'golpea' la base de datos) varias
veces.

Por ejemplo:

.. code-block:: html+django

    {% with total=business.employees.count %}
        {{ total }} employee{{ total|pluralize }}
    {% endwith %}

La variable poblada (en el ejemplo anterior, ``total``) está únicamente
disponible entre las etiquetas ``{% with %}`` y ``{% endwith %}``.

Puedes asignar más de una variable al contexto:

.. code-block:: html+django

    {% with alpha=1 beta=2 %}
        ...
    {% endwith %}

Filtros predefinidos
====================

.. templatefilter:: add

add
---

Agrega el argumento al valor.

Ejemplo::

    {{ valor|add:"2" }}

Si el ``valor`` es ``4``, la salida será ``6``.

.. templatefilter:: addslashes

addslashes
----------

Añade barras invertidas antes de las comillas, ya sean simples o dobles. Es
útil para pasar cadenas de texto como javascript, o para escapar cadenas en CVS
por ejemplo::

    {{ valor|addslashes }}

Si el ``valor`` es ``"I'm using Django"``, la salida será: ``"I\'m using Django"``

.. templatefilter:: capfirst

capfirst
--------

Pasa a mayúsculas la primera letra de la primera palabra. Si el primer carácter
no es una letra el filtro no tiene efectos.

Por ejemplo::

    {{ valor|capfirst }}

Si el ``valor`` es ``"django"``, la salida sea ``"Django"``.

.. templatefilter:: center

center
------

Centra el texto en un campo de la anchura indicada.

Por ejemplo::

    "{{ valor|center:"15" }}"

Si ``valor`` es ``"Django"``, la salida será ``"     Django    "``.

cut
---

Elimina todos los valores de los argumentos de la cadena dada.

Por ejemplo::

    {{ valor|cut:" " }}

Si el ``valor``es ``"Cadena con espacios"``, la salida será ``"Cadenaconespacioss"``.

.. templatefilter:: date

date
----

Formatea una fecha de acuerdo al formato indicado en la cadena de texto (Se usa
el mismo formato que con la etiqueta ``now``).

Ejemplo::

    {{ valor|date:"F j, Y" }}

La tabla F-2 muestra las cadenas de formato que se pueden utilizar.

.. table:: Cadenas de formato para fechas y horas

    ==============  ========================================  ======================================
    Carác. formato  Descripción                               Ejemplo de salida
    ==============  ========================================  ======================================
    a               ``'a.m.'`` o ``'p.m.'``.

    A               ``'AM'`` o ``'PM'``.                      ``'AM'``

    b               El nombre del mes, en forma de            ``'jan'``
                    abreviatura de tres letras minúsculas.

    d               Día del mes, dos dígitos que incluyen     ``'01'`` a ``'31'``
                    rellenando con cero por la izquierda si
                    fuera necesario.

    D               Día de la semana, en forma de             ``'Fri'``
                    abreviatura de tres letras.

    f               La hora, en formato de 12 horas y         ``'1'``, ``'1:30'``
                    minutos, omitiendo los minutos
                    si estos son cero.

    F               El mes, en forma de texto                 ``'January'``

    g               La hora, en formato de 12 horas, sin      ``'1'`` a ``'12'``
                    rellenar por la izquierda con ceros.

    G               La hora, en formato de 24 horas, sin      ``'0'`` a ``'23'``
                    rellenar por la izquierda con ceros.

    h               La hora, en formato de 12 horas.          ``'01'`` a ``'12'``

    H               La hora, en formato de 24 horas.          ``'00'`` a ``'23'``

    i               Minutos.                                  ``'00'`` a ``'59'``

    j               El día del mes, sin rellenar por          ``'1'`` a ``'31'``
                    la izquierda con ceros.

    l               El nombre del día de la semana.           ``'Friday'``

    L               Booleano que indica si el año es          ``True`` o ``False``
                    bisiesto.

    m               El día del mes, rellenando por            ``'01'`` a ``'12'``
                    la izquierda con ceros si fuera
                    necesario.

    M               Nombre del mes, abreviado en forma de     ``'Jan'``
                    abreviatura de tres letras.

    n               El mes, sin rellenar con ceros            ``'1'`` a ``'12'``

    N               La abreviatura del mes siguiendo          ``'Jan.'``, ``'Feb.'``
                    el estilo de la Associated Press.         , ``'March'``, ``'May'``

    O               Diferencia con respecto al                ``'+0200'``
                    tiempo medio de Grennwich (*Greenwich
                    Mean Time* - GMT)

    P               La hora, en formato de 12 horas, más      ``'1 a.m.'``, ``'1:30 p.m.'``
                    los minutos, recto si estos son cero      , ``'midnight'``, ``'noon'``
                    y con la indicación a.m./p.m. Además,     , ``'12:30 p.m.'``
                    se usarán las cadenas de texto
                    especiales ``'midnight'`` y ``'noon'``
                    para la medianoche y el mediodía
                    respectivamente.

    r               La fecha en formato RFC 822.              ``'Thu, 21 Dec 2000 16:01:07 +0200'``

    s               Los segundos, rellenos con ceros por la   ``'00'`` a ``'59'``
                    izquierda de ser necesario.

    S               El sufijo inglés para el día del          ``'st'``, ``'nd'``, ``'rd'``
                    mes (dos caracteres).                     o ``'th'``

    t               Número de días del mes.                   ``28`` a ``31``

    T               Zona horaria                              ``'EST'``, ``'MDT'``

    w               Día de la semana, en forma de dígito.     ``'0'`` (Domingo) a ``'6'`` (Sábado)

    W               Semana del año, siguiente la norma        ``1``, ``23``
                    ISO-8601, con la semana empezando el
                    lunes.

    y               Año, con dos dígitos.                     ``'99'``

    Y               Año, con cuatro dígitos.                  ``'1999'``

    z               Día del año                               ``0`` a ``365``

    Z               Desfase de la zona horaria, en            ``-43200`` a ``43200``
                    segundos. El desplazamiento siempre
                    es negativo para las zonas al oeste
                    del meridiano de Greenwich, y positivo
                    para las zonas que están al este.
    ==============  ========================================  ======================================

Por ejemplo::

    {{ valor|date:"D d M Y" }}

Si el  ``valor`` es un objeto :py:class:`~datetime.datetime` (e.g., el resultado de
``datetime.datetime.now()``), la salida será la cadena ``'Wed 09 Jan 2008'``.

Asumiendo que :setting:`USE_L10N` como  ``True`` y :setting:`LANGUAGE_CODE` sea,
por ejemplo, ``"es"``, luego::

    {{ valor|date:"SHORT_DATE_FORMAT" }}

La salida será la cadena ``"09/01/2008"`` (en el  formato especifico para el
local ``es`` usando ``"SHORT_DATE_FORMAT"``).

.. templatefilter:: default

default
-------

Si el valor evaluado es ``False``, usa el valor definido como predeterminado
o ``default``.

Por ejemplo::

     {{ valor|default:"nada" }}

Si el ``valor`` es ``""``  (una cadena vacía), la salida será ``nada``.

.. templatefilter:: default_if_none

default_if_none
---------------

Si (y únicamente si) el valor es ``None``, se usa el valor del argumento en su
lugar.

Observa que si le pasas una cadena vacía, el valor predeterminado *no* será
usado. Usa el fitro :tfilter:`default` si quieres tratar con cadena vacías.

Por ejemplo::

    {{ valor|default_if_none:"nada" }}

Si ``valor`` es ``None``, la salida será una cadena ``"nada"``.

.. templatefilter:: dictsort

dictsort
--------

Acepta una lista de diccionarios y devuelve una lista ordenada según la
propiedad indicada en el argumento.

Por ejemplo::

    {{ valor |dictsort:"nombre" }}

Si el ``valor`` es:

.. code-block:: python

    [
        {'nombre': 'zed', 'edad': 19},
        {'nombre': 'amy', 'edad': 22},
        {'nombre': 'joe', 'edad': 31},
    ]

La salida será:

.. code-block:: python

    [
        {'nombre': 'amy', 'edad': 22},
        {'nombre': 'joe', 'edad': 31},
        {'nombre': 'zed', 'edad': 19},
    ]

Puedes hacer cosas más complicadas como:

.. code-block:: html+django

    {% for libro in libros|dictsort:"autor.edad" %}
        {{ libro.titulo }} ({{ libro.autor.nombre }})
    {% endfor %}

Si ``libros`` es:

.. code-block:: python

    [
        {'titulo': '1984', 'autor': {'nombre': 'George', 'edad': 45}},
        {'titulo': 'Timequake', 'autor': {'nombre': 'Kurt', 'edad': 75}},
        {'titulo': 'Alice', 'autor': {'nombre': 'Lewis', 'edad': 33}},
    ]

La salida será::

    * Alice (Lewis)
    * 1984 (George)
    * Timequake (Kurt)

.. templatefilter:: dictsortreversed

dictsortreversed
------------------

Acepta una lista de diccionarios y devuelve una lista ordenada de forma
descendente según la propiedad indicada en el argumento. Trabaja de forma
parecida al anterior filtro, pero retorna el valor en orden inverso.

Por ejemplo::

    {{ lista|dictsortreversed:"foo" }}

.. templatefilter:: divisibleby

divisibleby
------------

Devuelve ``True`` si el valor pasado es divisible por el argumento.

Por ejemplo::

    {{ valor|divisibleby:"3" }}

Si el ``valor`` es ``21``, la salida será ``True``.


.. templatefilter:: escape

escape
------

Escapea una cadena en HTML,  concretamente, realiza los siguientes remplazos:


* ``<`` es convertido a ``&lt;``
* ``>`` es convertido a  ``&gt;``
* ``'`` (comillas simples) es convertido a  ``&#39;``
* ``"`` (comillas dobles) es convertido a  ``&quot;``
* ``&`` es convertido a  ``&amp;``

El escape es únicamente aplicado en la salida de la cadena, así que no importa
donde se encadenen la serie de filtros usando ``escape``: este siempre será
aplicado como al último filtro. Si quieres  que el escape se aplique
inmediatamente, utiliza el filtro :tfilter:`force_escape`.

Aplicar ``escape`` a una variable que normalmente esta ``auto-escapeada``,  da
como resultado que el escapeo se aplique una sola vez. Por lo que es seguro usar
esta función incluso en ambientes de ``auto-escape``. Si quieres pasar múltiples
escapes usa el filtro :tfilter:`force_escape`

Por ejemplo, puedes aplicar ``escape`` a campos cuando  la etiqueta
:ttag:`autoescape`  esta desactivada o en ``of``:

.. code-block:: html+django

    {% autoescape off %}
        {{ titulo|escape }}
    {% endautoescape %}

.. templatefilter:: escapejs

escapejs
---------

Escapa caracteres para usar en cadenas Javascript. Esta *no* marca las cadenas
como seguras para usar en HTML, pero las protege de errores de sintaxis cuando
se usan plantillas generadas por ``JavaScript/JSON.``

Por ejemplo::

    {{ valor|escapejs }}

Si ``valor`` es ``"testing\r\njavascript \'string" <b>escaping</b>"``,
la salida será ``"testing\\u000D\\u000Ajavascript \\u0027string\\u0022 \\u003Cb
\\u003Eescaping\\u003C/b\\u003E"``.

.. templatefilter:: filesizeformat

filesizeformat
--------------

Representa un valor, interpretándolo como si fuera el tamaño de un fichero y
"humanizando" el resultado, de forma que sea fácil de leer. Por ejemplo, las
salidas podrían ser ``'13 KB'``, ``'4.1 MB'``, ``'102 bytes'``, etc.

Por ejemplo::

    {{ valor|filesizeformat }}

Si ``valor`` es 123456789, la salida será ``117.7 MB``.

.. admonition:: Tamaño de archivos y unidades SI

    Estrictamente hablando ``filesizeformat`` no  se ajusta al Sistema
    Internacional de Unidades (International System of Units) que recomiende
    usar KiB, MiB, GiB, cuando el tamaño de los bytes se calcula en torno
    a 1024(como en este caso). En lugar de eso, Django usa tradicionalmente
    nombres de unidades (KB, MB, GB, etc.) correspondiendo a los nombres que
    se utilizan más comúnmente.

.. templatefilter:: first

first
-----

Devuelve el primer elemento de una lista.

Por ejemplo::

    {{ valor|first }}


Si el ``valor`` está en la lista ``['a', 'b', 'c']``, la salida será ``'a'``.

.. templatefilter:: floatformat

floatformat
-----------

Si se usa sin argumento, redondea un número en coma flotante a un único
dígito decimal (pero sólo si hay una parte decimal que mostrar), por
ejemplo:

.. table::  Ejemplos de ``floatformat``

    ============  ===========================  ========
    ``valor``     Plantilla                     Salida
    ============  ===========================  ========
    ``34.23234``  ``{{ valor|floatformat }}``  ``34.2``
    ``34.00000``  ``{{ valor|floatformat }}``  ``34``
    ``34.26000``  ``{{ valor|floatformat }}``  ``34.3``
    ============  ===========================  ========

Si te utiliza un argumento numérico, ``floatformat`` redondea a ese número
de lugares decimales, por ejemplo:

.. table::  Ejemplos de ``floatformat``

    ============  =============================  ==========
    ``valor``     Plantilla                      Salida
    ============  =============================  ==========
    ``34.23234``  ``{{ valor|floatformat:3 }}``  ``34.232``
    ``34.00000``  ``{{ valor|floatformat:3 }}``  ``34.000``
    ``34.26000``  ``{{ valor|floatformat:3 }}``  ``34.260``
    ============  =============================  ==========

Particularmente útil al pasárselo al 0 (cero) como el argumento que redondea
el numero flotante, al valor entero más cercano.

.. table:: Ejemplos de ``floatformat``

    ============  ================================  ==========
    ``valor``     Plantilla                         Salida
    ============  ================================  ==========
    ``34.23234``  ``{{ valor|floatformat:"0" }}``   ``34``
    ``34.00000``  ``{{ valor|floatformat:"0" }}``   ``34``
    ``39.56000``  ``{{ valor|floatformat:"0" }}``   ``40``
    ============  ================================  ==========

Si el argumento pasado a ``floatformat`` es negativo, redondeará a ese
número de decimales, pero sólo si el número tiene parte decimal.
Por ejemplo:

.. table::  Ejemplos de ``floatformat``

    ============  ================================  ==========
    ``valor``     Plantilla                         Salida
    ============  ================================  ==========
    ``34.23234``  ``{{ valor|floatformat:"-3" }}``  ``34.232``
    ``34.00000``  ``{{ valor|floatformat:"-3" }}``  ``34``
    ``34.26000``  ``{{ valor|floatformat:"-3" }}``  ``34.260``
    ============  ================================  ==========

Usar ``floatformat`` sin argumentos es equivalente a usar ``floatformat`` con el
argumento de ``-1``.

.. templatefilter:: force_escape

force_escape
------------

Aplica escapeo HTML a la cadena(consulta el filtro :tfilter:`escape` para
mas detalles). Este filtro es aplicado *inmediatamente* y devuelve una nueva
cadena escapada. Es útil en raros casos, por ejemplo  cuando es necesario el uso
de múltiples escapeos o cuando es necesario aplicar otros filtro a el resultado
escapado. Normalmente se usa el filtro  :tfilter:`escape`.

Por ejemplo, si quieres  atrapara los elemento HTML ``<p>`` creados por el filtro
tfilter:`linebreaks`:

.. code-block:: html+django

    {% autoescape off %}
        {{ cuerpo|linebreaks|force_escape }}
    {% endautoescape %}

.. templatefilter:: get_digit

get_digit
---------

Dado un número, devuelve el dígito que esté en la posición indicada, siendo
1 el dígito más a la derecha. En caso de que la entrada sea inválida, devolverá
el valor original (Si la entrada o el argumento no fueran enteros, o si
el argumento fuera inferior a 1). Si la entrada es correcta, la salida siempre
será un entero.

Por ejemplo::

    {{ valor|get_digit:"2" }}


Si ``valor`` es ``123456789``, la salida será ``8``.

.. templatefilter:: iriencode

iriencode
---------

Convierte un IRI (Identificador Internacional de Recursos o Internationalized
Resource Identifier) a una cadena que es conveniente para incluir en una URL.
Esto es necesario su están tratando de usar cadenas que contienen caracteres que
no son ASCII en una URL.

Es seguro usar este filtro en una cadena que ha pasado por un filtro
:tfilter:`urlencode`.

Por ejemplo::

    {{ valor|iriencode }}

Si ``valor`` es ``"?test=1&me=2"``, la salida será ``"?test=1&amp;me=2"``.

.. templatefilter:: join

join
----

Concatena todos los elementos de una lista para formar una cadena
de texto, usando como separador el texto que se le pasa como
argumento. Es equivalente a la llamada en Python ``str.join(list)``

Por ejemplo::

    {{ valor|join:" // " }}

Si ``valor`` es la lista ``['a', 'b', 'c']``, la salida será la cadena:
``"a // b // c"``.

.. templatefilter:: last

last
^^^^

Devuelve el ultimo ítem de una lista.

Por ejemplo::

    {{ valor|last }}

Si ``valor`` es la lista ``['a', 'b', 'c', 'd']``, la salida será la cadena
``"d"``.


.. templatefilter:: length

length
------

Devuelve la longitud del valor. Funciona tanto en listas como en cadenas.

Por ejemplo::

    {{ valor|length }}

Si el ``valor`` es ``['a', 'b', 'c', 'd']`` o ``"abcd"``, la salida será ``4``.

El filtro devuelve ``0`` cuando las variables no están definidas.

.. templatefilter:: length_is

length_is
---------

Devuelve el valor ``True`` si la longitud de la entrada coincide con el argumento
suministrado, o de lo contrario ``False``.

Por ejemplo::

    {{ valor|length_is:"4" }}

Si el ``valor`` es ``['a', 'b', 'c', 'd']`` o ``"abcd"``, la salida será ``True``.

.. templatefilter:: linebreaks

linebreaks
----------

Remplaza saltos de línea en texto plano con los apropiados formatos en HTML;
una simple nueva línea  se convierte en un salto de línea en HTML (``<br />``)
y una nueva línea seguida de una línea en blanco se convierte en un
párrafo (``</p>``).

Por ejemplo::

    {{ valor|linebreaks }}

Si el  ``valor`` es ``Joel\nes un slug``, la salida será ``<p>Joel<br />es un
slug</p>``.

.. templatefilter:: linebreaksbr

linebreaksbr
------------

Convierte todos los saltos de línea en etiquetas ``<br />``.

Por ejemplo::

    {{ valor|linebreaksbr }}

Si el ``valor`` es ``Joel\nes un slug``, la salida será ``Joel<br />es un
slug``.

.. templatefilter:: linenumbers

linenumbers
-----------

Muestra el texto de la entrada con números de línea.

Por ejemplo::

    {{ valor|linenumbers }}

Si el ``valor`` es::

    uno
    dos
    tres

La salida será::

    1. uno
    2. dos
    3. tres

.. templatefilter:: ljust

ljust
-----

Justifica el texto de la entrada a la izquierda utilizando la anchura indicada.

**Argumento:** tamaño de campo

Por ejemplo::

    "{{ valor|ljust:"10" }}"

Si el ``valor`` is ``Django``, la salida será ``"Django    "``.

.. templatefilter:: lower

lower
-----

Convierte el texto de la entrada dada, a letras en minúsculas

Por ejemplo::

    {{ valor|lower }}

Si el ``valor`` es ``Sigo ENOJADO con Yoko``, la salida será ``sigo enojado con
yoko``.

.. templatefilter:: make_list

make_list
---------

Devuelve la entrada en forma de lista. Si la entrada es un número
entero, se devuelve una lista de dígitos. Si es una cadena de
texto, se devuelve una lista de caracteres.

Por ejemplo::

    {{ valor|make_list }}

Si el ``valor`` es la cadena ``"Joel"``, la salida será la lista:
``['J', 'o', 'e', 'l']``. Si el ``valor`` es ``123``, la salida será la lista:
``['1', '2', '3']``

.. templatefilter:: phone2numeric

phone2numeric
-------------

Convierte un número de teléfono (que incluso puede contener letras) a
su forma numérica equivalente.

La entrada no tiene porque ser un número de teléfono válido. El filtro
convertirá alegremente cualquier texto que se le pase.

Por ejemplo::

    {{ valor|phone2numeric }}

Si el ``valor`` es ``800-COLLECT``, la salida será: ``800-2655328``.

.. templatefilter:: pluralize

pluralize
---------

Retorno el sufijo para formar el plural si el valor es mayor que uno. Por
defecto el sufijo es ``'s'``.

Ejemplo::

    Tú tienes {{ num_mensajes }} mensaje {{ num_mensajes|pluralize }}.

Si ``num_mensajes`` es ``1``, la salida será ``Tu tienes 1 mensaje.``
Si ``num_mensajes`` es ``2``, la salida será ``Tu tienes 2 mensajes.``

Para aquellas palabras que requieran otro sufijo para formar el plural, podemos
usar una sintaxis alternativa en la que indicamos el sufijo que queramos
con un argumento.

Ejemplo::

    Hay registrados {{ num_autores }} autor{{ num_autores|pluralize:"es" }}.

Para aquellas palabras que forman el plural de forma más compleja que
con un simple sufijo, hay disponible una opción, que permite indicar las formas
en singular y en plural,  separándolas con una coma.

Ejemplo::

    Tú tienes{{ num_cherries }} cherr{{ num_cherries|pluralize:"y,ies" }}.

Usa la etiqueta :ttag:`blocktrans` para pluralizar cadenas traducidas.

.. templatefilter:: pprint

pprint
------

Un ``wrapper`` que permite llamar a la función de Python ``pprint.pprint``. Se
usa sobre todo para tareas de depurado de errores.

Ejemplo::

    {{ objeto|pprint }}

.. templatefilter:: random

random
------

Devuelve un elemento elegido al azar de la lista.

Por ejemplo::

    {{ valor|random }}

Si el ``valor`` es la lista ``['a', 'b', 'c', 'd']``, la salida podría ser: ``"b"``.

.. templatefilter:: rjust

rjust
-----

Justifica el texto de la entrada a la derecha utilizando la anchura indicada.

**Argumento:** El tamaño del campo

Por ejemplo::

    "{{ valor|rjust:"10" }}"

Si el  ``valor`` es ``Django``, la salida será ``"    Django"``.

.. templatefilter:: safe

safe
----

Marca una cadena como no requerida para escapeo antes de la salida en HTML.
Cuando el ``autoescape`` está en ``of``, este filtro no tiene efecto.

.. admonition:: Nota:

    Si estas encadenando filtros, un filtro aplicado después de ``safe`` puede
    hacer el contenido inseguro otra vez. Por ejemplo, el siguiente código
    imprime las variables como si no estuvieran ``escapadas``:

    .. code-block:: html+django

        {{ varible|safe|escape }}

.. templatefilter:: safeseq

safeseq
^^^^^^^

Aplica el filtro :tfilter:`safe` a cada elemento de una secuencia. Útil en
conjunto con otros filtros que operan en secuencia, tal como el filtro
:tfilter:`join`.  Por ejemplo::

    {{ alguna_lista|safeseq|join:", " }}

No se puede usar el filtro :tfilter:`safe` directamente en este caso, es
necesario convertir la variable en una cadena,  en vez de trabajar con lo
los elementos individuales de la secuencia.

.. templatefilter:: slice

slice
-----

Devuelve una sección de la lista.

Usa la misma sintaxis que se usa en Python para seccionar una lista.
Véase:  http://www.diveintopython3.net/native-datatypes.html#slicinglists
para una rápida introducción.

Ejemplo::

    {{ una_lista|slice:":2" }}

Si ``una_lista`` es ``['a', 'b', 'c']``, la salida será: ``['a', 'b']``.

.. templatefilter:: slugify

slugify
-------

Convierte a ASCCI. Convierte el texto a minúsculas, elimina los caracteres que no
formen palabras (caracteres alfanuméricos y carácter subrayado), y convierte los
espacios en guiones. También elimina los espacios que hubiera al principio y al
final del texto.

Por ejemplo::

    {{ valor|slugify }}

Si el ``valor`` es ``"Joel es un slug"``, la salida será  ``"joel-es-un-slug"``.

.. templatefilter:: stringformat

stringformat
------------

Formatea el valor de entrada de acuerdo a lo especificado en el formato
que se le pasa como parámetro. La sintaxis a utilizar es idéntica a la
de Python, con la excepción de que el carácter "%" se omite.

Puedes consultar las opciones de formateo de cadenas de Python: en
http://docs.python.org/library/stdtypes.html#string-formatting-operations
para más detalles.

Por ejemplo::

    {{ valor|stringformat:"E" }}

Si el ``valor`` es ``10``, la salida será ``1.000000E+01``.

.. templatefilter:: striptags

striptags
---------

Hace todo los posible por eliminar todas las etiquetas [X]HTML.

Por ejemplo::

    {{ valor|striptags }}

Si el ``valor`` es ``"<b>Joel</b> <button>es</button> un <span>slug</span>"``,
la salida será:  ``"Joel es un slug"``.

.. admonition:: No se garantiza que sea seguro.

    Nota que ``striptags`` no ofrece ninguna garantía acerca de la salida segura
    en HTML, en particular con entradas no validas de HTML. Por lo que **NUNCA**
    apliques el filtro ``safe`` a la salida de  ``striptags``. Si estas buscando
    algo más robusto usa la librería Python ``bleach``, en especial el método
    `clean`_ .

.. _clean: http://bleach.readthedocs.org/en/latest/clean.html

.. templatefilter:: time

time
----

Formateas una fecha de acuerdo al formato dado.

El formato puede ser predefinido con :setting:`TIME_FORMAT`, o con un formato
personalizado, al igual que el filtro :tfilter:`date`. Nota que el formato
predefinido es dependiente del valor local.

Por ejemplo::

    {{ valor|time:"H:i" }}

Si el ``valor`` es equivalente a ``datetime.datetime.now()``, la salida será la
cadena ``"01:23"``.

Otro ejemplo:

Asumiendo  que  :setting:`USE_L10N` sea ``True``  y :setting:`LANGUAGE_CODE` sea,
por ejemplo ``"de"``, entonces para::

    {{ valor|time:"TIME_FORMAT" }}

La salida será la cadena  ``"01:23:00"`` (El formato especifico ``"TIME_FORMAT"``
para el valor local  ``de`` en Django es  ``"H:i:s"``)

El filtro ``time`` únicamente acepta parámetros en el formato de cadenas o
strings que se relacionen con la hora, no con la fecha (por obvias razones). Si
necesitas un formato para valores ``date`` usa el filtro :tfilter:`date`  en su
lugar.

Hay una excepción a la regla anterior: Cuando se pasa un valor ``datetime`` con
información adjunta ``timezone``,  el filtro ``time`` acepta el formato
``timezone`` específicamente los formatos ``'e'``, ``'O'`` , ``'T'`` y ``'Z'``.

Cuando se usa sin un formato de cadenas::

    {{ valor|time }}

El formato definido con  :setting:`TIME_FORMAT` será usado si se aplica
la ``localización``.

.. templatefilter:: timesince

timesince
---------

Formatea una fecha como un intervalo de tiempo (por ejemplo, "4 días, 6 horas").

Acepta un argumento opcional, que es una variable con la fecha a usar como
punto de referencia para calcular el intervalo (Si no se especifica, la
referencia es el momento *actual*). Por ejemplo, si ``blog_date`` es una fecha
con valor igual a la medianoche del 1 de junio de 2006, y ``comment_date`` es
una fecha con valor las 08:00 horas del día 1 de junio de 2006, entonces
lo siguiente devolverá "8 horas".::

     {{ blog_date|timesince:comment_date }}

Los minutos son la unidad más pequeña usada y "0 minutos" será devuelto por
cualquier fecha que este en el futuro con relación al punto de comparación.

.. templatefilter:: timeuntil

timeuntil
---------

Es similar a ``timesince``, excepto en que mide el tiempo desde la fecha de
referencia hasta la fecha dada. Por ejemplo, si hoy es 1 de junio de 2006 y
``conference_date`` es una fecha cuyo valor es igual al 29 de junio de 2006,
entonces ``{{ conference_date|timeuntil:from_date }}`` devolverá "4 semanas".

Acepta un argumento opcional, que es una variable con la fecha a usar como
punto de referencia para calcular el intervalo, si se quiere usar otra
distinta del momento *actual*. Si ``from_date`` apunta al 22 de junio de
2006, entonces ``{{ conference_date|timeuntil:from_date }}``
devolvera "1 semana".::

    {{ conference_date|timeuntil:from_date }}

Los minutos son la unidad más pequeña usada y "0 minutos" será devuelto por
cualquier fecha que este en el futuro con relación al punto de comparación.

.. templatefilter:: title

title
-----

Convierte una cadena de texto en forma de título, siguiendo las convenciones
del idioma inglés (todas las palabras con la inicial en mayúscula).

Por ejemplo::

    {{ valor|titulo }}

Si el ``valor`` es ``"mi PRIMER post"``, la salida será ``"Mi primer Post"``.

.. templatefilter:: truncatechars

truncatechars
-------------

Recorta la salida de una cadena de forma que tenga como máximo el número de
caracteres que se indican en el argumento. Las cadenas truncadas terminarán con
una secuencia de puntos de suspensión ("...").

**Argumento:** El numero de caracteres a recortar

Por ejemplo::

    {{ valor|truncatechars:9 }}

SI el ``valor`` es ``"Joel es un slug"``, la salida será ``"Joel e..."``.

.. templatefilter:: truncatechars_html

truncatechars_html
------------------

Parecida al filtro  :tfilter:`truncatechars`, excepto que es capaz de reconocer
las etiquetas HTML y, por tanto, no deja etiquetas "huérfanas". Cualquier
etiqueta que se hubiera abierto antes del punto de recorte es cerrada
por el propio filtro.

Por ejemplo::

    {{ valor|truncatechars_html:9 }}

Si el ``valor`` es ``"<p>Joel es un slug</p>"``, la salida será:
``"<p>Joel i...</p>"``.

Las nuevas líneas en el contenido del HTML serán conservadas.


.. templatefilter:: truncatewords

truncatewords
-------------

Recorta la salida de forma que tenga como máximo el número de palabras
que se indican en el argumento.

**Argumento**: El numero de palabras a recortar o truncar

Por ejemplo::

    {{ valor|truncatewords:2 }}

Si el ``valor`` es ``"Joel es un slug"``, la salida será: ``"Joel es ..."``.

Las nuevas líneas en la cadena serán removidas.

.. templatefilter:: truncatewords_html

truncatewords_html
------------------

Es similar a :tfilter:`truncatewords`, excepto que es capaz de reconocer las
etiquetas HTML y, por tanto, no deja etiquetas "huérfanas". Cualquier
etiqueta que se hubiera abierto antes del punto de recorte es cerrada
por el propio filtro.

Es menos eficiente que :tfilter:`truncatewords`, así que debe ser usado solamente
si sabemos que en la entrada va texto HTML.

Por ejemplo::

    {{ valor|truncatewords_html:2 }}

Si el ``valor`` es ``"<p>Joel es un slug</p>"``, la salida será:
``"<p>Joel es ...</p>"``.

Las nuevas líneas en el contenido HTML serán conservadas.

.. templatefilter:: upper

upper
-----

Convierte una cadena o string a mayúsculas.

Por ejemplo::

    {{ valor|upper }}

If ``valor`` is ``"Joel es un slug"``, la salida será: ``"JOEL ES UN SLUG"``.

.. templatefilter:: urlencode

urlencode
---------

Escapa la entrada de forma que pueda ser utilizado dentro de una URL.

Por ejemplo::

    {{ valor|urlencode }}

Si el ``valor`` es "http://www.example.org/foo?a=b&c=d", la salida será:
"http%3A//www.example.org/foo%3Fa%3Db%26c%3Dd".

Opcionalmente podemos pasarle un argumento que contiene los carácteres que no
deben ser ``escapados``. Si no se le provee, el carácter '/' es asumido como
seguro. Una cadena vacía puede proveerse cuando *todos* los caracteres deben
ser escapados. Por ejemplo::

    {{ valor|urlencode:"" }}

Si el ``valor`` es "http://www.example.org/", la salida será:
"http%3A%2F%2Fwww.example.org%2F".

.. templatefilter:: urlize

urlize
------

Convierte URLs y direcciones de email en texto a enlaces HTML.

Esta plantilla de etiqueta funciona en enlaces que contienen prefijos como
``http://``, ``https://``, o ``www.``. Por ejemplo, ``http://goo.gl/aia1t``
será convertido, pero ``goo.gl/aia1t`` no.

También soporta links, únicamente en el nivel superior de dominios (``.com``,
``.edu``, ``.gov``, ``.int``, ``.mil``, ``.net``, y ``.org``). Por ejemplo
funciona con ``djangoproject.com``.

Por ejemplo::

    {{ valor|urlize }}

Si ``valor`` es "Check out www.djangoproject.com", la salida será
"Check out <a href="http://www.djangoproject.com rel="nofollow">www.djangoproject.com</a>".

.. templatefilter:: urlizetrunc

urlizetrunc
------------

Convierte las direcciones URL de un texto en enlaces al igual que
:tfilter:`urlize`, recortando la representación de la URL para que el número
de caracteres sea como máximo el del argumento suministrado.

**Argumento:** Numero de caracteres que el enlace de texto debe contener
incluyendo los puntos suspensivos que agrega el filtro.

Por ejemplo::

    {{ valor|urlizetrunc:15 }}

Si el ``valor`` es "Check out www.djangoproject.com", la salida será:
"Check out <a href="http://www.djangoproject.com" rel="nofollow">www.djangopr...</a>".

Al igual que :tfilter:`urlize`, solo se puede aplicar al texto plano.

.. templatefilter:: wordcount

wordcount
---------

Devuelve el número de palabras en la entrada.

Por ejemplo::

    {{ valor|wordcount }}

Si el ``valor`` es ``"Joel es un slug"``, la salida será ``4``.

.. templatefilter:: wordwrap

wordwrap
--------

Ajusta la longitud del texto para las líneas se adecúen a la longitud
especificada como argumento.

**Argumento:** El numero de caracteres  a los cuales ajustar el texto.

Por ejemplo::

    {{ valor|wordwrap:5 }}

Si el ``valor`` es ``Joel es un slug``, la salida será::

    Joel
    is a
    slug

.. templatefilter:: yesno

yesno
-----

Dada una serie de textos que se asocian a los valores de ``True``, ``False`` y
(opcionalmente) ``None``, devuelve uno de esos textos según el valor de la
entrada. Véase la siguiente tabla:

Por ejemplo::

    {{ valor|yesno:"yeah,no,maybe" }}

.. table::  Ejemplos del filtro yesno

    ==========  ======================  ========================================
      Valor       Argumento               Salida
    ==========  ======================  ========================================
     ``True``    ``"yeah,no,maybe"``     ``yeah``

     ``False``   ``"yeah,no,maybe"``     ``no``

     ``None``    ``"yeah,no,maybe"``     ``maybe``

      ``None``    ``"yeah,no"``           ``"no"`` (considera ``None`` como
                                          ``False`` si no se asigna ningún
                                          texto a ``None``.
    ==========  ======================  ========================================

Filtros y etiquetas de internacionalización
===========================================

Django proporciona una serie de etiquetas y filtros que controlan cada aspecto
de la :doc:`Internacionalizacion </chapter19>` en las plantillas. Permiten
mantener de forma granular las traducciones, el formato, y las conversiones de
las zonas horarias.

i18n
----

Esta libreria permite especificar el texto traducible en las plantillas. Para
usarla asegúrate que :setting:`USE_I18N` este establecido en ``True``, luego
cárgala con ``{% load i18n %}``.

l10n
----

Esta libreria proporciona control sobre los valores de ``localización`` en las
plantillas. Únicamente necesitas cargar esta libreria usando
``{% load l10n %}``, pero necesitas que  :setting:`USE_L10N` a ``True`` de modo
que  la localización este activa de forma predeterminada.

tz
--

Esta libreria proporciona control sobre las conversiones de zonas horario en las
plantillas, tal como ``l10n``, únicamente necesitas cargar la libreria usando
``{% load tz %}`` pero necesitas que  :setting:`USE_TZ` sea ``True`` de modo
que  la conversión  este activa de forma predeterminada.

Otras etiquetas y filtro
========================

Django viene además con unas par de bibliotecas, que permiten usar otras
etiquetas,  que es necesario habilitar explícitamente en :setting:`INSTALLED_APPS`
para usarlas en las plantillas con la etiqueta  :ttag:`{% load %}<load>`.

django.contrib.humanize
-----------------------

Un conjunto de filtros de plantillas, útiles para darle un toque humano a los
datos.

django.contrib.webdesign
------------------------

Una colección de etiquetas de plantilla, que pueden ser útiles en el diseño
de sitios web, tal como la generación de texto del tipo: ``Lorem Ipsum``.

.. templatetag:: static

.. highlight:: html+django

static
------

Para enlazar los archivos estáticos que se guardan en :setting:`STATIC_ROOT`
Django usa la etiqueta :ttag:`static`. Puedes usar esta etiqueta de plantilla
independientemente de que uses :class:`~django.template.RequestContext` o no.::

    {% load static %}
    <img src="{% static "imagenes/hola.jpg" %}" alt="Hola!" />

Puedes usarla para enlazar y consumir diferentes variables de contexto, además
de los estándar, por ejemplo asumiendo que la variable ``hoja_de_estilo.css`` sea
pasada a la plantilla::

    {% load static %}
    <link rel="stylesheet" href="{% static hoja_de_estilo.css %}"
        type="text/css" media="screen" />

Si lo que quieres es recuperar la URL estática para mostrarla, puedes usar una
llamada un poco diferente:

.. code-block:: html+django

    {% load static %}
    {% static "imagenes/hola.jpg" as mifoto %}
    <img src="{{ mifoto }}"></img>

.. highlight:: html+django

get_static_prefix
^^^^^^^^^^^^^^^^^

Es preferible que uses la etiqueta de plantilla :ttag:`static`, pero si
necesitas tener un control más exacto sobre cómo y dónde :setting:`STATIC_URL`
es inyectado en la  plantilla, puedes usar la etiqueta de plantilla:
:ttag:`get_static_prefix`::

    {% load static %}
    <img src="{% get_static_prefix %}imagenes/hi.jpg" alt="Hi!" />

Existe una segunda forma de poder utilizarla y así evitar el procesamiento extra
si necesitas usar varias veces, múltiples valores::

    {% load static %}
    {% get_static_prefix as STATIC_PREFIX %}

    <img src="{{ STATIC_PREFIX }}imagenes/hi.jpg" alt="Hi!" />
    <img src="{{ STATIC_PREFIX }}imagenes/hi2.jpg" alt="Hello!" />

.. templatetag:: get_media_prefix

get_media_prefix
^^^^^^^^^^^^^^^^

.. highlight:: html+django

Parecida a la etiqueta :ttag:`get_static_prefix`, ``get_media_prefix`` puebla
la variable de la plantilla  con el prefijo de ``media`` :setting:`MEDIA_URL`.

Por ejemplo::

    <script type="text/javascript" charset="utf-8">
        var media_path = '{% get_media_prefix %}';
    </script>

