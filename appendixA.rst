==================================================
Apéndice A: Referencia de la definición de modelos
==================================================

Él :doc:`capítulo 5<chapter05>` explica lo básico de la definición de modelos,
y lo utilizamos en el resto del libro.  Existe un enorme rango de opciones
disponibles que no se han cubierto en otro lado. Este apéndice explica toda
opción disponible en la **definición de modelos**.

A pesar de que estas APIs se consideran muy estables, los desarrolladores de
Django agregan en forma consistente nuevos atajos y conveniencias a la
definición de modelos. Es buena idea chequear siempre la última documentación
online en http://www.djangoproject.com/documentation/

Campos
======

Un campo es una clase abstracta que representa una columna de una tabla de una
base de datos. Django usa campos o ``fields`` para crear las tablas de
la base de datos.

La parte más importante de un modelo -- y la única parte requerida de un modelo
es la lista de campos de la base de datos que la definen.

.. admonition:: Restricciones en el nombre de los campos

    Django pone solo dos restricciones en el nombre de los campos:

    1. Un nombre de campo no puede ser una palabra reservada de Python,
       porque eso ocasionaría un error de sintaxis en Python, por ejemplo::

            class Ejemplo(models.Model):
                pass = models.IntegerField() # 'pass' es una palabra reservada!

    2. Un nombre de campo no puede contener dos o más guiones bajos
       consecutivos, debido a la forma en que trabaja la sintaxis de las
       consultas de búsqueda de , por ejemplo::

            class Ejemplo(models.Model):
                foo__bar = models.IntegerField() # 'foo__bar' tiene dos guiones bajos!

Estas limitaciones se pueden manejar sin mayores problemas, dado que el
nombre del campo no necesariamente tiene que coincidir con el nombre de la
columna en la base de datos. Ver "db_column", más abajo.

Las palabras reservadas de SQL, como ``join``, ``where``, o ``select``,
*son* permitidas como nombres de campo, dado que Django "escapa" todos los
nombres de tabla y columna de la base de datos en cada consulta SQL
subyacente. Utiliza la sintaxis de "comillas" del motor de base de datos
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

BigIntegerField
---------------

Un campo para almacenar numeros enteros de 64 bits, es parecido a un campo
``IntegerField`` excepto que garantiza ajustar numeros de 9223372036854775808 a
9223372036854775807.

BinaryField
-----------

Un campo que almacena datos binarios. Únicamente soporta la asignación de bytes.
Ten en cuenta que este campo tiene funcionalidades limitadas. Por ejemplo no es
posible filtrar un ``queryset`` en un valor de un campo ``BinaryField``.


BooleanField
------------

Un campo Verdadero/Falso.

.. admonition:: Para usuarios de MySQL...

    Un campo booleano en MySQL es almacenado en una columna ``TINYINT`` con un
    valor de 0 o 1 (la mayoría de las bases de datos tienen una apropiada
    instancia de tipo ``BOLEAN``.) Por lo que en MySQL únicamente cuando se
    recupera un valor almacenado ``BooleanField`` de la base de datos, este
    tiene un valor de 1 o 0, en lugar de ``True`` o ``False``. Normalmente esto
    no debería ser un problema, ya que Python garantiza que ``1 == True`` y
    ``0 == False``. Simplemente se cuidadoso si escribes algo como: ``obj is
    True`` cuando ``obj`` es el valor de un atributo boleano de un modelo. Si
    el modelo fue construido usando el ``backend`` ``mysql``, las pruebas
    "``is``" fallaran. Es mejor usar una prueba usando  "``==``" en casos
    como estos.

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

.. table:: Argumentos opcionales extra de DateField

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

DecimalField
------------

Un numero decimal de precisión-fija , representado en Python por una instancia
de ``decimal.Decimal``. Requiere de dos argumentos:

.. table:: Argumentos opcionales extra de DateField

    ======================  ================================================
    Argumento               Descripción
    ======================  ================================================
     ``max_digits``          La cantidad máxima de dígitos permitidos en el
                             número.

     ``decimal_places``      La cantidad de posiciones decimales a almacenar
                             con  el número.
    ======================  ================================================


Por ejemplo, para almacenar números hasta 999 con una resolución de dos
decimales, usa::

    models.DecimalField(..., max_digits=5, decimal_places=2)

Y para almacenar números hasta aproximadamente mil millones con una resolución
de diez dígitos decimales, usa::

    models.DecimalField(..., max_digits=19, decimal_places=10)

Cuando asignes a ``DecimalField``, utiliza cualquiera de los objetos
``decimal.Decimal`` o una cadena -- no un numero de punto flotante Python.

EmailField
----------

Un ``CharField`` que chequea que el valor sea una dirección de email válida. No
acepta ``max_length``; ``max_length`` se establece automáticamente en 254.

FileField
---------

Un campo para subir archivos.

.. admonition:: Nota

    Los argumentos ``primary_key`` y ``unique``, no están soportados, si los
    usas  se lanzara un error del tipo: ``TypeError``

Tiene un argumento *requerido*:

``upload_to``:  La ruta del sistema de archivos local que se agregará a la
configuración de ``MEDIA_ROOT`` para determinar el valor de el atributo
``django.core.files.File.url``.

La ruta puede contener el "formato strftime", (consulta la documentación
de Python para obtener ayuda sobre el modulo estándar ``time`` ) el cual se
usa para remplazar la fecha/tiempo de el archivo a subir (de modo que los
ficheros subidos no llenen el directorio dado.)

También puede contener un llamable, tal como una función, la cual debe ser
llamada para obtener la ruta a la cual subir los archivos, incluyendo el
nombre del archivo. Este llamable  debe permitir aceptar dos argumentos y
devolver la ruta estilo tipo Unix (con barras inclinadas) para pasarlas a
el sistema de almacenamiento. Los dos argumentos que se pasas son:

.. table:: Argumentos opcionales de FileField

    ======================  =================================================
    Argumento                Descripción
    ======================  =================================================
    ``instance``            Una instancia de un modelo donde este definido
                            ``FileField``. Más específicamente,
                            esta es la instancia en particular donde el
                            actual fichero esta adjunto.

                            En la mayoría de los casos, este objeto no habrá
                            sido guardado en la base de datos todavía, así
                            que si utiliza por defecto ``AutoField``, *puede
                            ser que todavía no tenga un valor para el campo
                            de la clave primaria*.

    ``filename``            El nombre del archivo que fue originalmente dado
                            al archivo. Esto puede o no ser tomado en
                            consideración, al determinar la ruta final del
                            destino.

    ``storage``             Un objeto para almacenamiento, el cual maneja el
                            almacenamiento y recuperación de los archivos.
    ======================  =================================================

