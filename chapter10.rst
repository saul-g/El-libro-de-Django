==============================
Capitulo 10: Modelos Avanzados
==============================

En el capítulo 5, presentamos una pequeña introducción a la capa de la base de
datos -- la cual define los modelos de la base de datos y la forma de usar la
API para crear, recuperar, actualizar y borrar registros. En este capítulo,
nos adentraremos un poco mas, en las **características avanzadas de la capa de
modelos**.

Objetos Relacionados
====================

Recuerdas el modelo que creamos en el :doc:`capítulo 5<chapter05>`,:

.. snippet:: python
    :filename: libros/models.py

    from django.db import models

    class Editor(models.Model):
        nombre = models.CharField(max_length=30)
        direccion = models.CharField(max_length=5)
        ciudad = models.CharField(max_length=60)
        estado = models.CharField(max_length=30)
        pais = models.CharField(max_length=5)
        website = models.URLField()

        def __str__(self):            # __unicode__ en Python 2
            return self.nombre

    class Autor(models.Model):
        nombre = models.CharField(max_length=30)
        apellidos = models.CharField(max_length=40)
        email = models.EmailField()

        def __str__(self):            # __unicode__ en Python 2
            return '%s %s' % (self.nombre, apellidos)

    class Libro(models.Model):
        titulo = models.CharField(max_length=100)
        autores = models.ManyToManyField(Author)
        editor = models.ForeignKey(Editor)
        fecha_publicacion = models.DateField()

        def __str__(self):#           # __unicode__ en Python 2
            return self.titulo

Como explicamos en el :doc:`capítulo 5<chapter05>`, para acceder directamente
al valor de un determinado campo  en la base de datos, es necesario usar
los atributos del objeto. Por ejemplo, para determinar el titulo de un libro
con un ID 5 (ID: El identificador o clave primaria), hacemos lo siguiente::

    >>> from biblioteca.models import Libro
    >>> b = Libro.objects.get(id=5)
    >>> b.titulo
    u'The Django Libro'

Pero una cosa que no mencionamos previamente, fueron las relaciones entre
objetos -- Nos referimos a los campos expresados como  ``ForeignKey`` o
``ManyToManyField``, los cuales actúan de modo ligeramente diferente.

Accediendo a valores en claves foráneas
---------------------------------------

Cuando accedes a un campo del tipo  ``ForeignKey`` (Relación foránea, del tipo
muchos a uno) Puedes obtener el modelo del objeto relacionado, de la
siguiente forma::

    >>> from biblioteca.models import Editor, Libro
    >>> b = Libro.objects.get(id=5)
    >>> b.editor
    <Publisher: Apress Publishing>
    >>> b.editor.website
    u'http://www.apress.com/'

Como habras notado, la forma en que trabajan los campos ``ForeignKey``, es
ligeramente diferente, debido a la naturaleza poco simétrica de la relación.
Por ejemplo para conseguir una lista de libros de un editor en especifico, usa
``editores.libro_set.all()``,  así::

    >>> p = Editor.objects.get(nombre='Apress Publishing')
    >>> p.libro_set.all()
    [<Libro: The Django Libro>, <Libro: Dive Into Python>, ...]

Detrás de escena, ``libro_set`` es solo un ``QuerySet`` (el cual cubrimos en el
capitulo 5) y puede ser filtrado y rebanado, tal como cualquier otro ``QuerySet``.
Por ejemplo::

    >>> p = Editor.objects.get(nombre='Apress Publishing')
    >>> p.libro_set.filter(titulo__icontains='django')
    [<Libro: The Django Libro>, <Libro: Pro Django>]

El nombre del atributo ``libro_set`` es generado agregando el nombre del modelo
en  minúsculas a  ``_set``.


Accediendo a valores muchos a muchos
------------------------------------

Los valores muchos a muchos (Many-to-many) trabajan de forma parecida a
los valores en campos foraneos, a menos que tratemos con valores ``QuerySet``
en lugar de  instancias del modelo. Por ejemplo, este es la
forma que se muestran los autores de un libro.::

    >>> b = Libro.objects.get(id=5)
    >>> b.autores.all()
    [<Author: Adrian Holovaty>, <Author: Jacob Kaplan-Moss>]
    >>> b.autores.filter(nombre='Adrian')
    [<Author: Adrian Holovaty>]
    >>> b.autores.filter(nombre='Adam')
    []

