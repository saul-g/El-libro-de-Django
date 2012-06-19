=========================================================
Apéndice F: Etiquetas de plantilla y filtros predefinidos
=========================================================

En el :doc:`Capítulo 4<chapter04>` se hace una introducción de las etiquetas de
plantilla y filtros más utilizados, pero Django incorpora muchas
más. En este apéndice se listan todas las que estaban incluidas
en el momento en que se escribió el libro, pero se añaden
nuevas etiquetas y filtros de forma regular.

La mejor referencia de todas las etiquetas y filtros disponibles
se encuentra en la propia página de administración. Allí se incluye
una referencia completa de todas las etiquetas y filtros que hay
disponibles para una determinada aplicación.  Para verla, sólo
tienes que pulsar con el ratón en el enlace de documentación que está
en la esquina superior derecha de la página.

Las secciones de etiquetas y filtros de esta documentación incluirán
tanto las etiquetas y filtros predefinidos (de hecho, las referencias
de este apéndice vienen directamente de ahí) como aquellas etiquetas
y filtros que se hayan incluido o escrito para la aplicación.

Este apéndice será más útil, por tanto, para aquellos que no dispongan de
acceso a la interfaz de administración. Como Django es altamente
configurable, las indicaciones de la interfaz de administración deben
ser consideradas como la documentación más actualizada y, por tanto, la
de mayor autoridad.

Etiquetas predefinidas
======================

block
-----

Define un bloque que puede ser sobreescrito por las plantillas derivadas. Véase
la sección acerca de herencia de plantillas en el `Capítulo 4`_ para más información.

comment
-------

Ignora todo lo que aparezca entre ``{% comment %}`` y ``{% endcomment %}``.

cycle
-----

Rota una cadena de texto entre diferentes valores, cada vez que
aparece la etiqueta.

Dentro de un bucle, el valor rotan entre los distintos valores
disponibles en cada iteración del bucle::

    {% for o in some_list %}
        <tr class="{% cycle row1,row2 %}">
            ...
        </tr>
    {% endfor %}

Fuera de un bucle, hay que asignar un nombre único la primera vez que se usa
la etiqueta, y luego hay que incluirlo ese nombre en las sucesivas llamadas::

        <tr class="{% cycle row1,row2,row3 as rowcolors %}">...</tr>
        <tr class="{% cycle rowcolors %}">...</tr>
        <tr class="{% cycle rowcolors %}">...</tr>

Se pueden usar cualquier número de valores, separándolos por comas. Asegúrate
de no poner espacios entre los valores, sólo comas.

debug
-----

Muestra un montón de información para depuración de errores, incluyendo el
contexto actual y los módulos importados.

extends
-------

Sirve para indicar que esta plantilla extiende una plantilla padre.

Esta etiqueta se puede usar de dos maneras:

* ``{% extends "base.html" %}`` (Con las comillas) interpreta
  literalmente ``"base.html"`` como el nombre de la plantilla
      a extender.

* ``{% extends variable %}`` usa el valor de ``variable``. Si
  la variable apunta a una cadena de texto, Django usará
  dicha cadena como el nombre de la plantilla padre. Si la variable
  es un objeto de tipo ``Template``, se usará ese mismo objeto como
  plantilla base.

En el :doc:`Capítulo 4<chapter04>` podrás encontrar muchos ejemplo de uso de esta
etiqueta.

filter
------

Filtra el contenido de una variable.

Los filtros pueden ser encadenados sucesivamente (La salida
de uno es la entrada del siguiente), y pueden tener argumentos, como
en la sintaxis para variables

He aquí un ejemplo::

    {% filter escape|lower %}
        This text will be HTML-escaped, and will appear in all lowercase.
    {% endfilter %}

firstof
-------

Presenta como salida la primera de las variables que se le pasen
que evalúe como no falsa. La salida será nula si todas las
variables pasadas valen ``False``.

He aquí un ejemplo::

    {% firstof var1 var2 var3 %}

