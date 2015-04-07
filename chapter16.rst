﻿===========================
Capítulo 16: django.contrib
===========================

Una de las muchas fortalezas de Python, es su filosofía de **baterías
incluidas**. Cuando instalas Python, viene con una amplia biblioteca de
paquetes que puedes comenzar a usar inmediatamente, sin necesidad de descargar
nada más. Django trata de seguir esa filosofía, e incluye su propia biblioteca
estándar de agregados útiles para realizar las tareas más comunes del desarrollo
web. Este capítulo cubre la colección de agregados, agrupados en el paquete
llamado ``django.contrib``.

La biblioteca estándar de Django
================================

La biblioteca estándar de Django se localiza en el paquete ``django.contrib``.
Dentro de cada sub-paquete hay una pieza aislada de funcionalidad para agregar.
Estas piezas no están necesariamente relacionadas, pero algunos sub-paquetes de
``django.contrib`` pueden requerir de otros.

No hay grandes requerimientos para los tipos de funcionalidad que hay en
``django.contrib``. Algunos de los paquetes incluyen modelos (y por lo tanto
requieren que instales sus tablas en tu base de datos), pero otros consisten
solamente de *middleware* o de etiquetas de plantillas (*template tags*).

La única característica común a todos los paquetes de ``django.contrib`` es
la siguiente: si borraras dicho paquete por completo, seguirías pudiendo usar
las capacidades fundamentales de Django sin problemas. Cuando los
desarrolladores de Django agregan nueva funcionalidad al *framework*, emplean
esa regla de oro al decidir en dónde va a residir la nueva funcionalidad, si en
``django.contrib``, o en algún otro lugar.

``django.contrib`` consiste de los siguientes paquetes:

* ``admin``: el sitio automático de administración. Consulta el capítulo 6.

* ``admindocs``: La autodocumentación para el sitio administrativo.

* ``auth``: el *framework* de autenticación de Django. Consulta el
  :doc:`capítulo 14<chapter14>`.

* ``contenttypes``: un *framework* para conectar "tipos" de   contenido, en que
  cada modelo de Django instalado es un tipo de contenido aislado. Este
  *framework* es usado internamente por otras aplicaciones "contrib", y está
  especialmente enfocada a los desarrolladores de Django muy avanzados. Dichos
  desarrolladores pueden hallar más información sobre esta aplicación, leyendo
  el código fuente que está en   ``django/contrib/contenttypes/``.

* ``csrf``: protección ante un ataque de falsificación de petición
  en sitios cruzados, en inglés *Cross-Site Request Forgery*
  (CSRF). Consulta la sección titulada "`Protección contra CSRF`_" más adelante.

* ``flatpages``: un *framework* para administrar contenido HTML simple, "plano",
  dentro de la base de datos. Consulta la sección titulada "`Flatpages`_" más
  adelante.

* ``humanize``: un conjunto de filtros de plantillas Django, útiles para
  darle un "toque de humanidad" a los datos. Consulta la sección titulada
  "`Humanizando datos`_" más adelante.

* ``gis``: Extencion para Django que provee soporte para GIS (Sistema de
  Información Geográfica). Permite a los modelos de Django, por ejemplo
  almacenar datos  geográficos y optimizar consultas geográficas. Esta es una
  larga y compleja librería, consulta mas detalles en: http://geodjango.org/

* ``redirects``: un *framework* para administrar redirecciones. Consulta la
  sección titulada "`Redirects`_" más adelante.

* ``sessions``: el *framework* de sesiones de Django. Consulta el
  :doc:`capítulo 12<chapter12>`.

* ``sitemaps``: un *framework* para generara archivos de mapas de sitio XML.
  Consulta él :doc:`capítulo 13<chapter13>`.

* ``sites``: un *framework* que te permite operar múltiples sitios  web desde
  la misma base de datos, y con una única instalación de Django.

* ``syndication``: un *framework* para generar documentos de sindicación
  (*feeds*), en RSS y en Atom. Consulta él :doc:`capítulo 13<chapter13>`.

* ``webdesign``: Agregados en Django, particularmente útiles en el *diseño* Web
  más que en el desarrollo. Este incluye únicamente una etiqueta ``{% lorem %}``.
  que permite escribir texto en las plantillas.

El resto de este capítulo entra en los detalles de cada paquete
``django.contrib`` que no ha sido cubierto aún en este libro.

Sites
=====

El sistema *sites* (sitios) de Django es un *framework* genérico que te permite
operar múltiples sitios Web desde la misma base de datos, y desde el mismo
proyecto de Django. Éste es un concepto abstracto, y puede ser difícil de
entender, así que  comenzaremos mostrando algunos escenarios en donde sería
útil usarlo.

Escenario 1: rehusó de datos en múltiples sitios
------------------------------------------------

Como explicamos en capítulos anteriores, los sitios LJWorld.com y Lawrence.com,
que funcionan gracias a Django, son operados por la misma organización de
prensa, el diario *Lawrence Journal-World* de Lawrence, Kansas. LJWorld.com se
enfoca en noticias, mientras que Lawrence.com se enfoca en el entretenimiento
local. Pero a veces los editores quieren publicar un artículo en *ambos* sitios.

La forma tonta de resolver el problema sería usar una base de datos para cada
sitio, y pedirle a los productores que publiquen la misma nota dos veces: una
para LJWorld.com y nuevamente para Lawrence.com. Pero esto es ineficiente para
los productores del sitio, y es redundante conservar múltiples copias de la
misma nota en las bases de datos.

¿Una solución mejor? Que ambos sitios usen la misma base de datos de artículos,
y que un artículo esté asociado con uno o más sitios por una relación de
muchos-a-muchos. El *framework* *sites* de Django, proporciona la tabla de base
de datos que hace que los artículos se puedan relacionar de esta forma. Sirve
para asociar datos con uno o más "sitios".