Esto también trabaja en orden inverso, Para visualizar todos los libros de un
determinado autor, usa ``autor.libro_set``, así::

    >>> from biblioteca.models import Autor
    >>> a = Autor.objects.get(nombre='Adrian', apellidos='Holovaty')
    >>> a.libro_set.all()
    [<Libro: The Django Libro>, <Libro: Adrian's Other Libro>]

Al igual que con lo campos ``Foraneos``, el nombre del atributo ``libro_set``
es generado agregando el nombre del modelo en minúsculas a ``_set``.

Como hacer cambios al esquema de la base de datos
=================================================

Cuando introducimos el comando ``migrate`` en el capítulo 5, hicimos énfasis
en que ``migrate`` crea las tablas que no existen en la base de datos
sincronizando los modelos -- pero nos  falto comentar que no solo crea modelos,
también agrega y renombra campos,  elimina y agrega modelos, por lo que en la
mayoría de casos no necesitaras hacer estos cambios manualmente. Esta sección
explica cómo hacer cambios al esquema de la base de datos, usando solo dos
comandos.

Cuando se trata con cambios al esquema de la base de datos, es importante tener
en cuenta algunas cuestiones relacionadas con la forma en que trabaja la
capa de base de datos de Django:

* Django se quejará estrepitosamente si un modelo contiene un campo que todavía
  no se ha creado en la tabla de base de datos. Esto causará un error la primera
  vez que utilices la API de la base de datos (es decir, esto sucede en tiempos
  de ejecución del código, no en tiempos de compilación).

* A Django no le importa si una tabla de la base de datos, contiene columnas
  que no están definidas en el modelo.

* A Django no le importa si una base de datos contiene una tabla que no esta
  representada por un modelo.

Por lo que realizar cambios al esquema, solo es cuestión de cambiar varias
piezas -- el código Python y la base de datos en sí mismo -- en el orden
correcto.

Migraciones
-----------

Los dos comandos que se encargan de interactuar con las migraciones y manejar
el esquema de la base de datos en Django son:

:makemigrations:
    Comando responsable de crear nuevas migraciones basadas en los cambios
    hechos a los modelos.

:migrate:
    Comando responsable de aplicar las migraciones y sincronizar los modelos de
    la base de datos y listar su estatus.

Las migraciones son la forma en que Django propaga los cambios que realizas a
tus modelos (agregando campos, eliminando un modelo, etc.) en el esquema de la
base de datos. Se diseñan para ser sobre todo automáticas, pero necesitas saber
cuándo hacerlas y cuando no, y sobre todo debes tener cuidado con los problemas
comunes que puedan surgir.

.. admonition:: Un poco de historia:

    Antes de la versión 1.7 de Django, solo era  posible agregar  modelos
    nuevos a la base de datos; no era posible alterar o quitar los modelos
    existentes, usando el comando ``syncdb`` (el precursor de ``migrate`` ).
    Por lo que si  se agregaba y cambiaba un campo de un modelo, o si se
    eliminaba un modelo, era necesario realizar el cambio en la base de datos
    manualmente usando SQL.

    Por lo que surgieron algunas herramientas de terceros en especial ``South``
    que proveían soporte para realizar estos cambios adicionales en el esquema
    de la base de datos, con el tiempo este tipo de soporte fue considerado,
    lo suficientemente importante que fue incluido en el código base de Django.

El sistema de migraciones de Django, se divide en dos partes: la lógica que
calcula y almacena las operaciones que se ejecutan (django.db.migrations), y
la capa de abstracción de la base de datos que se encarga de cosas como
"crear un modelo" "borrar un campo" en SQL --el cual es trabajo del Editor de
esquema (SchemaEditor).

Trabajar con migraciones es sencillo, cambia tu modelo -- es decir agrega un
campo y/o remueve un modelo... -- y ejecuta los comando **makemigrations** y
**migrate** en ese orden.

Agregar campos
--------------

Cuando se agrega un campo a una tabla/modelo en un entorno en producción, el
truco es realizarlo primero en un servidor de desarrollo y luego llevar los
cambios al sitio de producción.

Sin embargo las migraciones funcionarán de la misma manera en el mismo conjunto
de datos y producirán resultados constantes, lo que significa que pueden ser
usadas en desarrollo y en producción bajo las mismas condiciones y
circunstancias y con los mismos resultados.

Para agregar campos a un modelos sigue estos pasos:

1. Agrega el campo a tu modelo.
2. Asegúrate que el campo incluya las opciones ``blank=True`` y ``null=True``.
3. Ejecuta el comando ``manage.py makemigrations``, para grabar los cambios.
4. Sincroniza los modelos con ``manage.py  migrate``.
5. Ejecuta ``manage.py shell`` y verifica que el nuevo campo se haya agregado
   correctamente, importa el modelo y realiza una consulta a la base de datos
   (por ejemplo con ``Libro.objects.all()[:5]``). Si la actualización fue
   correcta, la declaración anterior debe trabajar sin errores.

Como ejemplo, examinemos los pasos necesarios para agregar un campo
``num_paginas`` al modelo ``Libro`` del :doc:`capítulo 5<chapter05>`,:.

Lo primero que haremos será cambiar el modelo y agregarle el nuevo campo así:

.. parsed-literal::

    class Libro(models.Model):
        titulo = models.CharField(max_length=100)
        autores = models.ManyToManyField(Autor)
        editores = models.ForeignKey(Editor)
        fecha_publicacion = models.DateField(blank=True, null=True)
        **num_paginas = models.IntegerField(blank=True, null=True)**

        def __str__(self):
            return self.titulo

.. admonition:: Nota:

    Lee la sección "Crear campos opcionales" del :doc:`capítulo 6<chapter06>`,
    para conocer los detalles importantes acerca del porque incluimos
    ``blank=True`` y  ``null=True``.


Ahora podemos ejecutar el comando ``manage.py sqlall libros``  para ver
la declaración  ``CREATE TABLE`` de SQL. Dependiendo de la base de datos
la salida puede variar::

    CREATE TABLE "libros_libro" (
        "id" serial NOT NULL PRIMARY KEY,
        "titulo" varchar(100) NOT NULL,
        "editores_id" integer NOT NULL REFERENCES "books_publisher" ("id"),
        "fecha_publicacion" date NOT NULL,
        "num_paginas" integer NULL
    );

La nueva columna es representada así::

    "num_pages" integer NULL

.. admonition:: ¿Por que agregamos columnas ``NOT NULL``?

    En este punto vale la pena hacer mención de una delicada sutileza, cuando
    agregamos el campo ``num_paginas`` al modelo, incluimos las opciones
    ``blank=True`` y ``null=True`` ya que una columna de una base de datos,
    debe de contener valores ``NULL`` cuando  es creada por primera vez.

    Sin embargo también es posible agregar columnas que no contengan valores
    ``NULL``. Para ello es necesario crear las columnas como ``NULL`` y agregar
    valores por defecto y después alterar la columna para modificarla a
    ``NOT NULL``.

    Usando SQL tendríamos que hacer esto:::

        BEGIN;
        ALTER TABLE libros_libro ADD COLUMN num_paginas integer;
        UPDATE libros_libro SET num_pages=0;
        ALTER TABLE libros_libro ALTER COLUMN num_paginas SET NOT NULL;
        COMMIT;

    Afortunadamente el comando ``migrate`` se encarga de realizar este trabajo
    por ti, ya que detecta cuando se quiera agregar un campo que contiene
    valores ``NOT NULL``, advirtiéndonos que tratamos de agregar un campo
    ``NOT NULL`` y que no se puede hacer eso (ya que la base de datos necesita
    rellenar las filas existentes.) Po lo que interactivamente nos ofrece dos
    opciones para corregirlo:

    * Introducir un valor por defecto, para rellenar las filas.
    * Salir para corregir el valor por defecto en los modelos.

    Si seleccionamos la primera opción, se inicia el interprete interactivo que
    nos pide agregar un valor por defecto, siempre y cuando sea un valor valido
    en Python, la segunda opción es obvia, es tu responsabilidad corregir el
    modelo manualmente usando SQL.

Una vez que hemos cambiado nuestro modelo, podemos validarlo usando el comando
``manage.py validate``, para asegurarnos de que todo está correctamente en su
lugar, si el comando no lanza ningún error, podemos crear las migraciones con
el comando ``manage.py makemigrations``, con el que obtendremos una salida como
esta::

    Migrations for 'libros':
      0002_auto.py:
        -Add field num_paginas to libro

Tus modelos serán explorados y comparados con las versiones contenidas en el
fichero  actual de migraciónes, y entonces un nuevo conjunto de migraciones
será escrito. Asegúrate de leer la salida para ver lo qué  el comando
makemigrations piensa que  ha cambiado -- no es perfecto, sobre todo en cambios
complejos,  puede ser que no detecte lo que esperabas.

Una vez que tengas un nuevo archivo de migraciones, debes aplicarlo a la base
de datos usando ``manage.py migrate`` para cerciorarte de que trabaja según lo
previsto.::

    Operations to perform:
      Synchronize unmigrated apps: sessions, admin, messages, auth, staticfiles, contenttypes
      Apply all migrations: libros
    Synchronizing apps without migrations:
      Creating tables...
      Installing custom SQL...
      Installing indexes...
    Installed 0 object(s) from 0 fixture(s)
    Running migrations:
      Applying libros.0002_auto... OK

El comando  se ejecuta en dos etapas, primero sincroniza las aplicaciones
que no han sido migradas(sincronizando los cambios en los modelos) y segundo
ejecuta las migraciones que no han sido aplicadas. Una vez que una migración
ha sido aplicada, esta se guarda en el sistema de control de versiones.

Una vez realizados los cambios podemos iniciar el intérprete interactivo, y
comprobar que todo trabaje según lo planeado::

    >>>from biblioteca.models import Libro
    >>>Libro.objects.all()[:5]
    >>>

Eliminar campos
---------------

Eliminar un campo de un modelo es mucho mas fácil que agregar uno. Para remover
un campo, solo sigue estos paso:

#. Remueve el campo de tu modelo.
#. Ejecuta el comando ``manage.py make migrations``, para grabar los cambios.
#. Haz los cambios en la base de datos con el comando ``manage.py  migrate``.
#. Reinicia el servidor Web.

Asegúrate de hacerlo en este orden.

Eliminar relaciones muchos a muchos
-----------------------------------

Debido a que los campos muchos a muchos, son diferentes a los campos normales
el proceso de eliminación es un poco  diferente.

Para eliminar manualmente una relación muchos a muchos, tendríamos que hacer lo
siguiente:

* Remueve el campo ``ManyToManyField`` de tu modelo y reinicia el servidor Web.

* Remueve la tabla muchos a muchos de base de datos usando un comando  SQL
  como este:::

      DROP TABLE libros_libro_autores;

Como en la sección anterior, podemos seguir los siguientes pasos, para usar
las migraciones:

#. Remueve el campo muchos a muchos  de tu modelo.
#. Ejecuta el comando ``manage.py make migrations``, para grabar los cambios.
#. Haz los cambios en la base de datos con el comando ``manage.py  migrate``.
#. Reinicia el servidor Web.

Asegúrate de hacerlo en este orden y asegurate de borrar cualquier modelo que
dependa de la relación muchos a muchos, de otra forma no funcionara.

Eliminar modelos
----------------

Eliminar un modelo completo es tan fácil como agregar uno. Para remover
un modelo, solo sigue estos paso:

#. Remueve el modelo.
#. Ejecuta el comando ``manage.py make migrations``, para grabar los cambios.
#. Haz los cambios en la base de datos con el comando ``manage.py  migrate``.
#. Reinicia el servidor Web.

Manualmente puedes hacerlo así:

* Elimina el modelo de tu archivo ``models.py`` y reinicia el servidor.
* Elimina la tabla de tu base de datos, usando el siguiente comando::

    DROP TABLE libros_libro;

.. warning::

    Ten en cuenta,  que también es necesario remover cualquier tabla que dependa
    de el modelo que quieras borrar de tu base de datos primero --por ejemplos
    alguna tabla que contenga un campo foraneo o una relación muchos a muchos.

Cómo en las secciones anteriores. Asegúrate de hacerlo en este orden.

.. class:: Manager()

Manejadores o Managers
======================

En la declaración ``Libro.objects.all()``, ``objects`` es un atributo especial
a través del cual se realizan las consultas a la base de datos. En el capitulo
:doc:`capitulo 5<chapter05>`, identificamos brevemente a este como el
*Manejador* (Manager). Es hora de sumergirnos en las profundidades y conocer
que son los manejadores y como podemos usarlos.

Un ``Manager`` es la interfaz a través de la cual se proveen las operaciones
de consulta de la base de datos a los modelos de Django. Existe al menos un
``Manager`` para cada modelo en una aplicación Django.

.. _nombres_manager:

Nombres de Manager
------------------

Por omisión, Django agrega un ``Manager`` llamado ``objects`` a cada clase
modelo de Django. De todas formas, si tu quieres usar ``objects`` como nombre
de campo, o quieres usar un nombre distinto de ``objects`` para el ``Manager``,
puedes renombrarlo en cada uno de los modelos. Para renombrar el ``Manager``
para una clase dada, define un atributo de clase de tipo ``models.Manager()``
en ese modelo, por ejemplo::

    from django.db import models

    class Persona(models.Model):
        ...

        gente = models.Manager()

Usando este modelo de ejemplo, ``Persona.objects`` generará una excepción
``AttributeError`` (dado que ``Persona`` no tiene un atributo ``objects``), pero
``Persona.gente.all()`` devolverá una lista de todos los objetos ``Persona``.


Managers Personalizados
-----------------------

Puedes utilizar un ``Manager`` personalizado en un modelo en particular
extendiendo la clase base ``Manager`` e instanciando tu ``Manager``
personalizado en tu modelo.

La forma en que trabajan las clases ``Manager`` está documentada en
:doc:`apéndice B<appendixB>`. Esta sección trata específicamente las opciones
del modelo que personaliza el comportamiento del ``Manager``.

Hay dos razones por las que puedes querer personalizar un ``Manager``: para
agregar métodos extra al ``Manager``, y/o para modificar el ``QuerySet``
inicial que devuelve el ``Manager``.


Agregando Métodos Extra al Manager
----------------------------------

Agregar métodos extra al ``Manager`` es la forma preferida de agregar
funcionalidad  a "nivel de tabla" a tus modelos. (Para agregar funcionalidad a
nivel de registro -- esto es, funciones que actúan sobre una instancia simple
de un objeto modelo -- usa métodos en los modelos, los cuales son explicados más
adelante en este capítulo.

Por ejemplo, démosle al ``Manager``  de nuestro modelo ``Libro``  un método
``contar_titulos()``,  el cual toma una palabra clave y retorna el numero de
libros que contienen un titulo que contiene dicha palabra. (Este ejemplo es
bastante superficial, pero demuestra cómo trabajan los ``Managers``)

.. parsed-literal::

    # models.py

    from django.db import models

    # ... Los modelos Autor y Editor van aqui ...

    **class ManejadorLibros(models.Manager):**
        **def contar_titulos(self, keyword):**
            **return self.filter(titulo__icontains=keyword).count()**

    class Libro(models.Model):
        titulo = models.CharField(max_length=100)
        autores = models.ManyToManyField(Autor)
        editores = models.ForeignKey(Editor)
        fecha_publicacion = models.DateField(blank=True, null=True)
        num_paginas = models.IntegerField(blank=True, null=True)
        **objects = ManejadorLibros()**

        def __str__(self):
            return self.titulo

Con el ``Manager`` en su lugar, ahora podemos hacer esto::

    >>> Libro.objects.contar_titulos('django')
    4
    >>> Libro.objects.contar_titulos('python')
    18

Algunas notas sobre el código:

* Creamos una clase ``ManejadorLibros`` que extiende a ``django.db.models.Manager``.
  El sencillo método ``contar_titulos()``, hace los cálculos. Observa que el método
  usa un filtro ``self.filter()``, donde  ``self`` se refiere al manager en si
  mismo.

* Asignamos ``ManejadorLibros()`` a los atributos de  ``objects`` en el modelo.
  Esto tiene el efecto de reemplazar el manejado por "defecto", el cual es
  llamado ``objects`` y es automáticamente creado si no especificas un
  manager personalizado. Lo hemos llamado  ``objects`` en vez de usar algún otro
  nombre, para ser consistentes  con los managers automáticamente creados.

¿Por qué agregamos un método tal como ``contar_titulos()`` aquí?  Bueno, para
encapsular la ejecución de consultas comunes, a fin de de evitar duplicar el
código.

Un método ``Manager`` personalizado puede retornar cualquier cosa que necesites.
No tiene que retornar un ``QuerySet``.

Por ejemplo, este ``Manager`` personalizado ofrece un método ``with_counts()``,
que retorna una lista de todos los objetos ``OpinionPoll``, cada uno con un
atributo extra ``num_responses`` que es el resultado de una consulta agregada::

    from django.db import models

    class PollManager(models.Manager):
        def with_counts(self):
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("""
                SELECT p.id, p.question, p.poll_date, COUNT(*)
                FROM polls_opinionpoll p, polls_response r
                WHERE p.id = r.poll_id
                GROUP BY p.id, p.question, p.poll_date
                ORDER BY p.poll_date DESC""")
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], question=row[1], poll_date=row[2])
                p.num_responses = row[3]
                result_list.append(p)
            return result_list

    class OpinionPoll(models.Model):
        question = models.CharField(max_length=200)
        poll_date = models.DateField()
        objects = PollManager()

    class Response(models.Model):
        poll = models.ForeignKey(OpinionPoll)
        person_name = models.CharField(max_length=50)
        response = models.TextField()


