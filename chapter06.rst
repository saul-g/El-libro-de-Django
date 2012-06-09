=============================================
Capítulo 6: El sitio de Administración Django
=============================================

Para cierto tipo de Sitios Web, una *interfaz de administración* es una parte
esencial de la infraestructura. Se trata de una interfaz basada en web, limitada
a los administradores autorizados, que permite agregar, editar y eliminar el
contenido del sitio. La interfaz que usas para escribir en tu blog, el sitio
privado que los editores usan para moderar los comentarios de los lectores, la
herramienta que tus clientes utilizan para actualizar los comunicados de prensa
en la web que construiste para ellos -- todos son ejemplos de interfaces de
administración.

Aunque hay un problema con las interfaces de administración: es aburrido
construirlas.  El desarrollo web es divertido cuando estás desarrollando
funcionalidades de lado público del sitio, pero construir interfaces de
administración es siempre lo mismo.  Tienes que autenticar usuarios, mostrar y
manipular formularios, validar las entradas y demás. Es aburrido y repetitivo.

¿Cuál es la solución de Django para estas tareas aburridas y repetitivas?  Las
hace todas por ti -- en sólo un par de líneas de código, ni más ni menos. Con
Django, construir interfaces de administración es un problema resuelto.

Este capítulo trata sobre la interfaz de administración automática de Django.
Esta característica funciona leyendo los meta-datos en tus modelos para brindar
una interfaz potente y lista para producción que los administradores del sitio
podrán usar inmediatamente. Aquí discutimos cómo activar, usar y personalizar
esta utilidad.

Activar la interfaz de administración
=====================================

Pensamos que la interfaz de administración es la característica más atractiva de
Django -- y la mayoría de Djangonautas están de acuerdo -- pero como no todo el
mundo lo necesita, es una pieza opcional. Esto significa que hay que dar tres
pasos para activar la interfaz de administración:

    1.  Agrega meta-datos de administración a tus modelos.

        No todos los modelos pueden (o deberían) ser editables por los usuarios
        administradores, por lo que necesitas "marcar" los modelos que deberían
        tener una interfaz de administración. Esto lo hacemos añadiendo al
        modelo una clase interna ``Admin`` (junto con la clase ``Meta``, si es
        que hay una).  Así que, para agregar una interfaz de administración a
        nuestro modelo ``Book`` del capítulo anterior, usamos:
            
        .. code-block:: python
       

            class Book(models.Model):
                title = models.CharField(maxlength=100)
                authors = models.ManyToManyField(Author)
                publisher = models.ForeignKey(Publisher)
                publication_date = models.DateField()
                num_pages = models.IntegerField(blank=True, null=True)

                def __unicode__(self):
                    return self.title

                **class Admin:**
                    **pass**

        La declaración de ``Admin`` marca la clase como poseedora de una
        interfaz de administración. Hay una serie de opciones que podemos
        incluir bajo ``Admin``, pero por ahora vamos a limitarnos al
        comportamiento por defecto, así que escribimos ``pass`` para decirle a
        Python que la clase ``Admin`` está vacía.

        Si estás siguiendo este ejemplo escribiendo tu propio código,
        probablemente sea buena idea agregar ahora declaraciones de ``Admin`` a
        las clases ``Publisher`` y ``Author``.

    2.  Instalar la aplicación ``admin``. Esto se hace agregando
        ``"django.contrib.admin"`` a tus ``INSTALLED_APPS`` de tu archivo de
        configuración ``settings.py``.

    3.  Además, asegurate de que las aplicaciones ``"django.contrib.sessions"``,
        ``"django.contrib.auth"``, y ``"django.contrib.contenttypes"`` no están
        comentadas,  ya que la aplicación ``admin`` depende de ellas. También
        descomenta todas las líneas de ``MIDDLEWARE_CLASSES`` configurando la
        tupla, y borra la definición de ``TEMPLATE_CONTEXT_PROCESSOR`` para
        permitir que tome los valores por defecto.

    4.  Ejecuta ``python manage.py syncdb``. Este paso instalará las tablas de
        la base de datos que la interfaz de administración necesita.

        .. admonition:: Nota:

            Es probable que la primera vez que ejecutaste ``syncdb`` con
            ``"django.contrib.auth"`` en INSTALLED_APPS, te preguntara algo
            sobre crear un superusuario. Si no lo hiciste en ese momento,
            tendrás que ejecutar:
            ``python manage.py createsuperuser``
            para crear este usuario administrador. En caso contrario no serás
            capaz de identificarte para entrar a la interfaz de administración.

    5.  Agrega el patrón de URL en tu ``urls.py``. Si aún estás usando el que
        fue creado por ``startproject``, el patrón de la URL de administración
        ya debería estar ahí, pero comentado. De cualquier forma, los patrones
        de URL deberían terminar siendo algo así:

