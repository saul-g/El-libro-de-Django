==================================================
Apéndice B: Referencia de la definición de modelos
==================================================

El :doc:`Capítulo 5<chapter05>` explica lo básico de la definición de modelos, y lo utilizamos en
el resto del libro.  Existe un enorme rango de opciones disponibles que no se
han cubierto en otro lado. Este apéndice explica toda opción disponible en la
definición de modelos.

A pesar de que estas APIs se consideran muy estables, los desarrolladores de
Django agregan en forma consistente nuevos atajos y conveniencias a la
definición de modelos. Es buena idea chequear siempre la última documentación
online en http://www.djangoproject.com/documentation/

Campos
======

La parte más importante de un modelo -- y la única parte requerida de un modelo
-- es la lista de campos de la base de datos que define.

.. admonition:: Restricciones en el nombre de los campos

    Django pone solo dos restricciones en el nombre de los campos:

1. Un nombre de campo no puede ser una palabra reservada de Python,
   porque eso ocasionaría un error de sintaxis en Python, por ejemplo::

        class Example(models.Model):
            pass = models.IntegerField() # 'pass' es una palabra reservada!

2. Un nombre de campo no puede contener dos o más guiones bajos
   consecutivos, debido a la forma en que trabaja la sintaxis de las
   consultas de búsqueda de , por ejemplo::

        class Example(models.Model):
            foo__bar = models.IntegerField() # 'foo__bar' tiene dos guiones bajos!

Estas limitaciones se pueden manejar sin mayores problemas, dado que el
nombre del campo no necesariamente tiene que coincidir con el nombre de la
columna en la base de datos. Ver "db_column", más abajo.

Las palabras reservadas de SQL, como ``join``, ``where``, o ``select``,
*son* permitidas como nombres de campo, dado que Django "escapea" todos los
nombres de tabla y columna de la base de datos en cada consulta SQL
subyacente. Utiliza la sintaxis de "quoteo" del motor de base de datos
particular.


Cada campo en tu modelo debe ser una instancia de la clase de campo apropiada.
Django usa los tipos de clase ``Field`` para determinar algunas cosas:

* El tipo de columna de la base de datos (ej.:, ``INTEGER``, ``VARCHAR``).

* El widget a usar en la interfaz de administración de Django, si vas a
  usarla (ej., ``<input type="text">``, ``<select>``).

* Los requerimientos mínimos de validación, que se usan en la interfaz de
  administración de Django.

A continuación, una lista completa de las clases de campo, ordenadas
alfabéticamente. Los campos de relación (``ForeignKey``, etc.) se tratan en la
siguiente sección.


AutoField
---------

Un ``IntegerField`` que se incrementa automáticamente de acuerdo con los IDs
disponibles.  Normalmente no necesitarás utilizarlos directamente; se agrega un
campo de clave primaria automáticamente a tu modelo si no especificas una clave
primaria.

BooleanField
------------

Un campo Verdadero/Falso.

CharField
---------

Un campo string, para cadenas cortas o largas. Para grandes cantidades de texto,
usa ``TextField``.

``CharField`` requiere un argumento extra, ``max_length``, que es la longitud
máxima (en caracteres) del campo. Esta longitud máxima es reforzada a nivel de
la base de datos y en la validación de Django.

CommaSeparatedIntegerField
--------------------------

Un campo de enteros separados por comas. Igual que en ``CharField``, se
requiere el argumento ``max_length``.

DateField
---------

Un campo de fecha. ``DateField`` tiene algunos argumentos opcionales extra,
como se muestra en la Tabla B-1.

.. tabla:: Tabla B-1. Argumentos opcionales extra de DateField

======================  ===================================================
    Argumento               Descripción
======================  ===================================================
    ``auto_now``        Asigna automáticamente al campo un valor igual al
                        momento en que se guarda el objeto. Es útil para
                        las marcas de tiempo "última modificación".
                        Observar que *siempre* se usa la fecha actual; no
                        es un valor por omisión que se pueda sobreescribir.

    ``auto_now_add``    Asigna automáticamente al campo un valor igual al
                        momento en que se crea el objeto. Es útil para la
                        creación de marcas de tiempo. Observar que
                        *siempre* se usa la fecha actual; no es un valor
                        por omisión que se pueda sobreescribir.
======================  ===================================================

DateTimeField
-------------

Un campo de fecha y hora. Tiene las mismas opciones extra que ``DateField``.

EmailField
----------

Un ``CharField`` que chequea que el valor sea una dirección de email válida. No
acepta ``max_length``; su ``max_length`` se establece automáticamente en 75.

FileField
---------

Un campo de upload de archivos. Tiene un argumento *requerido*, como se ve en
la Tabla B-2.

.. tabla:: Tabla B-2. Opciones extra de FileField

======================  ===================================================
    Argumento                Descripción
======================  ===================================================
    ``upload_to``       Una ruta del sistema de archivos local que se
                        agregará a la configuración de ``MEDIA_ROOT``
                        para determinar el resultado de la función de ayuda
                        ``get_<fieldname>_url()``
======================  ===================================================

