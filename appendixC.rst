=================================================
Apéndice C: Referencia de la API de base de datos
=================================================

La API de base de datos de Django es la otra mitad de la API de modelos
discutido en el Apéndice B. Una vez que hayas definido un modelo, usarás esta
API en cualquier momento que necesites acceder a la base de datos. Has visto
ejemplos del uso de esta API a través del libro; este apéndice explica todas las
varias opciones detalladamente.

De manera similar a lo que ocurre con las APIs de modelos descriptos en el
apéndice B, estas APIs son considerados muy estables, aunque los desarrolladores
de Django constantemente añaden nuevos atajos y conveniencias. Es buena idea
consultar siempre la documentación en línea más actual que está disponible en
http://www.djangoproject.com/documentation/0.96/db-api/.

A lo largo de este apéndice, vamos a hacer referencia a los siguientes modelos,
los cuales pueden formar una simple aplicación de blog::

    from django.db import models

    class Blog(models.Model):
        name = models.CharField(max_length=100)
        tagline = models.TextField()

        def __str__(self):
            return self.name

    class Author(models.Model):
        name = models.CharField(max_length=50)
        email = models.EmailField()

        def __str__(self):
            return self.name

    class Entry(models.Model):
        blog = models.ForeignKey(Blog)
        headline = models.CharField(max_length=255)
        body_text = models.TextField()
        pub_date = models.DateTimeField()
        authors = models.ManyToManyField(Author)

        def __str__(self):
            return self.headline

Creando Objetos
===============

Para crear un objeto, crea una instancia de la clase modelo usando argumentos
de palabra clave y luego llama a ``save()`` para grabarlo en la base de datos::

    >>> from mysite.blog.models import Blog
    >>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
    >>> b.save()

Esto, detrás de escena, ejecuta una sentencia SQL ``INSERT``. Django no accede a
la base de datos hasta que tú explícitamente invoques a ``save()``.

El método ``save()`` no retorna nada.

Para crear un objeto y grabarlo todo en un paso revisa el método ``create`` de
la clase ``Manager`` que describiremos en breve.

Qué pasa cuando grabas?
-----------------------

Cuando grabas un objeto, Django realiza los siguientes pasos:

#. **Emitir una señal pre_save.** Esto provee una notificación de que un
   objeto está a punto de ser grabado. Puedes registrar un ***listener***
   que será invocado en cuanto esta señal sea emitida. Estas señales
   todavía están en desarrollo y no estaban documentadas cuando este libro
   fue a impresión; revisa la documentación en línea para obtener la
   información más actual.

#. **Pre-procesar los datos.** Se le solicita a cada campo del objeto
   implementar cualquier modificación automatizada de datos que pudiera
   necesitar realizar.

   La mayoría de los campos *no* realizan pre-procesamiento -- los datos
   del campo se guardan tal como están. Sólo se usa pre-procesamiento
   en campos que tienen comportamiento especial, como campos de archivo.

#. **Preparar los datos para la base de datos.** Se le solicita a cada
   campo que provea su valor actual en un tipo de dato que puede ser
   grabado en la base de datos.

   La mayoría de los campos no requieren preparación de los datos. Los
   tipos de datos simples, como enteros y cadenas, están
   "listos para escribir" como un objeto de Python. Sin embargo,
   tipo de datos más complejos requieren a menudo alguna modificación. Por
   ejemplo, ``DateFields`` usa un objeto ``datetime`` Python para almacenar
   datos. Las bases de datos no almacenan objetos ``datetime``, de manera
   que el valor del campo debe ser convertido en una cadena de fecha que
   cumpla con la norma ISO correspondiente para la inserción en la base de
   datos.

#. **Insertar los datos en la base.**  Los datos pre-procesados y preparados
   son entonces incorporados en una sentencia SQL para su inserción en la
   base de datos.

#. **Emitir una señal post_save.** Como con la señal ``pre_save``, esta es
   utilizada para proporcionar notificación de que un objeto ha sido
   grabado satisfactoriamente. De nuevo, estas señales todavía no han sido
   documentadas.

Claves primarias autoincrementales
----------------------------------

Por conveniencia, a cada modelo se le da una clave primaria autoincremental
llamada ``id`` a menos que explícitamente especifiques ``primary_key=True`` en
el campo (ver la sección titulada "`AutoField`_" en el Apéndice B).

Si tu modelo tiene un ``AutoField``, ese valor incrementado automáticamente
será calculado y grabado como un atributo de tu objeto la primera vez que
llames a ``save()``::

    >>> b2 = Blog(name='Cheddar Talk', tagline='Thoughts on cheese.')
    >>> b2.id     # Returns None, because b doesn't have an ID yet.
    None

    >>> b2.save()
    >>> b2.id     # Returns the ID of your new object.
    14

No hay forma de saber cual será el valor de un identificador antes que llames a
``save()`` esto se debe a que ese valor es calculado por tu base de datos, no
por Django.

Si un modelo tiene un ``AutoField`` pero quieres definir el identificador de un
nuevo objeto explícitamente cuando grabas, solo defínelo explícitamente antes
de grabarlo en vez de confiar en la asignación automática de valor del
identificador::

    >>> b3 = Blog(id=3, name='Cheddar Talk', tagline='Thoughts on cheese.')
    >>> b3.id
    3
    >>> b3.save()
    >>> b3.id
    3

Si asignas manualmente valores de claves primarias autoincrementales ¡Asegúrate
de no usar un valor de clave primaria que ya existe!. Si creas un objeto con
un valor explícito de clave primaria que ya existe en la base de datos, Django
asumirá que estás cambiando el registro existente en vez de crear uno nuevo.

Dado el ejemplo precedente de blog ``'Cheddar Talk'``, este ejemplo
sobrescribiría el registro previo en la base de datos::

    >>> b4 = Blog(id=3, name='Not Cheddar', tagline='Anything but cheese.')
    >>> b4.save()  # Overrides the previous blog with ID=3!

El especificar explícitamente valores de claves primarias autoincrementales es
más útil cuando se están grabando objetos en lotes, cuando estás seguro de que
no tendrás colisiones de claves primarias.

Grabando cambios de objetos
===========================

Para grabar los cambios hechos a un objeto que existe en la base de datos, usa
``save()``.

Dada la instancia de ``Blog`` ``b5`` que ya ha sido grabada en la base de
datos, este ejemplo cambia su nombre y actualiza su registro en la base::

    >>> b5.name = 'New name'
    >>> b5.save()

Detrás de escena, esto ejecuta una sentencia SQL ``UPDATE``. De nuevo: Django no
accede a la base de datos hasta que llamas explícitamente a ``save()``.

.. admonition:: Como sabe Django cuando usar ``UPDATE`` y cuando usar ``INSERT``

    Habrás notado que los objetos de base de datos de Django usan el mismo
    método ``save()`` para crear y cambiar objetos. Django abstrae la necesidad
    de usar sentencias SQL ``INSERT`` o ``UPDATE``.  Específicamente, cuando
    llamas a ``save()``, Django sigue este algoritmo:

    * Si el atributo clave primaria del objeto tiene asignado un valor que
      evalúa ``True`` (esto es, un valor distinto a ``None`` o a la cadena
      vacía) Django ejecuta una consulta ``SELECT`` para determinar si
      existe un registro con la clave primaria especificada.

    * Si el registro con la clave primaria especificada ya existe, Django
      ejecuta una consulta ``UPDATE``.

    * Si el atributo clave primaria del objeto *no* tiene valor o si lo
      tiene pero no existe un registro, Django ejecuta un ``INSERT``.

Debido a esto, debes tener cuidado de no especificar un valor explícito para
una clave primaria cuando grabas nuevos objetos si es que no puedes
garantizar que el valor de clave primaria está disponible para ser usado.

La actualización de campos ``ForeignKey`` funciona exactamente de la misma
forma; simplemente asigna un objeto del tipo correcto al campo en cuestión::

    >>> joe = Author.objects.create(name="Joe")
    >>> entry.author = joe
    >>> entry.save()

Django se quejará si intentas asignar un objeto del tipo incorrecto.

Recuperando objetos
===================

A través del libro has visto cómo se recuperan objetos usando código como el
siguiente::

    >>> blogs = Blog.objects.filter(author__name__contains="Joe")