El uso de un ``FileField`` o un ``ImageField`` en un modelo requiere algunos
pasos:

1. En el archivo de configuración (settings.py), es necesario definir
   ``MEDIA_ROOT`` con la ruta completa al directorio donde quieras que
   Django almacene los archivos subidos. (Para mayor rendimiento, estos
   archivos no se almacenan en la base de datos.) Define ``MEDIA_URL`` con
   la URL pública base de ese directorio. Asegúrate de que la cuenta del
   usuario del servidor web tenga permiso de escritura en este directorio.

2. Agregar el ``FileField`` o ``ImageField`` al modelo, asegúrate de
   definir la opción ``upload_to`` para decirle a Django a cual
   subdirectorio de ``MEDIA_ROOT`` debe subir los archivos.

3. Todo lo que se va a almacenar en la base de datos es la ruta al archivo
   (relativa a ``MEDIA_ROOT``). Seguramente preferirás usar la facilidad de
   la función ``url`` provista por Django. Por ejemplo, si tu ``ImageField``
   se llama ``portada``, puedes obtener la URL absoluta
   a tu imagen en un plantilla con ``{{ object.portada.url }}``.

Por ejemplo, digamos que tu ``MEDIA_ROOT`` es ``'/home/media'``, y
``upload_to`` es ``'photos/%Y/%m/%d'``. La parte ``'%Y/%m/%d'`` de
``upload_to`` está en el formato strftime; ``'%Y'`` es el año en cuatro
dígitos, ``'%m'`` es el mes en dos digitos, y ``'%d'`` es el día en dos
dígitos. Si subes un archivo el 15 de enero de 2007, será guardado en
``/home/media/photos/2007/01/15``.

Si quieres recuperar el nombre en disco del archivo subido, o una URL que se
refiera a ese archivo, o el tamaño del archivo, puedes referirte al archivo
mediante sus atributos ``name``, ``url`` y ``size``.

Cualquiera que sea la forma en que manejes los archivos subidos, tienes que
prestar mucha atención a donde los estás subiendo y qué tipo de archivos
son, para evitar huecos en la seguridad. *Valida todos los archivos
subidos* para asegurarte que esos archivos son lo que piensas que son.
Por ejemplo, si dejas que cualquiera suba archivos ciegamente, sin
validación, a un directorio que está dentro de la raíz de documentos
(*document root*) de tu servidor web, alguien podría subir un script CGI o
PHP y ejecutarlo visitando su URL en tu sitio. ¡No permitas que pase!

Por defecto las instancias de  ``FileField`` son creadas usando columnas
``varchar(100)`` en la base de datos. Como otros campos, puedes cambiar el
máximo permitido, usando el argumento ``max_length``.

FilePathField
-------------

Un campo cuyas opciones están limitadas a los nombres de archivo en un cierto
directorio en el sistema de archivos. Tiene tres argumentos especiales, que se
muestran en la Tabla B-3.

.. table:: Opciones extra de FilePathField

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
                          ``"foo.*\.txt^"``, va a coincidir con un archivo
                          llamado ``foo23.txt``, pero no con ``bar.txt`` o
                          ``foo23.gif``).

      ``recursive``       Opcional; ``True`` o ``False``. El valor por omisión
                          es ``False``. Especifica si deben incluirse todos
                          los subdirectorios de ``path``.

     ``alow_files``       Opcional, ``True`` o ``False``. El valor por
                          omisión  es ``True`` Especifica si todos los
                          los archivos de los directorios especificados
                          deben ser incluidos. Utiliza este o
                          ``allow_folders`` como ``True``.

     ``alow_folders``     Opcional, ``True`` o ``False``. El valor por
                          omisión  es ``False`` Especifica si todas las
                          carpetas de los directorios especificados
                          deben ser incluidas. Utiliza este o
                          ``allow_files`` como ``True``.
  ======================  ===================================================

Por supuesto, estos argumentos pueden usarse juntos.

El único peligro potencial es que ``match`` se aplica sobre el nombre de
archivo base, no la ruta completa. De esta manera, este ejemplo::

    FilePathField(path="/home/images", match="foo.*", recursive=True)

Esto va a coincidir con ``/home/images/foo.gif`` pero no con
``/home/images/foo/bar.gif`` porque el  ``match`` se aplica al nombre de
archivo base (``foo.gif`` y ``bar.gif``).

FloatField
----------

Un numero de punto flotante, representado en Python por una instancia de
``float``.

ImageField
----------

Similar a ``FileField``, pero valida que el objeto subido sea una imagen
válida. Tiene dos argumentos opcionales extra:

* ``height_field``: Nombre del campo del modelo usado para auto-rellenar con la
  altura de la  imagen cada vez que se guarde una instancia de una imagen.

* ``width_field``: Nombre del campo del modelo usado para auto-rellenar con ancho
  de la imagen cada vez que se guarde una instancia de una imagen.

Además de los atributos  especiales requeridos  que están disponibles para
``FileField``, un ``ImageField`` puede contener atributos ``height`` y ``width``
que corresponden a la altura y al ancho de la imagen en pixeles.

Requiere PIL, la librería de Imágenes Python, en especial de ``Pillow``
disponible en:

Por defecto las instancias de  ``ImageField``  son creadas usando columnas
``varchar(100)`` en la base de datos. Como con otros campos, puedes cambiar el
máximo permitido, usando el argumento ``max_length``.

IntegerField
------------

Un entero. Valores desde -2147483648 hasta 2147483647 son soportados por Django
de forma segura en todas las bases de datos.

GenericIPAddressField
---------------------

Una dirección IP, en formato string (ej.: ``"24.124.1.30"``).

NullBooleanField
----------------

Similar a ``BooleanField``, pero permite ``None``/``NULL`` como opciones.
Usar éste en lugar de un ``BooleanField`` con ``null=True``.

PositiveIntegerField
--------------------

Similar a ``IntegerField``, pero debe ser positivo.

PositiveSmallIntegerField
-------------------------

Similar a ``PositiveIntegerField``, pero solo permite valores por debajo de un
límite. Valores desde 0 a 32767 son soportados de forma segura en Django.

SlugField
---------

"Slug" es un término de la prensa. Un *slug* es una etiqueta corta para algo,
que contiene solo letras, números, guiones bajos o simples. Generalmente se
usan en URLs.

De igual forma que en ``CharField``, puedes especificarlo con ``max_length``. Si
``max_length`` no está especificado, Django asume un valor por omisión de 50.

Un ``SlugField`` implica ``db_index=True`` debido a que este tipo de campo se
usa principalmente para búsquedas en la base de datos.

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
omisión), se comprueba la existencia de la URL dada (la URL que arroja  y no da una
respuesta 404).