Escenario 2: alojamiento del nombre/dominio de tu sitio en un solo lugar
------------------------------------------------------------------------

Los dos sitios LJWorld.com y Lawrence.com, tienen la funcionalidad de alertas
por correo electrónico, que les permite a los lectores registrarse para obtener
notificaciones. Es bastante básico: un lector se registra en un formulario web,
e inmediatamente obtiene un correo electrónico que dice "Gracias por su
suscripción".

Sería ineficiente y redundante implementar el código del procesamiento de
registros dos veces, así que los sitios usan el mismo código detrás de escena.
Pero la noticia "Gracias por su suscripción" debe ser distinta para cada sitio,
empleando objetos ``Site``, podemos abstraer el agradecimiento para usar los
valores del nombre y dominio del sitio, variables ``name`` (ejemplo: ``'LJWorld.com'``)
y ``domain`` (ejemplo: ``'www.ljworld.com'``).

El *framework* *sites* te proporciona un lugar para que puedas almacenar el
nombre (``name``) y el dominio (``domain``) de cada sitio de tu proyecto, lo
que significa que puedes reutilizar estos valores de manera genérica.

Como usar el framework sites
----------------------------

``Sites`` más que un *framework*, es una serie de convenciones. Toda la cosa se
basa en dos conceptos simples:

* el modelo ``Site``, que se halla en ``django.contrib.sites``, tiene los
  campos ``domain`` y ``name``.

* la opción de configuración ``SITE_ID`` especifica el ID de la base de datos
  del objeto ``Site`` asociado con este archivo de  configuración en particular.

La manera en que uses estos dos conceptos queda a tu criterio, pero Django los
usa de varios modos de manera automática, siguiendo convenciones simples.

Para instalar la aplicación *sites*, sigue estos pasos:

1. Agrega ``'django.contrib.sites'`` a tu ``INSTALLED_APPS``.

2. Ejecuta el comando ``manage.py makemigartiones`` y ``manage.py migrate``
   para instalar la tabla ``django_site`` en tu base de datos.

3. Agrega uno o más objetos ``Site``, por medio del sitio de administración de
   Django, o por medio de la API de Python. Crea un objeto ``Site`` para cada
   sitio/dominio que esté respaldado por este proyecto Django.

4. Define la opción de configuración ``SITE_ID`` en cada uno de tus archivos de
   configuración (*settings*). Este valor debería ser el ID de base de datos
   del objeto ``Site`` para el sitio respaldado por el archivo de configuración.

Las capacidades del framework Sites
-----------------------------------

Las siguientes secciones describen las cosas que puedes hacer con este
*framework*

Rehusó de datos en múltiples sitios
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Para rehusar los datos en múltiples sitios, como explicamos en el primer
escenario, simplemente debes agregarle un campo muchos-a-muchos,
``ManyToManyField`` hacia ``Site`` en tus modelos. Por ejemplo:

.. code-block:: python

    from django.db import models
    from django.contrib.sites.models import Site

    class Libro(models.Model):
      titulo = models.CharField(max_length=100)
      autores = models.ManyToManyField(Autor)
      # ...
      sites = models.ManyToManyField(Site)

Esa es toda la infraestructura necesaria para asociar el modelo ``Libro`` con
múltiples sitios en tu base de datos. Con eso en su lugar, puedes rehusar el
mismo código de vista para múltiples sitios. Continuando con el modelo ``Libro``
del ejemplo, aquí mostramos cómo luciría una vista ``detalles_libro``::

    from django.conf import settings
    from biblioteca.models import Libro

    def detalles_libro(request, libro_pk):
        try:
            libro = Libro.objects.get(pk=libro_pk, sites__id=settings.SITE_ID)
        except Libro.DoesNotExist:
            raise Http404
        return render_to_response('biblioteca/detalles_libro.html', {'libro': libro})

Esta función de vista es reusable porque comprueba el sitio del artículo
dinámicamente, según cuál sea el valor de la opción ``SITE_ID``.

Por ejemplo, digamos que el archivo de configuración de LJWorld.com tiene un
``SITE_ID`` asignado a ``1``, y que el de Lawrence.com lo tiene asignado a ``2``.
Si esta vista es llamada cuando el archivo de configuración de LJWorld.com está
activado, entonces la búsqueda de artículos se limita a aquellos en que la lista
de sitios incluye LJWorld.com.

Asociación de contenido con un solo sitio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

De manera similar, puedes asociar un modelo con el modelo ``Site`` en una
relación muchos-a-uno, usando ``ForeignKey``.

Por ejemplo, si un artículo sólo se permite en un sitio, puedes usar
un modelo como este::

    from django.db import models
    from django.contrib.sites.models import Site

    class Libro(models.Model):
      titulo = models.CharField(max_length=100)
      autores = models.ManyToManyField(Autor)
      # ...
      sites = models.ForeignKey(Site)

Este tiene los mismos beneficios, como se describe en la última
sección..

Obtención del sitio actual desde las vistas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A un nivel más bajo, puedes usar el *framework sites* en tus vistas de
Django para hacer cosas particulares, según el sitio en el cual la vista sea
llamada. Por ejemplo::

    from django.conf import settings

    def mi_vista(request):
        if settings.SITE_ID == 3:
            # Haz algo.
        else:
            # Haz otra cosa.

Por supuesto, es horrible meter el ID en el código del sitio de esa manera.
Una forma levemente más limpia de lograr lo mismo, es comprobar el dominio
actual del sitio::

    from django.conf import settings
    from django.contrib.sites.models import Site

    def mi_vista(request):
        sitio_actual = Site.objects.get(id=settings.SITE_ID)
        if sitio_actual.domain == 'foo.com':
            # Haz algo.
        else:
            # Haz otra cosa.

