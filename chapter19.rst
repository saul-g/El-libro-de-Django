=================================
Capítulo 19: Internacionalización
=================================

Django fue desarrollado originalmente en medio de los Estados Unidos 
(literalmente; Lawrence, Kansas, se halla a menos de 40 millas del centro
geográfico de la porción continental, de los Estados Unidos). Sin embargo, como 
la mayoría de los proyectos open source, la comunidad de Django creció hasta
incluir a gente de todo el mundo. A medida que la comunidad fue tornándose más
diversa, la *internacionalización* y la *localización* fueron tomando una
importancia creciente. 

Debido a que muchos desarrolladores tienen, en el mejor de los casos, una 
comprensión difusa de dichos términos vamos a definirlos brevemente.

El termino **Internacionalización** se refiere al proceso de diseñar programas 
para el uso potencial de cualquier localidad. Esto incluye marcas de texto 
(tales como elementos de la interfaz de usuario o mensajes de error) para su 
futura traducción, abstrayendo la visualización de fechas y horarios de manera
que sea posible respetar diferentes estándares locales, proveer soporte para 
diferentes zonas horarias y  en general el asegurarse de que el código no 
contenga ninguna suposición acerca de la ubicación de sus usuarios. Encontrarás 
a menudo "internacionalización" abreviada como **I18N** (el número 18 se refiere 
al número de letras omitidos entre la "I" inicial  y la "N" final).

El termino **Localización** se refiere al proceso específico de traducir un 
programa internacionalizado para su uso en una localidad en particular. 
Encontrarás a menudo "localización" abreviada como **L10N**.

Django en si está totalmente internacionalizado; todas las cadenas están
marcadas para su traducción, y existen variables de configuración que controlan
la visualización de valores locales dependientes como fechas y horarios. 
Django también incluye más de 40 archivos de localización. Si no hablas inglés 
en forma nativa, existe una buena probabilidad de que Django ya se encuentre 
traducido a tu idioma nativo.

El mismo framework de internacionalización usado para esas localizaciones está
disponible para que lo uses en tu propio código y plantillas.

En resumen, necesitarás agregar una cantidad mínima de ganchos  a tu código
Python y a tus plantillas. Estos ganchos reciben el nombre de *cadenas de
traducción*. Los mismos le indican a Django "Este texto debe ser traducido al
idioma del usuario final si existe una traducción a dicho idioma de ese
texto."

Django se encarga de usar estos ganchos para traducir las aplicaciones Web
"al vuelo" de acuerdo a las preferencias de idioma del usuario.

Esencialmente, Django hace dos cosas:

* Le permite a los desarrolladores y autores de plantillas especificar qué
  partes de sus aplicaciones deben ser traducibles.

* Usa esta información para traducir las aplicaciones Web para usuarios
  particulares de acuerdo a sus preferencias de idioma.