En este ejemplo, puedes usar ``OpinionPoll.objects.with_counts()`` para
retornar la lista de objetos ``OpinionPoll`` con el atributo ``num_responses``.

Otra cosa a observar en este ejemplo es que los métodos de un ``Manager``
pueden acceder a ``self.model`` para obtener la clase modelo a la cual están
anexados.


Modificando los QuerySets iníciales del Manager
-----------------------------------------------

Un ``QuerySet`` base de un ``Manager`` devuelve todos los objetos en el sistema.
Por ejemplo, ``Libro.objects.all()`` retornará todos los libros de la base de
datos.

Puedes sobrescribir el ``QuerySet`` base, sobrescribiendo el método
``Manager.get_query_set()``. ``get_query_set()`` debe retornar un ``QuerySet``
con las propiedades que tu requieres.

Por ejemplo, el siguiente modelo tiene *dos* managers -- uno que devuelve todos
los objetos, y otro que retorna solo los libros de Roald Dahl:

.. parsed-literal::

    from django.db import models

    **# Primero, definimos una subclase para el Manager.**
    **class DahlLibroManager(models.Manager):**
        **def get_query_set(self):**
            **return super(DahlLibroManager, self).get_query_set().filter(autor='Roald Dahl')**

    **# Despues lo anclamos al modelo Libro explicitamente.**
    class Libro(models.Model):
        titulo = models.CharField(max_length=100)
        autor = models.CharField(max_length=5)
        # ...

        **objects = models.Manager() # El manager predeterminado.**
        **dahl_objects = DahlLibroManager() # El manager "Dahl" especial.**

