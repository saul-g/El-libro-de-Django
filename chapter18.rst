=================================
Capítulo 18: Internacionalización
=================================

Django fue originalmente desarrollado exactamente en el medio de los Estados
Unidos (literalmente; Lawrence, Kansas, se halla a menos de 40 millas del centro
geográfico de la porción continental de los Estados Unidos). Como la mayoría de
los proyectos open source, sin embargo, la comunidad de Django creció hasta
incluir gente de todo el globo. A medida que la comunidad fue tornándose más
diversa, la *internacionalización* y la *localización* fueron tomando una
importancia creciente. Debido a que muchos desarrolladores tienen, en el mejor
de los casos, una comprensión difusa de dichos términos vamos a definirlos
brevemente.

*Internacionalización* se refiere al proceso de diseño de programas para el uso
potencial de cualquier ***locale***  Esto incluye el marcado del texto (tales
como elementos de la interfaz con el usuario o mensajes de error) para su futura
traducción, la abstracción de la visualización de fechas y horarios de manera
que sea posible respetar diferentes estándares locales, la provisión de lo
necesario para admitir diferentes zonas horarias, y en general el asegurarse de
que el código no contenga ninguna suposición acerca de la ubicación de sus
usuarios.  Encontrarás a menudo "internacionalización" abreviada como *I18N* (el
número 18 se refiere al número de letras omitidos entre la "I" inicial  y la "N"
final).

*Localización* se refiere al proceso específico de traducir un programa
internacionalizado para su uso en un ***locale*** particular. Encontrarás a
menudo "localización" abreviada como *L10N*.

Django en si está totalmente internacionalizado; todas las cadenas están
marcadas para su traducción, y existen variables de configuración que controlan
la visualización de valores dependientes del ***locale*** como fechas y
horarios.  Django también incluye más de 40 archivos de localización. Si no
hablas inglés en forma nativa, existe una buena probabilidad de que Django ya se
encuentre traducido a tu idioma nativo.

El mismo framework de internacionalización usado para esas localizaciones está
disponible para que lo uses en tu propio código y plantillas.

En resumen, necesitarás agregar una cantidad mínima de ***hooks*** a tu código
Python y a tus plantillas. Esos ***hooks*** reciben el nombre de *cadenas de
traducción*. Los mismos le indican a Django "Este texto debe ser traducido al
idioma del usuario final si existe una traducción a dicho idioma de ese
texto."

Django se encarga de usar esos ***hooks*** para traducir las aplicaciones Web
"al vuelo" de acuerdo a las preferencias de idioma del usuario.

Esencialmente, Django hace dos cosas:

* Le permite a los desarrolladores y autores de plantillas especificar qué
  partes de sus aplicaciones deben ser traducibles.

* Usa esta información para traducir las aplicaciones Web para usuarios
  particulares de acuerdo a sus preferencias de idioma.