La maquinaria de traducción de Django usa ``gettext`` de GNU
(http://www.gnu.org/software/gettext/) vía el módulo estándar ``gettext``
incluido en Python.

.. admonition:: Si no necesitas usar internacionalización:

    Los ganchos de internacionalización de Django se encuentran activos por
    omisión, lo cual incurre en un pequeña sobrecarga. Si no utilizas la
    internacionalización, deberías establecer ``USE_I18N = False`` en tu archivo
    de configuración. Si ``USE_I18N`` tiene el valor ``False`` Django
    implementará algunas optimizaciones de manera de no cargar la maquinaria de
    localización.

    Probablemente querrás también eliminar ``django.core.context_processors.i18n``
    de tu variable de configuración ``TEMPLATE_CONTEXT_PROCESSORS``.

Los tres pasos para usar la internacionalización en aplicaciones Django son:

1. Especifica las cadenas de traducción en el código Python y en las plantillas.

2. Implementa las traducciones para esas cadenas, en cualquiera de los lenguajes 
   que quieras soportar.

3. Activa el middleware local en la configuración de Django.

Cubriremos cada uno de estos pasos detalladamente.

1. Especifica las cadenas de traducción 
=======================================

Las cadenas de traducción especifican "Este texto debería ser traducido." dichas
cadenas pueden aparecer en tu código Python y en tus plantillas. Es tú
responsabilidad marcar las cadenas traducibles; el sistema sólo puede traducir
cadenas sobre las que está al tanto.

En código Python
----------------

Funciones estándar de traducción
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Las cadenas de traducción se especifican usando la función ``ugettext()``. 
Este por convención usa el alias ``_`` (guion bajo), como un atajo para importar
la función. 

En este ejemplo, el texto ``"Bienvenido a mi sitio."`` está marcado como una
cadena de traducción, usando el alias ``_``::

    from django.utils.translation import ugettext as _
    from django.http import HttpResponse

    def mi_vista(request):
        salida = _("Bienvenido a mi sitio.")
        return HttpResponse(salida)

La función ``django.utils.translation.gettext()`` es idéntica a ``_()``. Este
ejemplo es idéntico al anterior::

    from django.utils.translation import ugettext

    def mi_vista(request):
        salida = ugettext("Bienvenido a mi sitio.")
        return HttpResponse(salida)

La mayoría de los desarrolladores prefiere usar el alias ``_()``, debido a que 
es más corto.

.. admonition:: Nota:

    La librería estándar de Python ``gettext`` instala un modulo ``_()``
    en el espacio de nombres global, como un alias para ``gettext()``. En Django
    hemos decidido no seguir esta práctica por un par de razones:
    
    1. Para el apoyo internacional del conjunto de caracteres (Unicode),
       La función ``django.utils.translation.ugettext`` es mas útil que 
       ``gettext()``.  Algunas veces puedes utilizar por defecto la 
       la función ``django.utils.translation.ugettext_lazy`` como método para 
       traducir un archivo en particular. Sin usar el ``_()`` en el espacio 
       de nombres global, el desarrollador tiene que pensar acerca de cuál es 
       la función más apropiada para usar en la traducción.

    2. El carácter de guion bajo  (``_``) es usado para representar "el 
       resultado previo" en el interprete interactivo Python y en las pruebas     
       de documentación. Instalar una función global ``_()`` causa interferencia.
       Explícitamente importando ``ugettext()`` como ``_()`` evitamos este 
       problema.

La traducción funciona también sobre valores computados. Este ejemplo es
idéntico a los dos anteriores::

    def mi_vista(request):
        palabras = ['Bienvenido', 'a', 'mi', 'sitio.']
        salida = _(' '.join(palabras))
        return HttpResponse(salida)

La traducción funciona también sobre variables. De nuevo, este es otro ejemplo
idéntico::

    def mi_vista(request):
        sentencia = 'Bienvenido a mi sitio.'
        salida = _(sentencia)
        return HttpResponse(salida)

(Algo a tener en cuenta cuando se usan variables o valores computados, como se
veía en los dos ejemplos previos, es que la utilidad de detección de cadenas de
traducción de Django, ``makemessages``, no será capaz de encontrar esas
cadenas. Trataremos el comando ``django-admin.py  makemessages`` más adelante).

Las cadenas que le pasas a ``_()`` o ``ugettext()`` pueden contener marcadores 
de posición especificados con la sintaxis estándar de
interpolación de cadenas de Python con nombres, por ejemplo::

  def mi_vista(request, m, d):
      salida = _('Hoy es %(mes)s %(dia)s.') % {'mes': m, 'dia': d}
      return HttpResponse(salida)

Esta técnica permite que las traducciones específicas de cada idioma reordenen
el texto de los marcadores de posición. Por ejemplo, una traducción al inglés
podría ser ``"Today is November 26."``, mientras que una traducción al español
podría ser ``"Hoy es 26 de Noviembre."``, usando marcadores de posición para 
el ``mes`` y el ``dia`` para intercambiarlos.

Por esta razón, deberías usar interpolación de cadenas con nombres (por ejemplo
``%(dia)s``) en lugar de interpolación posicional (por ejemplo ``%s`` o
``%d``). Si usas interpolación posicional las traducciones no serán capaces de
reordenar el texto de los marcadores de posición.

Comentarios para traducciones
-----------------------------

Si te gustaría darle indicios a los traductores acerca de una cadena traducible, 
puedes añadir un comentario, usando un prefijo con la palabra clave 
``Translators`` en la línea anterior a la cadena, por ejemplo:

.. code-block:: python

  def mi_vista(request):
      # Translators: Este mensaje aparece en la página de inicio únicamente.
      output = ugettext("Bienvenidos a mi sitio.")

El comentario después aparecerá en el fichero resultante .po asociado, con la 
traducción compilada y localizado debajo de él mensaje traducido, como en el
siguiente fragmento::

  #. Translators: Este mensaje aparece en la página de inicio únicamente.
  # path/to/python/file.py:123
  msgid "Bienvenidos a mi sitio."
  msgstr ""

Esto también funciona en plantillas. Así como en el código Python, las notas 
para traductores pueden especificarse usando comentarios en las plantillas de la
siguiente forma.

.. code-block:: python

  {% comment %}Translators: Verbo de la vista{% endcomment %}
  {% trans "Vista" %}

  {% comment %}Translators: Introducción corta sobre publicidad{% endcomment %}
  <p>{% blocktrans %}Traducir varias líneas
  literal.{% endblocktrans %}</p>

o con etiquetas ``{# ... #}`` uno por línea, para construir comentarios:

.. code-block:: python

  {# Translators: Etiqueta de un botón de búsqueda #}
  <button type="submit">{% trans "Ir" %}</button>

  {# Translators: Éste es texto de la plantilla base #}
  {% blocktrans %}Bloque ambiguo de texto traducible{% endblocktrans %}

Como complemento, este es un fragmento de el resultado en un archivo .po.

.. code-block:: python  

  #. Translators: Verbo de la vista
  # ruta/a/plantilla/archivo.html:10
  msgid "Vista"
  msgstr ""

  #. Translators: Introducción corta sobre publicidad
  # path/to/template/file.html:13
  msgid ""
  "Traducir varias líneas"
  "literal."
  msgstr ""

  # ...

  #. Translators: Etiqueta de un botón de búsqueda
  # ruta/a/plantilla/archivo.html:100
  msgid "Ir"
  msgstr ""

  #. Translators: Éste es texto de la plantilla base 
  # ruta/a/plantilla/archivo.html:103
  msgid "bloque ambiguo de texto traducible"
  msgstr ""

Marcando cadenas como no-op
---------------------------

Usa la función ``django.utils.translation.ugettext_noop()`` para marcar una
cadena como una cadena de traducción sin realmente traducirla en ese momento. 
Las cadenas así marcadas no son traducidas sino hasta el último momento que 
sea posible.

Usa este enfoque si deseas tener cadenas constantes que deben ser almacenadas en
el idioma original -- tales como cadenas en una base de datos, pero que deben
ser traducidas en el último momento posible, por ejemplo cuando la cadena es
presentada al usuario.

Traducción perezosa
-------------------

Usa la función ``django.utils.translation.ugettext_lazy()`` para traducir cadenas
en forma perezosa -- cuando el valor es accedido en lugar de cuando se llama a
la función ``ugettext_lazy()``.

Por ejemplo, para marcar el atributo ``texto_ayuda`` de un campo como traducible,
haz lo siguiente::

    from django.db import models
    from django.utils.translation import ugettext_lazy

    class Mimodelo(models.Model):
        nombre = models.CharField(help_text=ugettext_lazy('Este es el texto de ayuda'))

En este ejemplo, ``ugettext_lazy()`` almacena una referencia perezosa a la cadena
-- no al verdadero texto traducido. La traducción en si misma se llevará a cabo
cuando sea usada en un contexto de cadena, tal como el renderizado de una
plantilla en el sitio de administración de Django.

El resultado de llamar a  ``ugettext_lazy()`` puede ser usado donde se necesite
usar una cadena en Unicode (un objeto del tipo ``Unicode``) en Python. Si tratas
de usar un ``bytestring`` donde se espera un objeto ``str``, las cosas no 
funcionaran como esperabas, ya que la función ``ugettext_lazy()`` no puede 
convertir en si mismo objetos ``bytestring``. Sin embargo puedes usar cadenas 
Unicode dentro de de cualquier ``bytestring`` esto es consistente con el 
comportamiento  normal de Python. Por ejemplo:

.. code-block:: python

    # Esto está bien: poner un marcador Unicode dentro de una cadena Unicode.
    “Hola %s" % ugettext_lazy("gente")

    # Esto no funcionara, ya que no se puede insertar un objeto Unicode
    # dentro de un bytestring.
    b"Hola %s" % ugettext_lazy("gente")

Si ves en la salida algo como esto ``"hola
<django.utils.functional...>"``, estas tratando de insertar el resultado de 
``ugettext_lazy()`` en un ``bytestring``. Se trata de un error en tu código.

Si no te gusta el nombre largo ``gettext_lazy`` puedes simplemente crear un
alias ``_`` (guión bajo) para el mismo, de la siguiente forma::

    from django.db import models
    from django.utils.translation import ugettext_lazy as _

    class Mimodelo(models.Model):
        titulo = models.CharField(help_text=_('Texto de ayuda'))

Usa siempre traducciones perezosas en modelos Django (de lo contrario no serán
traducidos correctamente para cada usuario). Y es una buena idea agregar también
traducciones de los nombres de campos y nombres de tablas. Esto significa que 
también puedes especificar las opciones ``verbose_name`` y ``verbose_name_plural`` 
como traducibles en forma explícita en la clase ``Meta``, así::

    from django.utils.translation import ugettext_lazy as _
    from biblioteca.models import Libro

    class Libro(models.Model):
        titulo = models.CharField(_('titulo'), help_text=_('Escribe el título del libro'))
        #..

        class Meta:
            verbose_name = _('libro')
            verbose_name_plural = _('libros')

Pluralización
-------------

Usa la función ``django.utils.translation.ungettext()`` para especificar mensajes
que tienen formas singular y plural distintas.

``ungettext`` toma tres argumentos: la cadena de traduccion en singular, la
cadena de traduccion en plural y el numero de objetos.

Esta función es útil cuando se necesita que una  aplicación Django sea 
localizable por los lenguajes donde el número y la complejidad de las formas que
toma el plural es mayor que las dos formas usadas en el inglés (``objeto`` para 
el singular y ``objetos`` para el plural,  para casos donde ``count`` es 
diferente a uno, sin distinción de su valor.)

Por ejemplo::

  from django.utils.translation import ungettext
  from django.http import HttpResponse

  def ejemplo_pluralizacion(request, count):
      page = ungettext(
          'Este es %(count)d objeto',
          'Estos son %(count)d objetos',
      count) % {
          'count': count,
      }
      return HttpResponse(page)

En este ejemplo el numero de objetos es pasado al lenguaje de traduccion como
la variable ``count``.      

Observa que la pluralización es complicada y funciona diferente en cada lenguaje
Comparar ``count`` con 1 no es siempre la regla correcta. Este código parece 
sofisticado, pero producirá resultados incorrectos en algunos lenguajes:

.. code-block::python

  from django.utils.translation import ungettext
  from biblioteca.models import Libro

  count = Libro.objects.count()
  if count == 1:
      nombre = Libro._meta.verbose_name
  else:
      nombre = Libro._meta.verbose_name_plural

  text = ungettext(
      'Este es %(count)d %(nombre)s disponible.',
      'Estos son %(count)d %(nombre)s disponibles.',
      count
  ) % {
      'count': count,
      'nombre': nombre
  }

No intentes implementar tu propia lógica singular o plural, no sería correcto. 
En un caso como este, considera hacer algo así como lo siguiente:

.. code-block::python

  text = ungettext(
      'Este es %(count)d %(nombre)s objeto disponible.',
      'Estos son %(count)d %(nombre)s objetos disponibles.',
      count
  ) % {
      'count': count,
      'nombre': Libro._meta.verbose_name,
  }

.. admonition:: Nota::

  Al usar ``ungettext ()``, asegúrate de utilizar un único ``nombre`` para cada
  variable extrapolada incluida literalmente.  En los ejemplos anteriores, nota 
  cómo utilizamos la variable de Python ``nombre``  en ambas cadenas de la 
  traduccion. En el siguiente ejemplo, nota que además de ser incorrecto en 
  algunos lenguajes según lo observado anteriormente, fallara:: 

    text = ungettext(
        'Este es %(count)d %(nombre)s disponible.',
        'Estos son %(count)d %(nombre_plural)s disponibles.',
        count
    ) % {
        'count': Libro.objects.count(),
        'nombre': Report._meta.verbose_name,
        'nombre_plural': Libro._meta.verbose_name_plural
    }

  Al ejecutar el comando ``django-admin compilemessages`` este retornara un 
  error::  

      a format specification for argument 'nombre', as in 'msgstr[0]', 
      doesn't exist in 'msgid'

Cadenas de traducción en plantillas
===================================

Las traducciones en las plantillas de Django usan dos etiquetas de plantilla y 
una sintaxis ligeramente diferente a la del código Python. Para que tus plantillas
puedan acceder a esas etiquetas coloca ``{% load i18n %}`` al principio de tu
plantilla.

La etiqueta de plantilla ``{% trans %}`` marcan una cadena para su traducción,
(encerradas por comillas simples o dobles) o el contenido de una variable:

.. code-block:: python

    <title>{% trans "Este es el titulo." %}</title>
    <title>{% trans soyunavariable %}</title>

Si la opción ``noop`` está presente, las operaciones de búsqueda de variables 
todavía ocurre, pero se salta la traducción. Esto es útil cuando el contenido 
"de fuera"  requiere la traducción en el futuro.

.. code-block:: python

    <title>{% trans "valor" noop %}</title>

No es posible mezclar en las plantillas variables dentro de cadenas sin 
la etiqueta ``{% trans %}`` . Si tu traducción requiere variables 
(marcadores de posición) puedes usar por ejemplo ``{% blocktrans %}``.

.. code-block:: python

     {% blocktrans %}
         Esta cadena tiene un {{ valor }} dentro.
     {% endblocktrans %}

Para traducir una expresión de plantilla -- por ejemplo, usando  filtros de
plantillas -- necesitas asociar la expresión a una variable local que será la
que se usará dentro del bloque de traducción:

.. code-block:: python

    {% blocktrans with valor|filter as variable %}
        Esta tiene una {{ variable }} dentro.
    {% endblocktrans %}

Si necesitas asociar más de una expresión dentro de una etiqueta ``blocktrans``,
separa las partes con ``and``:

.. code-block:: python

    {% blocktrans with libro|titulo as mi_libro and autor|titulo as mi_autor %}
      Este es {{ mi_libro }} por {{ mi_autor}}
    {% endblocktrans %}

Para pluralizar, especifica tanto la forma singular como la plural con la
etiqueta ``{% plural %}`` la cual aparece dentro de ``{% blocktrans %}`` y
``{% endblocktrans %}``, por ejemplo:

.. code-block:: python

    {% blocktrans count list|length as counter %}
        Hay únicamente {{ nombre }} objeto.
    {% plural %}
        Hay  {{ counter }} {{ nombre }} objetos.
    {% endblocktrans %}

Internamente, todas las traducciones en bloque y en línea usan las llamadas
apropiadas a ``ugettext``/ ``ungettext``.

Cuando usas ``RequestContext`` , tus plantillas tienen acceso a tres variables 
específicas relacionadas con la traducción:

* ``{{ LANGUAGES }}`` es una lista de tuplas en las cuales el primer
  elemento es el código de idioma y el segundo es el nombre y escrito usando
  el mismo).

* ``{{ LANGUAGE_CODE }}`` es el idioma preferido del usuario actual,
  expresado como una cadena (por ejemplo ``en-us``). (Consulta la sección
  "`3. Cómo descubre Django la preferencia de idioma`_" para información
  adicional).

* ``{{ LANGUAGE_BIDI }}`` es el sistema de escritura del idioma actual. Si
  el valor es ``True``, se trata de un idioma derecha-a-izquierda (por
  ejemplo hebreo, árabe). Si el valor es ``False``, se trata de de un idioma
  izquierda-a-derecha (por ejemplo inglés, francés, alemán).

Si no usas la extensión ``RequestContext``, puedes usar estos valores con estas
tres etiquetas de plantilla:

.. code-block:: python

    {% get_current_language as LANGUAGE_CODE %}
    {% get_available_languages as LANGUAGES %}
    {% get_current_language_bidi as LANGUAGE_BIDI %}

Estas etiquetas también requieren de ``{% load i18n %}``.

Los ganchos pasa las traducciones están disponibles en el interior de cualquier 
etiqueta de bloque de plantilla que acepte cadenas constantes. En dichos casos 
basta con que uses la sintaxis ``_()`` para especificar que es una cadena para
traducción, por ejemplo::

    {% alguna_etiqueta_especial _("Pagina no encontrada") value|yesno:_("si,no") %}

En este caso tanto la etiqueta como el filtro verán la cadena ya traducida (en
otras palabras la cadena es traducida *antes* de ser pasada a las funciones de
manejo de etiquetas), de manera que no necesitan estar preparadas para manejar
traducción.

.. admonition:: Nota

  En este ejemplo, la infraestructura de traducciones pasa la cadena ``"si,no"``
  como una sola y no como cadenas individuales ``"si"`` y ``"no"``. La cadena de
  traducción necesitará contener la coma de modo que el filtro de análisis 
  sepa dividir los argumentos. Por ejemplo, una traductor Alemán podría traducir
  la cadena ``"si,no"`` como ``"ja,nein"`` (manteniendo la coma intacta).

Trabajando con objetos en traducción perezosas
-----------------------------------------------

El uso de ``ugettext_lazy()`` y ``ungettext_lazy()`` para marcar cadenas en 
modelos y funciones de utilidad general es una operación muy común, Cuando 
trabajamos con estos objetos en cualquier parte de nuestro código,  debemos 
asegurarnos de no convertir nuestro código accidentalmente en cadenas, para ello
necesitamos asegurarnos de convertir las cadenas lo más tarde posible (de modo 
que la traducción correcta surta efecto). Esto hace necesario el uso de unas par 
de funciones de ayuda.

* string_concat()

* allow_lazy()

Juntando cadenas con: string_concat()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

El método estándar de Python ``join``, usado para juntar cadenas (``''.join([...])``) 
no trabaja en listas que contienen traducciones perezosas. En su lugar debes usar
``django.utils.translation.string_concat()``, el cual crea un objeto perezoso
que concatena el contenido *y* convierte las cadenas únicamente cuando el 
``resultado`` es incluido en la cadena. 

Por ejemplo:

.. code-block:: python

    from django.utils.translation import string_concat
    # ...
    nombre = ugettext_lazy(u'John Lennon')
    instrumento = ugettext_lazy(u'guitarra')
    resultado = string_concat([nombre, ': ', instrumento])

En este caso, la traducción perezosa en la variable ``resultado`` únicamente 
convierte la cadena cuando ``resultado`` es usado en una cadena (usualmente 
cuando se  renderiza la plantilla) 

EL decorador allow_lazy()
~~~~~~~~~~~~~~~~~~~~~~~~~

Django ofrece muchas funciones útiles (agrupadas en el paquete ``django.utils``) 
que toman una cadena como su primer argumento y hacen algo con la cadena. Estas 
funciones son usadas por los filtros de plantillas así como directamente en el 
código. 

Si escribes tus propias funciones y te ocupas de las traducciones, lo más seguro
es que te has encontrado con este problema, ¿Qué hacer cuando el primer
argumento es un objeto perezoso de una traducción? Si necesitas convertirlo a
una cadena inmediatamente, porque tal vez necesites usarlo fuera de una función 
de vista (y por lo tanto la configuración actual no funciona)

Para casos como este,  usa el decorador ``django.utils.functional.allow_lazy()``
El cual modifica la función *si* es llamado con una traducción perezosa como
su primer argumento, de esta forma el decorador demora la función hasta que 
necesite convertirse a cadena.

Por ejemplo:

.. code-block:: python

    from django.utils.functional import allow_lazy

    def fancy_utility_function(s, ...):
        # Hace la conversión en cadena 's'
        # ...
    fancy_utility_function = allow_lazy(fancy_utility_function, Unicode)

El decorador ``allow_lazy()`` toma, en adición a la función que decora, un 
numero extra de argumentos (``*args``) especificando el tipo que la función
original debe devolver. Usualmente, es suficiente incluir ``Unicode`` y 
asegurarse que la función devuelva únicamente cadenas Unicode.

Usando este decorador significa que puedes escribir tu función y asumir que la 
entrada es justamente una cadena, después solo agrega el soporte para 
traducciones de objetos perezosos al final.

2. Como crear archivos de idioma
================================

Una vez que hayas etiquetado tus cadenas para su posterior traducción, necesitas
escribir (u obtener) las traducciones propiamente dichas. En esta sección
explicaremos como es que eso funciona.

.. admonition:: Restricciones locales
    
    Django no soporta *Localización*  en una aplicación local para la cual 
    Django en sí mismo no ha sido traducido. En este caso solo ignorara
    el archivo de traducción. Si intentas hacer esto y Django lo soporta,
    inevitablemente veras una mezcla de cadenas traducidas (de tu aplicación)
    y cadenas en Ingles (de Django mismo) Si quieres soportar el idioma de tu 
    aplicación en un formato local, que no sea parte de Django, necesitarás 
    hacer por lo menos una traducción mínima del ``nucleo`` de Django.

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
``django/conf/locale/`` para ver cuáles son los idiomas actualmente incluidos.

El script debe ser ejecutado desde una de tres ubicaciones:

* El directorio raíz de tu proyecto Django.
* El directorio raíz de tu aplicación Django.
* El directorio raíz ``django`` (no una copia de git, sino  el que se halla 
  referenciado por ``$PYTHONPATH`` o que se encuentra en algún punto debajo de 
  esa ruta. Este es únicamente relevante si estas creando una traducción para 
  Django mismo.

El script recorre completamente el árbol en el cual es ejecutado y extrae todas
las cadenas marcadas para traducción. Crea (o actualiza) un archivo de mensajes
en el directorio ``locale/LANG/LC_MESSAGES``. En el ejemplo ``de``, el archivo
será ``locale/de/LC_MESSAGES/django.po``.

Por defecto ``django-admin.py makemessages`` examina cada archivo que tenga
una extensión ``.html`` . En el caso de que quieras sobrescribirá el valor
por default usa la opción ``--extension`` o ``-e`` para especificar la extensión
del archivo a examinar::

    django-admin.py makemessages -l de -e txt

Separa múltiples extensiones con comas y/o usa ``-e`` o ``--extension`` varias 
veces.::

    django-admin.py makemessages -l de -e html,txt -e xml


Al crear traducciones para catálogos JavaScript (el cual cubriremos mas
adelante en este capítulo), necesitaras usar un dominio especial 'djangojs' 
**no** ``-e js``.

.. admonition:: ¿Sin gettext?

    Si no tienes instaladas las utilidades ``gettext``, ``django-admin.py
    makemessages`` creará archivos vacíos. Si te encuentras ante esa situación 
    debes o instalar dichas utilidades o simplemente copiar el archivo de 
    mensajes de inglés (``conf/locale/en/LC_MESSAGES/django.po``) y usar el 
    mismo como un punto de partida; se trata simplemente de un archivo de 
    traducción vacío, que te servirá para crear el tuyo.

.. admonition:: ¿GNU gettext en Windows?

  Si estas usando Windows y necesitas instalar las utilidades GNU gettext
  para que ``django-admin makemessages`` funcione, consulta la sección
  "gettext en Windows" para obtener más información.

El formato de los archivos ``.po`` es sencillo. Cada archivo ``.po`` contiene
una pequeña cantidad de metadatos tales como la información de contacto de
quiénes mantienen la traducción, pero el grueso del archivo es una lista de
*mensajes* -- mapeos simples entre las cadenas de traducción y las traducciones
al idioma en cuestión propiamente dichas.

Por ejemplo, si tu aplicación Django contiene una cadena de traducción para el
texto ``Bienvenido a mi sitio.``::

    _("Bienvenido a mi sitio.")

Entonces el comando ``django-admin.py makemessages`` creara un archivo ``.po`` 
que contendrá el siguiente fragmento -- un mensaje::

    #: ruta/a/python/module.py:23
    msgid "Bienvenido a mi sitio."
    msgstr ""

Es necesaria una rápida explicación:

* ``msgid`` es la cadena de traducción, la cual aparece en el código fuente.
  No la modifiques.
* ``msgstr`` es donde colocas la traducción específica a un idioma. Su valor
  inicial es vacío de manera que es tu responsabilidad el cambiar esto.
  Asegúrate de mantener las comillas alrededor de tu traducción.
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
    "There's been an error. It's been reported to the site administrators vía e-"
    "mail and should be fixed shortly. Thanks for your patience."
    msgstr ""
    "Ha ocurrido un error. Se ha informado a los administradores del sitio "
    "mediante correo electrónico y debería arreglarse en breve. Gracias por su "
    "paciencia."

Observa los espacios finales.

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

    django-admin.py makemessages -a

Compilando archivos de mensajes
-------------------------------

Luego de que has creado tu archivo de mensajes, y cada vez que realices cambios
sobre el mismo necesitarás compilarlo a una forma más eficiente, según los usa
``gettext``. Usa para ello la utilidad ``django-admin.py compilemessages``.

Esta herramienta recorre todos los archivos ``.po`` disponibles y crea archivos
``.mo``, los cuales son archivos binarios optimizados para su uso por parte de
``gettext``. En el mismo directorio desde el cual ejecutaste
``django-admin.py makemessages``,  ejecuta ``django-admin.py compilemessages`` 
de la siguiente manera::

   django-admin.py compilemessages

Y eso es todo. Tus traducciones están listas para ser usadas.

3. Cómo descubre Django la preferencia de idioma
================================================

Una vez que has preparado tus traducciones -- o, si solo deseas usar las que
están incluidas en Django, necesitarás activar el sistema de traducción para
tu aplicación.

Detrás de escena, Django tiene un modelo muy flexible para decidir qué idioma
se usará -- determinado a nivel de la instalación, para un usuario particular, 
o ambas.

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
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.locale.LocaleMiddleware',
       'django.middleware.common.CommonMiddleware',
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

Notas:

* En cada uno de dichas ubicaciones, el formato esperado para la preferencia de
  idioma es el formato estándar, como una cadena. Por ejemplo, portugués de Brasil
  es ``pt-br``. 

* Si un idioma base está disponible pero el sub-idioma especificado
  no, Django usará el idioma base. Por ejemplo, si un usuario especifica ``de-at``
  (alemán Austríaco) pero Django solo tiene disponible ``de`` , usará ``de``.

* Sólo pueden seleccionarse idiomas que se encuentren listados en la variable de
  configuración ``LANGUAGES``. Si deseas restringir la selección de idiomas a un
  subconjunto de los idiomas provistos (debido a que tu aplicación no incluye
  todos esos idiomas), fija tu ``LANGUAGES`` a una lista de idiomas, por ejemplo::

    LANGUAGES = (
        ('de', _('German')),
        ('en', _('English')),
    )

  Este ejemplo restringe los idiomas que se encuentran disponibles para su
  selección automática a alemán e inglés (y cualquier sub-idioma, como 
  ``de-ch`` o  ``en-us``).


* Si defines un ``LANGUAGES`` personalizado es posible marcar los idiomas como
  cadenas de traducción -- pero usa una función ``gettext()`` "boba", no la que 
  se  encuentra en ``django.utils.translation``. *Nunca* debes importar
  ``django.utils.translation`` desde el archivo de configuración debido a que ese
  módulo a su vez depende de las variables de configuración, y eso crearía una
  importación  circular.

* La solución es usar una función ``gettext()``` "boba". A continuación un archivo
  de configuración de ejemplo::

      ugettext = lambda s: s

      LANGUAGES = (
          ('de', ugettext('German')),
          ('en', ugettext('English')),
      )

  Con este esquema, ``django-admin.py makemessages``  todavía será capaz de 
  encontrar y marcar dichas cadenas para su traducción pero la misma no ocurrirá
  en tiempo de ejecución, de manera que tendrás que recordar envolver los 
  idiomas con la  *verdadera* ``gettext()`` en cualquier código que use 
  ``LANGUAGES`` en tiempo de  ejecución.

* El ``LocaleMiddleware`` sólo puede seleccionar idiomas para los cuales exista
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

    def hola_mundo(request):
        if request.LANGUAGE_CODE == 'de-at':
            return HttpResponse("You prefer to read Austrian German.")
        else:
            return HttpResponse("You prefer to read another language.")

Nota que con traducción estática (en otras palabras sin middleware) el idioma
está en ``settings.LANGUAGE_CODE``, mientras que con traducción dinámica (con
middleware) el mismo está en ``request.LANGUAGE_CODE``.

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
* Todas las rutas listadas en ``LOCALE_PATHS`` en tu archivo de
  configuración son examinadas en el orden de búsqueda de
  ``<language>/LC_MESSAGES/django.(po|mo)``
* ``$PYTHONPATH/django/conf/locale/<language>/LC_MESSAGES/django.(po|mo)``

Para crear archivos de mensajes, usas la misma herramienta 
``django-admin.py makemessages`` que usabas con los archivos de mensajes de 
Django. Solo necesitas estar en la ubicación adecuada -- en el directorio en 
el cual exista ya sea el directorio ``conf/locale`` (en el caso del árbol de 
código fuente) o el directorio ``locale/`` (en el caso de mensajes de aplicación
o de proyecto). Usas también la misma herramienta ``django-admin.py compilemessages``
para producir los archivos binarios ``django.mo`` usados por ``gettext``.

Tambien  puedes ejecutar ``django-admin.py compilemessages --settings=path.to.settings``
Para hacer que el compilador procese todo los directorios de tu configuración
``LOCALE_PATHS``.

Los archivos de mensajes de aplicaciones son un poquito complicados a la hora de
buscar por los mismos -- necesitas el ``LocaleMiddleware``. Si no usas el
middleware, solo serán procesados los archivos de mensajes de Django y del
proyecto.

Finalmente, debes dedicarle tiempo al diseño de la estructura de tus archivos de
traducción. Si tus aplicaciones necesitan ser enviadas a otros usuarios y serán
usadas en otros proyectos, posiblemente quieras usar traducciones específicas a
dichas aplicaciones. Pero el usar traducciones específicas a aplicaciones y
aplicaciones en proyectos podrían producir problemas extraños con
``makemessages.py``: ``makemessages`` recorrerá todos los directorios situados
por debajo de la ruta actual y de esa forma podría colocar en el archivo de
mensajes del proyecto identificadores de mensajes  que ya se encuentran en los
archivos de mensajes de la aplicación.

La salida más fácil de este problema es almacenar las aplicaciones que no son
partes del proyecto (y por ende poseen sus propias traducciones) fuera del árbol
del proyecto. De esa forma ``django-admin.py makemessages`` ejecutado a nivel 
proyecto sólo traducirá cadenas que están conectadas a tu proyecto y no cadenas
que son distribuidas en forma independiente.

La vista de redirección ``set_language``
========================================

Por conveniencia, Django incluye una vista ``django.views.i18n.set_language``,
que fija la preferencia de idioma de un usuario y redirecciona de vuelta a la
página previa.

Activa esta vista agregando la siguiente línea a tu URLconf::

    url(r'^i18n/', include('django.conf.urls.i18n')),

(Nota que este ejemplo hace que la vista esté disponible en ``/i18n/setlang/``).

La vista espera ser llamada vía el método ``POST``, con un parámetro ``language``
incluido en la cadena de petición. Si el soporte para sesiones está activo, la
vista guarda la opción de idioma en la sesión del usuario. En caso contrario,
guarda el idioma en una cookie ``django_language``. (El nombre puede ser cambiado
a través de la configuración ``LANGUAGE_COOKIE_NAME``.)

Después de haber fijado la opción de idioma Django redirecciona al usuario, para
eso sigue el siguiente algoritmo:

* Django busca un parámetro ``next`` en los datos ``POST``.
* Si el mismo no existe o está vació, Django intenta la URL contenida en la
  cabecera ``Referer``.
* Si la misma está vacía -- por ejemplo, si el navegador de un usuario
  suprime dicha cabecera -- entonces el usuario será redireccionado a
  ``/`` (la raíz del sitio) como un último recurso.

Este es un fragmento de código de plantilla HTML de ejemplo:

.. code-block:: html

    <form action="/i18n/setlang/" method="post">
    <input name="next" type="hidden" value="/next/page/" />
    <select name="language">
        {% for lang in LANGUAGES %}
        <option value="{{ lang.0 }}">{{ lang.1 }}</option>
        {% endfor %}
    </select>
    <input type="submit" value="Go" />
    </form>


Traducciones y JavaScript
=========================

Agregar  traducciones a JavaScript plantea algunos problemas:

* El código JavaScript no tiene acceso a una implementación de ``gettext``.
* El código JavaScript no tiene acceso a los archivos ``.po`` o ``.mo``; los
  mismos necesitan ser enviados desde el servidor.

* Los catálogos de traducción para JavaScript deben ser mantenidos tan
  pequeños como sea posible.

Django provee una solución integrada para estos problemas: convierte las
traducciones a JavaScript, de manera que puedas llamar a ``gettext`` y demás
desde JavaScript.

La vista ``javascript_catalog``
-------------------------------

La solución principal a esos problemas es la vista ``javascript_catalog``, que
genera una biblioteca de código JavaScript con funciones que emulan la interfaz
``gettext`` más un arreglo de cadenas de traducción. Dichas cadenas de
traducción se toman desde la aplicación, el proyecto o el núcleo de Django, de
acuerdo a lo que especifiques ya sea en el diccionario ``info_dict`` o en la URL.

La forma de usar esto es así::

    js_info_dict = {
        'packages': ('your.app.package',),
    }

    urlpatterns [
        
        url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    ]

Cada cadena en ``package`` debe seguir la sintaxis de paquetes separados por puntos
de Python (el mismo formato que las cadenas en ``INSTALLED_APPS``) y deben
referirse a un paquete que contenga un directorio ``locale``. Si se especifican
múltiples paquetes, todos esos catálogos son fusionados en un único catálogo.
esto es útil si usas JavaScript que usa cadenas de diferentes aplicaciones.

Puedes hacer que la vista sea dinámica colocando los paquetes en el patrón de la
URL::

    urlpatterns = [
        url(r'^jsi18n/(?P<packages>\S+?)/$, 'django.views.i18n.javascript_catalog'),
    ]

Con esto, especificas los paquetes como una lista de nombres de paquetes
delimitados por un símbolo ``+`` en la URL. Esto es especialmente útil si tus
páginas usan código de diferentes aplicaciones, este cambia frecuentemente y no
deseas tener que descargar un único gran catálogo. Como una medida de
seguridad, esos valores pueden solo tomar los valores ``django.conf`` o
cualquier paquete de la variable de configuración ``INSTALLED_APPS``.

Usando el catálogo de traducciones JavaScript
---------------------------------------------

Para usar el catálogo simplemente descarga el script generado dinámicamente de
la siguiente forma:

.. code-block:: python

     <script type="text/javascript" src="/path/to/jsi18n/"></script>

Esta es la forma en la que el sitio de administración obtiene el catálogo de
traducciones desde el servidor. Una vez que se ha cargado el catálogo, tu código
JavaScript puede usar la interfaz estándar ``gettext`` para acceder al mismo:

.. code-block:: python

    document.write(gettext('esto será traducido'));

Hay también un interfaz de ``ngettext``:

.. code-block:: python

    var object_cnt = 1 // or 0, or 2, or 3, ...
    s = ngettext('literal para algún caso en singular',
            'literal para casos en plural', object_cnt);

E incluso, una función de interpolación de cadenas:

.. code-block:: python

    function interpolate(fmt, obj, named);

La sintaxis de interpolación se tomó prestada de Python, por lo que 
la función ``interpolate`` soporta tanto la interpolación por nombre y posicional.

**Interpolación posicional**: un ``obj`` que contiene un arreglo de objetos
cuyos valores de sus elementos son secuencialmente interpolados en su
correspondiente marcador de posición ``fmt`` en el mismo orden en que 
aparecen. Por ejemplo::

    fmts = ngettext('There is %s object. Remaining: %s',
        'There are %s objects. Remaining: %s', 11);
    s = interpolate(fmts, [11, 20]);
    // s is 'There are 11 objects. Remaining: 20'


**Interpolación por nombre**: Este modo es seleccionado pasando opcionalmente
un parámetro booleano ``named`` como ``true```. El ``obj`` puede contener un
objeto JavaScript o un arreglo asociado. Por ejemplo::

      d = {
          count: 10
          total: 50
      };

      fmts = ngettext('Total: %(total)s, there is %(count)s object',
          'there are %(count)s of a total of %(total)s objects', d.count);
      s = interpolate(fmts, d, true);

Sin embargo, no debes exagerar con el uso de la interpolación de cadenas -- 
esto sigue siendo JavaScript así que el código tendrá que realizar múltiples 
sustituciones de expresiones regulares. Esto no es tan rápido como la 
interpolación de cadenas en Python, de manera que deberías reservarlo para los 
casos en los que realmente lo necesites (por ejemplo en combinación con 
``ngettext`` para generar pluralizaciones en forma correcta).

Creando catálogos de traducciones JavaScript
--------------------------------------------

Los catálogos de traducciones se crean y actualizan de la misma manera que el
resto de los catálogos de traducciones de Django, con la herramienta
``django-admin.py makemessages``. La única diferencia es que es necesario que 
proveas un parámetro ``-d djangojs``, de la siguiente forma::

    django-admin.py makemessages -d djangojs -l de

Esto crea o actualiza el catálogo de traducción para JavaScript para alemán.
Luego de haber actualizado catálogos, sólo ejecuta 
``django-admin.py compilemessages`` de la misma manera que lo haces con los 
catálogos de traducción normales de Django.

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

* Django no usa ``xgettext`` en forma independiente. Usa envoltorios 
  Python alrededor de ``xgettext`` y ``msgfmt``. Esto es más que nada por
  conveniencia.

``gettext`` en Windows
======================

La siguiente sección es únicamente para personas que necesitan extraer mensajes
IDs o compilar archivos de mensajes (``.po``) en Windows. El trabajo de 
traducción en sí mismo, sólo implica editar los archivos existentes de este tipo, 
excepto si quieres crear tus  propios archivos de mensajes, o si deseas 
compilar o probar cambios en archivos de mensajes, necesitaras usar las 
utilidades ``gettext``.

* Descarga los siguientes archivos zip de los servidores de GNOME desde: 
  http://ftp.gnome.org/pub/gnome/binaries/win32/dependencies/ o de cualquiera de
  los espejos_.

.. _espejos: http://ftp.gnome.org/pub/GNOME/MIRRORS

* ``gettext-runtime-X.zip``
* ``gettext-tools-X.zip``
  
  ``X`` es el numero de versión, la mínima requerida es la 0.15 o superior.

Extrae los 3 archivos en un mismo folder (por ejemplo:
``C:\Archivos de Programas\utilidades gettext``)

* Actualiza las rutas del sistema (PATH):   

  * Dirígete al ``Panel de Control > Sistema > Avanzados > Variables de entorno``
  * En la lista de  ``Variables del sistema`` busca ``Path``, da clic en ``Editar``
  * Y agrega ``;C:\Archivos de Programas\utilidades  gettext\bin`` al final del 
    valor del campo ``valor de la variable``. 

Puedes usar también los binarios ``gettext`` obtenidos en alguna otra parte, 
usando la versión larga ``xgettext --version`` para que el comando trabaje 
adecuadamente. 

.. Warning::

  No intentes usar en Django, utilidades de traducción con un paquete ``gettext``
  si el comando ``xgettext --version`` causa errores al ejecutarse en una ventana 
  de una terminal tal como "xgettext.exe has generated errors and will be closed 
  by   Windows". Algunos binarios de la serie 0.14.4  no soportan este comando. 

¿Qué sigue?
===========

El :doc:`capítulo final<chapter20>` se enfoca en la seguridad -- como proteger
tu sitio y a tus usuarios de atacantes maliciosos.