.. SL Tested ok


Con este modelo de ejemplo, ``Libro.objects.all()`` retornará todos los libros
de la base de datos, pero ``Libro.dahl_objects.all()`` solo retornará aquellos
escritos por Roald Dahl.

Por supuesto, como ``get_query_set()`` devuelve un objeto ``QuerySet``, puedes
usar ``filter()``, ``exclude()``, y todos los otros métodos de ``QuerySet``
sobre él. Por lo tanto, todas estas sentencias son legales::

    Libro.dahl_objects.all()
    Libro.dahl_objects.filter(titulo='Matilda')
    Libro.dahl_objects.count()


Este ejemplo también nos muestra otra técnica interesante: usar varios managers
en el mismo modelo. Puedes agregar tantas instancias de ``Manager()`` como quieras.
Esta es una manera fácil de definir "filters" comunes para tus modelos.

Aquí hay un ejemplo::

    class ManejadorHombres(models.Manager):
        def get_query_set(self):
            return super(ManejadorHombres, self).get_query_set().filter(sexo='H')

    class ManejadorMujeres(models.Manager):
        def get_query_set(self):
            return super(ManejadorMujeres, self).get_query_set().filter(sexo='M')

    class Persona(models.Model):
        nombre = models.CharField(max_length=50)
        apellido = models.CharField(max_length=50)
        sexo = models.CharField(max_length=1, choices=(('M', 'Mujer'), ('H', 'Hombre')))
        gente = models.Manager() # EL manejador predeterminado.
        hombre = ManejadorHombres()# Devuelve solo hombres.
        mujer = ManejadorMujeres()# Devuelve solo mujeres.