Esta ruta puede contener formato ``strftime`` (ver
http://www.djangoproject.com/r/python/strftime/), que será reemplazada por la
fecha y hora del upload del archivo (de manera que los archivos subidos no
llenen el directorio dada).

El uso de un ``FileField`` o un ``ImageField`` en un modelo requiere algunos
pasos:

1. En el archivo de configuración (settings), es necesario definir
   ``MEDIA_ROOT`` con la ruta completa al directorio donde quieras que
   Django almacene los archivos subidos. (Por performance, estos archivos
   no se almacenan en la base de datos.) Definir ``MEDIA_URL`` con la URL
   pública base de ese directorio. Asegurarse de que la cuenta del usuario
   del servidor web tenga permiso de escritura en este directorio.

2. Agregar el ``FileField`` o ``ImageField`` al modelo, asegurándose de
   definir la opción ``upload_to`` para decirle a Django a cual
   subdirectorio de ``MEDIA_ROOT`` debe subir los archivos.

3. Todo lo que se va a almacenar en la base de datos es la ruta al archivo
   (relativa a ``MEDIA_ROOT``). Seguramente preferirás usar la facilidad de
   la función ``get_<fieldname>_url`` provista por Django. Por ejemplo, si
   tu ``ImageField`` se llama ``mug_shot``, puedes obtener la URL absoluta
   a tu image en un plantilla con ``{{object.get_mug_shot_url }}``.

Por ejemplo, digamos que tu ``MEDIA_ROOT`` es ``'/home/media'``, y
``upload_to`` es ``'photos/%Y/%m/%d'``. La parte ``'%Y/%m/%d'`` de
``upload_to`` es formato strftime; ``'%Y'`` es el año en cuatro dígitos,
``'%m'`` es el mes en dos digitos, y ``'%d'`` es el día en dos dígitos. Si
subes un archivo el 15 de enero de 2007, será guardado en
``/home/media/photos/2007/01/15``.

Si quieres recuperar el nombre en disco del archivo subido, o una URL que se
refiera a ese archivo, o el tamaño del archivo, puedes usar los métodos
``get_FIELD_filename()``, ``get_FIELD_url()``, y ``get_FIELD_size()``. Ver
el Apéndice C para una explicación completa de estos métodos.

.. admonition:: Nota.

    Cualquiera sea la forma en que manejes tus archivos subidos, tienes que
    prestar mucha atención a donde los estás subiendo y que tipo de archivos
    son, para evitar huecos en la seguridad. *Valida todos los archivos
    subidos* para asegurarte que esos archivos son lo que piensas que son.

    Por ejemplo, si dejas que cualquiera suba archivos ciegamente, sin
    validación, a un directorio que está dentro de la raíz de documentos
    (*document root*) de tu servidor web, alguien podría subir un script CGI o
    PHP y ejecutarlo visitando su URL en tu sitio. ¡No permitas que pase!

FilePathField
-------------

Un campo cuyas opciones están limitadas a los nombres de archivo en un cierto
directorio en el sistema de archivos. Tiene tres argumentos especiales, que se
muestran en la Tabla B-3.

.. tabla:: Tabla B-3. Opciones extra de FilePathField

======================  ===================================================
    Argumento               Descripción
======================  ===================================================
    ``path``            *Requerido*; la ruta absoluta en el sistema de
                        archivos hacia el directorio del cual este
                        ``FilePathField`` debe tomar sus opciones
                        (ej.: ``"/home/images"``).

    ``match``           Opcional; una expresión regular como string, que
                        ``FilePathField`` usará para filtrar los nombres
                        de archivo. Observar que la regex será aplicada al
                        nombre de archivo base, no a la ruta completa (ej.:
                        ``"foo.*\.txt^"``, va a matchear con un archivo
                        llamado ``foo23.txt``, pero no con ``bar.txt`` o
                        ``foo23.gif``).

    ``recursive``       Opcional; ``True`` o ``False``.El valor por omisión
                        es ``False``. Especifica si deben incluirse todos
                        los subdirectorios de ``path``.
======================  ===================================================

Por supuesto, estos argumentos pueden usarse juntos.

El único 'gotcha' potencial es que ``match`` se aplica sobre el nombre de
archivo base, no la ruta completa. De esta manera, este ejemplo::

    FilePathField(path="/home/images", match="foo.*", recursive=True)

va a matchear con ``/home/images/foo.gif`` pero no con
``/home/images/foo/bar.gif`` porque el  ``match`` se aplica al nombre de
archivo base (``foo.gif`` y ``bar.gif``).

FloatField
----------

Un numero de punto flotante, representado en Python por una instancia de
``float``. Tiene dos argumentos requeridos, que se muestran en la Tabla B-4.

.. tabla:: Tabla B-4. Opciones extra de FloatField

======================  ===================================================
    Argumento               descripción
======================  ===================================================
    ``max_digits``      La cantidad máximo de dígitos permitidos en el
                        número.

   ``decimal_places``   La cantidad de posiciones decimales a almacenar con
                        el número.
======================  ===================================================

Por ejemplo, para almacenar números hasta 999 con una resolución de dos
decimales, hay que usar::

    models.FloatField(..., max_digits=5, decimal_places=2)

Y para almacenar números hasta aproximadamente mil millones con una resolución
de diez dígitos decimales, hay que usar::

    models.FloatField(..., max_digits=19, decimal_places=10)

ImageField
----------

Similar a ``FileField``, pero valida que el objeto subido sea una imagen
válida. Tiene dos argumentos opcionales extra, ``height_field`` y
``width_field``, que si se utilizan, serán auto-rellenados con la altura y el
ancho de la imagen cada vez que se guarde una instancia del modelo.

Además de los métodos especiales ``get_FIELD_*`` que están disponibles para
``FileField``, un ``ImageField`` tiene también los métodos
``get_FIELD_height()`` y ``get_FIELD_width()``. Éstos están documentados en el
Apéndice C.

``ImageField`` requiere la biblioteca Python Imaging Library
(http://www.pythonware.com/products/pil/).

IntegerField
------------

Un entero.

IPAddressField
--------------

Una dirección IP, en formato string (ej.: ``"24.124.1.30"``).

NullBooleanField
----------------

Similar a ``BooleanField``, pero permite ``None``/``NULL`` como opciones.
Usar éste en lugar de un ``BooleanField`` con ``null=True``.

PhoneNumberField
----------------

Un ``CharField`` que chequea que el valor es un teléfono válido estilo U.S.
(en formato ``XXX-XXX-XXXX``).

.. Admonition:: Nota:

    Si necesitas representar teléfonos de otros países, consulta el paquete
    ``django.contrib.localflavor`` para ver si ya están incluidas las
    definiciones para tu país.

PositiveIntegerField
--------------------

Similar a ``IntegerField``, pero debe ser positivo.

PositiveSmallIntegerField
-------------------------

Similar a ``PositiveIntegerField``, pero solo permite valores por debajo de un
límite. El valor máximo permitido para estos campos depende de la base de
datos, pero como las bases de datos tienen un tipo entero corto de 2 bytes, el
valor máximo positivo usualmente es 65,535.

SlugField
---------

"Slug" es un término de la prensa. Un *slug* es una etiqueta corta para algo,
que contiene solo letras, números, guiones bajos o simples. Generalmente se
usan en URLs.

De igual forma que en ``CharField``, puedes especificar ``max_length``. Si
``max_length`` no está especificado, Django asume un valor por omisión de 50.


Un ``SlugField`` implica ``db_index=True`` debido a que son los se usan
principalmente para búsquedas en la base de datos.

``SlugField`` acepta una opción extra, ``prepopulate_from``, que es una lista
de campos a partir de los cuales auto-rellenar el slug, vía JavaScript, en el
formulario de administración del objeto::

    models.SlugField(prepopulate_from=("pre_name", "name"))

``prepopulate_from`` no acepta nombres ``DateTimeField`` como argumentos.

SmallIntegerField
-----------------

Similar a ``IntegerField``, pero solo permite valores en un cierto rango
dependiente de la base de datos (usualmente -32,768 a +32,767).

TextField
---------

Un campo de texto de longitud ilimitada.

TimeField
---------

Un campo de hora. Acepta las mismas opciones de autocompletación de
``DateField`` y ``DateTimeField``.

URLField
--------

Un campo para una URL. Si la opción ``verify_exists`` es ``True`` (valor por
omisión), se chequea la existencia de la URL dada (la URL carga y no da una
respuesta 404).

Como los otros campos de caracteres, ``URLField`` toma el argumento
``max_length``. Si no se especifica, el valor por omisión es 200.


USStateField
------------

Una abreviatura de dos letras de un estado de U.S.

.. admonition:: Nota:

    Si necesitas representar otros países o estados, busca en el paquete
    ``django.contrib.localflavor`` para ver si Django ya incluye los campos
    para tu localización.


XMLField
--------

Un ``TextField`` que chequea que el valor sea un XML válido que matchea con un
esquema dado. Tiene un argumento requerido, ``schema_path``, que es la ruta en
el sistema de archivos a un esquema RELAX NG (http://www.relaxng.org/) contra
el cual validar el campo.

Requiere ``jing`` (http://thaiopensource.com/relaxng/jing.html) para validar el
XML.

Opciones Universales de Campo
=============================

Los siguientes argumentos están disponibles para todos los tipos de campo.
Todos son opcionales.

null
----

Si está en ``True``, Django almacenará valores vacíos como ``NULL`` en la base
de datos. El valor por omisión es ``False``.

Observar que los valores de string nulo siempre se almacenan como strings
vacíos, no como ``NULL``. Utiliza ``null=True`` solo para campos no-string,
como enteros, booleanos y fechas. En los dos casos, también necesitarás
establecer ``blank=True`` si deseas permitir valores vacíos en los formularios,
ya que el parámetro ``null`` solo afecta el almacenamiento en la base de datos
(ver la siguiente sección, titulada "`blank`_").

Evita utilizar ``null`` en campos basados en string como ``CharField`` y
``TextField`` salvo que tengas una excelente razón para hacerlo. Si un campo
basado en string tiene ``null=True``, eso significa que tiene dos valores
posibles para "sin datos": ``NULL`` y el string vacío. En la mayoría de los
casos, esto es redundante; la convención de Django es usar el string vacío, no
``NULL``.

blank
-----

Si está en ``True``, está permitido que el campo esté en blanco. El valor por
omisión es ``False``.

Observar que esto es diferente de ``null``. ``null`` solo se relaciona con la
base de datos, mientras que ``blank`` está relacionado con la validación. Si
un campo tiene ``blank=True``, la validación del administrador de Django
permitirá la entrada de un valor vacío. Si un campo tiene ``blank=False``, es
un campo requerido.

choices
-------

Un iterable (ej.: una lista, tupla, o otro objeto iterable de Python) de dos
tuplas para usar como opciones para este campo.

Si esto está dado,la interfaz de administración de Django utilizará un cuadro
de selección en lugar del campo de texto estándar, y limitará las opciones a
las dadas.

Una lista de opciones se ve así::

    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    )

El primer elemento de cada tupla es el valor real a ser almacenado.
El segundo elemento es el nombre legible por humanos para la opción.

La lista de opciones puede ser definida también como parte de la clase del
modelo::

    class Foo(models.Model):
        GENDER_CHOICES = (
            ('M', 'Male'),
            ('F', 'Female'),
        )
        gender = models.CharField(maxlength=1, choices=GENDER_CHOICES)

o fuera de la clase del modelo::

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    class Foo(models.Model):
        gender = models.CharField(maxlength=1, choices=GENDER_CHOICES)

Para cada campo del modelo que tenga establecidas ``choices``, Django agregará
un método para recuperar el nombre legible por humanos para el valor actual del
campo. Ver Apéndice C para más detalles.

db_column
---------

El nombre de la columna de la base de datos a usar para este campo. Si no está
dada, Django utilizará el nombre del campo. Esto es útil cuando estás
definiendo un modelo sobre una base de datos existente.

Si tu nombre de columna de la base de datos es una palabra reservada de SQL, o
contiene caracteres que no están permitidos en un nombre de variable de Python
(en particular el guión simple), no hay problema. Django quotea los nombres de
columna y tabla detrás de la escena.

db_index
--------

Si está en ``True``, Django creará un índice en la base de datos para esta
columna cuando cree la tabla (es decir, cuando ejecute ``manage.py syncdb``).

default
-------

El valor por omisión del campo.

editable
--------

Si es ``False``, el campo no será editable en la interfaz de administración o
via procesamiento de formularios. El valor por omisión es ``True``.

help_text
---------

Texto de ayuda extra a ser mostrado bajo el campo en el formulario de
administración del objeto.  Es útil como documentación aunque tu objeto no tenga
formulario de administración.

primary_key
-----------

Si es ``True``, este campo es la clave primaria del modelo.

Su no se especifica ``primary_key=True`` para ningún campo del modelo, Django
agregará automáticamente este campo::

    id = models.AutoField('ID', primary_key=True)

Por lo tanto, no necesitas establecer ``primary_key=True`` en ningún campo,
salvo que quieras sobreescribir el comportamiento por omisión de la clave
primaria.

``primary_key=True`` implica ``blank=False``, ``null=False``, y
``unique=True``. Solo se permite una clave primaria en un objeto.

radio_admin
-----------

Por omisión,el administrador de Django usa una interfaz de cuadro de selección
(<select>) para campos que son ``ForeignKey`` o tienen ``choices``.
Si ``radio_admin`` es ``True``, Django utilizará una interfaz radio-button en
su lugar.

No utilice esto para un campo que no sea ``ForeignKey`` o no tenga ``choices``.

unique
------

Si es ``True``, el valor para este campo debe ser único en la tabla.

unique_for_date
---------------

Asignar como valor el nombre de un ``DateField`` o ``DateTimeField`` para
requerir que este campo sea único para el valor del campo tipo fecha, por
ejemplo::

    class Story(models.Model):
        pub_date = models.DateTimeField()
        slug = models.SlugField(unique_for_date="pub_date")
        ...

En este código, Django no permitirá la creación de dos historias con el mismo
slug publicados en la misma fecha. Esto difiere de usar la restricción
``unique_together`` en que solo toma en cuenta la fecha del campo ``pub_date``;
la hora no importa.

unique_for_month
----------------

Similar a ``unique_for_date``, pero requiere que el campo sea único con respecto
al mes del campo dado.

unique_for_year
---------------

Similar a ``unique_for_date`` y ``unique_for_month``, pero para el año.

verbose_name
------------

Cada tipo de campo, excepto ``ForeignKey``, ``ManyToManyField``, y
``OneToOneField``, toma un primer argumento posicional opcional -- un nombre
descriptivo. Si el nombre descriptivo no está dado, Django lo creará
automáticamente usando el nombre de atributo del campo, convirtiendo guiones
bajos en espacios.

En este ejemplo, el nombre descriptivo es ``"Person's first name"``::

    first_name = models.CharField("Person's first name", maxlength=30)

En este ejemplo, el nombre descriptivo es ``"first name"``::

    first_name = models.CharField(maxlength=30)

``ForeignKey``, ``ManyToManyField``, y ``OneToOneField`` requieren que el
primer argumento sea una clase del modelo, en este caso hay que usar
``verbose_name`` como argumento con nombre::

    poll = models.ForeignKey(Poll, verbose_name="the related poll")
    sites = models.ManyToManyField(Site, verbose_name="list of sites")
    place = models.OneToOneField(Place, verbose_name="related place")

La convención es no capitalizar la primera letra del ``verbose_name``.  Django
convertirá a mayúscula automáticamente la primera letra cuando lo necesite.

Relaciones
=============

Es claro que el poder de las bases de datos se basa en relacionar tablas entre
sí. Django ofrece formas de definir los tres tipos de relaciones más comunes en
las bases de datos: muchos-a-uno, muchos-a-muchos, y uno-a-uno.

Sin embargo, la semántica de las relaciones uno-a-uno esta siendo revisada
mientras se imprime este libro, así que no se cubren en esta sección. Consulte
en la documentación on-line la información más actualizada.

Relaciones Muchos-a-Uno
-------------------------

Para definir una relación muchos-a-uno, usa ``ForeignKey``. Se usa como
cualquier otro tipo ``Field``: incluyéndolo como un atributo de clase en tu
modelo.

``ForeignKey`` requiere un argumento posicional: la clase a la cual se relaciona
el modelo.

Por ejemplo, si un modelo ``Car`` tiene un ``Manufacturer`` -- es decir, un
``Manufacturer`` fabrica múltiples autos pero cada ``Car`` tiene solo un
``Manufacturer`` -- usa la siguiente definición::

    class Manufacturer(models.Model):
        ...

    class Car(models.Model):
        manufacturer = models.ForeignKey(Manufacturer)
        ...

Para crear una relación *recursiva* -- un objeto que tiene una relación
muchos-a-uno con él mismo -- usa ``models.ForeignKey('self')``::

    class Employee(models.Model):
        manager = models.ForeignKey('self')

Si necesitas crear una relación con un modelo que aún no se ha definido,
puedes usar el nombre del modelo en lugar del objeto modelo::

    class Car(models.Model):
        manufacturer = models.ForeignKey('Manufacturer')
        ...

    class Manufacturer(models.Model):
        ...

Observar que de todas formas solo puedes usar strings para hacer referencia a
modelos dentro del mismo archivo ``models.py`` -- no puedes usar un string para
hacer referencia a un modelo en una aplicación diferente, o hacer referencia a
un modelo que ha sido importado de cualquier otro lado.

Detrás de la escena, Django agrega ``"_id"`` al nombre de campo para crear su
nombre de columna en la base de datos. En el ejemplo anterior, la tabla de la
base de datos correspondiente al modelo ``Car``, tendrá una columna
``manufacturer_id``. (Puedes cambiar esto explícitamente especificando
``db_column``; ver más arriba en la sección "`db_column`_".) De todas formas, tu
código nunca debe utilizar el nombre de la columna de la base de datos, salvo
que escribas tus propias SQL. Siempre te manejarás con los nombres de campo de
tu objeto modelo.

Se sugiere, pero no es requerido, que el nombre de un campo ``ForeignKey``
(``manufacturer`` en el ejemplo) sea el nombre del modelo en minúsculas. Por
supuesto, puedes ponerle el nombre que quieras. Por ejemplo::

    class Car(models.Model):
        company_that_makes_it = models.ForeignKey(Manufacturer)
        # ...

Los campos ``ForeignKey`` reciben algunos argumentos extra para definir como
debe trabajar la relación (ver Tabla B-5). Todos son opcionales.

.. tabla:: Tabla B-5. Opciones de ForeignKey

=======================  ===================================================================
    Argumento                Descripción
=======================  ===================================================================
    ``edit_inline``          Si no es ``False``, este objeto relacionado se edita
                             "inline" en la página del objeto relacionado. Esto significa
                             que el objeto no tendrá su propia interfaz de
                             administración. Usa ``models.TABULAR`` o ``models.STACKED``,
                             que designan si los objetos editables inline se muestran como
                             una tabla o como una pila de conjuntos de campos,
                             respectivamente.

 ``limit_choices_to``        Un diccionario para buscar argumentos y valores (ver el
                             Apéndice C) que limita las opciones de administración
                             disponibles para este objeto. Usa esto con funciones del
                             módulo ``datetime`` de Python para limitar las opciones de
                             fecha de los objetos. Por ejemplo::

                                limit_choices_to = {'pub_date__lte': datetime.now}

                             sólo permite la elección de objetos relacionados con
                             ``pub_date`` anterior a la fecha/hora actual.

                             En lugar de un diccionario, esto puede ser un objeto ``Q``
                             (ver Apéndice C) para consultas más complejas.

                             No es compatible con ``edit_inline``.

``max_num_in_admin``         Para objetos editados inline, este es el número máximo de
                             objetos relacionados a mostrar en la interfaz de
                             administración.
                             Por lo tanto, si una pizza puede tener como máximo diez
                             ingredientes, ``max_num_in_admin=10`` asegurará que un
                             usuario nunca ingresará más de diez ingredientes.

                             Observar que esto no asegura que no se puedan crear más
                             de diez ingredientes relacionados. Simplemente controla
                             la interfaz de administración; no fortalece cosas a nivel
                             de Python API o base de datos.

 ``min_num_in_admin``        La cantidad mínima de objetos relacionados que se muestran
                             en la interfaz de administración. Normalmente,
                             en el momento de la creación se muestran ``num_in_admin``
                             objetos inline , y en el momento de edición se muestran
                             ``num_extra_on_change`` objetos en blanco además de todos
                             los objetos relacionados preexistentes. De todas formas,
                             nunca se mostrarán menos de ``min_num_in_admin`` objetos
                             relacionados.

``num_extra_on_change``      La cantidad de campos en blanco extra de objetos
                             relacionados a mostrar en el momento de realizar cambios.

  ``num_in_admin``           El valor por omisión de la cantidad de objetos inline a
                             mostrar en la página del objeto en el momento de agregar.

    ``raw_id_admin``         Solo muestra un campo para ingresar un entero en lugar de
                             un menú desplegable. Esto es útil cuando se relaciona con
                             un tipo de objeto que tiene demasiadas filas para que sea
                             práctico utilizar una caja de selección.

                             No es utilizado con ``edit_inline``.

    ``related_name``         El nombre a utilizar para la relación desde el objeto
                             relacionado de hacia éste objeto. Para más información,
                             ver el Apéndice C.

    ``to_field``             El campo en el objeto relacionado con el cual se establece
                             la relación. Por omisión, Django usa la clave primaria del
                             objeto relacionado.
=======================  ===================================================================

Relaciones Muchos-a-Muchos
--------------------------

Para definir una relación muchos-a-muchos, usa ``ManyToManyField``. Al igual que
``ForeignKey``, ``ManyToManyField`` requiere un argumento posicional: la clase a
la cual se relaciona el modelo.

Por ejemplo, si una ``Pizza`` tiene múltiples objetos ``Topping`` -- es decir,
un ``Topping`` puede estar en múltiples pizzas y cada ``Pizza`` tiene múltiples
ingredientes (toppings) -- debe representarse así::

    class Topping(models.Model):
        ...

    class Pizza(models.Model):
        toppings = models.ManyToManyField(Topping)
        ...

Como sucede con ``ForeignKey``, una relación de un objeto con sí mismo puede
definirse usando el string ``'self'`` en lugar del nombre del modelo, y puedes
hacer referencia a modelos que todavía no se definieron usando un string que
contenga el nombre del modelo. De todas formas solo puedes usar strings para
hacer referencia a modelos dentro del mismo archivo ``models.py`` -- no puedes
usar un string para hacer referencia a un modelo en una aplicación diferente, o
hacer referencia a un modelo que ha sido importado de cualquier otro lado.

Se sugiere, pero no es requerido, que el nombre de un campo ``ManyToManyField``
(``toppings``, en el ejemplo) sea un término en plural que describa al conjunto
de objetos relacionados con el modelo.

Detrás de la escena, Django crea una tabla join intermedia para representar la
relación muchos-a-muchos.

No importa cual de los modelos tiene el  ``ManyToManyField``, pero es necesario
que esté en uno de los modelos -- no en los dos.

Si estás usando la interfaz de administración, las instancias
``ManyToManyField`` deben ir en el objeto que va a ser editado en la interfaz de
administración. En el ejemplo anterior, los ``toppings`` están en la ``Pizza``
(en lugar de que el ``Topping`` tenga ``pizzas`` ``ManyToManyField`` ) porque es
más natural pensar que una ``Pizza`` tiene varios ingredientes (toppings) que
pensar que un ingrediente está en muchas pizzas. En la forma en que está
configurado el ejemplo, el formulario de administración de la``Pizza`` permitirá
que los usuarios selecciones los ingredientes.

Los objetos ``ManyToManyField`` toman algunos argumentos extra para definir como
debe trabajar la relación (ver Tabla B-6). Todos son opcionales.

.. tabla:: Tabla B-6. Opciones de ManyToManyField

=======================  ==================================================================
    Argumento                Descripción
=======================  ==================================================================
    ``related_name``        El nombre a utilizar para la relación desde el objeto
                            relacionado hacia este objeto. Ver Apéndice C para más
                            información.

   ``filter_interface``     Usa una interfaz de "filtro" JavaScript agradable y discreta
                            en lugar de la menos cómoda ``<select multiple>`` en el
                            formulario administrativo de este objeto. El valos debe ser
                            ``models.HORIZONTAL`` o ``models.VERTICAL`` (es decir, la
                            interfaz debe apilarse horizontal o verticalmente).

   ``limit_choices_to``     Ver la descripción en ``ForeignKey``.

    ``symmetrical``         Solo utilizado en la definición de ``ManyToManyField``  
                            sobre sí mismo. Considera el siguiente modelo::

                            class Person(models.Model):
                            friends = models.ManyToManyField("self")

                            Cuando Django procesa este modelo, identifica que tiene un
                            ``ManyToManyField`` sobre sí mismo, y como resultado, no
                            agrega un atributo ``person_set`` a la clase ``Person``.
                            En lugar de eso, se asumen que el ``ManyToManyField`` es
                            simétrico -- esto es, si yo soy tu amigo, entonces tu eres
                            mi amigo.

                            Si no deseas la simetría en las relaciones ``ManyToMany``
                            con ``self``, establece ``symmetrical`` en ``False``. Esto
                            forzará a Django a agregar el descriptor para la relación
                            inversa, permitiendo que las relaciones ``ManyToMany`` sean
                            asimétricas.

    ``db_table``            El nombre de la tabla a crear para almacenar los datos de
                            la relación muchos-a-muchos. Si no se provee, Django asumirá
                            un nombre por omisión basado en los nombres de las dos
                            tablas a ser vinculadas.

=======================  ==================================================================

Opciones de los Metadatos del Modelo
====================================

Los metadatos específicos de un modelo viven en una ``class Meta`` definida en
el cuerpo de tu clase modelo::

    class Book(models.Model):
        title = models.CharField(maxlength=100)

        class Meta:
            # model metadata options go here
            ...

Los metadatos del modelo son "cualquier cosa que no sea un campo", como
opciones de ordenamiento, etc.

Las secciones que siguen presentan una lista de todas las posibles ``Meta``
opciones. Ninguna de estas opciones es requerida. Agregar ``class Meta`` a un
modelo es completamente opcional.

db_table
--------

El nombre de la tabla de la base de datos a usar para el modelo.

Para ahorrarte tiempo, Django deriva automáticamente el nombre de la tabla de la
base de datos a partir del nombre de la clase modelo y la aplicación que la
contiene. Un nombre de tabla de base de datos de un modelo se construye uniendo
la etiqueta de la aplicación del modelo -- el nombre que usaste en
``manage.py startapp`` -- con el nombre de la clase modelo, con un guión bajo
entre ellos.

Por ejemplo, si tienes una aplicación  ``books`` (creada por
``manage.py startapp books``), un modelo definido como ``class Book`` tendrá
una tabla en la base de datos llamada ``books``.

Para sobreescribir el nombre de la tabla de la base de datos, use el parámetro
``db_table`` dentro de ``class Meta``::

    class Book(models.Model):
        ...

        class Meta:
            db_table = 'things_to_read'

Si no se define, Django utilizará ``app_label + '_' + model_class_name``.  Ver
la sección "`Nombres de Tabla`_" para más información.

Si tu nombre de tabla de base de datos es una palabra reservada de SQL, o
contiene caracteres que no están permitidos en los nombres de variable de Python
(especialmente el guión simple), no hay problema. Django quotea los nombres de
tabla y de columna detrás de la escena.

get_latest_by
-------------

El nombre de un  ``DateField`` o ``DateTimeField`` del modelo. Esto especifica
el campo a utilizar por omisión en el método ``latest()`` del ``Manager`` del
modelo.

Aquí hay un ejemplo::

    class CustomerOrder(models.Model):
        order_date = models.DateTimeField()
        ...

        class Meta:
            get_latest_by = "order_date"

Ver el Apéndice C para más información sobre el método ``latest()``.

order_with_respect_to
---------------------

Marca este objeto como "ordenable" con respecto al campo dado. Esto se utiliza
casi siempre con objetos relacionados para permitir que puedan ser ordenados
respecto a un objeto padre. Por ejemplo, si una ``Answer`` se relaciona a un
objeto ``Question``, y una pregunta tiene más de una respuesta, y el orden de
las respuestas importa, harás esto::

    class Answer(models.Model):
        question = models.ForeignKey(Question)
        # ...

        class Meta:
            order_with_respect_to = 'question'

ordering
--------

El ordenamiento por omisión del objeto, utilizado cuando se obtienen listas de
objetos::

    class Book(models.Model):
        title = models.CharField(maxlength=100)

        class Meta:
            ordering = ['title']

Esto es una tupla o lista de strings. Cada string es un nombre de campo con un
prefijo opcional ``-``, que indica orden descendiente. Los campos sin un ``-``
precedente se ordenarán en forma ascendente. Use el string ``"?"`` para ordenar
al azar.

Por ejemplo, para ordenar por un campo ``title`` en orden ascendente (A-Z), usa
esto::

    ordering = ['title']

Para ordenar por ``title`` en orden descendente (Z-A), usa esto::

    ordering = ['-title']

Para ordenar por ``title`` en orden descendente, y luego por ``author`` en
orden ascendente, usa esto::

    ordering = ['-title', 'author']

Observar que no importa cuantos campos haya en ``ordering``, el sitio de
administración usa sólo el primer campo.

permissions
-----------

Permisos extra para almacenar en la tabla de permisos cuando se crea este
objeto. Se crean automáticamente permisos para agregar, eliminar y cambiar para
cada objeto que tenga establecida la opción ``admin``. Este ejemplo especifica
un permiso extra, ``can_deliver_pizzas``::

    class Employee(models.Model):
        ...

        class Meta:
            permissions = (
                ("can_deliver_pizzas", "Can deliver pizzas"),
            )

Esto es una lista o tupla de dos tuplas de la forma
``(permission_code, human_readable_permission_name)``.

Ver el :doc:`Capítulo 12<chapter12>` para más detalles sobre permisos.

unique_together
---------------

Conjuntos de nombres de campo que tomados juntos deben ser únicos::

    class Employee(models.Model):
        department = models.ForeignKey(Department)
        extension = models.CharField(maxlength=10)
        ...

        class Meta:
            unique_together = [("department", "extension")]

Esto es una lista de listas de campos que deben ser únicos cuando se consideran
juntos. Es usado en la interfaz de administración de Django y se refuerza a
nivel de base de datos (esto es, se incluyen las sentencias ``UNIQUE``
apropiadas en la sentencia ``CREATE TABLE``).

verbose_name
------------

Un nombre legible por humanos para el objeto, en singular::

    class CustomerOrder(models.Model):
        order_date = models.DateTimeField()
        ...

        class Meta:
            verbose_name = "order"

Si no se define, Django utilizará una versión adaptada del nombre de la clase,
en la cual ``CamelCase`` se convierte en ``camel case``.

verbose_name_plural
-------------------

El nombre del objeto en plural::

    class Sphynx(models.Model):
        ...

        class Meta:
            verbose_name_plural = "sphynges"

Si no se define, Django agregará una "s" al final del ``verbose_name``.

Managers
========

Un ``Manager`` es la interfaz a través de la cual se proveen las operaciones
de consulta de la base de datos a los modelos de Django. Existe al menos un
``Manager`` para cada modelo en una aplicación Django.

La forma en que trabajan las clases ``Manager`` está documentada en el Apéndice
C. Esta sección trata específicamente las opciones del modelo que personaliza el
comportamiento del ``Manager``.

Nombres de Manager
------------------

Por omisión, Django agrega un ``Manager`` llamado ``objects`` a cada clase
modelo de Django. De todas formas, si tu quieres usar ``objects`` como nombre
de campo, o quieres usar un nombre distinto de ``objects`` para el ``Manager``,
puedes renombrarlo en cada uno de los modelos. Para renombrar el ``Manager``
para una clase dada, define un atributo de clase de tipo ``models.Manager()``
en ese modelo, por ejemplo::

    from django.db import models

    class Person(models.Model):
        ...

        people = models.Manager()

Usando este modelo de ejemplo, ``Person.objects`` generará una excepción
``AttributeError`` (dado que ``Person`` no tiene un atributo ``objects``), pero
``Person.people.all()`` devolverá una lista de todos los objetos ``Person``.

Managers Personalizados
-----------------------

Puedes utilizar un ``Manager`` personalizado en un modelo en particular
extendiendo la clase base ``Manager`` e instanciando tu ``Manager``
personalizado en tu modelo.

Hay dos razones por las que puedes querer personalizar un ``Manager``: para
agregar métodos extra al ``Manager``, y/o para modificar el ``QuerySet``
inicial que devuelve el ``Manager``.

Agregando Métodos Extra al Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Agregar métodos extra al ``Manager`` es la forma preferida de agregar
funcionalidad  a nivel de tabla a tus modelos. (Para funcionalidad a nivel de
registro -- esto es, funciones que actúan sobre una instancia simple de un
objeto modelo -- usa métodos modelo (ver más abajo), no métodos de ``Manager``
personalizados .)

Un método ``Manager`` personalizado puede retornar cualquier cosa que necesites.
No tiene que retornar un ``QuerySet``.

Por ejemplo, este ``Manager`` personalizado ofrece un método ``with_counts()``,
que retorna una lista de todos los objetos ``OpinionPoll``, cada uno con un
atributo extra ``num_responses`` que es el resultado de una consulta agregada::

    from django.db import connection

    class PollManager(models.Manager):

        def with_counts(self):
            cursor = connection.cursor()
            cursor.execute("""
                SELECT p.id, p.question, p.poll_date, COUNT(*)
                FROM polls_opinionpoll p, polls_response r
                WHERE p.id = r.poll_id
                GROUP BY 1, 2, 3
                ORDER BY 3 DESC""")
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], question=row[1], poll_date=row[2])
                p.num_responses = row[3]
                result_list.append(p)
            return result_list

    class OpinionPoll(models.Model):
        question = models.CharField(maxlength=200)
        poll_date = models.DateField()
        objects = PollManager()

    class Response(models.Model):
        poll = models.ForeignKey(Poll)
        person_name = models.CharField(maxlength=50)
        response = models.TextField()

En este ejemplo, puedes usar ``OpinionPoll.objects.with_counts()`` para
retornar la lista de objetos ``OpinionPoll`` con el atributo ``num_responses``.

Otra cosa a observar en este ejemplo es que los métodos de un ``Manager``
pueden acceder a ``self.model`` para obtener la clase modelo a la cual están
anexados.

Modificando los QuerySets iniciales del Manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Un ``QuerySet`` base de un ``Manager`` devuelve todos los objetos en el sistema.
Por ejemplo, usando este modelo::

    class Book(models.Model):
        title = models.CharField(maxlength=100)
        author = models.CharField(maxlength=50)

la sentencia ``Book.objects.all()`` retornará todos los libros de la base de
datos.

Puedes sobreescribir el ``QuerySet`` base, sobreescribiendo el método
``Manager.get_query_set()``. ``get_query_set()`` debe retornar un ``QuerySet``
con las propiedades que tu requieres.

Por ejemplo, el siguiente modelo tiene *dos* managers -- uno que devuelve todos
los objetos, y otro que retorna solo los libros de Roald Dahl::

    # First, define the Manager subclass.
    class DahlBookManager(models.Manager):
        def get_query_set(self):
            return super(DahlBookManager, self).get_query_set().filter(author='Roald Dahl')

    # Then hook it into the Book model explicitly.
    class Book(models.Model):
        title = models.CharField(maxlength=100)
        author = models.CharField(maxlength=50)

        objects = models.Manager() # The default manager.
        dahl_objects = DahlBookManager() # The Dahl-specific manager.

Con este modelo de ejemplo, ``Book.objects.all()`` retornará todos los libros
de la base de datos, pero ``Book.dahl_objects.all()`` solo retornará aquellos
escritos por Roald Dahl.

Por supuesto, como ``get_query_set()`` devuelve un objeto ``QuerySet``, puedes
usar ``filter()``, ``exclude()``, y todos los otro métodos de ``QuerySet``
sobre él. Por lo tanto, estas sentencias son todas legales::

    Book.dahl_objects.all()
    Book.dahl_objects.filter(title='Matilda')
    Book.dahl_objects.count()

Este ejemplo también señala otra técnica interesante: usar varios managers en
el mismo modelo. Puedes agregar tantas instancias de ``Manager()`` como quieras.
Esta es una manera fácil de definir "filters" comunes para tus modelos. Aquí
hay un ejemplo::

    class MaleManager(models.Manager):
        def get_query_set(self):
            return super(MaleManager, self).get_query_set().filter(sex='M')

    class FemaleManager(models.Manager):
        def get_query_set(self):
            return super(FemaleManager, self).get_query_set().filter(sex='F')

    class Person(models.Model):
        first_name = models.CharField(maxlength=50)
        last_name = models.CharField(maxlength=50)
        sex = models.CharField(maxlength=1, choices=(('M', 'Male'), ('F', 'Female')))
        people = models.Manager()
        men = MaleManager()
        women = FemaleManager()

Este ejemplo te permite consultar ``Person.men.all()``, ``Person.women.all()``,
y ``Person.people.all()``, con los resultados predecibles.

Si usas objetos ``Manager`` personalizados, toma nota que el primer ``Manager``
que encuentre Django (en el orden en el que están definidos en el modelo) tiene
un status especial. Django interpreta el primer ``Manager`` definido en una
clase como el ``Manager`` por omisión. Ciertas operaciones -- como las del
sitio de administración de Django -- usan el ``Manager`` por omisión para
obtener listas de objetos, por lo que generalmente es una buena idea que el
primer ``Manager`` esté relativamente sin filtrar. En el último ejemplo, el
manager ``people`` está definido primero -- por lo cual es el ``Manager`` por
omisión.

Métodos de Modelo
=================

Define métodos personalizados en un modelo para agregar funcionalidad
personalizada a nivel de registro para tus objetos. Mientras que los métodos
``Manager`` están pensados para hacer cosas a nivel de tabla, los métodos de
modelo deben actuar en una instancia particular del modelo.

Esta es una técnica valiosa para mantener la lógica del negocio en un sólo
lugar: el modelo. Por ejemplo, este modelo tiene algunos métodos
personalizados::

    class Person(models.Model):
        first_name = models.CharField(maxlength=50)
        last_name = models.CharField(maxlength=50)
        birth_date = models.DateField()
        address = models.CharField(maxlength=100)
        city = models.CharField(maxlength=50)
        state = models.USStateField() # Yes, this is America-centric...

        def baby_boomer_status(self):
            """Returns the person's baby-boomer status."""
            import datetime
            if datetime.date(1945, 8, 1) <= self.birth_date <= datetime.date(1964, 12, 31):
                return "Baby boomer"
            if self.birth_date < datetime.date(1945, 8, 1):
                return "Pre-boomer"
            return "Post-boomer"

        def is_midwestern(self):
            """Returns True if this person is from the Midwest."""
            return self.state in ('IL', 'WI', 'MI', 'IN', 'OH', 'IA', 'MO')

        @property
        def full_name(self):
            """Returns the person's full name."""
            return '%s %s' % (self.first_name, self.last_name)

El último método en este ejemplo es una *propiedad* -- un atributo implementado
por código getter/setter personalizado. Las propiedades son un truco ingenioso
agregado en Python 2.2; puedes leer más acerca de ellas en
http://www.python.org/download/releases/2.2/descrintro/#property.

Existen también un puñado de métodos de modelo que tienen un significado
"especial" para Python o Django. Estos métodos se describen en las secciones
que siguen.

__str__
-------

``__str__()`` es un "método mágico" de Python que define lo que debe ser
devuelto si llamas a ``str()`` sobre el objeto. Django usa ``str(obj)`` (o la
función relacionada ``unicode(obj)``, que se describe más abajo) en varios
lugares, particularmente como el valor mostrado para hacer el render de un
objeto en el sitio de administración de Django y como el valor insertado en un
plantilla cuando muestra un objeto. Por eso, siempre debes retornar un string
agradable y legible por humanos en el ``__str__`` de un objeto.
A pesar de que esto no es requerido, es altamente recomendado.

Aquí hay un ejemplo::

    class Person(models.Model):
        first_name = models.CharField(maxlength=50)
        last_name = models.CharField(maxlength=50)

        def __str__(self):
            return '%s %s' % (self.first_name, self.last_name)

get_absolute_url
----------------

Define un método ``get_absolute_url()`` para decirle a Django cómo calcular la
URL de un objeto, por ejemplo::

    def get_absolute_url(self):
        return "/people/%i/" % self.id

Django usa esto en la interfaz de administración. Si un objeto define
``get_absolute_url()``, la página de edición del objeto tendrá un enlace
"View on site", que te llevará directamente a la vista pública del objeto,
según ``get_absolute_url()``.

También un par de otras partes de Django, como el framework de sindicación de
feeds, usan ``get_absolute_url()`` como facilidad para recompensar a las
personas que han definido el método.

Es una buena práctica usar ``get_absolute_url()`` en plantillas, en lugar de
codificar en duro las URL de tus objetos. Por ejemplo, este código de plantilla
es *malo*::

    <a href="/people/{{ object.id }}/">{{ object.name }}</a>

Pero este es bueno::

    <a href="{{ object.get_absolute_url }}">{{ object.name }}</a>

El problema con la forma en que simplemente escribimos ``get_absolute_url()``
es que viola levemente el principio DRY: la URL de este objeto de define dos
veces, en el archivo URLconf y en el modelo.

Además puedes desacoplar tus modelos de el URLconf usando el decorator
``permalink``. A este decorator se le pasa función de view, una lista de
parámetros posicionales, y (opcionalmente) un diccionario de parámetros por
nombre. Django calcula la URL completa correspondiente usando el  URLconf,
sustituyendo los parámetros que le has pasado en la URL. Por ejemplo, si tu
URLconf contiene una línea como ésta::

    (r'^people/(\d+)/$', 'people.views.details'),

tu modelo puede tener un método ``get_absolute_url`` como éste::

    @models.permalink
    def get_absolute_url(self):
        return ('people.views.details', [str(self.id)])

En forma similar, si tienes una entrada en URLconf que se ve como esta::

    (r'/archive/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', archive_view)

puedes hacer referencia a la misma usando ``permalink()`` como sigue::

    @models.permalink
    def get_absolute_url(self):
        return ('archive_view', (), {
            'year': self.created.year,
            'month': self.created.month,
            'day': self.created.day})

Observar que especificamos una secuencia vacía para el segundo argumento en
este caso, porque sólo queremos pasar argumentos por clave, no argumentos por
nombre.

De esta forma, estás estás ligando la URL absoluta del modelo a la vista que se
utiliza para mostrarla, sin repetir la información de la URL en ningún lado.
Aún puedes usar el método ``get_absolute_url`` en plantillas, como antes.

Ejecutando SQL personalizado
----------------------------

Siéntete libre de escribir sentencias SQL personalizadas en métodos
personalizados de modelo y métodos a nivel de módulo. El objeto
``django.db.connection`` representa la conexión actual a la base de datos. Para
usarla, invoca ``connection.cursor()`` para obtener un objeto cursor. Después,
llama a ``cursor.execute(sql, [params])`` para ejecutar la SQL, y
``cursor.fetchone()`` o ``cursor.fetchall()`` para devolver las filas
resultantes::

    def my_custom_sql(self):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
        row = cursor.fetchone()
        return row

``connection`` y ``cursor`` implementan en su mayor parte la DB-API estándar de
Python (http://www.python.org/peps/pep-0249.html). Si no estás familiarizado con
la DB-API de Python, observa que la sentencia SQL en ``cursor.execute()`` usa
placeholders, ``"%s"``, en lugar de agregar los parámetros directamente dentro
de la SQL. Si usas esta técnica, la biblioteca subyacente de base de datos
automáticamente agregará comillas y secuencias de escape a tus parámetros según
sea necesario. (Observar también que Django espera el placeholder ``"%s"``, *no*
el placeholder ``"?"``, que es utilizado por los enlaces Python a SQLite. Python
bindings. Esto es por consistencia y salud mental).

Una nota final: Si todo lo que quieres hacer es usar una cláusula ``WHERE``
personalizada, puedes usar los argumentos ``where``, ``tables``, y ``params``
de la API estándar de búsqueda. Ver Apéndice C.

Sobreescribiendo los Métodos por omisión del Modelo
---------------------------------------------------

Como se explica en el Apéndice C, cada modelo obtiene algunos métodos
automáticamente -- los más notables son ``save()`` y ``delete()``. Puedes
sobreescribir estos métodos para alterar el comportamiento.

Un caso de uso clásico de sobreescritura de los métodos incorporados es cuando
necesitas que suceda algo cuando guardas un objeto, por ejemplo::

    class Blog(models.Model):
        name = models.CharField(maxlength=100)
        tagline = models.TextField()

        def save(self):
            do_something()
            super(Blog, self).save() # Call the "real" save() method.
            do_something_else()

También puedes evitar el guardado::

    class Blog(models.Model):
        name = models.CharField(maxlength=100)
        tagline = models.TextField()

        def save(self):
            if self.name == "Yoko Ono's blog":
                return # Yoko shall never have her own blog!
            else:
                super(Blog, self).save() # Call the "real" save() method

Opciones del Administrador
==========================

La clase ``Admin`` le dice a Django cómo mostrar el modelo en el sitio de
administración.

Las siguientes secciones presentan una lista de todas las opciones posibles de
``Admin``. Ninguna de estas opciones es requerida. Para utilizar una interfaz
de administración sin especificar ninguna opción, use ``pass``, como en::

    class Admin:
        pass

Agregar ``class Admin`` a un modelo es completamente opcional.

date_hierarchy
--------------

Establece ``date_hierarchy`` con el nombre de un ``DateField`` o
``DateTimeField`` en tu modelo, y la página de la lista de cambios incluirá una
navegación basada en la fecha usando ese campo.

Aquí hay un ejemplo::

    class CustomerOrder(models.Model):
        order_date = models.DateTimeField()
        ...

        class Admin:
            date_hierarchy = "order_date"

fields
------

Establece ``fields`` para controlar la disposición de las páginas "agregar" y
"modificar" de la interfaz de administración.

``fields`` es una estructura anidada bastante compleja que se demuestra mejor
con un ejemplo. Lo siguiente está tomado del modelo ``FlatPage`` que es parte
de ``django.contrib.flatpages``::

    class FlatPage(models.Model):
        ...

        class Admin:
            fields = (
                (None, {
                    'fields': ('url', 'title', 'content', 'sites')
                }),
                ('Advanced options', {
                    'classes': 'collapse',
                    'fields' : ('enable_comments', 'registration_required', 'template_name')
                }),
            )

Formalmente, ``fields`` es una lista de tuplas dobles, en la que cada tupla
doble representa un ``<fieldset>`` en el formulario de la página de
administración. (Un ``<fieldset>`` es una "sección" del formulario.)

Las tuplas dobles son de la forma ``(name, field_options)``, donde ``name`` es
un string que representa el título del conjunto de campos, y ``field_options``
es un diccionario de información acerca del conjunto de campos, incluyendo una
lista de los campos a mostrar en él.

Si ``fields`` no está definido, Django mostrará por omisión cada campo que no
sea un ``AutoField`` y tenga ``editable=True``, en un conjunto de campos simple,
en el mismo orden en que aparecen los campos definidos en el modelo.

El diccionario ``field_options`` puede tener las clave que se describen en la
siguiente sección.

fields
~~~~~~

Una tupla de nombres de campo a mostrar en el conjunto de campos. Esta clave es
requerida.

Para mostrar múltiples campos en la misma linea, encierra esos campos en su
propia tupla. En este ejemplo, los campos ``first_name`` y ``last_name`` se
mostrarán en la misma línea::

    'fields': (('first_name', 'last_name'), 'address', 'city', 'state'),

classes
~~~~~~~

Un string conteniendo clases extra CSS para aplicar al conjunto de campos.

Aplica múltiples clases separándolas con espacios::

    'classes': 'wide extrapretty',

Dos clases útiles definidas por la hoja de estilo del sitio de administración
por omisión son ``collapse`` y ``wide``. Los conjuntos de campos con el estilo
``collapse`` serán colapsados inicialmente en el sitio de administración y
reemplazados por un pequeño enlace "click to expand". Los conjuntos de campos
con el estilo ``wide`` tendrán espacio horizontal extra.

description
~~~~~~~~~~~

Un string de texto extra opcional para mostrar encima de cada conjunto de
campos, bajo el encabezado del mismo. Se usa tal cual es, de manera que puedes
usar cualquier HTML, y debes crear las secuencias de escape correspondientes
para cualquier carácter especial HTML (como los ampersands).

js
--

Una lista de strings representando URLs de archivos JavaScript a vincular en la
pantalla de administración mediante etiquetas ``<script src="">``. Esto puede
ser usado para ajustar un tipo determinado de página de administración en
JavaScript o para proveer "quick links" para llenar valores por omisión para
ciertos campos.

Si usas URLs relativas -- esto es, URLs que no empiezan con  ``http://`` o
``/`` -- entonces el sitio de administración prefijará automáticamente estos
enlaces con ``settings.ADMIN_MEDIA_PREFIX``.

list_display
------------

Establece ``list_display`` para controlar que campos se muestran en la página
de la lista de del administrador.

Si no se define ``list_display``, el sitio de administración mostrará una
columna simple con la representación ``__str__()`` de cada objeto.

Aquí hay algunos casos especiales a obsevar acerca de ``list_display``:

* Si el campo es una ``ForeignKey``, Django mostrará el ``__str__()`` del
  objeto relacionado.

* No se admiten los campos ``ManyToManyField``, porque eso implicaría
  la ejecución de una sentencia SQL separada para cada fila en la tabla. Si
  de todas formas quieres hacer esto, dale a tu modelo un método
  personalizado, y agrega el nombre de ese método a ``list_display``.
  (Más información sobre métodos personalizados en ``list_display`` en
  breve.)

* Si el campo es un ``BooleanField`` o ``NullBooleanField``, Django
  mostrará unos bonitos iconos "on" o "off" en lugar de ``True`` o
  ``False``.

* Si el string dado es un método del modelo, Django lo invocará y mostrará
  la salida. Este método debe tener un atributo de función
  ``short_description`` para usar como encabezado del campo.

Aquí está un modelo de ejemplo completo::


          class Person(models.Model):
              name = models.CharField(maxlength=50)
              birthday = models.DateField()

              class Admin:
                  list_display = ('name', 'decade_born_in')

              def decade_born_in(self):
                  return self.birthday.strftime('%Y')[:3] + "0's"
              decade_born_in.short_descripción = 'Birth decade'

* Si el string dado es un método del modelo, Django hará un HTML-escape de
  la salida por omisión. Si no quieres 'escapear' la salida del método,
  dale al método un atributo ``allow_tags`` con el valor en ``True``.

Aquí está un modelo de ejemplo completo::

          class Person(models.Model):
              first_name = models.CharField(maxlength=50)
              last_name = models.CharField(maxlength=50)
              color_code = models.CharField(maxlength=6)

              class Admin:
                  list_display = ('first_name', 'last_name', 'colored_name')

              def colored_name(self):
                  return '<span style="color: #%s;">%s %s</span>' % (self.color_code, self.first_name, self.last_name)
              colored_name.allow_tags = True

* Si el string dado es un método del modelo que retorna ``True`` o
  ``False``, Django mostrará un bonito icono "on" o "off" si le das al
  método un atributo ``boolean`` con valor en ``True``.

Aquí está un modelo de ejemplo completo::

          class Person(models.Model):
              first_name = models.CharField(maxlength=50)
              birthday = models.DateField()

              class Admin:
                  list_display = ('name', 'born_in_fifties')

              def born_in_fifties(self):
                  return self.birthday.strftime('%Y')[:3] == 5
              born_in_fifties.boolean = True


* Los métodos ``__str__()`` son tan válidos en ``list_display`` como
  cualquieras otro método del modelo, por lo cual está perfectamente OK
  hacer esto::

          list_display = ('__str__', 'some_other_field')

* Usualmente, los elementos de ``list_display`` que no son campos de la
  base de datos no pueden ser utilizados en ordenamientos (porque Django
  hace todo el ordenamiento a nivel de base de datos).

De todas formas, si un elemento de ``list_display`` representa cierto
campo de la base de datos, puedes indicar este hecho estableciendo el
atributo ``admin_order_field`` del ítem, por ejemplo::

        class Person(models.Model):
            first_name = models.CharField(maxlength=50)
            color_code = models.CharField(maxlength=6)

            class Admin:
                list_display = ('first_name', 'colored_first_name')

            def colored_first_name(self):
                return '<span style="color: #%s;">%s</span>' % (self.color_code, self.first_name)
            colored_first_name.allow_tags = True
            colored_first_name.admin_order_field = 'first_name'

El código precedente le dirá a Django que ordene según el campo
``first_name`` cuando trate de ordenar por ``colored_first_name`` en el
sitio de administración.

list_display_links
------------------

Establece ``list_display_links`` para controlar cuales campos de
``list_display`` deben ser vinculados a la pagina de cambios de un objeto.

Por omisión, la página de la lista de cambios vinculará la primera columna --
el primer campo especificado en ``list_display`` -- a la página de cambios de
cada ítem. Pero ``list_display_links`` te permite cambiar cuáles columnas se
vinculan. Establece ``list_display_links`` a una lista o tupla de nombres de
campo (en el mismo formato que ``list_display``) para vincularlos.

``list_display_links`` puede especificar uno o varios nombres de campo.
Mientras los nombres de campo aparezcan en ``list_display``, a Django no le
preocupa si los campos vinculados son muchos o pocos. El único requerimiento es
que si quieres usar``list_display_links``, debes definir ``list_display``.

En este ejemplo, los campos ``first_name`` y ``last_name`` serán vinculados a
la página de la lista de cambios::

    class Person(models.Model):
        ...

        class Admin:
            list_display = ('first_name', 'last_name', 'birthday')
            list_display_links = ('first_name', 'last_name')

Finalmente, observa que para usar ``list_display_links``, debes definir también
``list_display``.

list_filter
-----------

Establece ``list_filter`` para activar los filtros en la barra lateral derecha
de la página de la lista de cambios en la interfaz de administración.
Debe ser una lista de nombres de campo, y cada campo especificado debe ser de
alguno de los tipos ``BooleanField``, ``DateField``, ``DateTimeField``,
o ``ForeignKey``.

Este ejemplo, tomado del modelo ``django.contrib.auth.models.User`` muestra
como trabajan ambos, ``list_display`` y ``list_filter``::

    class User(models.Model):
        ...

        class Admin:
            list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
            list_filter = ('is_staff', 'is_superuser')

list_per_page
-------------

Establece ``list_per_page`` para controlar cuantos items aparecen en cada
página de la lista de cambios del administrador. Por omisión, este valor se
establece en ``100``.

list_select_related
-------------------

Establece ``list_select_related`` para indicarle a Django que use
``select_related()`` al recuperar la lista de objetos de la página de la lista
de cambios del administrador. Esto puede ahorrarte una cantidad de consultas a
la base de datos si estás utilizando objetos relacionados en la lista de
cambios que muestra el administrador.

El valor debe ser ``True`` o ``False``. Por omisión es ``False``, salvo que uno
de los campos ``list_display`` sea una ``ForeignKey``.

Para más detalles sobre ``select_related()``, ver Apéndice C.

ordering
--------

Establece ``ordering`` para especificar como deben ordenarse los objetos en la
página de la lista de cambios del administrador. Esto debe ser una lista o
tupla en el mismo formato que el parámetro ``ordering`` del modelo.

Si no está definido, la interfaz de administración de Django usará el
ordenamiento por omisión del modelo.

save_as
-------

Establece ``save_as`` a ``True`` para habilitar la característica "save as" en
los formularios de cambios del administrador.

Normalmente, los objetos tienen tres opciones al guardar: "Save",
"Save and continue editing" y "Save and add another". Si ``save_as`` es
``True``, "Save and add another" será reemplazado por un botón "Save as".

"Save as" significa que el objeto será guardado como un objeto nuevo (con un
identificador nuevo), en lugar del objeto viejo.

Por omisión, ``save_as`` es ``False``.

save_on_top
-----------

Establece ``save_on_top`` para agregar botones de guardado a lo largo del
encabezado de tus formularios de cambios del administrador.

Normalmente, los botones de guardado aparecen solamente al pie de los
formularios. Si estableces ``save_on_top``, los botones aparecerán en el
encabezado y al pié del formulario.

Por omisión, ``save_on_top`` es ``False``.

search_fields
-------------

Establece ``search_fields`` para habilitar un cuadro de búsqueda en la página
de la lista de cambios del administrador. Debe ser una lista de nombres de
campo que se utilizará para la búsqueda cuando alguien envíe una consulta en
ese cuadro de texto.

Estos campos deben ser de alguna tipo de campo de texto, como ``CharField`` o
``TextField``. También puedes realizar una búsqueda relacionada sobre una
``ForeignKey`` con la notación de búsqueda de la API::

    class Employee(models.Model):
        department = models.ForeignKey(Department)
        ...

        class Admin:
            search_fields = ['department__name']

Cuando alguien hace una búsqueda en el cuadro de búsqueda del administrador,
Django divide la consulta de búsqueda en palabras y retorna todos los objetos
que contengan alguna de las palabras, sin distinguir mayúsculas y minúsculas,
donde cada palabra debe estar en al menos uno de los ``search_fields``. Por
ejemplo, si ``search_fields`` es ``['first_name', 'last_name']`` y un usuario
busca ``john lennon``, Django hará el equivalente a esta cláusula ``WHERE`` en
SQL::

    WHERE (first_name ILIKE '%john%' OR last_name ILIKE '%john%')
    AND (first_name ILIKE '%lennon%' OR last_name ILIKE '%lennon%')

Para búsquedas más rápidas y/o más restrictivas, agrega como prefijo al nombre
de campo un operador como se muestra en la Tabla B-7.

.. tabla:: Tabla B-7. Operadores Permitidos en search_fields

==========  =======================================================================
  erador    Significado
==========  =======================================================================
    ``^``    Matchea el principio del campo. Por ejemplo, si ``search_fields``
             es ``['^first_name', '^last_name']``, y un usuario busca  ``john
             lennon``, Django hará el equivalente a esta cláusula ``WHERE``
             en SQL::

             WHERE (first_name ILIKE 'john%' OR last_name ILIKE 'john%')
             AND (first_name ILIKE 'lennon%' OR last_name ILIKE 'lennon%')

             Esta consulta es más eficiente que la consulta ``'%john%'``, dado
             que la base de datos solo necesita examinar el principio de una
             columna de datos, en lugar de buscar a través de todos los
             datos de la columna. Además, si la columna tiene un índice,
             algunas bases de datos pueden permitir el uso del índice para
             esta consulta, a pesar de que sea una consulta ``LIKE``.

    ``=``    Matchea exactamente, sin distinguir mayúsculas y minúsculas.
             Por ejemplo, si ``search_fields`` es ``['=first_name', '=last_name']``
             y un usuario busca ``john lennon``, Django hará el equivalente a
             esta clausula ``WHERE`` en SQL::

             WHERE (first_name ILIKE 'john' OR last_name ILIKE 'john')
             AND (first_name ILIKE 'lennon' OR last_name ILIKE 'lennon')

             Observar que la entrada de la consulta se divide por los espacios,
             por lo cual actualmente no es posible hacer una búsqueda de todos
             los registros en los cuales ``first_name`` es exactamente ``'john
             winston'`` (con un espacio en el medio).

    ``@``    Realiza una búsqueda en todo el texto. Es similar al método de
             búsqueda predeterminado, pero usa un índice. Actualmente solo está
             disponible para MySQL.
==========  =======================================================================