Como los otros campos de caracteres, ``URLField`` toma el argumento
``max_length``. Si no se especifica, el valor por omisión es 200.

UUIDField
---------

Un campo para almacenar ``Identificadores Universales Únicos``. Usando la clase
``UUID`` de Python.

Los Identificadores Universales Únicos,  son una buena alternativa para campos
``AutoField`` que usan una ``primary_key``. La base de datos no genera el UUID,
lo más recomendable es usarlos con un parámetro ``default``::

  import uuid
  from django.db import models

  class ModeloUUID(models.Model):
      id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      # otros campos

Observa como el llamable (sin paréntesis) es pasado a ``default``, no a una
instancia de UUID.

Opciones Universales de Campo
=============================

Los siguientes argumentos están disponibles para todos los tipos de campo.
Todos son opcionales.

null
----

Si está en ``True``, Django almacenará valores vacíos como ``NULL`` en la base
de datos. Si esta en ``False``, los valores vacíos que se guarden resultaran
probablemente en errores de la base de datos. El valor por omisión es ``False``.

Observa que los valores de string nulo siempre se almacenan como strings
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

.. admonition:: Nota

  Cuando uses como base de datos un ``backend`` de Oracle, la opción ``null=True``
  será usada para obligar a los campos basados en cadenas a aceptar cadena vacías
  como sea posible, y el valor ``NULL`` será almacenado para denotar la cadena
  vacía.

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

Si esto está dado, la interfaz de administración de Django utilizará un cuadro
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
        gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

o fuera de la clase del modelo::

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    class Foo(models.Model):
        gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

Para cada campo del modelo que tenga establecidas ``choices``, Django agregará
un método para recuperar el nombre legible por humanos para el valor actual del
campo.

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
columna cuando cree la tabla (es decir, cuando ejecute ``manage.py migrate``).

db_tablespace
-------------

El nombre de la tabla de la base de datos para usar en este índice de campo, si
el campo tiene un índice.

default
-------

El valor por omisión del campo.

editable
--------

Si es ``False``, el campo no será editable en la interfaz de administración o
vía procesamiento de formularios. El valor por omisión es ``True``.

error_messages
--------------

Argumento que permite sobrescribir el mensaje por omisión que el campo
lanza.

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

    first_name = models.CharField("Person's first name", max_length=30)

En este ejemplo, el nombre descriptivo es ``"first name"``::

    first_name = models.CharField(max_length=30)

``ForeignKey``, ``ManyToManyField``, y ``OneToOneField`` requieren que el
primer argumento sea una clase del modelo, en este caso hay que usar
``verbose_name`` como argumento con nombre::

    poll = models.ForeignKey(Poll, verbose_name="the related poll")
    sites = models.ManyToManyField(Site, verbose_name="list of sites")
    place = models.OneToOneField(Place, verbose_name="related place")

La convención es no capitalizar la primera letra del ``verbose_name``.  Django
convertirá a mayúscula automáticamente la primera letra cuando lo necesite.

validators
----------

Una lista de validadores que se ejecutaran para este campo.

Relaciones
=============

Es claro que el poder de las bases de datos se basa en relacionar tablas entre
sí. Django ofrece formas de definir los tres tipos de relaciones más comunes en
las bases de datos: muchos-a-uno, muchos-a-muchos, y uno-a-uno.

Relaciones Muchos-a-Uno
-------------------------

Para definir una relación muchos-a-uno, usa un campo tipo ``ForeignKey``. El cual
se usa como cualquier otro tipo ``Field``: incluyéndolo como un atributo de
clase en tu modelo.

``ForeignKey`` requiere un argumento posicional: la clase a la cual se relaciona
el modelo.

Por ejemplo, si un modelo ``Carro`` tiene un ``Fabricante`` -- es decir, un
``Fabricante`` fabrica múltiples carros pero cada ``Carro`` tiene solo un
``Fabricante`` -- usa la siguiente definición::

    class Fabricante(models.Model):
        ...

    class Carro(models.Model):
        fabricante = models.ForeignKey(Fabricante)
        ...

Para crear una relación *recursiva* -- un objeto que tiene una relación
muchos-a-uno consigo mismo -- usa ``models.ForeignKey('self')``::

    class Empleado(models.Model):
        manager = models.ForeignKey('self')

Si necesitas crear una relación con un modelo que aún no ha sido  definido,
puedes usar el nombre del modelo en lugar del objeto modelo::

  from django.db import models

  class Carro(models.Model):
      fabricante = models.ForeignKey('Fabricante')
      # ...

  class Fabricante(models.Model):
      # ...
      pass

Para referirte a modelos que han sido definidos en otra aplicación, puedes
explícitamente especificar un modelo con el nombre completo de la etiqueta
de la aplicación. Por ejemplo si el modelo ``Manufactura`` arriba definido es
definido en otra aplicación llamada ``producción``, necesitas usar::

    class Carro(models.Model):
        fabricante = models.ForeignKey('producccion.Fabricante')

Esta clase de referencia puede ser útil al resolver dependencias circulares
de importaciones entre dos aplicaciones.

Toma en cuenta que cada vez que creas una relación foránea, se crea un
un índice en la base de datos de forma automática. Puedes desactivar este
comportamiento fijando ``db_index = False``,  en el archivo del modelo.
Si quieres evitar la sobrecarga que ocasiona un índice, o si estas creando un
índice alternativo.

.. warning::

  No es recomendable tener un campo ``ForeignKey`` de una aplicación sin
  migraciones, enlazado a una aplicación con las migraciones aplicadas.

Detrás de escena, Django agrega ``"_id"`` al nombre de campo para crear su
nombre de columna en la base de datos. En el ejemplo anterior, la tabla de la
base de datos correspondiente al modelo ``Carro``, tendrá una columna
``fabricante_id``. (Puedes cambiar esto explícitamente especificando
``db_column``; ver más arriba en la sección "`db_column`_".) De todas formas, tu
código nunca debe utilizar el nombre de la columna de la base de datos, salvo
que escribas tus propias SQL. Siempre te manejarás con los nombres de campo de
tu objeto modelo.

Se sugiere, pero no es requerido, que el nombre de un campo ``ForeignKey``
(``fabricante`` en el ejemplo) sea el nombre del modelo en minúsculas. Por
supuesto, puedes ponerle el nombre que quieras. Por ejemplo::

    class Carro(models.Model):
        fabrica_de_autos  = models.ForeignKey(Fabricante)
        # ...

Los campos ``ForeignKey`` reciben algunos argumentos extra para definir como
debe trabajar la relación (ver Tabla B-5). Todos son opcionales.