Este ejemplo te permite consultar ``Persona.hombre.all()``, ``Persona.mujer.all()``,
y ``Persona.gente.all()``, con los resultados predecibles.

Si usas objetos ``Manager`` personalizados, toma nota que el primer ``Manager``
que encuentre Django (en el orden en el que están definidos en el modelo) tiene
un status especial. Django interpreta el primer ``Manager`` definido en una
clase como el ``Manager`` por omisión. Ciertas operaciones -- como las del
sitio de administración de Django -- usan el ``Manager`` por omisión para
obtener listas de objetos, por lo que generalmente es una buena idea que el
primer ``Manager`` esté relativamente sin filtrar. En el último ejemplo, el
manager ``people`` está definido primero -- por lo cual es el ``Manager`` por
omisión.

En resumen, Un ``Manager`` es la interfaz a través de la cual se proveen las
operaciones de consulta de la base de datos a los modelos de Django. Existe al
menos un ``Manager`` para cada modelo en una aplicación Django. puedes crear
manejadores personalizados para modificar el acceso a la base de datos para
requisitos particulares.

Métodos de Modelo
=================

Define métodos personalizados en un modelo para agregar funcionalidad
personalizada a nivel de registro para tus objetos. Mientras que los métodos
``Manager`` están pensados para hacer cosas a nivel de tabla, los métodos de
modelo deben actuar en una instancia particular del modelo.