Equivale a::

    {% if var1 %}
        {{ var1 }}
    {% else %}{% if var2 %}
        {{ var2 }}
    {% else %}{% if var3 %}
        {{ var3 }}
    {% endif %}{% endif %}{% endif %}

for
---

Itera sobre cada uno de los elementos de un lista o *array*. Por ejemplo, para mostrar
una lista de atletas, cuyos nombres estén en la lista ``athlete_list``, podríamos
hacer::

    <ul>
    {% for athlete in athlete_list %}
        <li>{{ athlete.name }}</li>
    {% endfor %}
    </ul>

También se puede iterar la lista en orden inverso usando ``{% for obj in list reversed %}``.

Dentro de un bucle, la propia sentencia ``for`` crea una serie de
variables. A estas variables se puede acceder únicamente dentro del
bucle. Las distintas variables se explican en la Tabla F-1.

.. tabla:: Tabla F-1. Variables accesibles dentro de bucles {% for %}

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
``forloop.first``           ``True`` si es la primera iteración.
``forloop.last``            ``True`` si es la última iteración.
``forloop.parentloop``       Para bucles anidados, es una referencia al bucle
                            externo.
==========================  ====================================================

if
--

La etiqueta ``{% if %}`` evalua una variable. Si dicha variable se evalua como
una expresión "verdadera" (Es decir, que el valor exista, no esté vacia y no
es el valor booleano ``False``), se muestra el contenido del bloque::

    {% if athlete_list %}
        Number of athletes: {{ athlete_list|length }}
    {% else %}
        No athletes.
    {% endif %}

Si la lista ``athlete_list`` no está vacía, podemos mostrar el
número de atletas con la expresión ``{{ athlete_list|length }}``

Además, como se puede ver en el ejemplo, la etiqueta ``if`` puede
tener un bloque opcional ``{% else %}`` que se mostrará en el
caso de que la evaluación de falso.