Hay bastantes partes móviles detrás de escena aquí: cuando recuperas objetos de
la base de datos, estás construyendo realmente un ``QuerySet`` usando el
``Manager`` del modelo. Este ``QuerySet`` sabe como ejecutar SQL y retornar los
objetos solicitados.

El Apéndice B trató ambos objetos desde el punto de vista de la definición del
modelo; ahora vamos a ver cómo funcionan.

Un ``QuerySet`` representa una colección de objetos de tu base de datos. Puede
tener cero, uno, o muchos filtros -- criterios que limitan la colección basados
en parámetros provistos. En términos de SQL un ``QuerySet`` se compara a una
declaración ``SELECT`` y un filtro es una cláusula de limitación como por
ejemplo ``WHERE`` o ``LIMIT``.

Consigues un ``QuerySet`` usando el ``Manager`` del modelo. Cada modelo tiene
por lo menos un ``Manager`` y tiene, por omisión, el nombre ``objects``. Accede
al mismo directamente a través de la clase del modelo, así::

    >>> Blog.objects
    <django.db.models.manager.Manager object at 0x137d00d>

Los ``Manager``\s solo son accesibles a través de las clases de los modelos, en
vez desde una instancia de un modelo, para así hacer cumplir con la separación
entre las operaciones a "nivel de tabla" y las operaciones a "nivel de
registro"::

    >>> b = Blog(name='Foo', tagline='Bar')
    >>> b.objects
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: Manager isn't accessible via Blog instances.

El ``Manager`` es la principal fuente de ``QuerySet``\s para un modelo. Actúa
como un ``QuerySet`` "raíz" que describe todos los objetos de la tabla de base
de datos del modelo.  Por ejemplo, ``Blog.objects`` es el ``QuerySet``\s inicial
que contiene todos los objetos ``Blog`` en la base de datos.

Caching y QuerySets
===================

Cada ``QuerySet`` contiene un cache, para minimizar el acceso a la base de
datos. Es importante entender como funciona, para escribir código mas eficiente.

En un ``QuerySet`` recién creado, el cache esta vacío. La primera vez que un
``QuerySet`` es evaluado -- y, por lo tanto, ocurre un acceso a la base de datos
-- Django graba el resultado de la consulta en el cache del ``QuerySet`` y
retorna los resultados que han sido solicitados explícitamente (por ejemplo, el
siguiente elemento, si se está iterando sobre el ``QuerySet``). Evaluaciones
subsecuentes del ``QuerySet`` re-usan los resultados alojados en el cache.

Ten presente este comportamiento de caching, porque puede morderte si no usas
tus ``QuerySet``\s correctamente. Por ejemplo, lo siguiente creará dos
``QuerySet``\s, los evaluará, y los descartará::

    print [e.headline for e in Entry.objects.all()]
    print [e.pub_date for e in Entry.objects.all()]

Eso significa que la consulta sera ejecutada dos veces en la base de datos,
duplicando la carga sobre la misma.  También existe una posibilidad de que las dos
listas pudieran no incluir los mismos registros de la base de datos, porque se
podría haber agregado o borrado un ``Entry`` durante el pequeñísimo período
de tiempo entre ambas peticiones.

Para evitar este problema, simplemente graba el ``QuerySet`` y re-úsalo::

    queryset = Poll.objects.all()
    print [p.headline for p in queryset] # Evaluate the query set.
    print [p.pub_date for p in queryset] # Reuse the cache from the evaluation.

Filtrando objetos
=================

La manera mas simple de recuperar objetos de una tabla es conseguirlos todos.
Para hacer esto, usa el método ``all()`` en un ``Manager``::

    >>> Entry.objects.all()

El método ``all()`` retorna un ``QuerySet`` de todos los objetos de la base de
datos.

Sin embargo, usualmente solo necesitarás seleccionar un subconjunto del conjunto
completo de objetos. Para crear tal subconjunto, refinas el ``QuerySet``
inicial, añadiendo condiciones con filtros. Usualmente harás esto usando los
métodos ``filter()`` y/o ``exclude()``::

    >>> y2006 = Entry.objects.filter(pub_date__year=2006)
    >>> not2006 = Entry.objects.exclude(pub_date__year=2006)

Tanto ``filter()`` como ``exclude()`` toman argumentos de *patrones de
búsqueda*, los cuales se discutirán detalladamente en breve.

Encadenando filtros
-------------------

El resultado de refinar un ``QuerySet`` es otro ``QuerySet`` así que es posible
enlazar refinamientos, por ejemplo::

    >>> qs = Entry.objects.filter(headline__startswith='What')
    >>> qs = qs.exclude(pub_date__gte=datetime.datetime.now())
    >>> qs = qs.filter(pub_date__gte=datetime.datetime(2005, 1, 1))

Esto toma el ``QuerySet`` inicial de todas las entradas en la base de datos,
agrega un filtro, luego una exclusión, y luego otro filtro. El resultado final
es un ``QuerySet`` conteniendo todas las entradas con un título que empieza con
"What" que fueron publicadas entre Enero 1, 2005, y el día actual.

Es importante precisar aquí que los ``QuerySet`` son perezosos -- el acto de
crear un ``QuerySet`` no implica ninguna actividad en la base de datos. De
hecho, las tres líneas precedentes no hacen *ninguna* llamada a la base de
datos; puedes enlazar/encadenar filtros todo el día y Django no ejecutará
realmente la consulta hasta que el ``QuerySet`` sea *evaluado*.

Puedes evaluar un ``QuerySet`` en cualquiera de las siguientes formas:

* *Iterando*: Un ``QuerySet`` es iterable, y ejecuta su consulta en la base
  de datos la primera vez que iteras sobre el. Por ejemplo, el siguiente
  ``QuerySet`` no es evaluado hasta que se iterado sobre él en el bucle
  ``for``::

          qs = Entry.objects.filter(pub_date__year=2006)
          qs = qs.filter(headline__icontains="bill")
          for e in qs:
              print e.headline

  Esto imprime todos los títulos desde el 2006 que contienen "bill" pero
  genera solo un acceso a la base de datos.

* *Imprimiéndolo*: Un ``QuerySet`` es evaluado cuando ejecutas ``repr()``
  sobre el mismo. Esto es por conveniencia en el interprete interactivo
  Python, así puedes ver inmediatamente tus resultados cuando usas el API
  interactivamente.

* *Rebanado*: Según lo explicado en la próxima sección "`Limitando
  QuerySets`_", un ``QuerySet`` puede ser rebanado usando la sintaxis de
  rebanado de arreglos de Python. Usualmente el rebanar un ``QuerySet``
  retorna otro ``QuerySet`` (no evaluado), pero Django ejecutará la consulta
  a la base de datos si usas el parámetro "step" de la sintaxis de rebanado.

* *Convirtiendo a una lista*: Puedes forzar la evaluación de un ``QuerySet``
  ejecutando ``list()`` sobre el mismo, por ejemplo::

          >>> entry_list = list(Entry.objects.all())

Sin embargo, quedas advertido de que esto podría significar un gran
impacto en la memoria porque Django cargará cada elemento de la lista en
memoria.  En cambio, el iterar sobre un ``QuerySet`` sacará ventaja de tu
base de datos para cargar datos e inicializar objetos solo a medida que
vas necesitando los mismos.

.. admonition:: Los QuerySets filtrados son únicos

    Cada vez que refinas un ``QuerySet`` obtienes un nuevo ``QuerySet`` que no
    está de ninguna manera atado al `QuerySet`` anterior. Cada refinamiento
    crea un ``QuerySet`` separado y distinto que puede ser almacenado, usado
    y re-usado::

        q1 = Entry.objects.filter(headline__startswith="What")
        q2 = q1.exclude(pub_date__gte=datetime.now())
        q3 = q1.filter(pub_date__gte=datetime.now())

Estos tres ``QuerySets`` son separados. El primero es un ``QuerySet`` base
que contiene todas las entradas que contienen un título que empieza con
"What". El segundo es un sub-conjunto del primero, con un criterio adicional
que excluye los registros cuyo ``pub_date`` es mayor que el día de hoy. El
tercero es un sub-conjunto del primero, con un criterio adicional que
selecciona solo los registros cuyo ``pub_date`` es mayor que el día de hoy.
El ``QuerySet`` inicial (``q1``) no es afectado por el proceso de
refinamiento.

Limitando QuerySets
-------------------