Esta es una técnica valiosa para mantener la lógica del negocio en un sólo
lugar: el modelo.

Por ejemplo, este modelo tiene algunos métodos personalizados::

    from django.db import models

    class Persona(models.Model):
        nombre = models.CharField(max_length=15)
        apellido = models.CharField(max_length=15)
        nacimiento = models.DateField()
        domicilio = models.CharField(max_length=100)
        ciudad = models.CharField(max_length=15)
        estado = models.CharField(max_length=2)

        def estatus_bebe(self):
            "Retorna el estatus baby-boomer de la persona."
            import datetime
            if datetime.date(1945, 8, 1) <= self.nacimiento <= datetime.date(1964, 12, 31):
                return "Baby boomer"
            if self.nacimiento < datetime.date(1945, 8, 1):
                return "Pre-boomer"
            return "Post-boomer"

        def es_del_medio_oeste(self):
            "Retorna True si la persona nacio en el medio-oeste."
            return self.estado in ('IL', 'WI', 'MI', 'IN', 'OH', 'IA', 'MO')

        def _nombre_completo(self):
            "Retorna el nombre completo de una persona."
            return '%s %s' % (self.nombre, self.apellido)
        nombre_completo = property(_nombre_completo)

Este es un ejemplo de su uso::

    >>> p = Persona.objects.get(nombre='Barack', apellido='Obama')
    >>> p.nacimiento
    datetime.date(1961, 8, 4)
    >>> p.estatus_bebe()
    'Baby boomer'
    >>> p.es_del_medio_oeste()
    True
    >>> p.nombre_completo  # Nota que no es un método -- es tratado como un atributo
    u'Barack Obama'

Existen también un puñado de métodos de modelo que tienen un significado
"especial" para Python o Django. Estos métodos se describen a continuación.

__unicode__
-----------

.. method:: Model.__unicode__()