La maquinaria de traducción de Django usa ``gettext`` de GNU
(http://www.gnu.org/software/gettext/) via el módulo estándar ``gettext``
incluido en Python.

.. admonition:: Si no necesitas usar internacionalización:

    Los ***hooks*** de internacionalización de Django se encuentran activos por
    omisión, lo cual incurre en un pequeño ***overhead***. Si no utilizas
    internacionalización, deberías establecer ``USE_I18N = False`` en tu archivo
    de configuración. Si ``USE_I18N`` tiene el valor ``False`` Django
    implementará algunas optimizaciones de manera de no cargar la maquinaria de
    localización.

    Probablemente querrás también eliminar
    ``'django.core.context_processors.i18n'`` de tu variable de configuración
    ``TEMPLATE_CONTEXT_PROCESSORS``.

Especificando cadenas de traducción en código Python
====================================================

Las cadenas de traducción especifican "Este texto debería ser traducido." dichas
cadenas pueden aparecer en tu código Python y en tus plantillas. Es tú
responsabilidad marcar las cadenas traducibles; el sistema sólo puede traducir
cadenas sobre las que está al tanto.

Funciones estándar de traducción
--------------------------------

Las cadenas de traducción se especifican usando la función ``_()``. (Si, el
nombre de la función es el carácter guión bajo). Esta función está disponible
globalmente (o sea como un componente incluido); no es necesario que lo
importes.

En este ejemplo, el texto ``"Welcome to my site."`` está marcado como una
cadena de traducción::

    def my_view(request):
        output = _("Welcome to my site.")
        return HttpResponse(output)

La función ``django.utils.translation.gettext()`` es idéntica a ``_()``. Este
ejemplo es idéntico al anterior::

    from django.utils.translation import gettext
    def my_view(request):
        output = gettext("Welcome to my site.")
        return HttpResponse(output)

La mayoría de los desarrolladores prefiere usar ``_()``, debido a que es más
corta.

La traducción funciona también sobre valores computados. Este ejemplo es
idéntico a los dos anteriores::

    def my_view(request):
        words = ['Welcome', 'to', 'my', 'site.']
        output = _(' '.join(words))
        return HttpResponse(output)

La traducción funciona también sobre variables. De nuevo, este es otro ejemplo
idéntico::

    def my_view(request):
        sentence = 'Welcome to my site.'
        output = _(sentence)
        return HttpResponse(output)

(algo a tener en cuenta cuando se usan variables o valores computados, como se
veía en los dos ejemplos previos, es que la utilidad de detección de cadenas de
traducción de Django, ``make-messages.py``, no será capaz de encontrar esas
cadenas. Trataremos ``make-messages`` más adelante).

Las cadenas que le pasas a ``_()`` o ``gettext()`` pueden contener marcadores de
posición (por *placeholders*), especificados con la sintaxis estándar de
interpolación de cadenas con nombres, por ejemplo::

    def my_view(request, n):
        output = _('%(name)s is my name.') % {'name': n}
        return HttpResponse(output)

Esta técnica permite que las traducciones específicas de cada idioma reordenen
el texto de los marcadores de posición. Por ejemplo, una traducción al inglés
podría ser ``Adrian is my name``, mientras que una traducción al español podría
ser ``Me llamo Adrian``, con el marcador de posición (el nombre) ubicado a
continuación del texto traducido y no antes del mismo.

Por esta razón, deberías usar interpolación de cadenas con nombres (por ejemplo
``%(name)s``) en lugar de interpolación posicional (por ejemplo ``%s`` o
``%d``). Si usas interpolación posicional las traducciones no serán capaces de
reordenar el texto de los marcadores de posición.

Marcando cadenas como no-op
---------------------------

Usa la función ``django.utils.translation.gettext_noop()`` para marcar una
cadena como una cadena de traducción sin realmente traducirla en ese momento. Las
cadenas así marcadas no son traducidas sino hasta el último momento que sea posible.

Usa este enfoque si deseas tener cadenas constantes que deben ser almacenadas en
el idioma original -- tales como cadenas en una base de datos -- pero que deben
ser traducidas en el último momento posible, por ejemplo cuando la cadena es
presentada al usuario.

Traducción perezosa
-------------------

Usa la función ``django.utils.translation.gettext_lazy()`` para traducir cadenas
en forma perezosa -- cuando el valor es accedido en lugar de cuando se llama a
la función ``gettext_lazy()``.

Por ejemplo, para marcar el atributo ``help_text`` de un campo como traducible,
haz lo siguiente::

    from django.utils.translation import gettext_lazy

    class MyThing(models.Model):
        name = models.CharField(help_text=gettext_lazy('This is the help text'))

En este ejemplo, ``gettext_lazy()`` almacena una referencia perezosa a la cadena
-- no el verdadero texto traducido. La traducción en si misma se llevará a cabo
cuando sea usada en un contexto de cadena, tal como el renderizado de una
plantilla en el sitio de administración de Django.

Si no te gusta el nombre largo ``gettext_lazy`` puedes simplemente crear un
alias ``_`` (guión bajo) para el mismo, de la siguiente forma::

    from django.utils.translation import gettext_lazy as _

    class MyThing(models.Model):
        name = models.CharField(help_text=_('This is the help text'))

Usa siempre traducciones perezosas en modelos Django (de lo contrario no serán
traducidos correctamente para cada usuario). Y es una buena idea agregar también
traducciones de los nombres de campos y nombres de tablas. Esto significa
escribir las opciones ``verbose_name`` y ``verbose_name_plural`` en forma
explícita en la clase ``Meta``::

    from django.utils.translation import gettext_lazy as _

    class MyThing(models.Model):
        name = models.CharField(_('name'), help_text=_('This is the help text'))
        class Meta:
            verbose_name = _('my thing')
            verbose_name_plural = _('mythings')

Pluralización
-------------

Usa la función ``django.utils.translation.ngettext()`` para especificar mensajes
que tienen formas singular y plural distintas, por ejemplo::

    from django.utils.translation import ngettext
    def hello_world(request, count):
        page = ngettext(
            'there is %(count)d object',
            'there are %(count)d objects', count
        ) % {'count': count}
        return HttpResponse(page)

``ngettext`` tiene tres argumentos: la cadena de traducción singular, la
cadena de traducción plural y el número de objetos (el cual es pasado a los
idiomas de traducción como la variable ``count``).

Especificando cadenas de traducción en código de plantillas
===========================================================

Las traducciones en las plantillas Django usan dos etiquetas de plantilla y una
sintaxis ligeramente diferente a la del código Python. Para que tus plantillas
puedan acceder a esas etiquetas coloca ``{% load i18n %}`` al principio de tu
plantilla.

La etiqueta de plantilla ``{% trans %}`` marca una cadena para su traducción::

    <title>{% trans "This is the title." %}</title>

Si solo deseas marcar un valor para traducción pero para traducción posterior,
usa la opción ``noop``::

    <title>{% trans "value" noop %}</title>

No es posible usar variables de plantilla en ``{% trans %}`` -- solo están
permitidas cadenas constantes, rodeadas de comillas simples o dobles. Si tu
traducción requiere variables (marcadores de posición) puedes usar por ejemplo
``{% blocktrans %}``::

    {% blocktrans %}This will have {{ value }} inside.{% endblocktrans %}

Para traducir una expresión de plantilla -- por ejemplo, cuando usas filtros de
plantillas -- necesitas asociar la expresión a una variable local que será la
que se usará dentro del bloque de traducción::

    {% blocktrans with value|filter as myvar %}
      This will have {{ myvar }} inside.
    {% endblocktrans %}

Si necesitas asociar más de una expresión dentro de una etiqueta ``blocktrans``,
separa las partes con ``and``::

    {% blocktrans with book|title as book_t and author|title as author_t %}
      This is {{ book_t }} by {{ author_t }}
    {% endblocktrans %}

Para pluralizar, especifica tanto la forma singular como la plural con la
etiqueta ``{% plural %}`` la cual aparece dentro de ``{% blocktrans %}`` y
``{% endblocktrans %}``, por ejemplo::

    {% blocktrans count list|length as counter %}
      There is only one {{ name }} object.
    {% plural %}
      There are {{ counter }} {{ name }} objects.
    {% endblocktrans %}

Internamente, todas las traducciones en bloque y en línea usan las llamadas
apropiadas a ``gettext``/``ngettext``.

Cuando usas ``RequestContext`` (ver :doc:`Capítulo 10<chapter10>`), tus plantillas tienen
acceso a tres variables específicas relacionadas con la traducción:

    * ``{{ LANGUAGES }}`` es una lista de tuplas en las cuales el primer
      elemento es el código de idioma y el segundo es el nombre y escrito usando
      el mismo).

    * ``{{ LANGUAGE_CODE }}`` es el idioma preferido del usuario actual,
      expresado como una cadena (por ejemplo ``en-us``). (Consulta la sección
      "`Cómo descubre Django la preferencia de idioma`_" para información
      adicional).

    * ``{{ LANGUAGE_BIDI }}`` es el sistema de escritura del idioma actual. Si
      el valor es ``True``, se trata de un idioma derecha-a-izquierda (por
      ejemplo hebreo, árabe). Si el valor es ``False``, se trata de de un idioma
      izquierda-a-derecha (por ejemplo inglés, francés, alemán).