Usa la sintaxis de rebanado de arreglos de Python para limitar tu ``QuerySet``
a un cierto número de resultados. Esto es equivalente a las clausulas de SQL
de ``LIMIT`` y ``OFFSET``.

Por ejemplo, esto retorna las primeras cinco entradas (``LIMIT 5``)::

    >>> Entry.objects.all()[:5]

Esto retorna las entradas desde la sexta hasta la décima
(``OFFSET 5 LIMIT 5``)::

    >>> Entry.objects.all()[5:10]

Generalmente, el rebanar un ``QuerySet`` retorna un nuevo ``QuerySet`` -- no
evalúa la consulta. Una excepción es si usas el parámetro "step" de la sintaxis
de rebanado de Python. Por ejemplo, esto realmente ejecutaría la consulta con el
objetivo de retornar una lista, objeto de por medio de los primeros diez::

    >>> Entry.objects.all()[:10:2]

Para recuperar *un* solo objeto en vez de una lista (por ej.
``SELECT foo FROM bar LIMIT 1``) usa un simple índice en vez de un rebanado.
Por ejemplo, esto retorna el primer ``Entry`` en la base de datos, después de
ordenar las entradas alfabéticamente por título::

    >>> Entry.objects.order_by('headline')[0]

y es equivalente a lo siguiente::

    >>> Entry.objects.order_by('headline')[0:1].get()

Nota, sin embargo, que el primero de estos generará ``IndexError`` mientras el
segundo generará ``DoesNotExist`` si ninguno de los objetos coincide con el
criterio dado.

Métodos de consulta que retornan nuevos QuerySets
-------------------------------------------------

Django provee una variedad de métodos de refinamiento de ``QuerySet`` que
modifican ya sea los tipos de resultados retornados por el ``QuerySet`` o la
forma como se ejecuta su consulta SQL.  Estos métodos se describen en las
secciones que siguen. Algunos de estos métodos reciben argumentos de patrones
de búsqueda, los cuales se discuten en detalle mas adelante.

filter(\*\*lookup)
~~~~~~~~~~~~~~~~~~

Retorna un nuevo ``QuerySet`` conteniendo objetos que son iguales a los
parámetros de búsqueda provistos.

exclude(\*\*kwargs)
~~~~~~~~~~~~~~~~~~~

Retorna un nuevo ``QuerySet`` conteniendo objetos que *no* son iguales a los
parámetros de búsqueda provistos.

order_by(\*campos)
~~~~~~~~~~~~~~~~~~

Por omisión, los resultados retornados por un ``QuerySet`` están ordenados por
la tupla de ordenamiento indicada por la opción ``ordering`` en los metadatos
del modelo (ver Apéndice B). Puedes sobrescribir esto para una consulta
particular usando el método ``order_by()``::

    >>> Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')

Este resultado será ordenado por ``pub_date`` de forma descendente, luego por
``headline`` de forma ascendente. El signo negativo en frente de ``"-pub_date"``
indica orden *descendiente*. Si el  ``-`` esta ausente se asume un orden
ascendente. Para ordenar aleatoriamente, usa ``"?"``, así::

    >>> Entry.objects.order_by('?')

distinct()
~~~~~~~~~~

Retorna un nuevo ``QuerySet`` que usa ``SELECT DISTINCT`` en su consulta SQL.
Esto elimina filas duplicadas en el resultado de la misma.

Por omisión, un ``QuerySet`` no eliminará filas duplicadas. En la práctica esto
raramente es un problema porque consultas simples como ``Blog.objects.all()`` no
introducen la posibilidad de registros duplicados.

Sin embargo, si tu consulta abarca múltiples tablas, es posible obtener
resultados duplicados cuando un ``QuerySet`` es evaluado. Esos son los casos en
los que usarías ``distinct()``.

values(\*campos)
~~~~~~~~~~~~~~~~

Retorna un ``QuerySet`` especial que evalúa a una lista de diccionarios en
lugar de objetos instancia de modelo. Cada uno de esos diccionarios representa
un objeto, con las las claves en correspondencia con los nombre de los atributos
de los objetos modelo::

    # This list contains a Blog object.
    >>> Blog.objects.filter(name__startswith='Beatles')
    [Beatles Blog]

    # This list contains a dictionary.
    >>> Blog.objects.filter(name__startswith='Beatles').values()
    [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]

``values()`` puede recibir argumentos posicionales opcionales, ``*campos``, los
cuales especifican los nombres de campos a los cuales debe limitarse el
``SELECT``. Si especificas los campos, cada diccionario contendrá solamente las
claves/valores de campos para los campos que especifiques. Si no especificas los
campos, cada diccionario contendrá una clave y un valor para todos los campos en
la table de base de datos::

    >>> Blog.objects.values()
    [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}],
    >>> Blog.objects.values('id', 'name')
    [{'id': 1, 'name': 'Beatles Blog'}]

Este método es útil cuando sabes de antemano que solo vas a necesitar valores de
un pequeño número de los campos disponibles y no necesitarás la funcionalidad de
un objeto instancia de modelo. Es más eficiente el seleccionar solamente los
campos que necesitas usar.

dates(campo, tipo, orden)
~~~~~~~~~~~~~~~~~~~~~~~~~

Retorna un ``QuerySet`` especial que evalúa a una lista de
objetos ``datetime.datetime`` que representan todas las fechas disponibles de un
cierto tipo en el contenido de la ``QuerySet``.

El argumento ``campo`` debe ser el nombre de un ``DateField`` o de un
``DateTimeField`` de tu modelo. El argumento ``tipo`` debe ser ya sea ``year``,
``month`` o ``day``. Cada objeto ``datetime.datetime`` en la lista de resultados
es truncado de acuerdo al ``tipo`` provisto:

* ``"year"`` retorna una lista de todos los valores de años distintos entre
  sí para el campo.

* ``"month"`` retorna una lista de todos los valores de años/mes distintos
  entre sí para el campo.

* ``"day"`` retorna una lista de todos los valores de años/mes/día distintos
  entre sí para el campo.

``orden``, cuyo valor por omisión es ``'ASC'``, debe ser ``'ASC'`` o
``'DESC'``. El mismo especifica cómo ordenar los resultados.

Aquí tenemos algunos ejemplos::

    >>> Entry.objects.dates('pub_date', 'year')
    [datetime.datetime(2005, 1, 1)]

    >>> Entry.objects.dates('pub_date', 'month')
    [datetime.datetime(2005, 2, 1), datetime.datetime(2005, 3, 1)]

    >>> Entry.objects.dates('pub_date', 'day')
    [datetime.datetime(2005, 2, 20), datetime.datetime(2005, 3, 20)]

    >>> Entry.objects.dates('pub_date', 'day', order='DESC')
    [datetime.datetime(2005, 3, 20), datetime.datetime(2005, 2, 20)]

    >>> Entry.objects.filter(headline__contains='Lennon').dates('pub_date', 'day')
    [datetime.datetime(2005, 3, 20)]

select_related()
~~~~~~~~~~~~~~~~

Retorna un ``QuerySet`` que seguirá automáticamente relaciones de clave foránea,
seleccionando esos datos adicionales de objetos relacionados cuando ejecuta su
consulta. Esto contribuye a la mejora de rendimiento que resulta en consultas
(aveces mucho) más grandes pero significan que el uso posterior de relaciones de
clave foránea no requerirán consultas a la base de datos.

Los siguientes ejemplos ilustran la diferencia entre búsquedas normales y
búsquedas ``select_related()``. Esta es una búsqueda normal::

    # Hits the database.
    >>> e = Entry.objects.get(id=5)

    # Hits the database again to get the related Blog object.
    >>> b = e.blog

Esta es una búsqueda ``select_related``::

    # Hits the database.
    >>> e = Entry.objects.select_related().get(id=5)

    # Doesn't hit the database, because e.blog has been prepopulated
    # in the previous query.
    >>> b = e.blog

``select_related()`` sigue claves foráneas tan lejos como le sea posible. Si
tienes los siguientes modelos::

    class City(models.Model):
        # ...

    class Person(models.Model):
        # ...
        hometown = models.ForeignKey(City)

    class Book(models.Model):
        # ...
        author = models.ForeignKey(Person)

entonces una llamada a ``Book.objects.select_related().get(id=4)`` colocará en
el cache la ``Person`` relacionada *y* la ``City`` relacionada::

    >>> b = Book.objects.select_related().get(id=4)
    >>> p = b.author         # Doesn't hit the database.
    >>> c = p.hometown       # Doesn't hit the database.

    >>> b = Book.objects.get(id=4) # No select_related() in this example.
    >>> p = b.author         # Hits the database.
    >>> c = p.hometown       # Hits the database.