Las etiquetas ``if`` pueden usar operadores lógicos como
``and``, ``or`` y ``not`` para evaluar expresiones más
complejas::

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
        There are no athletes or there are some coaches (OK, so
        writing English translations of Boolean logic sounds
        stupid; it's not our fault).
    {% endif %}

    {% if athlete_list and not coach_list %}
        There are some athletes and absolutely no coaches.
    {% endif %}

La etiqueta ``if`` no admite, sin embargo, mezclar los operadores
``and`` y ``or`` dentro de la misma comprobación, porque la orden
de aplicación de los operadores lógicos sería ambigua. Por ejemplo,
el siguiente código es inválido::

    {% if athlete_list and coach_list or cheerleader_list %}

Para combinar operadores ``and`` y ``or``, puedes usar sentencias
``if`` anidadas, como en el siguiente ejemplo::

    {% if athlete_list %}
        {% if coach_list or cheerleader_list %}
            We have athletes, and either coaches or cheerleaders!
        {% endif %}
    {% endif %}

Es perfectamente posible usar varias veces un operador lógico, siempre
que sea el mismo siempre. Por ejemplo, el siguiente código es válido::

    {% if athlete_list or coach_list or parent_list or teacher_list %}

ifchanged
---------

Comprueba si un valor ha sido cambiado desde la última iteración de un bucle.

La etiqueta ``ifchanged`` solo tiene sentido dentro de un bucle. Tiene dos
usos posibles:

1. Comprueba su propio contenido mostrado contra su estado anterior, y
   solo lo muestra si el contenido ha cambiado. El siguiente ejemplo
   muestra una lista de días, y solo aparecerá el nombre del mes
   si este cambia::

        <h1>Archive for {{ year }}</h1>

        {% for date in days %}
            {% ifchanged %}<h3>{{ date|date:"F" }}</h3>{% endifchanged %}
            <a href="{{ date|date:"M/d"|lower }}/">{{ date|date:"j" }}</a>
        {% endfor %}

2. Se le pasa una o más variables, y se comprueba si esas variables han sido
   cambiadas::

        {% for date in days %}
            {% ifchanged date.date %} {{ date.date }} {% endifchanged %}
            {% ifchanged date.hour date.date %}
                {{ date.hour }}
            {% endifchanged %}
        {% endfor %}

   El ejemplo anterior muestra la fecha cada vez que cambia, pero sólo
   muestra la hora si tanto la hora como el día han cambiado.

ifequal
-------

Muestra el contenido del bloque si los dos argumentos suministrados
son iguales.

He aquí un ejemplo::

    {% ifequal user.id comment.user_id %}
        ...
    {% endifequal %}

Al igual que con la etiqueta ``{% if %}``, existe una cláusula ``{% else %}`` opcional.

Los argumentos pueden ser cadenas de texto, así que el siguiente código es
válido::

    {% ifequal user.username "adrian" %}
        ...
    {% endifequal %}

Sólo se puede comprobar la igualdad de variables o cadenas de texto. No se
puede comparar con objetos Python como ``True`` o ``False``. Para ello, utilice
la etiqueta ``if`` directamente.

ifnotequal
----------

Es igual que ``ifequal``, excepto que comprueba que los dos parámetros
suministrados *no* sean iguales.

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


load
----

Carga una biblioteca de plantillas. En el `Capítulo 10`_ puedes encontrar
más información acerca de las bibliotecas de plantillas.

now
---

Muestra la fecha, escrita de acuerdo a un formato indicado.

Esta etiqueta fue inspirada por la función ``date()`` de PHP(), y
utiliza el mismo formato que esta (http://php.net/date). La versión
Django tiene, sin embargo, algunos extras.

La tabla F-2 muestra las cadenas de formato que se pueden utilizar.

.. tabla:: Tabla F-2. Cadenas de formato para fechas y horas

==============  ========================================  ==================================================
Carác. formato  Descripción                               Ejemplo de salida
==============  ========================================  ==================================================
a               ``'a.m.'`` o ``'p.m.'``. (Obsérvese       ``'a.m.'``
                que la salida es ligeramente distinta
                de la de PHP, ya que aquí se incluyen
                puntos para adecuarse al libro de estilo
                de Associated Press).
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
==============  ========================================  ==================================================


He aquí un ejemplo::

    It is {% now "jS F Y H:i" %}

Se pueden escapar los caracteres de formato con una barra invertida, si se
quieren incluir de forma literal. En el siguiente ejemplo, se escapa el
significado de la letra "f" con la barra invertida, ya que de otra manera
se interpretaría como una indicación de incluir la hora. La "o", por otro
lado, no necesita ser escapada, ya que no es un carácter de formato::

    It is the {% now "jS o\f F" %}

El ejemplo mostraría: "It is the 4th of September".

regroup
-------

Reagrupa una lista de objetos similares usando un atributo común.

Para comprender esta etiqueta, es mejor recurrir a un ejemplo. Digamos
que ``people`` es una lista de objetos de tipo ``Person``, y que dichos
objetos tienen los atributos ``first_name``, ``last_name`` y ``gender``. Queremos
mostrar un listado como el siguiente::

* Male:
    * George Bush
    * Bill Clinton
* Female:
    * Margaret Thatcher
    * Condoleezza Rice
* Unknown:
    * Pat Smith

El siguiente fragmento de plantilla mostraría como realizar esta
tarea::

    {% regroup people by gender as grouped %}
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

    {% regroup people|dictsort:"gender" by gender as grouped %}


spaceless
---------

Elimina los espacios en blanco entre etiquetas Html. Esto incluye
tabuladores y saltos de línea.

El siguiente ejemplo::

    {% spaceless %}
        <p>
            <a href="foo/">Foo</a>
        </p>
    {% endspaceless %}

Retornaría el siguiente código HTML::

    <p><a href="foo/">Foo</a></p>

Sólo se eliminan los espacios *entre* las etiquetas, no los espacios
entre la etiqueta y el texto. En el siguiente ejemplo, no se quitan
los espacios que rodean la palabra ``Hello``::

    {% spaceless %}
        <strong>
            Hello
        </strong>
    {% endspaceless %}

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

.. tabla:: Tabla F-3. Argumentos válidos de templatetag

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

url
---

Devuelve una URL absoluta (Es decir, una URL sin la parte del dominio) que
coincide con una determinada vista, incluyendo sus parámetros opcionales. De
esta forma se posibilita realizar enlaces sin violar el
principio DRY, codificando las direcciones en nuestras plantillas::

    {% url path.to.some_view arg1,arg2,name1=value1 %}

El primer argumento es la ruta a la función de vista, en el formato
``paquete.paquete.modulo.funcion``. El resto de parámetros son opcionales
y deben ir separados con comas, convirtiéndose en parámetros posicionales
o por nombre que se incluirán en la URL. Deben estar presentes todos los
argumentos que se hayan definido como obligatorios en el URLconf.

Por ejemplo, supongamos que tenemos una vista,  ``app_name.client``, y que
en el URLconf se la indica que acepta un parámetro, el identificador
del cliente. La línea del URL podría ser algo así::

    ('^client/(\d+)/$', 'app_name.client')

Si este URLconf fuera incluido en el URLconf del proyecto bajo un
directorio, como en este ejemplo::

    ('^clients/', include('project_name.app_name.urls'))

Podríamos crear un enlace a esta vista, en nuestra plantilla, con la
siguiente etiqueta::

    {% url app_name.client client.id %}

La salida de esta etiqueta será ``/clients/client/123/``.

widthratio
----------

Esta etiqueta es útil para presentar gráficos de barras y similares. Calcula
la proporción entre un valor dado y un máximo predefinido, y luego multiplica ese
cociente por una constante.

Veamos un ejemplo::

    <img src="bar.gif" height="10" width="{% widthratio this_value max_value 100 %}" />

Si ``this_value`` vale 175 y ``max_value`` es 200, la imagen resultante
tendrá un ancho de 88 pixels (porque 175/200 = 0.875 y 0.875 * 100 = 87.5,
que se redondea a 88).

Filtros predefinidos
====================

add
---

Ejemplo::

    {{ value|add:"5" }}

Suma el argumento indicado.

addslashes
----------

Ejemplo::

    {{ string|addslashes }}

Añade barras invertidas antes de las comillas, ya sean simples o dobles. Es útil para
pasar cadenas de texto como javascript, por ejemplo:

capfirst
--------

Ejemplo::

    {{ string|capfirst }}

Pasa a mayúsculas la primera letra de la primera palabra.

center
------

Ejemplo::

    {{ string|center:"50" }}

Centra el texto en un campo de la anchura indicada.

cut
---

Ejemplo::

    {{ string|cut:"spam" }}

Elimina todas las apariciones del valor indicado.

date
----

Ejemplo::

    {{ value|date:"F j, Y" }}

Formatea una fecha de acuerdo al formato indicado en la cadena de texto (Se usa
el mismo formato que con la etiqueta ``now``).

default
-------

Ejemplo::

    {{ value|default:"(N/A)" }}

Si ``value`` no está definido, se usa el valor del argumento en su lugar.


default_if_none
---------------

Ejemplo::

    {{ value|default_if_none:"(N/A)" }}

Si ``value`` es nulo, se usa el valor del argumento en su lugar.

dictsort
--------

Ejemplo::

    {{ list|dictsort:"foo" }}

Acepta una lista de diccionarios y devuelve una lista ordenada según la
propiedad indicada en el argumento.

dictsortreversed
------------------

Ejemplo::

    {{ list|dictsortreversed:"foo" }}

Acepta una lista de diccionarios y devuelve una lista ordenada de forma
descendente según la propiedad indicada en el argumento.

divisibleby
------------

Ejemplo::

    {% if value|divisibleby:"2" %}
        Even!
    {% else %}
        Odd!
    {% else %}

Devuelve ``True`` si es valor pasado es divisible por el argumento.

escape
------

Ejemplo::

    {{ string|escape }}

Transforma un texto que esté en HTML de forma que se pueda representar en una página web. Concretamente, realiza
los siguientes cambios:

* ``"&"`` a ``"&amp;"``
* ``<`` a ``"&lt;"``
* ``>`` a ``"&gt;"``
* ``'"'`` (comilla doble) a ``'&quot;'``
* ``"'"`` (comillas simple) a ``'&#39;'``

filesizeformat
--------------

Ejemplo::

    {{ value|filesizeformat }}

Representa un valor, interpretándolo como si fuera el tamaño de un fichero y
"humanizando" el resultado, de forma que sea fácil de leer. Por ejemplo, las
salidas podrían ser ``'13 KB'``, ``'4.1 MB'``, ``'102 bytes'``, etc.

first
-----

Ejemplo::

    {{ list|first }}

Devuelve el primer elemento de una lista.

fix_ampersands
---------------

Ejemplo::

    {{ string|fix_ampersands }}

Reemplaza los símbolos *ampersand* con la entidad ``&amp;``.

floatformat
-----------

Ejemplos::

    {{ value|floatformat }}
    {{ value|floatformat:"2" }}

Si se usa sin argumento, redondea un número en coma flotante a un único
dígito decimal (pero sólo si hay una parte decimal que mostrar), por
ejemplo:

* ``36.123`` se representaría como ``36.1``.
* ``36.15`` se representaría como ``36.2``.
* ``36`` se representaría como ``36``.

Si te utiliza un argumento numérico, ``floatformat`` redondea a ese número
de lugares decimales:

* ``36.1234`` con floatformat:3 se representaría como ``36.123``.
* ``36`` con floatformat:4 se representaría como ``36.0000``.

Si el argumento pasado a ``floatformat`` es negativo, redondeará a ese
número de decimales, pero sólo si el número tiene parte decimal.

* ``36.1234`` con floatformat:-3 gets converted to ``36.123``.
* ``36`` con floatformat:-4 gets converted to ``36``.

Usar ``floatformat`` sin argumentos es equivalente a usarlo con un argumento
de -1.

get_digit
---------

Ejemplo::

    {{ value|get_digit:"1" }}

Dado un número, devuelve el dígito que esté en la posición indicada, siendo
1 el dígito más a la derecha. En caso de que la entrada sea inválida, devolverá
el valor original (Si la entrada o el argumento no fueran enteros, o si
el argumento fuera inferior a 1). Si la entrada es correcta, la salida siempre
será un entero.

join
----

Ejemplo::

    {{ list|join:", " }}

Concatena todos los elementos de una lista para formar una cadena
de texto, usando como separador el texto que se le pasa como
argumento. Es equivalente a la llamada en Python ``str.join(list)``

length
------

Ejemplo::

    {{ list|length }}

Devuelve la longitud del valor.

length_is
---------

Ejemplo::

    {% if list|length_is:"3" %}
        ...
    {% endif %}

Devuelve un valor booleano que será verdadero si la longitud
de la entrada coincide con el argumento suministrado.

linebreaks
----------

Ejemplo::

    {{ string|linebreaks }}

Convierte los saltos de línea en etiquetas ``<p>`` y ``<br />``.

linebreaksbr
------------

Ejemplo::

    {{ string|linebreaksbr }}

Convierte los saltos de línea en etiquetas ``<br />``.

linenumbers
-----------

Ejemplo::

    {{ string|linenumbers }}

Muestra el texto de la entrada con números de línea.

ljust
-----

Ejemplo::

    {{ string|ljust:"50" }}

Justifica el texto de la entrada a la izquierda utilizando
la anchura indicada.


lower
-----

Ejemplo::

    {{ string|lower }}

Convierte el texto de la entrada a letras minúsculas.

make_list
---------

Ejemplo::

    {% for i in number|make_list %}
        ...
    {% endfor %}

Devuelve la entrada en forma de lista. Si la entrada es un número
entero, se devuelve una lista de dígitos. Si es una cadena de
texto, se devuelve una lista de caracteres.

phone2numeric
-------------

Ejemplo::

    {{ string|phone2numeric }}

Convierte un número de teléfono (que incluso puede contener letras) a
su forma numérica equivalente. Por ejemplo ``'800-COLLECT'`` se transformará
en ``'800-2655328'``.

La entrada no tiene porque ser un número de teléfono válido. El filtro
convertirá alegremente cualquier texto que se le pase.

pluralize
---------

Ejemplo::

    The list has {{ list|length }} item{{ list|pluralize }}.

Retorno el sufijo para formar el plural si el valor es mayor que uno. Por
defecto el sufijo es ``'s'``.

Ejemplo::

    You have {{ num_messages }} message{{ num_messages|pluralize }}.

Para aquellas palabras que requieran otro sufijo para formar el plural, podemos
usar una sintaxis alternativa en la que indicamos el sufijo que queramos
con un argumento.

Ejemplo::

    You have {{ num_walruses }} walrus{{ num_walrus|pluralize:"es" }}.

Para aquellas palabras que forman el plural de forma más compleja que
con un simple sufijo, hay otra tercera sintaxis que permite indicar
las formas en singular y en plural a partir de una raíz común.

Ejemplo::

    You have {{ num_cherries }} cherr{{ num_cherries|pluralize:"y,ies" }}.

pprint
------

Ejemplo::

    {{ object|pprint }}

Un recubrimiento que permite llamar a la función de Python ``pprint.pprint``. Se
usa sobre todo para tareas de depurado de errores.

random
------

Ejemplo::

    {{ list|random }}

Devuelve un elemento elegido al azar de la lista.

removetags
----------

Ejemplo::

    {{ string|removetags:"br p div" }}

Elimina de la entrada una o varias clases de etiquetas [X]HTML. Las etiquetas
se indican en forma de texto, separando cada etiqueta a eliminar por un
espacio.

rjust
-----

Ejemplo::

    {{ string|rjust:"50" }}

Justifica el texto de la entrada a la derecha utilizando
la anchura indicada..

slice
-----

Ejemplo::

    {{ some_list|slice:":2" }}

Devuelve una sección de la lista.

Usa la misma sintaxis que se usa en Python para seccionar una lista.
Véase
http://diveintopython.org/native_data_types/lists.html#odbchelper.list.slice
para una explicación.

slugify
-------

Ejemplo::

    {{ string|slugify }}

Convierte el texto a minúsculas, elimina los caracteres que no
formen palabras (caracteres alfanuméricos y carácter subrayado), y
convierte los espacios en guiones. También elimina los espacios
que hubiera al principio y al final del texto.

stringformat
------------

Ejemplo::

    {{ number|stringformat:"02i" }}

Formatea el valor de entrada de acuerdo a lo especificado en el formato
que se le pasa como parámetro. La sintaxis a utilizar es idéntica a la
de Python, con la excepción de que el carácter "%" se omite.

En http://docs.python.org/lib/typesseq-strings.html puedes consultar
las opciones de formateo de cadenas de Python.

striptags
---------

Ejemplo::

    {{ string|striptags }}

Elimina todas las etiquetas [X]HTML.

time
----

Ejemplo::

    {{ value|time:"P" }}

Formatea la salida asumiendo que es una fecha/hora, con el formato indicado como
argumento (Lo mismo que la etiqueta ``now``).

timesince
---------

Ejemplos::

    {{ datetime|timesince }}
    {{ datetime|timesince:"other_datetime" }}

Representa una fecha como un intervalo de tiempo (por ejemplo, "4 days, 6 hours").

Acepta un argumento opcional, que es una variable con la fecha a usar como
punto de referencia para calcular el intervalo (Si no se especifica, la
referencia es el momento actual). Por ejemplo, si ``blog_date`` es una fecha
con valor igual a la medianoche del 1 de junio de 2006, y ``comment_date`` es
una fecha con valor las 08:00 horas del día 1 de junio de 2006, entonces
``{{ comment_date|timesince:blog_date }}`` devolvería "8 hours".

timeuntil
---------

Ejemplos::

    {{ datetime|timeuntil }}
    {{ datetime|timeuntil:"other_datetime" }}

Es similar a ``timesince``, excepto en que mide el tiempo desde
la fecha de referencia hasta la fecha dada. Por ejemplo, si hoy
es 1 de junio de 2006 y ``conference_date`` es una fecha cuyo valor
es igual al 29 de junio de 2006, entonces
``{{ conference_date|timeuntil }}`` devolvería "28 days".

Acepta un argumento opcional, que es una variable con la fecha a usar como
punto de referencia para calcular el intervalo, si se quiere usar otra
distinta del momento actual. Si ``from_date`` apunta al 22 de junio de
2006, entonces ``{{ conference_date|timeuntil:from_date }}``
devolvería "7 days".

title
-----

Ejemplo::

    {{ string|titlecase }}

Representa una cadena de texto en forma de título, siguiendo las convenciones
del idioma inglés (todas las palabras con la inicial en mayúscula).

truncatewords
-------------

Ejemplo::

    {{ string|truncatewords:"15" }}

Recorta la salida de forma que tenga como máximo el número de palabras
que se indican en el argumento.

truncatewords_html
------------------

Ejemplo::

    {{ string|truncatewords_html:"15" }}

Es similar a ``truncatewords``, excepto que es capaz de reconocer las
etiquetas HTML y, por tanto, no deja etiquetas "huérfanas". Cualquier
etiqueta que se hubiera abierto antes del punto de recorte es cerrada
por el propio filtro.

Es menos eficiente que ``truncatewords``, así que debe ser usada solamente
si sabemos que en la entrada va texto HTML.

unordered_list
--------------

Ejemplo::

    <ul>
        {{ list|unordered_list }}
    </ul>

Acepta una lista, e incluso varias listas anidadas, y recorre
recursivamente las mismas representándolas en forma de listas
HTML no ordenadas, *sin incluir* las etiquetas de inicio
y fin de lista (``<ul>`` y ``</ul>`` respectivamente).

Se asume que las listas está en el formato correcto. Por ejemplo, si
``var`` contiene
``['States', [['Kansas', [['Lawrence', []], ['Topeka', []]]], ['Illinois', []]]]``,
entonces ``{{ var|unordered_list }}`` retornaría lo siguiente::

    <li>States
    <ul>
            <li>Kansas
            <ul>
                    <li>Lawrence</li>
                    <li>Topeka</li>
            </ul>
            </li>
            <li>Illinois</li>
    </ul>
    </li>

upper
-----

Ejemplo::

    {{ string|upper }}

Convierte una string a mayúsculas.

urlencode
---------

Ejemplo::

    <a href="{{ link|urlencode }}">linkage</a>

Escapa la entrada de forma que pueda ser utilizado dentro de una URL.

urlize
------

Ejemplo::

    {{ string|urlize }}

Transforma un texto de entrada, de forma que si contiene direcciones
URL en texto plano, las convierte en enlaces HTML.

urlizetrunc
------------

Ejemplo::

    {{ string|urlizetrunc:"30" }}

Convierte las direcciones URL de un texto en enlaces, recortando la representación
de la URL para que el número de caracteres sea como máximo el del argumento
suministrado.

wordcount
---------

Ejemplo::

    {{ string|wordcount }}

Devuelve el número de palabras en la entrada.

wordwrap
--------

Ejemplo::

    {{ string|wordwrap:"75" }}

Ajusta la longitud del texto para las líneas se adecúen a la longitud
especificada como argumento.

yesno
-----

Ejemplo::

    {{ boolean|yesno:"Yes,No,Perhaps" }}

Dada una serie de textos que se asocian a los
valores de ``True``, ``False`` y (opcionalmente) ``None``, devuelve
uno de esos textos según el valor de la entrada. Véase la
tabla F-4.


.. tabla:: Tabla F-4. Ejemplos del filtro yesno

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