Puedes también cargar los siguientes valores usando etiquetas de plantilla::

    {% load i18n %}
    {% get_current_language as LANGUAGE_CODE %}
    {% get_available_languages as LANGUAGES %}
    {% get_current_language_bidi as LANGUAGE_BIDI %}

También existen ***hooks*** de traducción que están disponibles en el interior de
cualquier etiqueta de bloque de plantilla que acepte cadenas constantes. En
dichos casos basta con que uses la sintaxis ``_()`` para especificar una
cadena de traducción, por ejemplo::

    {% some_special_tag _("Page not found") value|yesno:_("yes,no") %}

En este caso tanto la etiqueta como el filtro verán la cadena ya traducida (en
otras palabras la cadena es traducida *antes* de ser pasada a las funciones de
manejo de etiquetas), de manera que no necesitan estar preparadas para manejar
traducción.

.. _Capítulo 10: ../chapter10/

Creando archivos de idioma
==========================

Una vez que hayas etiquetado tus cadenas para su posterior traducción, necesitas
escribir (u obtener) las traducciones propiamente dichas. En esta sección
explicaremos como es que eso funciona.

Creando los archivos de mensajes
--------------------------------

El primer paso es crear un *archivo de mensajes* para un nuevo idioma. Un
archivo de mensajes es un archivo de texto común que representa un único idioma
que contiene todas las cadenas de traducción disponibles y cómo deben ser
representadas las mismas en el idioma en cuestión. Los archivos de mensajes
tiene una extensión ``.po``.

Django incluye una herramienta, ``bin/make-messages``, que automatiza la
creación y el mantenimiento de dichos archivos.

Para crear o actualizar un archivo de mensajes, ejecuta este comando::

    bin/make-messages.py -l de