Notar que ``select_related`` no sigue claves foráneas que tienen ``null=True``.

Usualmente, el usar ``select_related()`` puede mejorar muchísimo el desempeño
porque tu aplicación puede puede entonces evitar muchas llamadas a la base de
datos. Sin embargo, en siuaciones con conjuntos de relaciones profundamente
anidadas, ``select_related()`` puede en algunos casos terminar siguiendo
"demasiadas" relaciones y puede generar consultas tan grandes que terminan
siendo lentas.

extra()
~~~~~~~

A veces, el lenguaje de consulta de Django no puede expresar facilmente
cláusulas ``WHERE`` complejas.  Para estos casos extremos, Django provee un
modificador de ``QuerySet`` llamado ``extra()`` -- una forma de inyectar
cláusulas especificas dentro del SQL generado por un ``QuerySet``.

Por definición, estas consultas especiales pueden no ser portables entre los
distintos motores de bases de datos (debido a que estás escribiendo código SQL
explícito) y violan el principio DRY, así que deberías evitarlas de ser posible.

Se puede especificar uno o más de ``params``, ``select``, ``where``, o
``tables``.  Ninguno de los argumentos es obligatorio, pero deberías indicar al
menos uno.

El argumento ``select`` permite indicar campos adicionales en una cláusula de
``SELECT``.  Debe contener un diccionario que mapee nombres de atributo a
cláusulas SQL que se utilizarán para calcular el atributo en cuestión::

    >>> Entry.objects.extra(select={'is_recent': "pub_date > '2006-01-01'"})

Como resultado, cada objeto ``Entry`` tendrá en este caso un atributo adicional,
``is_recent``, un booleano que representará si el atributo ``pub_date`` del
entry es mayor que el 1 de Enero de 2006.

El siguiente ejemplo es más avanzado; realiza una subconsulta para darle a cada
objeto ``Blog`` resultante un atributo ``entry_count``, un entero que indica la
cantidad de objetos ``Entry`` asociados al blog::

    >>> subq = 'SELECT COUNT(*) FROM blog_entry WHERE blog_entry.blog_id = blog_blog.id'
    >>> Blog.objects.extra(select={'entry_count': subq})

(En este caso en particular, estamos aprovechando el hecho de que la consulta
ya contiene la tabla ``blog_blog`` en su cláusula ``FROM``.)

También es posible definir cláusulas ``WHERE`` explícitas -- quizás para
realizar joins implícitos -- usando el argumento ``where``.  Se puede agregar
tablas manualmente a la cláusula ``FROM`` del SQL usando el argumento
``tables``.

Tanto ``where`` como ``tables`` reciben una lista de cadenas.  Todos los
argumentos de ``where`` son unidos con AND a cualquier otro criterio de
búsqueda::

    >>> Entry.objects.extra(where=['id IN (3, 4, 5, 20)'])

Los parámetros ``select`` y ``where`` antes descriptos pueden utilizar los
comodines normales para bases de datos en Python: ``'%s'`` para indicar
parámetros que deberían ser escapados automáticamente por el motor de la base de
datos.  El argumento ``params`` es una lista de los parámetros que serán
utilizados para realizar la sustitución::

    >>> Entry.objects.extra(where=['headline=%s'], params=['Lennon'])

Siempre se debe utilizar ``params`` en vez de utilizar valores directamente en
``select`` o ``where`` ya que ``params`` asegura que los valores serán escapados
correctamente de acuerdo con tu motor de base de datos particular.

Este es un ejemplo de lo que está incorrecto::

    Entry.objects.extra(where=["headline='%s'" % name])

Este es un ejemplo de lo que es correcto::

    Entry.objects.extra(where=['headline=%s'], params=[name])

Metodos de ``QuerySet`` que no devuelven un ``QuerySet``
--------------------------------------------------------

Los métodos de ``QuerySet`` que se describen a continuación evaluan el
``QuerySet`` y devuelven algo *que no es* un ``QuerySet`` -- un objeto, un
valor, o algo así.

get(\*\*lookup)
~~~~~~~~~~~~~~~

Devuelve el objeto que matchee el parámetro de búsqueda provisto.  El
parámetro debe proveerse de la manera descripta en la sección
"`Patrones de búsqueda`_".  Este método levanta ``AssertionError`` si más de un
objecto concuerda con el patrón provisto.

Si no se encuentra ningún objeto que coincida con el patrón de búsqueda provisto
``get()`` levanta una excepción de ``DoesNotExist``.  Esta excepción es un
atributo de la clase del modelo, por ejemplo::

    >>> Entry.objects.get(id='foo') # levanta Entry.DoesNotExist

La excepción ``DoesNotExist`` hereda de
``django.core.exceptions.ObjectDoesNotExist``, así que puedes protegerte de
múltiples excepciones ``DoesNotExist``::

    >>> from django.core.exceptions import ObjectDoesNotExist
    >>> try:
    ...     e = Entry.objects.get(id=3)
    ...     b = Blog.objects.get(id=1)
    ... except ObjectDoesNotExist:
    ...     print "Either the entry or blog doesn't exist."

create(\*\*kwargs)
~~~~~~~~~~~~~~~~~~

Este método sirve para crear un objeto y guardarlo en un mismo paso.  Te
permite abreviar dos pasos comunes::

    >>> p = Person(first_name="Bruce", last_name="Springsteen")
    >>> p.save()

en una sola línea::

    >>> p = Person.objects.create(first_name="Bruce", last_name="Springsteen")