El método ``__unicode__()`` es un "método mágico" de Python que define lo que
debe ser devuelto si llamas a ``unicode()`` sobre el objeto. Django usa
``unicode(obj)`` (o la función relacionada :meth:`str(obj) <Model.__str__>`
que se describe más abajo) en varios lugares, particularmente como el valor
mostrado para hacer el render de un objeto en el sitio de administración de
Django y como el valor insertado en un plantilla cuando muestra un objeto. Por
eso, siempre debes retornar un string agradable y legible por humanos en el
formato ``__unicode__()`` de un objeto. A pesar de que esto no es requerido, es
altamente recomendado.

Por ejemplo::

    from django.db import models

    class Persona(models.Model):
        nombre = models.CharField(max_length=50)
        apellido = models.CharField(max_length=50)

        def __unicode__(self):
            return u'%s %s' % (self.nombre, self.apellido)

__str__
-------

.. method:: Model.__str__()

``__str__()`` es un "método mágico" de Python que define lo que debe ser
devuelto si llamas a ``str()``. En Python3, Django usa ``str(obj)``, en varios
lugares, particularmente como el valor mostrado para hacer el render de un
objeto en el sitio de administración de Django y como el valor insertado en un
plantilla cuando muestra un objeto. Por eso, siempre debes retornar un string
agradable y legible por humanos en el ``__str__`` de un objeto.
A pesar de que esto no es requerido, es altamente recomendado, al usar Python3.

Aquí hay un ejemplo::

    class Persona(models.Model):
        nombre = models.CharField(maxlength=50)
        apellido = models.CharField(maxlength=50)

        def __str__(self):
            return '%s %s' % (self.nombre, self.apellido)


``__eq__``
----------

.. method:: Model.__eq__()

Un método de igualdad que es definido cuando las instancias con la misma clave
primaria son evaluadas y la clase en concreto es considerada igual.

POr ejemplo::

    from django.db import models

    class MiModelo(models.Model):
        id = models.AutoField(primary_key=True)

    class ModeloProxy(MiModelo):
        class Meta:
            proxy = True

    class HerenciaMultiple(MiModelo):
        pass

    MiModelo(id=1) == MiModelo(id=1)
    MiModelo(id=1) == ModeloProxy(id=1)
    MiModelo(id=1) != HerenciaMultiple(id=1)
    MiModelo(id=1) != MiModelo(id=2)


``__hash__``
------------

.. method:: Model.__hash__()

Calcula el valor ``hash`` para una clave primaria.

El método ``__hash__`` esta basado en la instancia de el valor de la clave
primaria. Usando (obj.pk). Si la instancia no tiene una clave primaria
lanzara un error ``TypeError``.

get_absolute_url
----------------

Define un método ``get_absolute_url()`` para decirle a Django cómo calcular la
URL de un objeto, por ejemplo::

    def get_absolute_url(self):
        return "/gente/%i/" % self.id

Django usa esto en la interfaz de administración. Si un objeto define
``get_absolute_url()``, la página de edición del objeto tendrá un enlace
"View on site", que te llevará directamente a la vista pública del objeto,
según ``get_absolute_url()``.

Sin embargo, a pesar de que este código es simple, no es muy portable, por lo
que la mejor forma de aprovechar esto es usando la función
:func:`~django.core.urlresolvers.reverse`

Por ejemplo::

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('gente.views.detalles', args=[str(self.id)])

También un par de otras partes de Django, como el framework de sindicación de
feeds, usan ``get_absolute_url()`` como facilidad para recompensar a las
personas que han definido el método.

.. warning::

    Debes evitar en lo posible, construir URL para entradas no validas, para
    reducir las posibilidades  de enlazar contenidos y redireccionamientos
    no deseados y potencialmente peligrosos, por ejemplo::

        def get_absolute_url(self):
            return '/%s/' % self.nombre

    Si ``self.nombre`` es ``'/example.com'`` este devolvera ``'//example.com/'``
    el cual es un esquema URL valido, pero no esperado ``'/%2Fexample.com/'``.

Es una buena práctica usar ``get_absolute_url()`` en plantillas, en lugar de
codificar en duro las URL de tus objetos. Por ejemplo, este código de plantilla
es *malo*::

.. code-block:: html+django

    <!-- MALO ¡No hagas esto! -->
    <a href="/gente/{{ object.id }}/">{{ object.nombre }}</a>

Pero este es bueno::

.. code-block:: html+django

    <a href="{{ object.get_absolute_url }}">{{ object.nombre }}</a>

La logica aqui, es que puedes cambiar la estructura completa, de las URL de tus
objetos, en un único lugar con ``get_absolute_url()``.

.. note::

    La cadena que devuelve el método  ``get_absolute_url()`` deve contener
    **únicamente** caracteres ASCII (requeridos por las especificaciones
    URI :rfc:`2396`) y deben ser encodificadas de ser necesario.

    Puedes usar la funcion ``django.utils.encoding.iri_to_uri()``  para
    realizar este trabajo y así garantizar que tus cadenas únicamente
    contendran caracteres dentro del rango ASCII.