donde ``de`` es el código de idioma para el archivo de mensajes que deseas
crear. El código de idioma en este caso está en formato locale. Por ejemplo,
el mismo es ``pt_BR`` para portugués de Brasil y ``de_AT`` para alemán de
Austria.  Echa un vistazo a los códigos de idioma en el directorio
``django/conf/locale/`` para ver cuales son los idiomas actualmente incluidos.

El script debe ser ejecutado desde una de tres ubicaciones:

    * El directorio raíz ``django`` (no una copia de trabajo de Subversion, sino
      el que se halla referenciado por ``$PYTHONPATH`` o que se encuentra en
      algún punto debajo de esa ruta.
    * El directorio raíz de tu proyecto Django
    * El directorio raíz de tu aplicación Django

El script recorre completamente el árbol en el cual es ejecutado y extrae todas
las cadenas marcadas para traducción. Crea (o actualiza) un archivo de mensajes
en el directorio ``conf/locale``. En el ejemplo ``de``, el archivo será
``conf/locale/de/LC_MESSAGES/django.po``.

Si es ejecutado sobre el árbol de tu proyecto o tu aplicación, hará lo mismo
pero la ubicación del directorio locale es ``locale/LANG/LC_MESSAGES`` (nota que
no tiene un prefijo ``conf``). La primera vez que lo ejecutes en tu árbol
necesitarás crear el directorio ``locale``.

.. admonition:: ¿Sin gettext?

    Si no tienes instaladas las utilidades ``gettext``, ``make-messages.py``
    creará archivos vacíos. Si te encuentras ante esa situación debes o instalar
    dichas utilidades o simplemente copiar el archivo de mensajes de inglés
    (``conf/locale/en/LC_MESSAGES/django.po``) y usar el mismo como un punto de
    partida; se trata simplemente de un archivo de traducción vacío.

El formato de los archivos ``.po`` es sencillo. Cada archivo ``.po`` contiene
una pequeña cantidad de metadatos tales como la información de contacto de
quiénes mantienen la traducción, pero el grueso del archivo es una lista de
*mensajes* -- mapeos simples entre las cadenas de traducción y las traducciones
al idioma en cuestión propiamente dichas.

Por ejemplo, si tu aplicación Django contiene una cadena de traducción para el
texto ``Welcome to my site``::

    _("Welcome to my site.")

entonces ``make-messages.py`` habrá creado un archivo ``.po`` que contendrá el
siguiente fragmento -- un mensaje::

    #: path/to/python/module.py:23
    msgid "Welcome to my site."
    msgstr ""

Es necesaria una rápida explicación:

    * ``msgid`` es la cadena de traducción, la cual aparece en el código fuente.
      No la modifiques.
    * ``msgstr`` es donde colocas la traducción específica a un idioma. Su valor
      inicial es vacío de manera que es tu responsabilidad el cambiar esto.
      Asegúrate de que mantienes las comillas alrededor de tu traducción.
    * Por conveniencia, cada mensaje incluye el nombre del archivo y el número
      de línea desde el cual la cadena de traducción fue extraída.

Los mensajes largos son un caso especial. La primera cadena inmediatamente a
continuación de ``msgstr`` (o ``msgid``) es una cadena vacía. El contenido en si
mismo se encontrará en las próximas líneas con el formato de una cadena por
línea. Dichas cadenas se concatenan en forma directa. ¡No olvides los espacios
al final de las cadenas; en caso contrario todas serán agrupadas sin espacios
entre las mismas!.

Por ejemplo, a continuación vemos una traducción de múltiples líneas (extraída
de la localización al español incluida con Django)::

    msgid ""
    "There's been an error. It's been reported to the site administrators via e-"
    "mail and should be fixed shortly. Thanks for your patience."
    msgstr ""
    "Ha ocurrido un error. Se ha informado a los administradores del sitio "
    "mediante correo electrónico y debería arreglarse en breve. Gracias por su "
    "paciencia."

Notar los espacios finales.

.. admonition:: Ten en cuenta el conjunto de caracteres

    Cuando crees un archivo ``.po`` con tu editor de texto favorito, primero
    edita la línea del conjunto de caracteres (busca por el texto ``"CHARSET"``)
    y fija su valor al del conjunto de caracteres usarás para editar el
    contenido. Generalmente, UTF-8 debería funcionar para la mayoría de los
    idiomas pero ``gettext`` debería poder manejar cualquier conjunto de
    caracteres.

Para reexaminar todo el código fuente y las plantillas en búsqueda de nuevas
cadenas de traducción y actualizar todos los archivos de mensajes para *todos*
los idiomas, ejecuta lo siguiente::

    make-messages.py -a

Compilando archivos de mensajes
-------------------------------

Luego de que has creado tu archivo de mensajes, y cada vez que realices cambios
sobre el mismo necesitarás compilarlo a una forma más eficiente, según los usa
``gettext``. Usa para ello la utilidad ``bin/compile-messages.py``.

Esta herramienta recorre todos los archivos ``.po`` disponibles y crea archivos
``.mo``, los cuales son archivos binarios optimizados para su uso por parte de
``gettext``. En el mismo directorio desde el cual ejecutaste
``make-messages.py``, ejecuta ``compile-messages.py`` de la siguiente manera::

   bin/compile-messages.py

Y eso es todo. Tus traducciones están listas para ser usadas.

Cómo descubre Django la preferencia de idioma
=============================================

Una vez que has preparado tus traducciones -- o, si solo deseas usar las que
están incluidas en Django -- necesitarás activar el sistema de traducción para
tu aplicación.

Detrás de escena, Django tiene un modelo muy flexible para decidir qué idioma
se usará -- determinado a nivel de la instalación, para un usuario particular, o
ambas.

Para configurar una preferencia de idioma a nivel de la instalación, fija
``LANGUAGE_CODE`` en tu archivo de configuración. Django usará este idioma como
la traducción por omisión -- la opción a seleccionarse en último término si
ningún otro traductor encuentra una traducción.

Si todo lo que deseas hacer es ejecutar Django con tu idioma nativo y hay
disponible un archivo de idioma para el mismo, simplemente asigna un valor a
``LANGUAGE_CODE``.

Si deseas permitir que cada usuario individual especifique el idioma que ella o
él prefiere, usa ``LocaleMiddleware``. ``LocaleMiddleware`` permite la selección
del idioma basado en datos incluidos en la petición. Personaliza el contenido
para cada usuario.

Para usar ``LocaleMiddleware``, agrega
``django.middleware.locale.LocaleMiddleware`` a tu variable de configuración
``MIDDLEWARE_CLASSES``. Debido a que el orden de los middlewares es relevante,
deberías seguir las siguientes guías:

    * Asegúrate de que se encuentre entre las primeras clases middleware
      instaladas.

    * Debe estar ubicado después de  ``SessionMiddleware``, esto es debido a que
      ``LocaleMiddleware`` usa datos de la sesión.

    * Si usas ``CacheMiddleware``, coloca ``LocaleMiddleware`` después de
      este (de otra forma los usuarios podrían recibir contenido cacheado del
      locale equivocado).

Por ejemplo tu ``MIDDLEWARE_CLASSES`` podría verse como esta::

    MIDDLEWARE_CLASSES = (
       'django.middleware.common.CommonMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.locale.LocaleMiddleware'
    )

``LocaleMiddleware`` intenta determinar la preferencia de idioma del usuario
siguiendo el siguiente algoritmo:

    * Primero, busca una clave ``django_language`` en la sesión del usuario
      actual.

    * Se eso falla, busca una cookie llamada ``django_language``.

    * Si eso falla, busca la cabecera HTTP ``Accept-Language``. Esta cabecera es
      enviada por tu navegador y le indica al servidor qué idioma(s) prefieres
      en orden de prioridad. Django intenta con cada idioma que aparezca en
      dicha cabecera hasta que encuentra uno para el que haya disponible una
      traducción.

    * Si eso falla, usa la variable de configuración global ``LANGUAGE_CODE``.

En cada uno de dichas ubicaciones, el formato esperado para la preferencia de
idioma es el formato estándar, como una cadena. Por ejemplo, portugués de Brasil
es ``pt-br``. Si un idioma base está disponible pero el sub-idioma especificado
no, Django usará el idioma base. Por ejemplo, si un usuario especifica ``de-at``
(alemán Austríaco) pero Django solo tiene disponible ``de`` , usará ``de``.

Sólo pueden seleccionarse idiomas que se encuentren listados en la variable de
configuración ``LANGUAGES``. Si deseas restringir la selección de idiomas a un
subconjunto de los idiomas provistos (debido a que tu aplicación no incluye
todos esos idiomas), fija tu ``LANGUAGES`` a una lista de idiomas, por ejemplo::

    LANGUAGES = (
        ('de', _('German')),
        ('en', _('English')),
    )

Este ejemplo restringe los idiomas que se encuentran disponibles para su
selección automática a alemán e inglés (y cualquier sub-idioma, como ``de-ch`` o
``en-us``).

Si defines un ``LANGUAGES`` personalizado es posible marcar los idiomas como
cadenas de traducción -- pero usa una función ``gettext()`` "boba", no la que se
encuentra en ``django.utils.translation``. *Nunca* debes importar
``django.utils.translation`` desde el archivo de configuración debido a que ese
módulo a su vez depende de las variables de configuración, y eso crearía una
importación  circular.

La solución es usar una función ``gettext()``` "boba". A continuación un archivo
de configuración de ejemplo::

    _ = lambda s: s

    LANGUAGES = (
          ('de', _('German')),
          ('en', _('English')),
    )

Con este esquema, ``make-messages.py`` todavía será capaz de encontrar y marcar
dichas cadenas para su traducción pero la misma no ocurrirá en tiempo de
ejecución, de manera que tendrás que recordar envolver los idiomas con la
*verdadera* ``gettext()`` en cualquier código que use ``LANGUAGES`` en tiempo de
ejecución.

El ``LocaleMiddleware`` sólo puede seleccionar idiomas para los cuales exista
una traducción base provista por Django. Si deseas ofrecer traducciones para tu
aplicación que no se encuentran en el conjunto de traducciones incluidas en el
código fuente de Django, querrás proveer al menos traducciones básicas para ese
idioma. Por ejemplo, Django usa identificadores de mensajes técnicos para
traducir formatos de fechas y de horas -- así que necesitarás al menos esas
traducciones para que el sistema funcione correctamente.

Un buen punto de partida es copiar el archivo ``.po`` de inglés y traducir al
menos los mensajes técnicos, y quizá también los mensajes de los validadores.

Los identificadores de mensajes técnicos son fácilmente reconocibles; están
completamente en mayúsculas. No necesitas traducir los identificadores de
mensajes como lo haces con otros mensajes; en cambio, deber proporcionar la
variante local correcta del valor provisto en inglés. Por ejemplo, con
``DATETIME_FORMAT`` (o ``DATE_FORMAT`` o ``TIME_FORMAT``), este sería la cadena
de formato que deseas usar en tu idioma. El formato es idéntico al de la cadena
de formato usado por la etiqueta de plantillas ``now``.

Una vez que el ``LocaleMiddleware`` ha determinado la preferencia del usuario,
la deja disponible como ``request.LANGUAGE_CODE`` para cada objeto petición. Eres
libre de leer este valor en tu código de vista. A continuación un ejemplo
simple::

    def hello_world(request, count):
        if request.LANGUAGE_CODE == 'de-at':
            return HttpResponse("You prefer to read Austrian German.")
        else:
            return HttpResponse("You prefer to read another language.")

Nota que con traducción estática (en otras palabras sin middleware) el idioma
está en ``settings.LANGUAGE_CODE``, mientras que con traducción dinámica (con
middleware) el mismo está en ``request.LANGUAGE_CODE``.

La vista de redirección set_language
====================================

Por conveniencia, Django incluye una vista ``django.views.i18n.set_language``,
que fija la preferencia de idioma de un usuario y redirecciona de vuelta a la
página previa.

Activa esta vista agregando la siguiente línea a tu URLconf::

    (r'^i18n/', include('django.conf.urls.i18n')),

(Nota que este ejemplo publica la vista en ``/i18n/setlang/``).

La vista espera ser llamada vía el método ``GET``, con un parámetro ``language``
incluido en la cadena de consulta. Si el soporte para sesiones está activo, la
vista guarda la opción de idioma en la sesión del usuario. Caso contrario,
guarda el idioma en una cookie ``django_language``.

Después de haber fijado la opción de idioma Django redirecciona al usuario, para
eso sigue el siguiente algoritmo:

    * Django busca un parámetro ``next`` en la cadena de consulta.
    * Si el mismo no existe o está vació, Django intenta la URL contenida en la
      cabecera ``Referer``.
    * Si la misma está vacía -- por ejemplo, si el navegador de un usuario
      suprime dicha cabecera -- entonces el usuario será redireccionado a
      ``/`` (la raíz del sitio) como un último recurso.

Este es un fragmento de código de plantilla HTML de ejemplo::

    <form action="/i18n/setlang/" method="get">
    <input name="next" type="hidden" value="/next/page/" />
    <select name="language">
    {% for lang in LANGUAGES %}
    <option value="{{ lang.0 }}">{{ lang.1 }}</option>
    {% endfor %}
    </select>
    <input type="submit" value="Go" />
    </form>

Usando traducciones en tus propios proyectos
============================================

Django busca traducciones siguiendo el siguiendo algoritmo:

    * Primero, busca un directorio ``locale`` en el directorio de la aplicación
      correspondiente a la vista que se está llamando. Si encuentra una
      traducción para el idioma seleccionado, la misma será instalada.
    * A continuación, busca un directorio ``locale`` en el directorio del
      proyecto. Si encuentra una traducción, la misma será instalada.
    * Finalmente, verifica la traducción base en ``django/conf/locale``.

De esta forma, puedes escribir aplicaciones que incluyan su propias
traducciones, y puedes reemplazar traducciones base colocando las tuyas propias
en la ruta de tu proyecto. O puedes simplemente construir un proyecto grande
a partir de varias aplicaciones y poner todas las traducciones en un gran
archivo de mensajes. Es tu elección.

.. admonition:: Nota:

    Si estás fijando manualmente la variables de configuración, el directorio
    ``locale`` en el directorio del proyecto no será examinado dado que Django
    pierde la capacidad de deducir la ubicación del directorio del proyecto.
    (Django normalmente usa la ubicación del archivo de configuración para
    determinar esto, y en el caso que estés fijando manualmente tus variables de
    configuración dicho archivo no existe).

Todos los repositorios de archivos de mensajes están estructurados de la misma
forma:

* ``$APPPATH/locale/<language>/LC_MESSAGES/django.(po|mo)``
* ``$PROJECTPATH/locale/<language>/LC_MESSAGES/django.(po|mo)``
* Todas las rutas listandas en ``LOCALE_PATHS`` en tu archivo de
  configuración son examinadas en ese orden en búsquda de
  ``<language>/LC_MESSAGES/django.(po|mo)``
* ``$PYTHONPATH/django/conf/locale/<language>/LC_MESSAGES/django.(po|mo)``

Para crear archivos de mensajes, usas la misma herramienta ``make-messages.py``
que usabas con los archivos de mensajes de Django. Solo necesitas estar en la
ubicación adecuada -- en el directorio en el cual exista ya sea el directorio
``conf/locale`` (en el caso del árbol de código fuente) o el directorio
``locale/`` (en el caso de mensajes de aplicación o de proyecto). Usas también
la misma herramienta ``compile-messages.py`` para producir los archivos binarios
``django.mo`` usados por ``gettext``.

Los archivos de mensajes de aplicaciones son un poquito complicados a la hora de
buscar por los mismos -- necesitas el ``LocaleMiddleware``. Si no usas el
middleware, solo serán procesados los archivos de mensajes de Django y del
proyecto.

Finalmente, debes dedicarle tiempo al diseño de la estructura de tus archivos de
traducción. Si tus aplicaciones necesitan ser enviadas a otros usuarios y serán
usadas en otros proeyctos, posiblemente quieras usar traducciones específicas a
dichas aplicaciones. Pero el usar traducciones específicas a aplicaciones y
aplicaciones en proyectos podrían producir problemas extraños con
``make-messages.py``. ``make-messages`` recorrerá todos los directorios situados
por debajo de la ruta actual y de esa forma podría colocar en el archivo de
mensajes del proyecto identificadores de mensajes  que ya se encuentran en los
archivos de mensajes de la aplicación.

la salida más fácil de este problema es almacenar las aplicaciones que no son
partes del proyecto (y por ende poseen sus propias traducciones) fuera del árbol
del proyecto. De esa forma `make-messages.py``` ejecutado a nivel proyecto
sólo traducirá cadenas que están conectadas a tu proyecto y no cadenas que son
distribuidas en forma independiente.

Traducciones y JavaScript
=========================

El agregar traducciones a JavaScript plantea algunos problemas:

* El código JavaScript no tiene acceso a una implementación de ``gettext``.
* El código JavaScript no tiene acceso a los archivos ``.po`` o ``.mo``; los
  mismos necesitan ser enviados desde el servidor.

* Los catálogos de traducción para JavaScript deben ser mantenidos tan
  pequeños como sea posible.

Django provee una solución integrada para esos problemas: convierte las
traducciones a JavaScript, de manera que puedas llamar a ``gettext`` y demás
desde JavaScript.

La vista javascript_catalog
---------------------------

La solución principal a esos problemas es la vista ``javascript_catalog``, que
genera una biblioteca de código JavaScript con funciones que emulan la interfaz
``gettext`` más un arreglo de cadenas de traducción. Dichas cadenas de
traducción se toman desde la aplicación, el proyecto o el núcleo de Django, de
acuerdo a lo que especifiques ya sea en el ``info_dict`` o en la URL.

La forma de usar esto es asi::

    js_info_dict = {
        'packages': ('your.app.package',),
    }

    urlpatterns = patterns('',
        (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    )

Cada cadena en ``package`` debe seguir la sintaxis paquete separados por puntos
de Python (el mismo formato que las cadenas en ``INSTALLED_APPS``) y deben
referirse a un paquete que contenga un directorio ``locale``. Si especificas
múltiples paquetes, todos esos catálogos son fusionados en un catálogo único.
esto es útil si usas JavaScript que usa cadenas de diferentes aplicaciones.

Puedes hacer que la vista sea dinámica colocando los paquetes en el patrón de la
URL::

    urlpatterns = patterns('',
        (r'^jsi18n/(?P<packages>\S+?)/$, 'django.views.i18n.javascript_catalog'),
    )

Con esto, especificas los paquetes como una lista de nombres de paquetes
delimitados por un símbolo ``+`` en la URL. Esto es especialmente útil si tus
páginas usan código de diferentes aplicaciones, este cambia frecuentemente y no
deseas tener que descargar un único gran catálogo. Como una medida de
seguridad, esos valores pueden solo tomar los valores ``django.conf`` o
cualquier paquete de la variable de configuración ``INSTALLED_APPS``.

Usando el catálogo de traducciones JavaScript
---------------------------------------------

Para usar el catálogo simplemente descarga el script generado dinámicamente de
la siguiente forma::

    <script type="text/javascript" src="/path/to/jsi18n/"></script>

Esta es la forma en la que el sitio de administración obtiene el catálogo de
traducciones desde el servidor. Una vez que se ha cargado el catálogo, tu código
JavaScript puede usar la interfaz estándar ``gettext`` para acceder al mismo::

    document.write(gettext('this is to be translated'));

Existe incluso una interfaz ``ngettext`` y una función de interpolación de
cadenas::

    d = {
        count: 10
    };
    s = interpolate(ngettext('this is %(count)s object', 'this are %(count)s objects', d.count), d);

La función ``interpolate`` admite tanto interpolación posicional como
interpolación con nombres. De manera que el código de arriba podría haber sido
escrito de la siguiente manera::

    s = interpolate(ngettext('this is %s object', 'this are %s objects', 11), [11]);

La sintaxis de interpolación se tomó prestada de Python. Sin embargo, no debes
exagerar con el uso de la interpolación de cadenas -- esto sigue siendo
JavaScript así que el código tendrá que realizar múltiples sustituciones de
expresiones regulares. Esto no es tan rápido como la interpolación de cadenas en
Python, de manera que deberías reservarlo para los casos en los que realmente
lo necesites (por ejemplo en combinación con ``ngettext`` para generar
pluralizaciones en forma correcta).

Creando catálogos de traducciones JavaScript
--------------------------------------------

Los catálogos de traducciones se crean y actualizan de la misma manera que el
resto de los catálogos de traducciones de Django: con la herramienta
``make-messages.py``. La única diferencia es que es necesario que proveas un
parámetro ``-d djangojs``, de la siguiente forma::

    make-messages.py -d djangojs -l de

Esto crea o actualiza el catálogo de traducción para JavaScript para alemán.
Luego de haber actualizado catálogos, sólo ejecuta ``compile-messages.py`` de la
misma manera que lo haces con los catálogos de traducción normales de Django.

Notas para usuarios familiarizados con ``gettext``
==================================================

Si conoces ``gettext`` podrías notar las siguientes particularidades en la forma
en que Django maneja las traducciones:

* El dominio de las cadenas es ``django`` o ``djangojs``. El dominio de
  cadenas se usa para diferenciar entre diferentes programas que almacenan
  sus datos en una biblioteca común de archivos de mensajes (usualmente
  ``/usr/share/locale/``). EL dominio ``django`` se usa para cadenas de
  traducción de Python y plantillas y se carga en los catálogos de
  traducciones globales. El dominio ``djangojs`` se usa sólo para catálogos
  de traducciones de JavaScript para asegurar que los mismos sean tan
  pequeños como sea posible.

* Django sólo usa ``gettext`` y ``gettext_noop``. Esto es debido a que
  Django siempre usa internamente cadenas ``DEFAULT_CHARSET``. Usar
  ``ugettext`` no significaría muchas ventajas ya que de todas formas
  siempre necesitarás producir UTF-8.

* Django no usa ``xgettext`` en forma independiente. Usa ***wrappers***
  Python alrededor de ``xgettext`` y ``msgfmt``. Esto es más que nada por
  conveniencia.

¿Qué sigue?
===========

Este capítulo esencialmente concluye nuestra cobertura de las características de
Django. Deberías conocer lo suficiente para comenzar a producir tus propios
sitios usando Django.

Sin embargo, escribir el código es solo el primer paso de la instalación de un
sitio Web exitoso. Los siguientes dos capítulos cubren las cosas que necesitarás
conocer si deseas que tu sitio sobreviva en el mundo real. El :doc:`Capítulo 19<chapter19>`
trata cómo puedes hacer para hace que tus sitios y tus usuarios estén seguros
ante atacantes maliciosos y el :doc:`Capítulo 20<chapter19>` detalla cómo instalar una
aplicación Django en uno o varios servidores.