get_or_create(\*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~

Este método sirve para buscar un objeto y crearlo si no existe.  Devuelve una
tupla ``(object, created)``, donde ``object`` es el objecto encontrado o creado,
y ``created`` es un booleano que indica si el objeto fue creado.

Está pensado como un atajo para el caso de uso típico y es más que nada útil
para scripts de importación de datos, por ejemplo::

    try:
        obj = Person.objects.get(first_name='John', last_name='Lennon')
    except Person.DoesNotExist:
        obj = Person(first_name='John', last_name='Lennon', birthday=date(1940, 10, 9))
        obj.save()

Este patrón se vuelve inmanejable a medida que aumenta el número de campos en el
modelo.  El ejemplo anterior puede ser escrito usando ``get_or_create`` así::

    obj, created = Person.objects.get_or_create(
        first_name = 'John',
        last_name  = 'Lennon',
        defaults   = {'birthday': date(1940, 10, 9)}
    )

Cualquier argumento que se le pase a ``get_or_create()`` -- *excepto* el
argumento opcional ``defaults`` -- será utilizado en una llamada a ``get()``.
Si se encuentra un objecto, ``get_or_create`` devolverá una tupla con ese objeto
y ``False``.  Si *no* se encuentra un objeto, ``get_or_create()`` instanciará y
guardará un objeto nuevo, devolviendo una tupla con el nuevo objeto y ``True``.
El nuevo objeto será creado de acuerdo con el siguiente algoritmo::

    defaults = kwargs.pop('defaults', {})
    params = dict([(k, v) for k, v in kwargs.items() if '__' not in k])
    params.update(defaults)
    obj = self.model(**params)
    obj.save()

Esto es, se comienza con los argumentos que no sean ``'defaults'`` y que no
contengan doble guión bajo (lo cual indicaría una búsqueda no exacta).
Luego se le agrega el contenido de ``defaults``, sobreescribiendo cualquier
valor que ya estuviera asignado, y se usa el resultado como claves para
el constructor del modelo.

Si el modelo tiene un campo llamado ``defaults`` y es necesario usarlo para
una búsqueda exacta en ``get_or_create()``, simplemente hay que utilizar
``'defaults__exact'`` así::

    Foo.objects.get_or_create(
        defaults__exact = 'bar',
        defaults={'defaults': 'baz'}
    )

.. admonition:: Nota:

    Como ya se mencionó, ``get_or_create`` es utilizado más que nada en scripts
    que necesiten procesar datos y crear nuevos campos si los que existen no
    están disponibles.
    Si necesitas utilizar ``get_or_create()`` en una vista, por favor asegurate
    de utilizarlo solo en pedidos ``POST`` salvo que tengas una buena razón para
    no hacerlo.  Los pedidos ``GET`` no deberían afectar los datos de ninguna
    manera; se debe utilizar ``POST`` en cualquier pedido a una página que pueda
    tener como efecto secundario una modificación a tus datos.

count()
~~~~~~~

Devuelve un entero representando el número de objetos en la base de datos que
coincidan con el ``QuerySet``.  ``count()`` nunca levanta excepciones.  He aquí
un ejemplo::

    # Returns the total number of entries in the database.
    >>> Entry.objects.count()
    4

    # Returns the number of entries whose headline contains 'Lennon'
    >>> Entry.objects.filter(headline__contains='Lennon').count()
    1

``count()`` en el fondo realiza un ``SELECT COUNT(*)``, así que deberías siempre
utilizar ``count()`` en vez de cargar todos los registros en objetos Python y
luego invocar ``len()`` sobre el resultado.

Dependiendo de la base de datos que estés utilizando (e.g., PostgreSQL o MySQL),
``count()`` podría devolver un entero largo en vez de un entero normal de
Python.  Esto es una característica particular de la implementación subyacente
que no debería ser ningún problema en la vida real.

in_bulk(id_list)
~~~~~~~~~~~~~~~~

Este método toma una lista de claves primarias y devuelve un diccionario que
mapea cada clave primaria en una instancia con el ID dado, por ejemplo::

    >>> Blog.objects.in_bulk([1])
    {1: Beatles Blog}
    >>> Blog.objects.in_bulk([1, 2])
    {1: Beatles Blog, 2: Cheddar Talk}
    >>> Blog.objects.in_bulk([])
    {}

Si no se encuentra un objeto en la base para un ID en particular, este id no
aparecerá en el diccionario resultante.  Si le pasas una lista vacía a
``in_bulk()``, obtendrás un diccionario vacío.

latest(field_name=None)
~~~~~~~~~~~~~~~~~~~~~~~

Devuelve el último objeto de la tabla, ordenados por fecha, utilizando el campo
que se provea en el argumento ``field_name`` como fecha.  Este ejemplo devuelve
el ``Entry`` más reciente en la tabla, de acuerdo con el campo ``pub_date``::

    >>> Entry.objects.latest('pub_date')

Si el ``Meta`` de tu modelo especifica ``get_latest_by``, se puede omitir el
argumento ``field_name``.  Django utilizará el campo indicado en
``get_latest_by`` por defecto.

Al igual que ``get()``, ``latest()`` levanta ``DoesNotExist`` si no existe
un objeto con los parámetros provistos.

Patrones de búsqueda
====================

Los patrones de búsqueda son la manera en que se especifica la carne de una
cláusula ``WHERE`` de SQL.  Consisten de argumentos de palabra clave para los
métodos ``filter()``, ``exclude()`` y ``get()`` de ``QuerySet``.

Los parámetros básicos de búsqueda toman la forma de
``campo__tipodebusqueda=valor`` (notar el doble guión bajo).  Por ejemplo::

    >>> Entry.objects.filter(pub_date__lte='2006-01-01')

se traduce (aproximadamente) al siguiente comando SQL::

    SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';

Si se suministra un argumento de palabra clave inválido, la función levantará
una excepción de ``TypeError``.

A continuación se listan los tipos de búsqueda que existen.

exact
-----

Realiza una búsqueda por coincidencias exactas::

    >>> Entry.objects.get(headline__exact="Man bites dog")

Esto busca objetos que tengan en el campo headline la frase exacta
"Man bites dog".

Si no se suministra un tipo de búsqueda -- O sea, si tu argumento de palabra
clave no contiene un doble guión bajo -- el tipo de búsqueda se asume como
``exact``.

Por ejemplo, las siguientes dos sentencias son equivalentes::

    >>> Blog.objects.get(id__exact=14) # Explicit form
    >>> Blog.objects.get(id=14) # __exact is implied

Esto es por conveniencia, dado que las búsquedas con tipo de búsqueda ``exact``
son las más frecuentes.

iexact
------

Realiza una búsqueda por coincidencias exactas sin distinguir mayúsculas de
minúsculas::

    >>> Blog.objects.get(name__iexact='beatles blog')

Traerá objetos con nombre ``'Beatles Blog'``, ``'beatles blog'``,
``'BeAtLes BLoG'``, etcétera.

contains
--------

Realiza una búsqueda de subcadenas, distinguiendo mayúsculas y minúsculas::

    Entry.objects.get(headline__contains='Lennon')

Esto coincidirá con el titular ``'Today Lennon honored'`` pero no con
``'today lennon honored'``.

SQLite no admite sentencias ``LIKE`` distinguiendo mayúsculas y minúsculas;
cuando se utiliza SQLite, ``contains`` se comporta como ``icontains``.

.. admonition:: Escapado de porciento y guión bajo en sentencias ``LIKE``

    Los patrones de búsqueda que resulten en sentencias SQL ``LIKE``
    (``iexact``, ``contains``, ``icontains``, ``startswith``, ``istartswith``,
    ``endswith``, y ``iendswith``) escaparán automáticamente los dos caracteres
    especiales utilizados en sentencias ``LIKE`` -- el porciento y el guión
    bajo.  (En una sentencia ``LIKE``, el símbolo de porciento indica una
    secuencia de caracteres cualesquiera, y el guión bajo indica un solo
    caracter cualquiera).

    Esto significa que las cosas deberían funcionar de manera intuitiva, por
    que la abstracción funciona bien.  Por ejemplo, para obtener todos los
    Entries que contengan un símbolo de porciento, simplemente hace falta
    utilizar el símbolo de porcentaje como cualquier otro caracter::

        Entry.objects.filter(headline__contains='%')

    Django se hace cargo del escapado.  El SQL resultante será algo similar a
    esto::

        SELECT ... WHERE headline LIKE '%\%%';

Lo mismo vale para el guión bajo.  Tanto el símbolo de porcentaje como el
guión bajo se deberían manejar de manera transparente.


icontains
---------

Realiza una búsqueda de subcadenas, sin distinguir mayúsculas y minúsculas::

    >>> Entry.objects.get(headline__icontains='Lennon')

A diferencia de ``contains``, ``icontains`` *sí* trerá ``today lennon honored``.

gt, gte, lt, and lte
--------------------

Estos representan los operadores de mayor a, mayor o igual a, menor a, y
menor o igual a, respectivamente::

    >>> Entry.objects.filter(id__gt=4)
    >>> Entry.objects.filter(id__lt=15)
    >>> Entry.objects.filter(id__gte=1)

Estas consultas devuelven cualquier objeto con un ID mayor a 4, un ID menor a
15, y un ID mayor o igual a 1, respectivamente.

Por lo general estos operadores se utilizarán con campos numéricos.  Se debe
tener cuidado con los campos de caracteres, ya que el orden no siempre es el que
uno se esperaría (i.e., la cadena "4" resulta ser *mayor* que la cadena "10").

in
--

Aplica un filtro para encontrar valores en una lista dada::

    Entry.objects.filter(id__in=[1, 3, 4])

Esto devolverá todos los objetos que tengan un ID de 1, 3 o 4.

startswith
----------

Busca coincidencias de prefijos distinguiendo mayúsculas y minúsculas::

    >>> Entry.objects.filter(headline__startswith='Will')

Esto encontrará los titulares "Will he run?" y "Willbur named judge", pero no
"Who is Will?" o "will found in crypt".

istartswith
-----------

Realiza una búsqueda por prefijos, sin distinguir mayúsculas y minúsculas::

    >>> Entry.objects.filter(headline__istartswith='will')

Esto devolverá los titulares "Will he run?", "Willbur named judge", y
"will found in crypt", pero no "Who is Will?"

endswith and iendswith
----------------------

Realiza búsqueda de sufijos, distinguiendo y sin distinguir mayúsculas de
minúsculas, respectivamente::

    >>> Entry.objects.filter(headline__endswith='cats')
    >>> Entry.objects.filter(headline__iendswith='cats')

range
-----

Realiza una búsqueda por rango::

    >>> start_date = datetime.date(2005, 1, 1)
    >>> end_date = datetime.date(2005, 3, 31)
    >>> Entry.objects.filter(pub_date__range=(start_date, end_date))

Se puede utilizar ``range`` en cualquier lugar donde podrías utilizar
``BETWEEN`` en SQL -- para fechas, números, e incluso cadenas de caracteres.

year, month, and day
--------------------

Para campos ``date`` y ``datetime``, realiza búsqueda exacta por año, mes o
día::

    # Búsqueda por año
    >>>Entry.objects.filter(pub_date__year=2005)

    # Búsqueda por mes -- toma enteros
    >>> Entry.objects.filter(pub_date__month=12)

    # Búsqueda por día
    >>> Entry.objects.filter(pub_date__day=3)

    # Combinación: devuelve todas las entradas de Navidad de cualquier año
    >>> Entry.objects.filter(pub_date__month=12, pub_date__day=25)

isnull
------

Toma valores ``True`` o ``False``, que corresponderán a consultas SQL de
``IS NULL``y ``IS NOT NULL``, respectivamente::

    >>> Entry.objects.filter(pub_date__isnull=True)

.. admonition:: ``__isnull=True`` vs. ``__exact=None``

    Hay una diferencia importante entre ``__isnull=True`` y ``__exact=None``.
    ``__exact=None`` *siempre* devolverá como resultado un conjunto vacío, ya
    que SQL requiere que ningún valor sea igual a ``NULL``.
    ``__isnull`` determina si el campo actualmente contiene un valor ``NULL``
    sin realizar la comparación.

search
------

Un booleano que realiza búsquedas ``full-text``, que aprovecha el indexado
``full-text``.  Esto es como ``contains`` pero significativamente más rápido
debido al indexado ``full-text``.

Nótese que este tipo de búsqueda sólo está disponible en MySQL y requiere de
manipulación directa de la base de datos para agregar el índice ``full-text``.

El patrón de búsqueda pk
------------------------

Por conveniencia, Django provee un patrón de búsqueda ``pk``, que realiza una
búsqueda sobre la clave primaria del modelo (``pk`` por ``primary key``, del
inglés).

En el modelo de ejemplo ``Blog``, la clave primaria es el campo ``id``, así que
estas sentencias serían equivalentes::

    >>> Blog.objects.get(id__exact=14) # Forma explícita
    >>> Blog.objects.get(id=14) # __exact implícito
    >>> Blog.objects.get(pk=14) # pk implica id__exact

El uso de ``pk`` no se limita a búsquedas ``__exact`` -- cualquier patrón de
búsqueda puede ser combinado con ``pk`` para realizar una búsqueda sobre la
clave primaria de un modelo::

    # Buscar entradas en blogs con id 1, 4, o 7
    >>> Blog.objects.filter(pk__in=[1,4,7])

    # Buscar entradas en blogs con id > 14
    >>> Blog.objects.filter(pk__gt=14)

Las búsquedas ``pk`` también funcionan con joins.  Por ejemplo, estas tres
sentencias son equivalentes::

    >>> Entry.objects.filter(blog__id__exact=3) # Forma explícita
    >>> Entry.objects.filter(blog__id=3) # __exact implícito
    >>> Entry.objects.filter(blog__pk=3) # __pk implica __id__exact

Búsquedas complejas con Objetos Q
=================================

Los argumentos de palabras clave en las búsquedas -- en ``filter()`` por
ejemplo -- son unidos con AND.  Si necesitas realizar búsquedas más complejas
(e.g., búsquedas con sentencias ``OR``), puedes utilizar objetos ``Q``.

Un objeto ``Q`` (``django.db.models.Q``) es un objeto que se utiliza para
encapsular una colección de argumentos de palabra clave.  Estos argumentos de
palabra clave son especificados como se indica en la sección
"`Patrones de búsqueda`_".

Por ejemplo, este objeto ``Q`` encapsula una consulta con un único ``LIKE``:

    Q(question__startswith='What')

Los objetos ``Q`` pueden ser combinados utilizando los operadores ``&`` y ``|``.
Cuando se utiliza un operador sobre dos objetos, se obtiene un nuevo objeto
``Q``.  Por ejemplo, un ``OR`` de dos consultas ``question__startswith`` sería::

    Q(question__startswith='Who') | Q(question__startswith='What')

Esto será equivalente a la siguiente cláusula ``WHERE`` en SQL::

    WHERE question LIKE 'Who%' OR question LIKE 'What%'

Puede componer sentencias de complejidad arbitraria combinando objetos ``Q`` con
los operadores ``&`` y ``|``.  También se pueden utilizar paréntesis para
agrupar.

Cualquier función de búsqueda que tome argumentos de palabra clave (e.g.,
``filter()``, ``exclude()``, ``get()``) puede recibir también uno o más objetos
``Q`` como argumento posicional (no nombrado).  Si se proveen multiples objetos
``Q`` como argumentos a una función de búsqueda, los argumentos serán unidos
con AND, por ejemplo::

    Poll.objects.get(
        Q(question__startswith='Who'),
        Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
    )

se traduce aproximadamente al siguiente SQL::

    SELECT * from polls WHERE question LIKE 'Who%'
        AND (pub_date = '2005-05-02' OR pub_date = '2005-05-06')

Las funciones de búsqueda pueden además mezclar el uso de objetos ``Q`` y de
argumentos de palabra clave.  Todos los argumentos provistos a una función de
búsqueda (sean argumentos de palabra clave u objetos ``Q``) son unidos con AND.
Sin embargo, si se provee un objeto ``Q`` debe preceder la definición de
todos los argumentos de palabra clave.  Por ejemplo, lo siguiente::

    Poll.objects.get(
        Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)),
        question__startswith='Who')