Sobreescribir métodos predefinidos de un modelo
------------------------------------------------

Existe otro conjunto de métodos en un modelo que encapsulan un montón de
comportamientos de la base de datos, estos pueden ser sobrescritos para
requisitos particulares que quieras modificar. Particularmente  los métodos
save() y delete().

Siente libre de sobreescribir estos métodos (y cualquier otro método de un
modelo) para alterar su comportamiento.

Un uso clásico para sobrescribir los métodos incorporados de un modelo, es por
ejemplo si quieres que pase algo cuando guardas un objeto, así::

    from django.db import models

    class Autor(models.Model):
        nombre = models.CharField(max_length=30)
        apellidos = models.CharField(max_length=40)
        email = models.EmailField()

        def save(self, *args, **kwargs):
            haz_algo()
            super(Autor, self).save(*args, **kwargs) # Llama al "verdadero" método save().

Tambien puedes evitar guardar un objeto en especifico::

    from django.db import models

    class Autor(models.Model):
        nombre = models.CharField(max_length=30)
        apellidos = models.CharField(max_length=40)
        email = models.EmailField()

        def save(self, *args, **kwargs):
            if self.nombre == "Foo":
                return # ¡Foo ha dicho que nunca publicara un libro!
            else:
                super(Autor, self).save(*args, **kwargs) # Llama al "verdadero" método save()

Es importante recordar llamar el método de los superclase - que es en este caso:
``super(Autor, self).save(*args, **kwargs)`` para asegurarse de que el objeto
se ha guardado en la base de datos, ya que el comportamiento por omisión no
toca la base de datos y el objeto no se guardara.

Es también importante pasar los argumentos que se pueda necesitar pasar al
método del modelo - que son ``*args``, ``**kwargs``. De vez en cuando en Django, se
amplían las capacidades incorporados de los métodos de los modelos, agregando
nuevos argumentos. Si utilizas ``*args`` y  ``**kwargs`` en tus definiciones del método,
garantizas que tu código soportará automáticamente esos argumentos cuando se
agreguen mas.

Ejecutando consultas personalizadas en SQL
------------------------------------------

Alguna veces te encontraras con que la API de bases de datos de Django
únicamente te permite realizar un cierto tipo de consultas, siéntete libre de
escribir sentencias SQL personalizadas en métodos personalizados de modelo y
métodos a nivel de módulo. Es muy sencilla accede al objeto
``django.db.connection`` el cual representa la conexión actual a la base de
datos. Para usarla, invoca  el método ``connection.cursor()`` para obtener un
objeto cursor. Después, llama a  ``cursor.execute(sql, [params])`` para
ejecutar sentencias SQL, y ``cursor.fetchone()`` o ``cursor.fetchall()`` para
devolver las filas resultantes:

Por ejemplo::

     >>> from django.db import connection
    >>> cursor = connection.cursor()
    >>> cursor.execute("""
    ...    SELECT DISTINCT nombre
    ...    FROM personas
    ...    WHERE apellido = %s""", ['Lennon'])
    >>> row = cursor.fetchone()
    >>> print row
    ['John']

.. SL Tested ok

``connection`` y ``cursor`` implementan en su mayor parte la DB-API estándar de
Python (http://www.python.org/peps/pep-0249.html). Si no estás familiarizado con
la DB-API de Python, observa que la sentencia SQL en ``cursor.execute()`` usa
marcadores de posición, ``"%s"``, en lugar de agregar los parámetros directamente
dentro del SQL. Si usas esta técnica, la biblioteca subyacente de base de datos
automáticamente agregará comillas y secuencias de escape a tus parámetros según
sea necesario. (Observa también que Django espera el marcador de posición
``"%s"``, *no* el  marcadores de posición ``"?"``, que es utilizado por los
enlaces Python a SQLite. Python bindings. Esto es por consistencia y salud
mental).

En vez de ensuciar el código de tu vista con esta declaración
``django.db.connection``,  es una buena idea ponerlo  en un método personalizado
en el modelo o en un método de un manager. De esta forma, el anterior ejemplo
puede ser integrado en un método de manager, así::

    from django.db import connection, models

    class PersonaManager(models.Manager):
        def nombres(self, apellido):
            cursor = connection.cursor()
            cursor.execute("""
                SELECT DISTINCT apellido
                FROM persona
                WHERE apellido = %s""", [apellido])
            return [row[0] for row in cursor.fetchone()]

    class Persona(models.Model):
        nombre = models.CharField(max_length=15)
        apellido = models.CharField(max_length=15)
        objects = PersonaManager()

Y un ejemplo de sus uso::

    >>> Persona.objects.nombres('Lennon')
    ['John', 'Cynthia']

Que sigue
============

En el :doc:`siguiente capitulo <chapter11>`, te mostraremos el framework
"Vistas genéricas", el cual te permite ahorrar tiempo para construir sitios
Web, que siguen patrones comunes.