.. code-block:: python

            from django.conf.urls.defaults import *
            urlpatterns = patterns('',
                **(r'^admin/', include('django.contrib.admin.urls')),**
            )

Eso es todo. Ahora ejecuta ``python manage.py runserver`` para iniciar el
servidor de pruebas. Verás algo como esto::

    Validating models...
    0 errors found.

    Django version 1.4, using settings 'mysite.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

Ahora puedes visitar la URL que te brinda Django
(``http://127.0.0.1:8000/admin/`` en el ejemplo precedente), identificarte, y
jugar un poco.

Usar la interfaz de administración
==================================

La interfaz de administración está diseñada para ser usada por usuarios no
técnicos, y como tal debería ser lo suficientemente clara como para explicarse
por sí misma. Aún así, se brindan unas pocas notas sobre sus características.

Lo primero que verás es una página de identificación, como se muestra en la
Figura 6-1.

    .. image:: graficos/chapter06/login.png
       :alt: Pantalla de autenticación de Django.

Figura 6-1. Pantalla de autenticación de Django.

Usarás el nombre de usuario y la clave que configuraste cuando agregaste tu
superusuario. Una vez identificado, verás que puedes gestionar usuarios, grupos
y permisos (veremos más sobre esto en breve).

Cada objeto al que se le dió una declaración ``Admin`` aparece en el índice de
la página principal, como se muestra en la Figura 6-2

.. image:: graficos/chapter06/admin_index.png
   :alt: El índice principal de la Administración de Django.

Figura 6-2. El índice principal de la Administración de Django.

Los enlaces para agregar y modificar objetos llevan a dos páginas a las que nos
referiremos como ``listas de cambio`` [#]_ y ``formularios de edición`` [#]_ de
objetos:

Las listas de cambio son esencialmente páginas de índices de objetos en el
sistema, como se muestra en la Figura 6-3.

.. image:: graficos/chapter06/changelist.png
   :alt: Captura de una típica vista de lista de cambio

Figura 6-3. Una típica vista de lista de cambio

Hay varias opciones que pueden controlar los campos que aparecen en esas listas
y la aparición de características extra como campos de búsqueda e accesos
directo a filtros predefinidos. Más adelante hablaremos sobre esto.

Los formularios de edición se usan para modificar objetos existente y crear
nuevos (mira la Figura 6-4). Cada campo definido en tu modelo aparece aquí, y
notarás que campos de tipos diferentes tienen diferentes controles. (Por
ejemplo, los campos de fecha/hora tienen controles tipo calendario, las claves
foráneas usan cajas de selección, etc.)

.. image:: graficos/chapter06/editform.png
   :alt: Captura de un típico formulario de edición.

Figura 6-4. Un típico formulario de edición

Te darás cuenta que la interfaz de administración también controla por ti la
validez de los datos ingresados.  Intenta dejar un campo requerido en blanco o
poner una fecha inválida en un campo de fecha, y verás esos avisos de esos
errores cuando intentes guardar el objeto, como se muestra en la Figura 6-5.

.. image:: graficos/chapter06/editform_errors.png
   :alt: Captura de de un formulario de edición mostrando errores.

Figura 6-5. Un formulario de edición mostrando errores

Cuando editas un objeto existente, verás el botón Historia en la esquina
superior derecha de la ventana.  Cada cambio realizado a través de la interfaz
de administración es registrado, y puedes examinar este registro haciendo
click en este botón (mira la Figura 6-6).

.. image:: graficos/chapter06/history.png
   :alt: Captura de una página de historia de un objeto django.

Figura 6-6. Página de historia de un objeto django.

Cuando eliminas un objeto existente, la interfaz de administración solicita una
confirmación para prevenir costosos errores. La eliminación de un objeto se
desencadena en cascada, y la página de confirmación de eliminación del objeto
muestra todos los objetos relacionados que se eliminarán con él (mira la Figura
6-7).

.. image:: graficos/chapter06/delete_confirm.png
   :alt: Captura de una página de confirmación de eliminación de un objeto Django.

Figura 6-7. Una página de confirmación de eliminación de un objeto Django

Usuarios, Grupos y Permisos
---------------------------

Desde que estás identificado como un superusuario, tienes acceso a crear, editar
y eliminar cualquier objeto. Sin embargo, la interfaz de administración tiene un
sistema de permisos de usuario que puedes usar para darle a otros usuarios
acceso limitado a las partes de la interfaz que ellos necesitan.

Puedes editar estos usuarios y permisos a través de la interfaz de
administración, como si fuese cualquier otro objeto. Los vínculos a los modelos
``Usuarios`` y ``Grupos`` se encuentran en el índice de la página principal
junto con todo el resto de los modelos que haz definido.

Los objetos ``usuario`` tienen el los campos estándar nombre de usuario,
contraseña, dirección de correo, y nombre real que puedes esperar, seguidos de
un conjunto de campos que definen lo que el usuario tiene permitido hacer en la
interfaz de administración. Primero, hay un conjunto de tres opciones
seleccionables:

    * La opción "Es staff"  indica que el usuario está habilitado a ingresar a
      la interfaz de administración (por ejemplo, indica que el usuario es
      considerado un miembro del staff en tu organización). Como el mismo
      sistema de usuarios puede usarse para controlar el acceso al sitio público
      (es decir, sitios restringidos no administrativos. Mira el :doc:`Capítulo 12<chapter12>`.),
      esta opción diferencia entre usuarios públicos y administradores.

    * La opción "Activo" define si el usuario está activo en todo sentido. Si
      está desactivada, el usuario no tendrá acceso a ninguna URL que requiera
      identificación.

    * La opción "es superusuario" da al usuario completo e irrestricto acceso a
      todos los elementos de la interfaz de administración, y sus permisos
      regulares son ignorados.

Los administradores "normales" -- esto es, activos, no superusuarios y miembros
del staff -- tienen accesos que dependen del conjunto de permisos concedidos.
Cada objeto editable a través de la interfaz de administración tiene tres
permisos: un permiso de *crear* [#]_, un permiso de *modificar* [#]_, y un
permiso de *eliminar* [#]_. Lógicamente, asignando permisos a un usuario
habilitas que este acceda a realizar la acción que el permiso describe.

.. admonition:: Nota:

    El acceso a editar usuarios y permisos también es controlado por el sistema
    de permisos.  Si le das a alguien el permiso de editar usuarios, ¡estará en
    condiciones de editar sus propios permisos, que probablemente no es lo que
    querías!

También puedes asignar usuarios a grupos. Un *grupo* es simplemente un conjunto
de permisos a aplicar a todos los usuarios de ese grupo. Los grupos son útiles
para otorgar idénticos permisos a un gran número de usuarios.

Personalizar la interfaz de administración
==========================================

Puedes personalizar el aspecto y la forma en que la interfaz de administración
se comporta de varias maneras. En esta sección sólo vamos a cubrir algunas de
ellas relacionadas con nuestro modelo ``Libro``. El :doc:`Capítulo 17<chapter17>` descubre la
personalización de la interfaz de administración en detalle.

Como estamos ahora, la lista de cambio de nuestros libros sólo muestra la cadena
de representación del modelo que agregamos con el método ``__unicode__``

Esto funciona bien sólo para algunos libros, pero si tuviéramos cientos o miles
de libros, se volvería tan difícil como encontrar una aguja en un pajar. Sin
embargo, fácilmente podremos agregar algunas columnas, funciones de búsqueda y
filtros y a esta interfaz.  Cambia la declaración de ``Admin`` como sigue:

.. code-block:: python

        class Book(models.Model):
            title = models.CharField(maxlength=100)
            authors = models.ManyToManyField(Author)
            publisher = models.ForeignKey(Publisher)
            publication_date = models.DateField()

            class Admin:
                **list_display = ('title', 'publisher', 'publication_date')**
                **list_filter = ('publisher', 'publication_date')**
                **ordering = ('-publication_date',)**
                **search_fields = ('title',)**

Estas cuatro líneas de código cambian dramáticamente la interfaz de nuestra
lista, como se muestra en la figura 6-8.

.. image:: graficos/chapter06/changelist2.png
   :alt: Captura de una lista de cambios modificada.

Figura 6-8. Página de lista de cambios modificada

Cada una de estas líneas indica a la interfaz de administración que construya
diferentes piezas de la interfaz:

    * La opción ``list_display`` controla que columnas aparecen en la tabla de
      la lista.  Por defecto, la lista de cambios muestra una sola columna que
      contiene la representación en cadena de caracteres del objeto. Aquí
      podemos cambiar eso para mostrar el título, el editor y la fecha de
      publicación.


    * La opción ``list_filter`` crea una barra de filtrado del lado derecho de
      la lista.  Estaremos habilitados a filtrar por fecha (que te permite ver
      sólo los libros publicados la última semana, mes, etc.)  y por editor.

      Puedes indicarle a la interfaz de administración que filtre por cualquier
      campo, pero las claves foráneas, fechas, booleanos, y campos con un
      atributo de opciones ``choices`` son las que mejor funcionan. Los filtros
      aparecen cuando tienen al menos 2 valores de dónde elegir.

    * La opción ``ordering`` controla el orden en el que los objetos son
      presentados en la interfaz de administración. Es simplemente una lista de
      campos con los cuales ordenar el resultado; anteponiendo un signo menos a
      un campo se obtiene el orden reverso.  En este ejemplo, ordenamos por
      fecha de publicación con los más recientes al principio.

    * Finalmente, la opción ``search_fields`` crea un campo que permite buscar
      texto.  En nuestro caso, buscará el texto en el campo ``título`` (entonces
      podrías ingresar **Django** para mostrar todos los libros con "Django" en
      el título).

Usando estas opciones (y las otras descriptas en el capítulo 17) puedes, con
sólo algunas líneas de código, hacer una interfaz de edición de datos realmente
potente y lista para producción.

Personalizar la apariencia de la interfaz de administración
===========================================================

Claramente, tener la frase "Administración de Django" en la cabecera de cada
página de administración es ridículo. Es sólo un texto de relleno que es fácil
de cambiar, usando el sistema de plantillas de Django. El sitio de
administración de Django está propulsado por el mismo Django, sus interfaces
usan el sistema de plantillas propio de Django. (El sistema de plantillas de
Django fue presentado en el :doc:`Capítulo4<chapter04>`.)

Como explicamos en el :doc:`Capítulo4<chapter04>`, la configuración de ``TEMPLATE_DIRS``
especifica una lista de directorios a verificar cuando se cargan plantillas
Django. Para personalizar las plantillas del sitio de administración,
simplemente copia el conjunto relevante de plantillas de la distribución Django
en uno de los directorios apuntados por ``TEMPLATE_DIRS``.

El sitio de administración  muestra "Administración de Django" en la cabecera
porque esto es lo que se incluye en la plantilla ``admin/base_site.html``.
Por defecto, esta plantilla se encuentra en el directorio de plantillas de
administración de Django, ``django/contrib/admin/templates``, que puedes
encontrar buscando en tu directorio ``site-packages`` de Python, o donde sea que
Django fue instalado. Para personalizar esta plantilla ``base_site.html``, copia
la original dentro de un subdirectorio llamado ``admin`` dentro de cualquier
directorio este usando ``TEMPLATE_DIRS``.  Por ejemplo, si tu
``TEMPLATE_DIRS`` incluye ``"/home/misplantillas"``, entonces copia
``django/contrib/admin/templates/admin/base_site.html`` a
``/home/misplantillas/admin/base_site.html``.  No te olvides del subdirectorio
``admin``.

Luego, sólo edita el nuevo archivo ``admin/base_site.html`` para reemplazar el
texto genérico de Django, por el nombre de tu propio sitio, tal como lo quieres
ver.

Nota que cualquier plantilla por defecto de Django Admin puede ser reescrita.
Para reescribir una plantilla, haz lo mismo que hicimos con ``base_site.html``:
copia esta desde el directorio original a tu directorio personalizado y haz los
cambios sobre esta copia.

Puede que te preguntes cómo, si ``TEMPLATE_DIRS`` estaba vació al principio,
Django encuentra las plantillas por defecto de la interfaz de administración. La
respuesta es que, por defecto, Django automáticamente busca plantillas dentro
del subdirectorio ``templates/`` de cada paquete de aplicación como alternativa.
Mira el :doc:``capítulo 10 <chapter10>`` para obtener más información sobre cómo funciona esto.

Personalizar la página índice del administrador
===============================================

En una nota similar, puedes tener la intención de personalizar la apariencia (el
*look & feel*) de la página principal del administrador. Por defecto, aquí se
muestran todas las aplicaciones, de acuerdo a la configuración que tenga
``INSTALLED_APPS``, ordenados por el nombre de la aplicación. Quizás quieras,
por ejemplo, cambiar el orden para hacer más fácil ubicar determinada aplicación
que estás buscando.  Después de todo, la página inicial es probablemente la más
importante de la interfaz de administración, y debería ser fácil utilizarla.

La plantilla para personalizarla es ``admin/index.html``. (Recuerda copiar
``admin/index.html`` a tu directorio de plantillas propio como en el ejemplo
previo). Edita el archivo, y verás que usa una etiqueta llamada ``{%
get_admin_app_list as app_list %}``. Esta etiqueta devuelve todas las
aplicaciones Django instaladas. En vez de usar esta etiqueta, puedes incluir
vínculos explícitos a objetos específicos de la manera que creas más
conveniente.  Si el código explícito en una plantilla no te satisface, puedes ver
el :doc:`Capítulo 10<chapter10>` para encontrar detalles sobre cómo implementar tu propias
etiquetas de plantillas.

Para detalles completos sobre la personalización del sitio de administración de
Django, mira el :doc:`Capítulo 17<chapter17>`.

Cuándo y porqué usar la interfaz de administración
==================================================

Pensamos que la interfaz de administración de Django es bastante espectacular.
De hecho, diríamos que es una de sus *killer feautures*, o sea, una de sus
características sobresalientes. Sin embargo, a menudo nos preguntan sobre "casos
de uso" para la interfaz de administración (¿Cuándo debemos usarlo y por qué?).
A lo largo de los años, hemos descubierto algunos patrones donde pensamos que
usar la interfaz de administración resulta útil.

Obviamente, es muy útil para modificar datos (se veía venir). Si tenemos
cualquier tipo de tarea de introducción de datos, el administrador es difícil de
superar. Sospechamos que la gran mayoría de lectores de este libro tiene una
horda de tareas de este tipo.

La interfaz de administración de Django brilla especialmente cuando usuarios no
técnicos necesitan ser capaces de ingresar datos; ese es el propósito detrás de
esta característica, después de todo. En el periódico donde Django fue creado
originalmente, el desarrollo de una característica típica online -- un reporte
especial sobre la calidad del agua del acueducto municipal, supongamos
-- implicaba algo así:

    * El periodista responsable del artículo se reúne con uno de los
      desarrolladores y discuten sobre la información disponible.

    * El desarrollador diseña un modelo basado en esta información y luego abre
      la interfaz de administración para el periodista.

    * Mientras el periodista ingresa datos a Django, el programador puede
      enfocarse en desarrollar la interfaz accesible públicamente (¡la parte
      divertida!).

En otras palabras, la razón de ser de la interfaz de administración de Django es
facilitar el trabajo simultáneo de productores de contenido y programadores.

Sin embargo, más allá de estas tareas de entrada de datos obvias, encontramos
que la interfaz de administración es útil en algunos otros casos:

    * *Inspeccionar modelos de datos*: La primer cosa que hacemos cuando hemos
      definido un nuevo modelo es llamarlo desde la interfaz de administración e
      ingresar algunos datos de relleno. Esto es usual para encontrar errores de
      modelado; tener una una interfaz gráfica al modelo revela problemas
      rápidamente.


    * *Gestión de datos adquiridos*: Hay una pequeña entrada de datos asociada a
      un sitio como ``http://chicagocrime.org``, puesto que la mayoría de los
      datos provienen de una fuente automática. No obstante, cuando surgen
      problemas con los datos automáticos, es útil poder entrar y editarlos
      fácilmente.

¿Qué sigue?
===========

Hasta ahora hemos creado algunos modelos y configurado una interfaz de primera
clase para modificar datos. En el :doc:`próximo capítulo<chapter07>`, nos meteremos en el
verdadero guiso del desarrollo Web: creación y procesamiento de formularios.

.. [#] \N. del T.: *change list* es el nombre que recibe en inglés
.. [#] \N. del T.: *edit forms* es el nombre que recibe en inglés
.. [#] \N. del T.: En el control de selección de permisos aparece como *Can add*
.. [#] \N. del T.: *Can change*
.. [#] \N. del T.: *Can delete*