es una consulta válida, equivalente al ejemplo anterior, pero esto::

    # CONSULTA INVALIDA
    Poll.objects.get(
        question__startswith='Who',
        Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)))

no es válido.

Hay algunos ejemplos disponibles online en
http://www.djangoproject.com/documentation/0.96/models/or_lookups/ .

Objetos Relacionados
====================

Cuando defines una relación en un modelo (i.e. un ``ForeignKey``,
``OneToOneField``, or ``ManyToManyField``), las instancias de ese modelo
tendrán una API conveniente para acceder a estos objetos relacionados.

Por ejemplo, si ``e`` es un objeto ``Entry``, puede acceder a su ``Blog``
asociado accediendo al atributo ``blog``, esto es ``e.blog``.

Django también crea una API para acceder al "otro" lado de la relación --
el vínculo del modelo relacionado al modelo que define la relación.
Por ejemplo, si ``b`` es un objeto ``Blog``, tiene acceso a la lista de todos
los objetos ``Entry`` a través del atributo ``entry_set``:
``b.entry_set.all()``.

Todos los ejemplos en esta sección utilizan los modelos de ejemplo ``Blog``,
``Author`` y ``Entry`` que se definen al principio de esta sección.

Consultas Que Cruzan Relaciones
-------------------------------

Django ofrece un mecanismo poderoso e intuitivo para "seguir" relaciones cuando
se realizan búsquedas, haciéndose cargo de los ``JOIN``\s de SQL de manera
automática.  Para cruzar una relación simplemente hace falta utilizar el nombre
de campo de los campos relacionados entre modelos, separados por dos guiones
bajos, hasta que llegues al campo que necesitabas.

Este ejemplo busca todos los objetos ``Entry`` que tengan un ``Blog`` cuyo
``nombre`` sea ``'Beatles Blog'``::

    >>> Entry.objects.filter(blog__name__exact='Beatles Blog')

Este camino puede ser tan largo como quieras.

También Funciona en la otra dirección.  Para referirse a una relación "inversa",
simplemente hay que utilizar el nombre en minúsculas del modelo.

Este ejemplo busca todos los objetos ``Blog`` que tengan al menos un ``Entry``
cuyo ``headline`` contenga ``'Lennon'``::

    >>> Blog.objects.filter(entry__headline__contains='Lennon')

Relaciones de Clave Foránea
---------------------------

Si un modelo contiene un ``ForeignKey``, las instancias de ese modelo tendrán
acceso al objeto relacionado (foráneo) vía un simple atributo del modelo, por
ejemplo::

    e = Entry.objects.get(id=2)
    e.blog # Devuelve el objeto Blog relacionado

Se puede acceder y asignar el valor de la clave foránea vía el atributo.  Como
sería de esperar, los cambios a la clave foránea no se guardan en el modelo
hasta que invoques el método ``save()``, por ejemplo::

    e = Entry.objects.get(id=2)
    e.blog = some_blog
    e.save()

Si un campo ``ForeignKey`` tiene la opción ``null=True`` seteada (i.e. permite
valores ``NULL``), se le puede asignar ``None``::

    e = Entry.objects.get(id=2)
    e.blog = None
    e.save() # "UPDATE blog_entry SET blog_id = NULL ...;"