Este fragmento de código usado para obtener el objeto ``Site`` según el valor
de ``settings.SITE_ID`` es tan usado, que el manejador de modelos de ``Site``
(``Site.objects``) tiene un método ``get_current()``. El siguiente ejemplo es
equivalente al anterior::

    from django.contrib.sites.models import Site

    def mi_vista(request):
        sitio_actual = Site.objects.get_current()
        if sitio_actual.domain == 'foo.com':
             # Haz algo.
        else:
            # Haz otra cosa.

.. admonition:: Nota:

    Observa que en este último ejemplo, no hay necesidad de importar
    ``django.conf.settings``.

Obtención del dominio actual para ser mostrado
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Una forma DRY (acrónimo del inglés *Don't Repeat Yourself*, "no te repitas") de
guardar el nombre del sitio y del dominio, como explicamos en "Escenario 2:
alojamiento del nombre/dominio de tu sitio en un solo lugar", se logra
simplemente haciendo referencia a ``name`` y a ``domain`` del objeto ``Site``
actual. Por ejemplo::

    from django.contrib.sites.models import Site
    from django.core.mail import send_mail

    def registrar_para_boletines(request):
        # Verifica los valores del formulario, etc., y suscribe al usuario.
        # ...
        sitio_actual = Site.objects.get_current()
        send_mail('Gracias por suscribirse a %s alertas' % sitio_actual.name,
            'Gracias por suscribirse. Se lo agradecemos.\n\n-El %s equipo.' % sitio_actual.name,
            'editor@%s' % sitio_actual.domain,
            [user_email])
        # ...

Continuando con nuestro ejemplo de LJWorld.com y Lawrence.com, en Lawrence.com
el correo electrónico tiene como sujeto la línea "Gracias por suscribirse a las
alertas de lawrence.com". En LJWorld.com, en cambio, el sujeto es "Gracias por
suscribirse a las alertas de LJWorld.com". Este comportamiento específico para
cada sitio, también se aplica al cuerpo del correo electrónico.

Una forma aún más flexible (aunque un poco más pesada) de hacer lo mismo, es
usando el sistema de plantillas de Django. Asumiendo que Lawrence.com y
LJWorld.com tienen distintos directorios de plantillas (``TEMPLATE_DIRS``),
puedes simplemente delegarlo al sistema de plantillas así::

    from django.core.mail import send_mail
    from django.template import loader, Context

    def registrar_para_boletines(request):
        # Verifica los valores del formulario, etc., y suscribe al usuario.
        # ...
        asunto = loader.get_template('alertas/asunto.txt').render(Context({}))
        mensaje = loader.get_template('alertas/mensaje.txt').render(Context({}))
        send_mail(asunto, mensaje, 'do-not-reply@example.com', [user_email])
        # ...

En este caso, debes crear las plantillas ``asunto.txt`` y ``mensaje.txt`` en
ambos directorios de plantillas, el de LJWorld.com y el de Lawrence.com . Como
mencionamos anteriormente, eso te da más flexibilidad, pero también es más complejo.

Una buena idea es explotar los objetos ``Site`` lo más posible, para que no
haya complejidad y redundancia innecesaria.

Obtención del dominio actual para las URLs completas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La convención de Django de usar ``get_absolute_url()`` para obtener las URLs de
los objetos sin el dominio, está muy bien. Pero en algunos casos puedes
querer mostrar la URL completa -- con ``http://`` y el dominio, y todo -- para
un objeto. Para hacerlo, puedes usar el *framework* *sites*. Este es un ejemplo::

    >>> from django.contrib.sites.models import Site
    >>> from biblioteca.models import Libro
    >>> obj = Libro.objects.get(id=3)
    >>> obj.get_absolute_url()
    '/detalle/libro/3/'
    >>> Site.objects.get_current().domain
    'localhost:9000'
    >>> 'http://%s%s' % (Site.objects.get_current().domain, obj.get_absolute_url())
    'http://localhost:9000/detalle/libro/3/'

El manejador CurrentSiteManager
-------------------------------

Si el modelo ``Site`` juegan roles importantes en tu aplicación, considera el
uso del útil manejador llamado: ``CurrentSiteManager`` en tu modelo (o modelos).
Es un administrador de modelos (consulta el Apéndice B) que filtra
automáticamente sus consultas para incluir sólo los objetos asociados
al ``Site`` actual.

Usa ``CurrentSiteManager`` agregándolo a tu modelo explícitamente. Por
ejemplo:

.. code-block:: python

    from django.db import models
    from django.contrib.sites.models import Site
    from django.contrib.sites.managers import CurrentSiteManager

    class Libro(models.Model):
      titulo = models.CharField(max_length=100)
      autores = models.ManyToManyField(Autor)
      # Agregamos una relacion foranea a "Sites"
      sites = models.ForeignKey(Site)
      # El manejador por defecto.
      objects = models.Manager()
      # Agregamos el manejador para "Sites"
      mi_sitio = CurrentSiteManager()


Con este modelo, ``Libro.objects.all()`` retorna todos los objetos ``Libro`` de
la base de datos, pero ``Libro.mi_sitio.all()`` retorna sólo los objetos
``Libro`` asociados con el sitio actual, de acuerdo a la opción de configuración
``SITE_ID``.

En otras palabras, estas dos sentencias son equivalentes::

    Libro.objects.filter(site=settings.SITE_ID)
    Libro.mi_sitio.all()

¿Cómo supo ``CurrentSiteManager`` cuál campo de ``Libro`` era el ``Site``?  Por
defecto busca un campo llamado ``site``. Si tu modelo tiene un campo
``ForeignKey`` o un campo ``ManyToManyField`` llamado de otra forma que
``site``, debes pasarlo explícitamente como el parámetro para
``CurrentSiteManager``.

El modelo a continuación,  tiene un campo llamado ``publicado_en``, como lo
demuestra el siguiente ejemplo::

    from django.db import models
    from django.contrib.sites.models import Site
    from django.contrib.sites.managers import CurrentSiteManager

    class Libro(models.Model):
      titulo = models.CharField(max_length=100)
      autores = models.ManyToManyField(Autor)
      # Agregamos una relacion foranea  usando otro nombre  en lugar de "sites"
      publicado_en = models.ForeignKey(Site)
      # El manejador por defecto.
      objects = models.Manager()
      # Agregamos al manejador el nombre del campo: "Sites"
      mi_sitio = CurrentSiteManager('publicado_en')

Si intentas usar ``CurrentSiteManager`` y pasarle un nombre de campo que no
existe, Django lanzará un error del tipo: ``ValueError``.

.. admonition:: Nota:

    Probablemente querrás tener un ``Manager`` normal (no específico al sitio)
    en tu modelo, incluso si usas ``CurrentSiteManager``. Como se explica en el
    Apéndice B, si defines un *manager* manualmente, Django no creará
    automáticamente el *manager* ``objects = models.Manager()``.

    Además, algunas partes de Django -- el sitio de administración y las vistas
    genéricas -- usan el *manager* que haya sido definido *primero* en el
    modelo. Así que si quieres que el sitio de administración tenga acceso a
    todos los objetos (no sólo a los específicos al sitio actual), pon un
    ``objects = models.Manager()`` en tu modelo, antes de definir
    ``CurrentSiteManager``.

Si utilizas a menudo esta configuración, en lugar de hacer esto en tus vistas:

.. code-block:: python

    from django.contrib.sites.models import Site

    def mi_vista(request):
        site = Site.objects.get_current()
        ...

Existe una manera simple de evitar repeticiones. Usando Middleware, solo agrega
``django.contrib.sites.middleware.CurrentSiteMiddleware`` a la variable
``MIDDLEWARE_CLASSES``. El middleware se encarga de configurar estos atributos
en cada petición de un objeto,  por lo que puedes usar ``request.site`` para
obtener el sitio actual.

Cómo utiliza Django el *framework* Sites
----------------------------------------

Si bien no es necesario que uses el *framework* *sites*, es extremadamente
recomendado, porque Django toma ventaja de ello en algunos lugares. Incluso si
tu instalación de Django está alimentando a un solo sitio, deberías tomarte unos
segundos para crear el objeto *site* con tu ``domain`` y ``name``, y apuntar su
ID en tu opción de configuración ``SITE_ID``.

Este es el uso que hace Django del *framework* *sites*:

* En el *framework* *redirects* (consulta la sección "`Redirects`_" más
  adelante), cada objeto *redirect* está asociado con un sitio en
  particular. Cuando Django busca un *redirect*, toma en cuenta el
  ``SITE_ID`` actual.

* En el *framework* *flatpages* (consulta la sección "`Flatpages`_" más
  adelante), cada página es asociada con un sitio en particular. Cuando una
  página es creada, tú especificas su ``site``, y el *middleware* de
  *flatpage* chequea el ``SITE_ID`` actual cuando se traen páginas para ser
  mostradas.

* En el *framework* *syndication* (consulta el :doc:`capítulo 13<chapter13>`.),
  las plantillas para ``title`` y ``description`` tienen acceso automático a la
  variable ``{{ site }}``, que es el objeto ``Site`` que representa al sitio
  actual. Además, la conexión para proporcionar las URLs de los elementos usan
  el ``domain`` desde el objeto ``Site`` actual si no especificas un nombre de
  dominio.

* En el *framework* *authentication* (consulta el :doc:`capítulo 14<chapter14>`.),
  la vista ``django.contrib.auth.views.login`` le pasa el nombre del ``Site``
  actual a la plantilla como ``{{ site_name }}``.

Flatpages
=========

A menudo tendrás una aplicación Web impulsada por bases de datos ya funcionando,
pero necesitarás agregar un par de páginas estáticas, tales como una página
*Acerca de* o una página de Política de Privacidad. Sería posible usar un
servidor Web estándar como por ejemplo Apache para servir esos archivos como
archivos HTML planos, pero eso introduce un nivel extra de complejidad en tu
aplicación, porque entonces tienes que preocuparte de la configuración de
Apache, tienes que preparar el acceso para que tu equipo pueda editar esos
archivos, y no puedes sacar provecho del sistema de plantillas de Django para
darle estilo a las páginas.

La solución a este problema es la aplicación flatpages de Django, la cual
reside en el paquete ``django.contrib.flatpages``. Esta aplicación te permite
manejar esas páginas aisladas mediante el sitio de administración de Django, y
te permite especificar plantillas para las mismas usando el sistema de
plantillas de Django. Detrás de escena usa modelos Django, lo que significa que
almacena las páginas en una base de datos, de la misma manera que el resto de
tus datos, y puedes acceder a las flatpages con la API de bases de datos
estándar de Django.

Las flatpages son identificadas por su URL y su sitio. Cuando creas una
flatpage, especificas con cual URL está asociada, junto con en cuál(es) sitio(s)
está (para más información acerca de sitios, consulta la sección "`Sites`_").

Usar flatpages
--------------

Para instalar la aplicación flatpages, sigue estos pasos:

1. Agrega ``'django.contrib.flatpages'`` a tu ``INSTALLED_APPS``.
   ``django.contrib.flatpages`` depende de ``django.contrib.sites``, asique
   asegúrate de que ambos paquetes se encuentren en ``INSTALLED_APPS``.

2. Agrega ``'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'``
   a tu variable de configuración ``MIDDLEWARE_CLASSES``.

3. Ejecuta el comando ``manage.py migrate`` para instalar las dos tablas
   necesarias en tu base de datos.

La aplicación flatpages crea dos tablas en tu base de datos: ``django_flatpage``
y ``django_flatpage_sites``. ``django_flatpage`` simplemente mantiene una
correspondencia entre URLs y títulos más contenido de texto.
``django_flatpage_sites`` es una tabla muchos a muchos que asocia una flatpage
con uno o más sitios.

La aplicación incluye un único modelo ``FlatPage``, definido en
``django/contrib/flatpages/models.py``. El mismo se ve así::

    from django.db import models
    from django.contrib.sites.models import Site

    class FlatPage(models.Model):
        url = models.CharField(maxlength=100)
        title = models.CharField(maxlength=200)
        content = models.TextField()
        enable_comments = models.BooleanField()
        template_name = models.CharField(maxlength=70, blank=True)
        registration_required = models.BooleanField()
        sites = models.ManyToManyField(Site)

Examinemos cada uno de los campos:

* ``url``: La URL donde reside esta flatpage, excluyendo el nombre del
  dominio pero incluyendo la barra (``/``) inicial (por ej.
  ``/about/contact/``).

* ``title``: El título de la flatpage. El framework no usa esto para nada en
  especial. Es tu responsabilidad visualizarlo en tu plantilla.

  ``content``: El contenido de la flatpage (por ej. el HTML de la página).
  El framework no usa esto para nada en especial. Es tu responsabilidad
  visualizarlo en tu plantilla.

* ``enable_comments``: Indica si deben activarse los comentarios e esta
  flatpage. El framework no usa esto para nada en especial. Puedes comprobar
  este valor en tu plantilla y mostrar un formulario de comentario si es
  necesario.

* ``template_name``: El nombre de la plantilla a usarse para renderizar esta
  flatpage. Es opcional; si no se indica o si esta plantilla no existe, el
  framework usará la plantilla ``flatpages/default.html``.

* ``registration_required``: Indica si se requerirá registro para ver esta
  flatpage. Esto se integra con el framework de autenticación/usuarios de
  Django, el cual se trata en él :doc:`capítulo 12<chapter12>`.

* ``sites``: Los sitios en los cuales reside esta flatpage. Esto se integra
  con el framework sites de Django, el cual se trata en la sección "`Sites`_"
  en este capítulo.

Puedes crear flatpages ya sea a través de la interfaz de administración de
Django o a través de la API de base de datos de Django. Para más información,
examina la sección "`Agregando, modificando y eliminando flatpages`".

Una vez que has creado flatpages, ``FlatpageFallbackMiddleware`` se encarga de
todo el trabajo. Cada vez que cualquier aplicación Django lanza un error, este
middleware verifica como último recurso la base de datos de flatpages en
búsqueda de la URL que se ha requerido.  Específicamente busca una flatpage con
la URL en cuestión y con un identificador de sitio que coincida con la variable
de configuración ``SITE_ID``.

Si encuentra una coincidencia, carga la plantilla de la flatpage, o
``flatpages/default.html`` si la flatpage no ha especificado una plantilla
personalizada. Le pasa a dicha plantilla una única variable de contexto:
``flatpage``, la cual es el objeto flatpage. Usa ``RequestContext`` para
renderizar la plantilla.

Si ``FlatpageFallbackMiddleware`` no encuentra una coincidencia, el proceso de
la petición continúa normalmente.

.. admonition:: Nota:

    Este middleware sólo se activa para errores 404 (página no encontrada) -- no
    para errores 500 (error en servidor) u otras respuestas de error. Nota
    también que el orden de ``MIDDLEWARE_CLASSES`` es relevante. Generalmente,
    puedes colocar el ``FlatpageFallbackMiddleware`` cerca o en el final de la
    lista, debido a que se trata de una opción de último recurso.

Agregar, modificar y eliminar flatpages
---------------------------------------

Puedes agregar, cambiar y eliminar flatpages de dos maneras:

A través de la interfaz de administración
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si has activado la interfaz automática de administración de Django, deberías
ver una sección "Flatpages" en la página de índice de la aplicación admin. Edita
las flatpages como lo harías con cualquier otro objeto en el sistema.

A través de la API Python
~~~~~~~~~~~~~~~~~~~~~~~~~

Como ya se describió, las flatpages se representan mediante un modelo Django
estándar que reside en ``django/contrib/flatpages/models.py``. Por lo tanto
puede acceder a objetos flatpage mediante la API de base de datos Django, por
ejemplo::

    >>> from django.contrib.flatpages.models import FlatPage
    >>> from django.contrib.sites.models import Site
    >>> fp = FlatPage(
    ...     url='/about/',
    ...     title='About',
    ...     content='<p>About this site...</p>',
    ...     enable_comments=False,
    ...     template_name='',
    ...     registration_required=False,
    ... )
    >>> fp.save()
    >>> fp.sites.add(Site.objects.get(id=1))
    >>> FlatPage.objects.get(url='/about/')
    <FlatPage: /about/ -- About>

Usar plantillas de flatpages
----------------------------

Por omisión, las flatpages son renderizadas vía la plantilla
``flatpages/default.html``, pero puedes cambiar eso para cualquier flatpage  con
el campo ``template_name`` en el objeto ``FlatPage``.

Es tu responsabilidad el crear la plantilla ``flatpages/default.html``. En tu
directorio de plantillas, crea un directorio ``flatpages`` que contenga un
archivo ``default.html``.

A las plantillas de flatpages se les pasa una única variable de contexto:
``flatpage``, la cual es el objeto flatpage.

Este es un ejemplo de una plantilla ``flatpages/default.html``:

.. code-block:: python

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"
        "http://www.w3.org/TR/REC-html40/loose.dtd">
    <html>
    <head>
    <title>{{ flatpage.title }}</title>
    </head>
    <body>
    {{ flatpage.content }}
    </body>
    </html>

Redirects
=========

El framework redirects de Django te permite administrar las redirecciones con
facilidad almacenándolos en una base de datos y tratándolos como cualquier otro
objeto modelo de Django. Por ejemplo puedes usar el framework redirects para
indicarle a Django "Redirecciona cualquier petición de ``/music/`` a
``/sections/arts/music/``.". Esto es útil cuando necesitas cambiar las cosas de
lugar en tu sitio; los desarrolladores Web deberían hacer lo que esté en sus
manos para evitar los enlaces rotos.

Usar el framework redirects
---------------------------

Para instalar la aplicación redirects, sigue estos pasos:

1. Agrega ``'django.contrib.redirects'`` a tu ``INSTALLED_APPS``.

2. Agrega ``'django.contrib.redirects.middleware.RedirectFallbackMiddleware'``
   a tu variable de configuración ``MIDDLEWARE_CLASSES``.

3. Ejecuta el comando ``manage.py syncdb`` para instalar la única tabla
   necesaria a tu base de datos.

``manage.py syncdb`` crea una tabla ``django_redirect`` en tu base de datos.
Esta se trata sencillamente de una tabla de búsqueda con campos ``site_id``,
``old_path`` y ``new_path``.

Puedes crear redirecciones tanto a través de la interfaz de administración como
a través de la API de base de datos de Django. Para más información puedes leer
la sección "`Agregar, modificar y eliminar redirecciones`_".

Una vez que has creado redirecciones, la clase ``RedirectFallbackMiddleware`` se
encarga de todo el trabajo. Cada vez que cualquier aplicación Django lanza un
error 404, este middleware verifica como último recurso la base de datos de
redirects en búsqueda de la URL que se ha requerido.  Específicamente busca un
redirect con el ``old_path`` provisto y con un identificador de sitio que
coincida con la variable de configuración ``SITE_ID``. (para más información
acerca de ``SITE_ID`` y el framework sites, consulta la sección "`Sites`_").

Luego entonces realiza los siguientes pasos:

* Si encuentra una coincidencia y ``new_path`` no está vacío, redirecciona
  la petición a ``new_path``.

* Si encuentra una coincidencia y ``new_path`` está vació, envía una
  cabecera HTTP 410 ("Ausente") y una respuesta vacía (sin contenido).

* Si no encuentra una coincidencia, el procesamiento de la petición continúa
  normalmente.

El middleware sólo se activa ante errores 404 -- no en errores 500 o respuestas
con otros códigos de estado.

Notar que el orden de ``MIDDLEWARE_CLASSES`` es relevante. Generalmente puedes
colocar ``RedirectFallbackMiddleware`` cerca del final de la lista, debido a que
se trata de una opción de último recurso.

.. admonition:: Nota:

    Si usas los middlewares redirect y flatpages, analiza cual de los dos
    (redirect o flatpages) desearías sea ejecutado primero. Sugerimos configurar
    flatpages antes que redirects (o sea colocar el middleware flatpages antes
    que el middleware redirects) pero tú podrías decidir lo contrario.

Agregar, modificar y eliminar redirecciones
-------------------------------------------

Puedes agregar, modificar y eliminar redirecciones de dos maneras:

A través de la interfaz de administración
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si has activado la interfaz automática de administración de Django, deberías
ver una sección "Redirects" en la página de índice de la aplicación admin. Edita
las redirecciones como lo harías con cualquier otro objeto en el sistema.

A través de la API Python
~~~~~~~~~~~~~~~~~~~~~~~~~

Las redirecciones se representan mediante un modelo estándar Django que reside
en ``django/contrib/redirects/models.py``. Por lo tanto puedes acceder a los
objetos redirect vía la API de base de datos de Django, por ejemplo::

    >>> from django.contrib.redirects.models import Redirect
    >>> from django.contrib.sites.models import Site
    >>> red = Redirect(
    ...     site=Site.objects.get(id=1),
    ...     old_path='/musica/',
    ...     new_path='/secccion/artista/musica/',
    ... )
    >>> red.save()
    >>> Redirect.objects.get(old_path='/musica/')
    <Redirect: /music/ ---> /secccion/artista/musica/>

Protección contra CSRF
======================

El paquete ``django.contrib.csrf`` provee protección contra *Cross-site request
forgery* (CSRF) (falsificación de peticiones inter-sitio).

CSRF, también conocido como *"session riding"* (montado de sesiones) es un exploit
de seguridad en sitios Web. Se presenta cuando un sitio Web malicioso induce a
un usuario a cargar sin saberlo una URL desde un sitio al cual dicho usuario ya
se ha autenticado, por lo tanto saca ventaja de su estado autenticado.
Inicialmente esto puede ser un poco difícil de entender así que en esta sección
recorreremos un par de ejemplos.

Un ejemplo simple de CSRF
-------------------------

Supongamos que posees una cuenta de *correo electronico* en ``example.com``.
Este sitio proveedor de *correo* tiene un botón *Log Out*  que apunta a la URL
``example.com/logout`` -- esta es, la única acción que necesitas realizar para
desconectarte (*log out*) es visitar la página ``example.com/logout``.

Un sitio malicioso puede obligarte a visitar la URL ``example.com/logout``
incluyendo esa URL como un ``<iframe>`` oculto en su propia página maliciosa. De
manera que si estás conectado (*logged in*) a tu cuenta de *correo* del sitio
``example.com`` y visitas la página maliciosa, el hecho de visitar la misma te
desconectará de ``example.com``.

Claramente, ser desconectado de un sitio de *correo* contra tu voluntad no es un
incidente de seguridad aterrorizante, pero este tipo de exploit puede sucederle
a *cualquier* sitio que "confía" en sus usuarios, tales como un sitio de un
banco o un sitio de comercio electrónico.

Un ejemplo más complejo de CSRF
-------------------------------

En el ejemplo anterior, el sitio ``example.com`` tenía parte de la culpa debido
a que permitía que se pudiera solicitar un cambio de estado (la desconexión del
sitio) mediante el método HTTP ``GET``. Es una práctica mucho mejor el requerir
el uso de un ``POST`` HTTP para cada petición que cambie el estado en el
servidor. Pero aun los sitios Web que requieren el uso de ``POST`` para acciones
que signifiquen cambios de estado son vulnerables a CSRF.

Supongamos que ``example.com`` ha mejorado su funcionalidad de desconexión  de
manera que "Log Out" es ahora un botón de un ``<form>`` que es enviado vía un
``POST`` a la URL ``example.com/logout``. Adicionalmente, el ``<form>`` de
desconexión incluye un campo oculto::

    <input type="hidden" name="confirm" value="true" />

Esto asegura que un simple ``POST`` a la URL ``example.com/logout`` no
desconectará a un usuario; para que los usuarios puedan desconectarse, deberán
enviar una petición a ``example.com/logout`` usando ``POST`` *y* enviar la
variable ``POST`` ``confirm`` con el valor ``'true'``.

Bueno, aun con dichas medidas extra de seguridad, este esquema también puede ser
atacado mediante CSRF -- la página maliciosa sólo necesita hacer un poquito
más de trabajo. Los atacantes pueden crear un formulario completo que envíe su
petición a tu sitio, ocultar el mismo en un ``<iframe>`` invisible y luego usar
JavaScript para enviar dicho formulario en forma automática.

Previniendo CSRF
----------------

Entonces, ¿Cómo puede tu sitio defenderse de este exploit?. El primer paso es
asegurarse que todas las peticiones ``GET`` no posean efectos colaterales. De
esa forma, si un sitio malicioso incluye una de tus páginas como un
``<iframe>``, esto no tendrá un efecto negativo.

Esto nos deja con las peticiones ``POST``. El segundo paso es dotar a cada
``<form>`` que se enviará vía POST un campo oculto cuyo valor sea secreto y sea
generado en base al identificador de sesión del usuario. Entonces luego, cuando
se esté realizando el procesamiento del formulario en el servidor, comprobar
dicho campo secreto y generar un error si dicha comprobación no es exitosa.

Esto es precisamente lo que hace la capa de prevención de CSRF de Django, tal
como se explica en la siguiente sección.

Usar el middleware CSRF
~~~~~~~~~~~~~~~~~~~~~~~

El paquete ``django.contrib.csrf``  contiene sólo un módulo: ``middleware.py``.
Este módulo contiene una clase middleware Django: ``CsrfMiddleware`` la cual
implementa la protección contra CSRF,  por defecto.

Para activar esta protección, agrega
``'django.contrib.csrf.middleware.CsrfMiddleware'`` a la variable de
configuración ``MIDDLEWARE_CLASSES`` en tu archivo de configuración. Este
middleware necesita procesar la respuesta *después* de ``SessionMiddleware``,
así que ``CsrfMiddleware`` debe aparecer *antes* que ``SessionMiddleware``
en la lista (esto es debido que el middleware de respuesta es procesado de
atrás hacia adelante). Por otra parte, debe procesar la respuesta antes que la
misma sea comprimida o alterada de alguna otra forma, de manera que
``CsrfMiddleware`` debe aparecer después de ``GZipMiddleware``. Una vez que has
agregado eso a tu ``MIDDLEWARE_CLASSES`` ya estás listo para usarlo, tanto en
plantillas como en vistas.

En cualquier plantilla que use un formulario ``POST``, usa la etiqueta
``csrf_token`` dentro de los elementos <form> si el formulario es para una
URL interna. Por ejemplo::

    <form action="." method="post">{% csrf_token %}

Esto no se debe de hacer en formularios ``POST`` que apunten a URLs externas, ya
que esto causaría que el CSRF sea escapado, conduciéndonos a problemas de
vulnerabilidad.

En las vistas, solo asegúrate de que el procesador de contexto:
``django.core.context_processors.csrf`` sea usado. Usualmente puedes hacerlo de
dos formas:

* Usando ``RequestContext,`` el cual siempre usa
  ``django.core.context_processors.csrf`` (no importando la configuración de
  ``TEMPLATE_CONTEXT_PROCESSORS``). Si estas usando una vista genérica o
  una aplicación del paquete ``contrib``, estas a salvo, ya que estas
  aplicaciones ya incluyen ``RequestContext`` por defecto.

* Manualmente importa y usa el procesador generado por el token CSRF y agrégalo
  en el contexto de la plantilla, así:

.. code-block:: python

    from django.core.context_processors import csrf
    from django.shortcuts import render_to_response

    def mi_vista(request):
        c = {}
        c.update(csrf(request))
        # ... el código de la vista aquí.
        return render_to_response("mi plantilla.html", c)

Finalmente puedes usar un decorador que envuelva tu vista y que tome en cuenta
estos pasos por ti.::

    from django.views.decorators.csrf import csrf_protect
    from django.shortcuts import render

    @csrf_protect
    def mi_vista(request):
        c = {}
        # ...
        return render(request, "a_template.html", c)

.. warning::

    El uso del decorador por sí mismo no es muy recomendable, ya que si olvidas
    utilizarlo, tendrás un gran agujero de seguridad.

En el caso en el que estés interesado, así es como trabaja ``CsrfMiddleware``.
Realiza estas dos cosas:

1. Modifica las respuestas salientes a peticiones agregando un campo de
   formulario oculto a todos los formularios ``POST``, con el nombre
   ``csrfmiddlewaretoken`` y un valor que es un *hash* del identificador
   de sesión más una clave secreta. El middleware *no* modifica la respuesta
   si no existe un identificador de sesión, de manera que el costo en
   rendimiento es despreciable para peticiones que no usan sesiones.

2. Para todas las peticiones ``POST`` que porten la cookie de sesión,
   comprueba que ``csrfmiddlewaretoken`` esté presente y tenga un valor
   correcto. Si no cumple estas condiciones, el usuario recibirá un error
   ``HTTP`` 403. El contenido de la página de error es el mensaje "Cross
   Site Request Forgery detected. Request aborted."

Esto asegura que solamente se puedan usar formularios que se hayan originado en
tu sitio Web para enviar datos vía POST al mismo.

Este middleware deliberadamente trabaja solamente sobre peticiones HTTP ``POST``
(y sus correspondientes formularios POST). Como ya hemos explicado, las
peticiones ``GET`` nunca deberían tener efectos colaterales; es tu
responsabilidad asegurar eso.

Las peticiones ``POST`` que no estén acompañadas de una cookie de sesión no son
protegidas simplemente porque no tiene sentido protegerlas, un sitio Web
malicioso podría de todas formas generar ese tipo de peticiones.

Para evitar alterar peticiones no HTML, el middleware revisa la cabecera
``Content-Type`` de la respuesta antes de modificarla. Sólo modifica las páginas
que son servidas como ``text/html`` o ``application/xml+xhtml``.

Limitaciones del middleware CSRF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``CsrfMiddleware`` necesita el framework de sesiones de Django para poder
funcionar. (Revisa el :doc:`capítulo 14<chapter14>` para obtener más información
sobre sesiones). Si estás usando un framework de sesiones o autenticación
personalizado que maneja en forma manual las cookies de sesión, este middleware
no te será de ayuda.

Si tu aplicación crea páginas HTML y formularios con algún método inusual (por
ej. si envía fragmentos de HTML en sentencias JavaScript ``document.write``),
podrías estar salteándote el filtro que agrega el campo oculto al formulario. De
presentarse esta situación, el envío del formulario fallará siempre. (Esto
sucede porque ``CsrfMiddleware`` usa una expresión regular para agregar el campo
``csrfmiddlewaretoken`` a tu HTML antes de que la página sea enviada al cliente,
y la expresión regular a veces no puede manejar código HTML muy extravagante).
Si sospechas que esto podría estar sucediendo, sólo examina el código en tu
navegador Web para ver si es que ``csrfmiddlewaretoken`` ha sido insertado en tu
``<form>``.

Para más información y ejemplos sobre CSRF, visita http://en.wikipedia.org/wiki/CSRF.

Humanizando Datos
=================

El paquete ``contrib.humanize`` es una aplicación que aloja un conjunto de
filtros de plantilla útiles a la hora de agregar un "toque humano" a los datos.
Para activar esos filtros, agrega ``django.contrib.humanize`` a tu variable de
configuración ``INSTALLED_APPS``.

Una vez que has hecho eso, carga las etiquetas con ``{% load humanize %}`` en
una plantilla, y tendrás acceso a los filtros que se describen en las siguientes
secciones.

apnumber
--------

Para números entre 1 y 9, este filtro retorna la representación textual del
número. Caso contrario retorna el numeral. Esto cumple con el estilo Associated
Press.

Ejemplos:

* ``1`` se convierte en ``uno``.
* ``2`` se convierte en ``dos``.
* ``0`` se convierte en ``10``.

Puedes pasarle ya sea un entero o una representación en cadena de un entero.

intcomma
--------

Este filtro convierte un entero a una cadena conteniendo comas cada tres
dígitos.

Ejemplos:

* ``4500`` se convierte en ``4,500``.
* ``45000`` se convierte en ``45,000``.
* ``450000`` se convierte en ``450,000``.
* ``4500000`` se convierte en ``4,500,000``.

Puedes pasarle ya sea un entero o una representación en cadena de un entero.

intword
-------

Este filtro convierte un entero grande a una representación amigable en texto.
Funciona mejor con números mayores a un millón.

Ejemplos:

* ``1000000`` se convierte en ``1.0 millón``.
* ``1200000`` se convierte en ``1.2 millón``.

Se admiten valores hasta de 10^100 (Googol).

Puedes pasarle ya sea un entero o una representación en cadena de un entero.

naturalday
----------

Este filtro se usa para mostrar fechas por ejemplo hoy, mañana o ayer. Tomando
como valor la fecha del día de hoy.

Ejemplos (cuando la etiqueta ‘now’ es 17 Feb 2007):

* ``16 Feb 2007`` se convierte en ``ayer``.
* ``17 Feb 2007`` se convierte en ``hoy``.
* ``18 Feb 2007`` se convierte en ``mañana``.
* Cualquier otro día se formatea según el argumento dado o configurado en
  ``DATE_FORMAT`` si no se da ningún argumento.

Argumentos: Una fecha formateada como una cadena.

naturaltime
-----------

Este filtro se usa para mostrar valores de tiempo, retorna una cadena que
representa cuantos segundos, minutos y horas han pasado  --recurre al formato
de la etiqueta ``timesince`` si el valor tiene más de un día. En este caso
retorna el valor usando una frase.

Ejemplo (cuando la etiqueta ‘now’ es 17 Feb 2007 16:30:00):

* ``17 Feb 2007 16:30:00`` se convierte en ``ahora``.
* ``17 Feb 2007 16:29:31`` se convierte en ``hace 29``
* ``17 Feb 2007 16:29:00`` se convierte en ``hace un minuto``.
* ``17 Feb 2007 16:25:35`` se convierte en ``hace 4 minutos``.
* ``17 Feb 2007 15:30:29`` se convierte en ``Hace 59 minutos``.

ordinal
-------

Este filtro convierte un entero a una cadena cuyo valor es su ordinal.

Ejemplos:

* ``1`` se convierte en ``1st``.
* ``2`` se convierte en ``2nd``.
* ``3`` se convierte en ``3rd``.

Puedes pasarle ya sea un entero o una representación en cadena de un entero.

¿Qué sigue?
===========

Muchos de estos frameworks contribuidos (CSRF, el sistema de autenticación,
etc.) hacen su magia proveyendo una pieza de middleware. El middleware es
esencialmente código que se ejecuta antes y/o después  de cada petición y puede
modificar cada petición y respuesta a voluntad. :doc:`A continuación<chapter17>`
trataremos el middleware incluido con Django y explicaremos cómo puedes crear
el tuyo propio.