.. table:: Opciones de ForeignKey

  =======================  ========================================================================
      Argumento                Descripción
  =======================  ========================================================================
  ``limit_choices_to``     Establece un límite a las opciones disponibles para el campo,
                           cuando es renderizado usando ``ModelForm`` en el admin (por omisión,
                           todos los objetos de el ``queryset`` están disponibles para elegir).
                           Usa un diccionario, un objeto ``Q``, o un llamable que devuelva
                           un diccionario, o un objeto ``Q``  que puede ser utilizado.

                           Por Ejemplo::

                               staff_member = models.ForeignKey(limit_choices_to={'is_staff': True}

                           Esto hace  que el campo correspondiente en ModelForm liste únicamente
                           ``Users`` que tengan asignado ``is_staff=True``.

  ``related_name``         El nombre a utilizar para la relación desde el objeto
                           relacionado hacia él objeto con el que se relaciona.

  ``related_query_name``   El nombre a utilizar para el nombre inverso del filtro del modelo.
                           Remplaza el valor de ``related_name`` si se establece, de otra
                           manera será el valor por defecto del nombre del modelo::

                             # Declara el campo foráneo con ``related_query_name``
                             class Tag(models.Model):
                                 article = models.ForeignKey(Article, related_name="tags",
                                     related_query_name="tag")
                                 name = models.CharField(max_length=255)

                             # Éste ahora es el nombre del filtro inverso
                             Article.objects.filter(tag__name="important")

  ``to_field``             El campo en el objeto relacionado con el cual se establece
                           la relación. Por omisión, Django usa la clave primaria del
                           objeto relacionado.

  ``db_constraint``         Regula la creación o no de  restricciones en la base de
                            datos para la clave foránea. Por omisión es ``True``, la mayoría
                            de las veces será cierto,  Usar ``False`` puede ser muy malo para
                            la integridad de los datos. Dicho esto, aquí hay algunos escenarios
                            donde podrías querer hacer esto:

                            * Tienes datos heredados que no son validos.
                            * Tu base de datos está rota.

  ``on_delete``             Cuando un objeto referenciado por un campo ``ForeignKey`` es
                            borrado. Django por omisión emula el comportamiento de las
                            restricciones SQL ``ON DELETE CASCADE`` y borra también el
                            objeto que contiene el campo ``ForeignKey``.

                            Este comportamiento puede ser sobrescrito usando algún
                            argumento con ``on_delete`` como los siguientes:

                            * ``CASCADE``:  Borra en cascada, el comportamiento por omisión.
                            * ``PROTECT``:  Previene que se borre la referencia a un objeto.
                            * ``SET_NULL`` Fija un campo ``ForeignKey`` a ``null``;  siempre y
                              cuando use ``null = True``.
                            * ``SET_DEFAULT`` Fija un campo ``ForeignKey`` como el valor por
                              omisión.
                            * ``SET()`` Fija un campo ``ForeignKey`` con el valor pasado a
                              ``SET()``, o mediante un llamable.

                            Por ejemplo si quieres tener un campo ``ForeignKey`` que
                            contenga valores nulos, cuando el objeto sea borrado utiliza
                            lo siguiente::

                                user = models.ForeignKey(User, blank=True, null=True,
                                    on_delete=models.SET_NULL).

  ``DO_NOTHING``           No toma ninguna acción.
  =======================  ========================================================================


Relaciones Muchos a Muchos
--------------------------

Para definir una relación muchos-a-muchos, usa un campo ``ManyToManyField``. Al
igual que los campos ``ForeignKey``, ``ManyToManyField`` requiere un argumento
posicional: la clase a la cual se relaciona el modelo,  trabaja de igual forma
que los campos ``ForeignKey``, incluyendo relaciones recursivas y perezosas.

Por ejemplo, si una ``Pizza`` tiene múltiples objetos ``Ingredientes`` -- es decir,
un ``Ingrediente`` puede estar en múltiples pizzas y cada ``Pizza`` tiene múltiples
ingredientes (ingredientes) -- debe representarse así::

    class Ingredientes(models.Model):
        ...

    class Pizza(models.Model):
        ingredientes = models.ManyToManyField(Ingredientes)
        ...

Como sucede con ``ForeignKey``, una relación de un objeto con sí mismo puede
definirse usando el string ``'self'`` en lugar del nombre del modelo, y puedes
hacer referencia a modelos que todavía no se definieron usando un string que
contenga el nombre del modelo. De todas formas solo puedes usar strings para
hacer referencia a modelos dentro del mismo archivo ``models.py`` -- no puedes
usar un string para hacer referencia a un modelo en una aplicación diferente, o
hacer referencia a un modelo que ha sido importado de cualquier otro lado.

Se sugiere, pero no es requerido, que el nombre de un campo ``ManyToManyField``
(``ingredientes``, en el ejemplo) sea un término en plural que describa al conjunto
de objetos relacionados con el modelo.

Detrás de la escena, Django crea una tabla join intermedia para representar la
relación muchos-a-muchos.

No importa cuál de los modelos tiene el  ``ManyToManyField``, pero es necesario
que esté en uno de los modelos -- no en los dos.

Si estás usando la interfaz de administración, las instancias
``ManyToManyField`` deben ir en el objeto que va a ser editado en la interfaz de
administración. En el ejemplo anterior, los ``ingredientes`` están en la ``Pizza``
(en lugar de que el ``Ingredientes`` tenga ``pizzas`` ``ManyToManyField`` )
porque es más natural pensar que una ``Pizza`` tiene varios ``Ingredientes``  que
pensar que un ingrediente está en muchas pizzas. En la forma en que está
configurado el ejemplo, el formulario de administración de la``Pizza`` permitirá
que los usuarios selecciones los ingredientes.

Los objetos ``ManyToManyField`` toman algunos argumentos extra para definir como
debe trabajar la relación (ver Tabla B-6). Todos son opcionales.

.. table:: Opciones de un campo ManyToManyField

  =======================  ==================================================================
      Argumento                Descripción
  =======================  ==================================================================
  ``related_name``          El nombre a utilizar para la relación desde el objeto
                            relacionado hacia este objeto.

  ``related_query_name``    El nombre a utilizar para el nombre inverso del filtro del
                            modelo. Remplaza el valor de ``related_name`` si se establece,
                            de otra manera será el valor por defecto del nombre del modelo.

  ``limit_choices_to``      Ver la descripción en ``ForeignKey``.
                            ``limit_choices_to``  no tiene efecto cuando es usado con una
                            tabla intermedia especificada usando el parámetro ``througth``

  ``symmetrical``           Solo utilizado en la definición de ``ManyToManyField``
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

  ``through``               Django automáticamente genera una tabla para manejar las
                            relaciones muchos a muchos. Si quieres especificar una tabla
                            intermedia, puedes usar la opción ``through`` para especificar el
                            modelo Django que representara la tabla intermedia que quieras usar.

                            Los casos más comunes para usar esta opción es cuando quieres
                            asociar datos extras con relaciones muchos a muchos.

                            Si no especificas explícitamente un modelo con ``through``,
                            todavía hay implícita una clase del modelo ``through``, que puedes
                            usar directamente para crear las tablas y sus asociaciones.
                            Tiene tres campos:

                            * ``id``: La clave primaria de la relación.
                            * ``<containing_model>_id``: El id del modelo que declara la relación
                              ``ManyToManyField``.
                            * ``<other_model>_id``: El id del modelo que enlaza a
                              ``ManyToManyField``

  ``through_fields``        Usado únicamente en modelos intermedios personalizados. Django
                            normalmente determina el campo intermedio de un modelo que se
                            usara para establecer el orden  en una relación muchos a muchos
                            automáticamente. Considera el siguiente ejemplo::

                                from django.db import models

                                class Persona(models.Model):
                                    nombre = models.CharField(max_length=50)

                                class Grupo(models.Model):
                                    nombre = models.CharField(max_length=128)
                                    miembros = models.ManyToManyField(Persona,
                                        through='mienbros', through_fields=('grupo',
                                            'persona'))

                                class Mienbros(models.Model):
                                    grupo = models.ForeignKey(Group)
                                    persona = models.ForeignKey(Person)
                                    invitados = models.ForeignKey(Person,
                                        related_name="mienbros_invitados")
                                    razon_invitacion = models.CharField(max_length=64)


                            ``Mienbros`` tiene *dos*  claves foráneas ``Persona`` (``persona`` e
                            ``invitados``) lo cual hace que la relación sea ambigua y Django no
                            sepa cual utilizar. En este caso, debes explícitamente especificar
                            cual clave foránea deberá utilizar Django, usando ``through_fields``,
                            como en el modelo ``Grupo``.

                            ``through_fields`` acepta 2 tuplas ``('field1', 'field2')``, donde
                            ``field1`` es el nombre de la clave foránea del modelo de la clase
                            ``ManyToManyField`` donde está definido con (``grupo`` en este caso),
                            y ``field2`` es el nombre de la clave foránea con el campo del modelo.

                            Cuando se usan más de una clave foráneas en un modelo intermedio para
                            cualquiera (o ambos) de los modelos participantes en la relación
                            muchos a muchos, es necesario *especificar* ``through_fields``.
                            Esto también se aplica a relaciones recursivas, cuando un modelo
                            intermedio es usado con más de dos claves foráneas en un modelo, o si
                            deseas explícitamente  especificar cuál de los dos debe usar Django.

  ``swappable``             Controla la reacción del framework de migraciones, si el campo
                            ``ManyToManyField`` apunta a un modelo intercambiable o ``swappable``,
                            Si este es ``True`` --el valor por omisión, el campo `ManyToManyField``
                            apunta al modelo con el cual coincide el valor actual de ``settings.
                            AUTH_USER_MODEL`` (u otra configuración de un modelo de intercambio),
                            la relación será almacenada en la migración usando una referencia a la
                            configuración, no al  modelo directamente.

                            Únicamente querrías sobrescribir esto a ``False`` si estás seguro de
                            que tu modelo apunta siempre hacia el modelo intercambiable -- por
                            ejemplo,  si es un modelo diseñado específicamente para un modelo de
                            usuario personalizado.

                            Por último, toma en cuenta que los campos ``ManyToManyField`` no
                            soporta validadores y  que  ``null`` no tiene efecto ya que no es
                            requerido en  una relación a nivel de base de datos.

  ``db_table``              El nombre de la tabla a crear para almacenar los datos de
                            la relación muchos-a-muchos. Si no se provee, Django asumirá
                            un nombre por omisión basado en los nombres de las dos
                            tablas a ser vinculadas.

  ``db_constraint``         Como en los campos ``ForeignKey``, regula la creación o no de
                            restricciones en la base de  datos para la clave foránea.  El
                            valor por defecto es ``True``
  =======================  ==================================================================


Relaciones uno a uno
--------------------

Una relación uno-a-uno, es conceptualmente muy parecida a una relación
foránea o ``ForeignKey`` con un parámetro ``unique=True``, solo que el lado
"inverso" de la relación devuelve directamente un único objeto.

Esto es más útil como la clave primaria de un modelo que "extiende" otro
modelo de la misma forma; la herencia multi-tablas es implementada agregando
implícitamente una relación uno a uno del modelo hijo al modelo padre.

Un argumento posicional es requerido, la clase a la cual el modelo se
relaciona. Esto funciona exactamente de la misma forma en que lo
hace para ``ForeignKey`` incluyendo todas las opciones incluyendo  relaciones
recursivas y perezosas.

Adicionalmente  ``OneToOneField`` acepta todos los argumentos extras aceptados
por un campo ``ForeignKey``, más un argumento extra.

* ``parent_link``: Cuando es ``True`` y es usado en un modelo el cual hereda de
  otro modelo (concretamente) indica que el campo se debe utilizar para enlazar
  la clase padre, en lugar de el extra ``OneToOneField`` que normalmente sería
  creado implícitamente por  la subclase

Si no especificas el nombre para el argumento ``related_name`` en un campo
``OneToOneField``, Django usara el nombre del modelo en minúsculas, como el
valor por default.

Por ejemplo::

    from django.conf import settings
    from django.db import models

    class UsuarioEspecial(models.Model):
        user = models.OneToOneField(settings.AUTH_USER_MODEL)
        supervisor = models.OneToOneField(settings.AUTH_USER_MODEL,
            related_name='supervisor')

El modelo ``User`` tendrá los siguientes atributos::

    >>> user = User.objects.get(pk=1)
    >>> hasattr(user, 'usuarioespecial')
    True
    >>> hasattr(user, 'supervisor')
    True


Una excepción del tipo ``DoesNotExist`` es lanzada cuando se accede a la relación
inversa de una entrada de una tabla que no existe. Por ejemplo, si un ``user``
no tiene un ``supervisor`` definido en ``UsuarioEspecial``::

    >>> user.supervisor
    Traceback (most recent call last):
        ...
    DoesNotExist: User matching query does not exist.


Opciones de los Metadatos de un Modelo
======================================

Los metadatos específicos de un modelo viven en una ``class Meta`` definida en
el cuerpo de la clase del modelo::

    class Libro(models.Model):
        titulo = models.CharField(max_length=100)

        class Meta:
            # Los metadatos van aquí
            ...

Los metadatos del modelo son "cualquier cosa que no sea un campo", como
opciones de ordenamiento, nombre en plural, etc.

Las secciones que siguen presentan una lista de todas las posibles opciones
``Meta``. Ninguna de estas opciones es requerida. Agregar ``class Meta`` a un
modelo es completamente opcional.

abstract
--------

Si es  ``True``, este modelo será una clase base abstracta.

db_table
--------

El nombre de la tabla de la base de datos a usar para el modelo.

Nombre de tablas
~~~~~~~~~~~~~~~~

Para ahorrarte tiempo, Django deriva automáticamente el nombre de la tabla de la
base de datos a partir del nombre de la clase modelo y la aplicación que la
contiene. Un nombre de tabla de base de datos de un modelo se construye uniendo
la etiqueta de la aplicación del modelo -- el nombre que usaste en
``manage.py startapp`` -- con el nombre de la clase modelo, con un guión bajo
entre ellos.

Por ejemplo, si tienes una aplicación  ``biblioteca`` (creada por
``manage.py startapp biblioteca``), un modelo definido como ``class Libro`` tendrá
una tabla en la base de datos llamada ``libros``.

Para sobreescribir el nombre de la tabla de la base de datos, use el parámetro
``db_table`` dentro de ``class Meta``::

    class Libro(models.Model):
        ...

        class Meta:
            db_table = 'un_nombre_cualquiera'

Si no se define, Django utilizará ``app_label`` + '_' + ``model_class_name``.

Si tu nombre de tabla de base de datos es una palabra reservada de SQL, o
contiene caracteres que no están permitidos en los nombres de variable de Python
(especialmente el guión simple), no hay problema. Django entrecomilla los nombres de
tabla y de columna detrás de la escena.

db_tablespace
-------------

El nombre de la tabla de la base de datos para usar por el modelo. Si el
``backend `` no  soporta ``tablespaces``, esta opción será ignorada.

get_latest_by
-------------

El nombre de un  ``DateField`` o ``DateTimeField`` del modelo. Esto especifica
el campo a utilizar por omisión en el método ``latest()`` del ``Manager`` del
modelo.

Aquí hay un ejemplo::

    get_latest_by = "fecha_publicacion"

managed
-------

Por defecto es  ``True``,  lo cual significa que Django creará las apropiadas
tablas de la  base de datos en las migraciones, o como parte de las migraciones
y las removerá como parte del comando ``flush``. Es decir, Django *maneja*
los ciclos vitales de las tablas de la base de datos.

Si es ``False``,   no se realizará ningunas operaciones de creación o borrado
de la tabla de base de datos para este modelo. Esto es útil si el modelo
representa una tabla existente o una vista de la base de datos que se ha
creado por algún otro medio. Ésta es la única diferencia cuando usas
``managed=False.`` El resto de los aspectos del manejo del modelo son
exactamente iguales que  los de uno normal. Esto incluye

1. Agregar una clave primaria automáticamente al modelo si no se declara una.
   Para evitar confusiones, para los que lean el código, es recomendable
   especificar todas las columnas de la base de datos que se están modelando, aun
   cuando se estén usando modelos ``unmanaged``

2. Si el modelo con ``managed=False`` contiene un campo ``ManyToManyField`` que
   enlace otro modelo ``unmanaged``, en lugar de una tabla intermedia para
   juntar  la tabla muchos a muchos esta no se creara.  Sin embargo, una tabla
   intermediaria  entre un modelo ``managed`` y un ``unmanaged`` si se puede
   crear.

   Si necesitas cambiar este comportamiento por defecto, crea una tabla
   intermedia como un modelo explicito (con ``managed`` según lo necesitado) y
   usa el atributo ``through`` para hacer que la relación use un modelo
   personalizado.

Para pruebas que incluyan modelos con ``managed=False``, necesitas asegurarte
que se están creando las tablas correctas, como parte de las pruebas.

Si estas interesado en cambiar el comportamiento a nivel-Python de un modelo
de una clase, *puedes* usar ``managed=False`` y crear una copia de un modelo
existente. Sin embargo existe una mejor forma de aprovechar esta situación:
usa ``proxy-models``

ordering
--------

El ordenamiento por omisión del objeto, utilizado cuando se obtienen listas de
objetos::

    ordering = ['-fecha_publicacion']

Esta es una tupla o lista de cadenas o strings. Cada string es un nombre de
campo con un prefijo opcional ``-``, que indica orden descendiente. Los campos
sin un ``-`` precedente se ordenarán en forma ascendente. Use el string ``"?"``
para ordenar al azar.

.. admonition:: Nota

    Sin importar de cuántos campos consista ``ordering``, el sitio
    administrativo únicamente usara el primer campo.

Por ejemplo, para ordenar por un campo ``titulo`` en orden ascendente (A-Z), usa
esto::

    ordering = ['titulo']

Para ordenar por ``titulo`` en orden descendente (Z-A), usa esto::

    ordering = ['-titulo']

Para ordenar por ``titulo`` en orden descendente, y luego por ``autor`` en
orden ascendente, usa esto::

    ordering = ['-titulo', 'autor']

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

.. admonition:: Cambiando order_with_respect_to

  ``order_with_respect_to`` agrega un campo a la base de datos, en especifico
  una columna llamada ``_order``, asi que asegúrate que los cambios sea aplicados
  correctamente en cada migración, si agregas o cambias ``order_with_respect_to``
  después de la  inicial migración.

proxy
-----

Si se establece en ``True``, un modelo de una subclase de otro modelo, será
tratado como un modelo ``proxi``.

unique_together
---------------

Conjuntos de nombres de campo que tomados juntos deben ser únicos::

    unique_together = (("driver", "restaurant"),)

Esto es una lista de listas de campos que deben ser únicos cuando se consideran
juntos. Es usado en la interfaz de administración de Django y se refuerza a
nivel de base de datos (esto es, se incluyen las sentencias ``UNIQUE``
apropiadas en la sentencia ``CREATE TABLE``).

verbose_name
------------

Un nombre legible por humanos para el objeto, en singular::

    verbose_name = "pizza"

Si no se define, Django utilizará una versión adaptada del nombre de la clase,
en la cual ``CamelCase`` se convierte en ``camel case``.

verbose_name_plural
-------------------

El nombre del objeto en plural::

    verbose_name_plural = "historias"

Si no se define, Django agregará una "s" al final del ``verbose_name``.


Opciones del Administrador
==========================

.. class:: ModelAdmin


La clase ``ModelAdmin`` le dice a Django cómo mostrar el modelo en el sitio de
administración. Usualmente se almacena en el archivo ``admin.py`` dentro de la
aplicación (el comando ``startapp`` crea el archivo ``admin.py`` ).

Por ejemplo::

        from biblioteca.models import Autor

        class InterfazAutor(admin.ModelAdmin):
            pass

        admin.site.register(Author, InterfazAutor)

De forma predeterminada la clase ``ModelAdmin`` registra todos los valores
del modelo, si esto es lo que buscas una manera muy sencilla de simplificar
el ejemplo anterior es usando lo siguiente ::

        from django.contrib import admin
        from biblioteca.models import Autor

         admin.site.register(Autor)

También puedes usar un decorador, para registrar la clase  ``ModelAdmin``,
directamente en el modelo::

        from django.contrib import admin
        from .models import Autor

        @admin.register(Author)
        class AuthorAdmin(admin.ModelAdmin):
            pass

Las siguientes secciones presentan una lista de alguna de las opciones que acepta
la clase ``ModelAdmin`` para personalizar sus atributos. Ninguna de estas
opciones es requerida. Para utilizar una interfaz de administración.

.. attribute:: ModelAdmin.date_hierarchy


Establece ``date_hierarchy`` con el nombre de un ``DateField`` o
``DateTimeField`` en tu modelo, y la página de la lista de cambios incluirá una
navegación basada en la fecha usando ese campo.

Aquí hay un ejemplo::

    # Archivo models.py
    class Libro(models.Model):
        fecha = models.DateTimeField()
        ...


    # Archivo admin.py
    from biblioteca.models import Autor

    class InterfazLibro(admin.ModelAdmin):
        date_hierarchy = "fecha"

    admin.site.register(Libro, InterfazLibro)

.. attribute:: ModelAdmin.exclude


Este atributo, establece la lista de nombres de campos que se deben excluir de un
formulario.

Por ejemplo, considera el siguiente modelo::

    from django.db import models

    class Autor(models.Model):
        nombre = models.CharField(max_length=100)
        titulo = models.CharField(max_length=3)
        fecha_nacimiento = models.DateField(blank=True, null=True)

Si solo quieres incluir en un formulario del modelo ``Autor`` los campos
``nombre`` y  ``titulo``,  puedes especificarlos a través de  ``exclude``
de la siguiente forma::

        from django.contrib import admin

        class AutorAdmin(admin.ModelAdmin):
            fields = ('nombre', 'titulo')

        class AuthorAdmin(admin.ModelAdmin):
            exclude = ('fecha_nacimiento',)


.. attribute:: ModelAdmin.fields

Una tupla de nombres de campo a mostrar en el conjunto de campos. Esta clave es
requerida.

Para mostrar múltiples campos en la misma linea, encierra esos campos en su
propia tupla. En este ejemplo, los campos ``nombre`` y ``apellido`` se
mostrarán en la misma línea.

Por ejemplo, para definir un simple formulario de un modelo de
:class:`django.contrib.flatpages.models.FlatPage`, podemos usar ``fields`` asi::

        class FlatPageAdmin(admin.ModelAdmin):
            fields = ('url', 'title', 'content')

.. admonition:: Note

    La opcion ``fields`` no debe de confundirse con el diccionario ``fields``
    de el atributo de la opcion :attr:`~ModelAdmin.fieldsets`, de la siguiente
    seccion.


.. attribute:: ModelAdmin.fieldsets

Establece ``fieldsets`` para controlar la disposición de las páginas "agregar" y
"modificar" de la interfaz de administración.

``fieldsets`` es una estructura anidada bastante compleja que se demuestra mejor
con un ejemplo. Lo siguiente está tomado del modelo ``FlatPage`` que es parte
de ``django.contrib.flatpages``::

    from django.contrib import admin

    class FlatPageAdmin(admin.ModelAdmin):
        fieldsets = (
            (None, {
                'fields': ('url', 'title', 'content', 'sites')
            }),
            ('Advanced options', {
                'classes': ('collapse',),
                'fields': ('enable_comments', 'registration_required', 'template_name')
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

* ``fields``

    Una tupla de nombres de campo a mostrar en el conjunto de campos. Esta
    clave es requerida.

    Ejemplo::

            {
            'fields': ('nombre', 'apellido', 'domicilio', 'ciudad', 'estado'),
            }


  Para mostrar múltiples campos en la misma linea, encierra esos campos en su
  propia tupla.::

       {
            'fields': (('nombre', 'apellido'), 'domicilio', 'ciudad', 'estado'),
       }


* ``classes``

    Un string conteniendo clases extra CSS para aplicar al conjunto de campos.

    Ejemplo::

        {
            'classes': ('wide', 'extrapretty'),
        }


   Dos clases útiles definidas por la hoja de estilo del sitio de administración
   por omisión son ``collapse`` y ``wide``. Los conjuntos de campos con el estilo
   ``collapse`` serán colapsados inicialmente en el sitio de administración y
   reemplazados por un pequeño enlace "click to expand". Los conjuntos de campos
   con el estilo ``wide`` tendrán espacio horizontal extra.

* ``description``

  Un string de texto extra opcional para mostrar encima de cada conjunto de
  campos, bajo el encabezado del mismo. Se usa tal cual es, de manera que puedes
  usar cualquier HTML, y debes crear las secuencias de escape correspondientes
  para cualquier carácter especial HTML (para evitar problemas de seguridad).


.. attribute:: ModelAdmin.list_display


Establece ``list_display`` para controlar que campos se muestran en la página
de la lista de del administrador.

    Ejemplo::

        list_display = ('nombre', 'apellido')


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

          from django.db import models
          from django.contrib import admin
          from django.utils.html import format_html

          class Persona(models.Model):
              nombre = models.CharField(max_length=50)
              apellido = models.CharField(max_length=50)
              color_codigo = models.CharField(max_length=6)

              def nombre_coloreado(self):
                  return format_html('<span style="color: #{0};">{1} {2}</span>',
                                     self.color_codigo,
                                     self.nombre,
                                     self.apellido)

              nombre_coloreado.allow_tags = True

          class PersonAdmin(admin.ModelAdmin):
              list_display = ('nombre', 'apellido', 'nombre_coloreado')

* Si el string dado es un método del modelo que retorna ``True`` o
  ``False``, Django mostrará un bonito icono "on" o "off" si le das al
  método un atributo ``boolean`` con valor en ``True``.

  Aquí está un modelo de ejemplo completo::

          class Person(models.Model):
              nombre = models.CharField(maxlength=50)
              fecha_nacimiento = models.DateField()

              class Admin:
                  list_display = ('nombre', 'fecha_nacimiento')

              def nacido_cincuentas(self):
                  return self.fecha_nacimiento.strftime('%Y')[:3] == 5
              nacido_cincuentas.boolean = True

* Los métodos ``__str__()`` son tan válidos en ``list_display`` como
  cualquieras otro método del modelo, por lo cual está perfectamente bien
  hacer esto::

          list_display = ('__str__', 'some_other_field')

* Usualmente, los elementos de ``list_display`` que no son campos de la
  base de datos no pueden ser utilizados en ordenamientos (porque Django
  hace todo el ordenamiento a nivel de base de datos).

* Django trata de interpretar cada elemento de ``list_display`` es este orden:

      * Un campo de un modelo.
      * Un llamable.
      * Una cadena de representacion de un atributo ``ModelAdmin``.
      * Una cadena de representacion de un atributo de un modelo.


.. attribute:: ModelAdmin.list_display_links

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

En este ejemplo, los campos ``nombre`` y ``apellido`` serán vinculados a
la página de la lista de cambios::

    class Persona(models.Model):
        ...

        class Admin:
            list_display = ('nombre', 'apellido', 'fecha_cumpleaños')
            list_display_links = ('nombre', 'apellido')

En este ejemplo, la lista de cambios no tiene links::

        class PersonaAdmin(admin.ModelAdmin):
            list_display = ('nombre', 'apellido')
            list_display_links = None

Finalmente, observa que para usar ``list_display_links``, debes definir también
``list_display``.


.. attribute:: ModelAdmin.list_filter


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
            list_display = ('username', 'email', 'nombre', 'apellido', 'is_staff')
            list_filter = ('is_staff', 'is_superuser')

.. attribute:: ModelAdmin.list_per_page


Establece ``list_per_page`` para controlar cuantos items aparecen en cada
página de la lista de cambios del administrador. Por omisión, este valor se
establece en ``100``.

.. attribute:: ModelAdmin.list_select_related


Establece ``list_select_related`` para indicarle a Django que use
``select_related()`` al recuperar la lista de objetos de la página de la lista
de cambios del administrador. Esto puede ahorrarte una cantidad de consultas a
la base de datos si estás utilizando objetos relacionados en la lista de
cambios que muestra el administrador.

El valor debe ser ``True`` o ``False``. Por omisión es ``False``, salvo que uno
de los campos ``list_display`` sea una ``ForeignKey``.

Para más detalles sobre ``select_related()``, ver Apéndice C.

.. attribute:: ModelAdmin.ordering


Establece ``ordering`` para especificar como deben ordenarse los objetos en la
página de la lista de cambios del administrador. Esto debe ser una lista o
tupla en el mismo formato que el parámetro ``ordering`` del modelo.

Si no está definido, la interfaz de administración de Django usará el
ordenamiento por omisión del modelo.

.. attribute:: ModelAdmin.save_as


Establece ``save_as`` a ``True`` para habilitar la característica "save as" en
los formularios de cambios del administrador.

Normalmente, los objetos tienen tres opciones al guardar: "Save",
"Save and continue editing" y "Save and add another". Si ``save_as`` es
``True``, "Save and add another" será reemplazado por un botón "Save as".

"Save as" significa que el objeto será guardado como un objeto nuevo (con un
identificador nuevo), en lugar del objeto viejo.

Por omisión, ``save_as`` es ``False``.

.. attribute:: ModelAdmin.save_on_top


Establece ``save_on_top`` para agregar botones de guardado a lo largo del
encabezado de tus formularios de cambios del administrador.

Normalmente, los botones de guardado aparecen solamente al pie de los
formularios. Si estableces ``save_on_top``, los botones aparecerán en el
encabezado y al pié del formulario.

Por omisión, ``save_on_top`` es ``False``.

.. attribute:: ModelAdmin.search_fields


Establece ``search_fields`` para habilitar un cuadro de búsqueda en la página
de la lista de cambios del administrador. Debe ser una lista de nombres de
campo que se utilizará para la búsqueda cuando alguien envíe una consulta en
ese cuadro de texto.

Estos campos deben ser de alguna tipo de campo de texto, como ``CharField`` o
``TextField``. También puedes realizar una búsqueda relacionada sobre una
``ForeignKey`` con la notación de búsqueda de la API::

    class Empleado(models.Model):
        departmento = models.ForeignKey(Departmento)
        ...

        class Admin:
            search_fields = ['departamento']

Cuando alguien hace una búsqueda en el cuadro de búsqueda del administrador,
Django divide la consulta de búsqueda en palabras y retorna todos los objetos
que contengan alguna de las palabras, sin distinguir mayúsculas y minúsculas,
donde cada palabra debe estar en al menos uno de los ``search_fields``. Por
ejemplo, si ``search_fields`` es ``['nombre', 'apellido']`` y un usuario
busca ``john lennon``, Django hará el equivalente a esta cláusula ``WHERE`` en
SQL::

    WHERE (nombre ILIKE '%john%' OR apellido ILIKE '%john%')
    AND (nombre ILIKE '%lennon%' OR apellido ILIKE '%lennon%')

Para búsquedas más rápidas y/o más restrictivas, agrega como prefijo al nombre
de campo un operador como se muestra en la Tabla B-7.

.. table:: Operadores Permitidos en search_fields

    ==========  =======================================================================
     Operador    Significado
    ==========  =======================================================================
        ``^``    Coincide al principio del campo. Por ejemplo, si ``search_fields``
                 es ``['^nombre', '^apellido']``, y un usuario busca  ``john
                 lennon``, Django hará el equivalente a esta cláusula ``WHERE``
                 en SQL::

                     WHERE (nombre ILIKE 'john%' OR apellido ILIKE 'john%')
                     AND (nombre ILIKE 'lennon%' OR apellido ILIKE 'lennon%')

                 Esta consulta es más eficiente que la consulta ``'%john%'``, dado
                 que la base de datos solo necesita examinar el principio de una
                 columna de datos, en lugar de buscar a través de todos los
                 datos de la columna. Además, si la columna tiene un índice,
                 algunas bases de datos pueden permitir el uso del índice para
                 esta consulta, a pesar de que sea una consulta ``LIKE``.

        ``=``    Coincide exactamente, sin distinguir mayúsculas y minúsculas.
                 Por ejemplo, si ``search_fields`` es ``['=nombre', '=apellido']``
                 y un usuario busca ``john lennon``, Django hará el equivalente a
                 esta clausula ``WHERE`` en SQL::

                     WHERE (nombre ILIKE 'john' OR apellido ILIKE 'john')
                     AND (nombre ILIKE 'lennon' OR apellido ILIKE 'lennon')

                 Observar que la entrada de la consulta se divide por los espacios,
                 por lo cual actualmente no es posible hacer una búsqueda de todos
                 los registros en los cuales ``nombre`` es exactamente ``'john
                 winston'`` (con un espacio en el medio).

        ``@``    Realiza una búsqueda en todo el texto. Es similar al método de
                 búsqueda predeterminado, pero usa un índice. Actualmente solo está
                 disponible para MySQL.
    ==========  =======================================================================