El acceso a relaciones uno-a-muchos se almacena la primera vez que se accede
al objeto relacionado.  Cualquier acceso subsiguiente a la clave foránea del
mismo objeto son cacheadas, por ejemplo::

    e = Entry.objects.get(id=2)
    print e.blog  # Busca el Blog asociado en la base de datos.
    print e.blog  # No va a la base de datos; usa la versión cacheada.

Notar que el método de ``QuerySet`` ``select_related()`` busca inmediatamente
todos los objetos de relaciones uno-a-muchos de la instancia::

    e = Entry.objects.select_related().get(id=2)
    print e.blog  # No va a la base de datos; usa la versión cacheada.
    print e.blog  # No va a la base de datos; usa la versión cacheada.

``select_related()`` está documentada en la sección
"`Métodos de consulta que retornan nuevos QuerySets`_".

Relaciones de Clave Foreánea "Inversas"
---------------------------------------

Las relaciones de clave foránea son automáticamente simétricas -- se infiere
una relación inversa de la presencia de un campo ``ForeignKey`` que apunte a
otro modelo.

Si un modelo tiene una ``ForeignKey``, las instancias del modelo de la clave
foránea tendrán acceso a un ``Manager`` que devuelve todas las instancias del
primer modelo.  Por defecto, este ``Manager`` se llama ``FOO_set``, donde
``FOO`` es el nombre modelo que contiene la clave foránea, todo en minúsculas.
Este ``Manager`` devuelve ``QuerySets``, que pueden ser filtradas y manipuladas
como se describe en la sección "`Recuperando objetos`_".

Aquí se muestra un ejemplo::

    b = Blog.objects.get(id=1)
    b.entry_set.all() # Encontrar todos los objetos Entry relacionados a b.

    # b.entry_set es un Manager que devuelve QuerySets.
    b.entry_set.filter(headline__contains='Lennon')
    b.entry_set.count()

Se puede cambiar el nombre del atributo ``FOO_set`` indicando el parámetro
``related_name`` en la definición del ``ForeignKey()``.  Por ejemplo, si el
modelo ``Entry`` fuera cambiado por
``blog = ForeignKey(Blog, related_name='entries')``, el ejemplo anterior pasaría
a ser así::

    b = Blog.objects.get(id=1)
    b.entries.all() # Encontrar todos los objetos Entry relacionados a b.

    # b.entries es un Manager que devuelve QuerySets.
    b.entries.filter(headline__contains='Lennon')
    b.entries.count()

No se puede acceder al ``Manager`` de ``ForeignKey`` inverso desde la clase
misma; debe ser accedido desde una instancia::

    Blog.entry_set # Raises AttributeError: "Manager must be accessed via instance".

Además de los metodos de ``QuerySet`` definidos en la sección
"`Recuperando Objetos`_", el ``Manager`` de ``ForeignKey`` tiene los siguientes
métodos adicionales:


* ``add(obj1, obj2, ...)``: Agrega los objetos del modelo indicado al
  conjunto de objetos relacionados, por ejemplo::

          b = Blog.objects.get(id=1)
          e = Entry.objects.get(id=234)
          b.entry_set.add(e) # Associates Entry e with Blog b.

* ``create(**kwargs)``: Crea un nuevo objeto, lo guarda, y lo deja en el
  conjunto de objetos relacionados.  Devuelve el objeto recién creado::

          b = Blog.objects.get(id=1)
          e = b.entry_set.create(headline='Hello', body_text='Hi', pub_date=datetime.date(2005, 1, 1))
          # No hace falta llamar a e.save() acá -- ya ha sido guardado

  Esto es equivalente a (pero más simple que) lo siguiente::

          b = Blog.objects.get(id=1)
          e = Entry(blog=b, headline='Hello', body_text='Hi', pub_date=datetime.date(2005, 1, 1))
          e.save()

   Notar que no es necesario especificar el argumento de palabra clave
   correspondiente al modelo que define la relación.  En el ejemplo anterior,
   no le pasamos el parámetro ``blog`` a ``create()``.  Django deduce que el
   campo ``blog`` del nuevo ``Entry``  debería ser ``b``.

* ``remove(obj1, obj2, ...)``: Quita los objetos indicados del conjunto de
  objetos relacionados::

          b = Blog.objects.get(id=1)
          e = Entry.objects.get(id=234)
          b.entry_set.remove(e) # Desasociar al Entry e del Blog b.

   Para evitar inconsistencias en la base de datos, este método sólo existe
   para objetos ``ForeignKey`` donde ``null=True``.  Si el campo relacionado
   no puede pasar ser ``None`` (``NULL``), entonces un objeto no puede ser
   quitado de una relación sin ser agregado a otra.  En el ejemplo anterior,
   el quitar a ``e`` de ``b.entry_set()`` es equivalente a hacer
   ``e.blog = None``, y dado que la definición del campo ``ForeignKey``
   ``blog`` (en el modelo ``Entry``) no indica ``null=True``, esto es una
   acción inválida.

* ``clear()``: Quita todos los objetos del conjunto de objetos
  relacionados::

          b = Blog.objects.get(id=1)
          b.entry_set.clear()

   Notar que esto no borra los objetos relacionados -- simplemente los
   desasocia.

   Al igual que ``remove()``, ``clear`` solo está disponible para campos
   ``ForeignKey`` donde ``null=True``.

Para asignar todos los miembros de un conjunto relacionado en un solo paso,
simplemente se le asigna al conjunto un objeto iterable, por ejemplo::

    b = Blog.objects.get(id=1)
    b.entry_set = [e1, e2]

Si el método ``clear()`` está definido, todos los objetos pre-existentes serán
quitados del ``entry_set`` antes de que todos los objetos en el iterable (en
este caso, la lista) sean agregados al conjunto.  Si el método ``clear()`` *no*
está disponible, todos los objetos del iterable son agregados al conjunto sin
quitar antes los objetos pre-existentes.

Todas las operaciones "inversas" definidas en esta sección tienen efectos
inmediatos en la base de datos.  Toda creación, borradura y agregado son
inmediata y automáticamente grabados en la base de datos.

Relaciones muchos-a-muchos
--------------------------

Ambos extremos de las relaciones muchos-a-muchos obtienen una API de acceso
automáticamente.  La API funciona igual que las funciones "inversas" de las
relaciones uno-a-muchos (descriptas en la sección anterior).

La única diferencia es el nombrado de los atributos: el modelo que define el
campo ``ManyToManyField`` usa el nombre del atributo del campo mismo, mientras
que el modelo "inverso" utiliza el nombre del modelo original, en minúsculas,
con el sufijo ``'_set'`` (tal como lo hacen las relaciones uno-a-muchos).

Un ejemplo de esto lo hará más fácil de entender::

    e = Entry.objects.get(id=3)
    e.authors.all() # Devuelve todos los objetos Author para este Entry.
    e.authors.count()
    e.authors.filter(name__contains='John')

    a = Author.objects.get(id=5)
    a.entry_set.all() # Devuelve todos los obejtos Entry para este Author.

Al igual que los campos ``ForeignKey``, los ``ManyToManyField`` pueden indicar
un ``related_name``.  En el ejemplo anterior, si el campo ``ManyToManyField``
en el modelo ``Entry`` indicara ``related_name='entries'``, cualquier instancia
de ``Author`` tendría un atributo ``entries`` en vez de ``entry_set``.

.. admonition:: Cómo son posibles las relaciones inversas?

    El mapeador objeto-relacional requiere que definas relaciones en ambos
    extremos.  Los desarrolladores Django creen que esto es una violación del
    principio DRY (Don't Repeat Yourself), así que Django sólo te exige que
    definas la relación en uno de los extremos.  Pero cómo es esto posible, dado
    que una clase modelo no sabe qué otros modelos se relacionan con él hasta
    que los otros modelos sean cargados?

    La respuesta yace en la variable ``INSTALLED_APPS``.  La primera vez que
    se carga cualquier modelo, Django itera sobre todos los modelos en
    ``INSTALLED_APPS`` y crea las relaciones inversas en memoria como sea
    necesario.  Esencialmente, una de las funciones de ``INSTALLES_APPS`` es
    indicarle a Django el dominio completo de modelos que se utiliza.

Consultas que Abarcan Objetos Relacionados
------------------------------------------

Las consultas que involucran objetos relacionados siguen las mismas reglas que
las consultas que involucran campos normales.  Cuando se indica el valor que
se requiere en una búsqueda, se puede utilizar tanto una instancia del modelo
o bien el valor de la clave primaria del objeto.

Por ejemplo, si ``b`` es un objeto ``Blog`` con ``id=5``, las tres siguientes
consultas son idénticas::

    Entry.objects.filter(blog=b) # Query using object instance
    Entry.objects.filter(blog=b.id) # Query using id from instance
    Entry.objects.filter(blog=5) # Query using id directly

Borrando Objectos
=================

El métodos para borrar se llama ``delete()``.  Este método inmediatamente borra
el objeto y no tiene ningún valor de retorno::

    e.delete()

También se puede borrar objetos en grupo.  Todo objeto ``QuerySet`` tiene un
método ``delete()`` que borra todos los miembros de ese ``QuerySet``.  Por
ejemplo, esto borra todos los objetos ``Entry`` que tengan un año de
``pub_date`` igual a 2005::

    Entry.objects.filter(pub_date__year=2005).delete()

Cuando Django borra un objeto, emula el comportamiento de la restricción de SQL
``ON DELETE CASCADE`` -- en otras palabras, todos los objetos que tengan una
clave foránea que apunte al objeto que está siendo borrado serán borrados
también, por ejemplo::

    b = Blog.objects.get(pk=1)
    # Esto borra el Blog y todos sus objetos Entry.
    b.delete()

Notar que ``delete()`` es el único método de ``QuerySet`` que no está expuesto
en el ``Manager`` mismo.  Esto es un mecanismo de seguridad para evitar que
accidentalmente solicites ``Entry.objects.delete()`` y borres *todos* los Entry.
Si *realmente* quieres borrar todos los objetos, hay que pedirlo explícitamente
al conjunto completo de objetos::

    Entry.objects.all().delete()

Métodos de Instancia Adicionales
================================

Además de ``save()`` y ``delete()``, un objeto modelo puede tener
cualquiera o todos de los siguientes métodos.

get_FOO_display()
-----------------

Por cada campo que indica la opción ``choices``, el objeto tendrá un método
``get_FOO_display()``, donde ``FOO`` es el nombre del campo.  Este método
devuelve el valor "humanamente legible" del campo.  Por ejemplo, en el
siguiente modelo::

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    class Person(models.Model):
        name = models.CharField(max_length=20)
        gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

cada instancia de ``Person`` tendrá un método ``get_gender_display``::

    >>> p = Person(name='John', gender='M')
    >>> p.save()
    >>> p.gender
    'M'
    >>> p.get_gender_display()
    'Male'

get_next_by_FOO(\**kwargs) y get_previous_by_FOO(\**kwargs)
-----------------------------------------------------------

Por cada campo ``DateField`` y ``DateTimeField`` que no tenga ``null=True``,
el objeto tendrá dos métodos ``get_next_by_FOO()`` y ``get_previous_by_FOO()``,
donde ``FOO`` es el nombre del campo.  Estos métodos devuelven el objeto
siguiente y anterior en orden cronológico respecto del campo en cuestión,
respectivamente, levantando la excepción ``DoesNotExist`` cuando no exista tal
objeto.

Ambos métodos aceptan argumentos de palabra clave opcionales, que deberían ser
de la forma descripta en la sección "`Patrones de búsqueda`_".

Notar que en el caso de valores de fecha idénticos, estos métodos utilizarán
el ID como un chequeo secundario.  Esto garantiza que no se saltearán registros
ni aparecerán duplicados.  Hay un ejemplo completo en los ejemplos de la API de
búsqueda, en
http://www.djangoproject.com/documentation/0.96/models/lookup/.

get_FOO_filename()
------------------

Todo campo ``FileField`` le dará al objeto un método ``get_FOO_filename()``,
donde ``FOO`` es el nombre del campo.  Esto devuelve el nombre de archivo
completo en el sistema de archivos, de acuerdo con la variable ``MEDIA_ROOT``.

Notar que el campo ``ImageField`` es técnicamente una subclase de ``FileField``,
así que todo modelo que tenga un campo ``ImageField`` obtendrá también este
método.

get_FOO_url()
-------------

Por todo campo ``FileField`` el objeto tendrá un método ``get_FOO_url()``,
donde ``FOO`` es el nombre del campo.  Este método devuelve la URL al archivo,
de acuerdo con tu variable ``MEDIA_URL``.  Si esta variable está vacía, el
método devolverá una cadena vacía.

get_FOO_size()
--------------

Por cada campo ``FileField`` el objeto tendrá un método ``get_FOO_size()``,
donde ``FOO`` es el nombre del campo.  Este método devuelve el tamaño del
archivo, en bytes.  (La implementación de este método utiliza
``os.path.getsize``.)

save_FOO_file(filename, raw_contents)
-------------------------------------

Por cada campo ``FileField``, el objeto tendrá un método ``save_FOO_file()``,
donde ``FOO`` es el nombre del campo.  Este método guarda el archivo en el
sistema de archivos, utilizando el nombre dado.  Si un archivo con el nombre
dado ya existe, Django le agrega guiones bajos al final del nombre de archivo
(pero antes de la extensión) hasta que el nombre de archivos esté disponible.

get_FOO_height() and get_FOO_width()
------------------------------------

Por cada campo ``ImageField``, el objeto obtendrá dos métodos,
``get_FOO_height()`` y ``get_FOO_width()``, donde ``FOO`` es el nombre del
campo.  Estos métodos devuelven el alto y el ancho (respectivamente) de la
imagen, en pixeles, como un entero.

Atajos (Shortcuts)
==================

A medida que desarrolles tus vistas, descubrirás una serie de modismos en la
manera de utilizar la API de la base de datos.  Django codifica algunos de estos
modismos como atajos que pueden ser utilizados par simplificar el proceso de
escribir vistas.  Estas funciones se pueden hallar en el módulo
``django.shortcuts``.

get_object_or_404()
-------------------

Un modismo frecuente es llamar a ``get()`` y levantar un ``Http404`` si el
objeto no existe.  Este modismo es capturado en la función
``get_object_or_404()``.
Esta funcion toma un modelo Django como su primer argumento, y una cantidad
arbitraria de argumentos de palabra clave, que le pasa al método ``get()`` del
``Manager`` por defecto del modelo.  Luego levanta un ``Http404`` si el objeto
no existe, por ejemplo::

    # Get the Entry with a primary key of 3
    e = get_object_or_404(Entry, pk=3)

Cuando se le pasa un modelo a esta función, se utiliza el ``Manager`` por
defecto para ejecutar la consulta ``get()`` subyacente.  Si no quieres que se
utilice el manager por defecto, o si quiere buscar en una lista de objetos
relacionados, se le puede pasar a ``get_object_or_404()`` un objeto ``Manager``
en vez::

    # Get the author of blog instance e with a name of 'Fred'
    a = get_object_or_404(e.authors, name='Fred')

    # Use a custom manager 'recent_entries' in the search for an
    # entry with a primary key of 3
    e = get_object_or_404(Entry.recent_entries, pk=3)

get_list_or_404()
-----------------

``get_list_or_404()`` se comporta igual que ``get_object_or_404()``,
salvo porque llama a ``filter()`` en vez de a ``get()``.  Levanta un
``Http404`` si la lista resulta vacía.

Utilizando SQL Crudo
====================

Si te encuentras necesitando escribir una consulta SQL que es demasiado compleja
para manejarlo con el mapeador de base de datos de Django, todavía puede optar
por escribir la sentencia directamente en SQL crudo.

La forma preferida para hacer esto es dándole a tu modelo métodos personalizados
o métodos de ``Manager`` personalizados que realicen las consultas.  Aunque no
exista ningún requisito en Django que *exija* que las consultas a la base de
datos vivan en la capa del modelo, esta implementación pone a toda tu lógica de
acceso a los datos en un mismo lugar, lo cual es una idea astuta desde el punto
de vista de organización del código.  Por más instrucciones, véase el
Apéndice B..

Finalmente, es importante notar que la capa de base de datos de Django es
meramente una interfaz a tu base de datos.  Puedes acceder a la base de datos
utilizando otras herramientas, lenguajes de programación o frameworks de bases
de datos -- No hay nada específicamente de Django acerca de tu base de datos.
