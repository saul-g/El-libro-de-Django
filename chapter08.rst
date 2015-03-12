=======================================
Capítulo 8: Vistas avanzadas y URLconfs
=======================================


Un esquema limpio y elegante en una URL, es un detalle importante en una
aplicación Web de alta calidad,  Django te permite **diseñar las URL** que
quieras, sin limitaciones del framework, por lo que no encontraras requerimientos
tipo ``.php`` o ``.cgi``. El sistema de URLconf que usa Django estimula a
generar URLs bonitas, haciendo más sencillo el usarlas, que el no usarlas.
Para más información sobre URLs elegantes, consulta  el artículo titulado
`Cool URIs don't change`_  de el creador de la World Wide Web; Tim Berners-Lee,
donde encontraras excelentes argumentos a favor de las URLs limpias y usables.

.. _`Cool URIs don't change`: http://www.w3.org/Provider/Style/URI

En él :doc:`capítulo 3<chapter03>`, explicamos las bases de las funciones
vista de Django y las URLconfs. En este capítulo conoceremos en detalle algunas
funcionalidades avanzadas en estas dos partes del framework.

Trucos de URLconf
=================

No hay nada de "especial" con las URLconfs -- como cualquier otra cosa en
Django, son sólo codigo Python. Puedes aprovecharte de esto de varias
formas, como se describe más adelante.

Importación de funciones de forma efectiva
------------------------------------------

Considera esta URLconf, que se basa en el ejemplo del
:doc:`capítulo 3<chapter03>`:

.. code-block:: python

    from django.conf.urls import url
    from misitio.views import hola, fecha_actual, horas_adelante

    urlpatterns = [
       url(r'^hola/$', hola),
       url(r'^fecha/$', fecha_actual),
       url(r'^fecha/mas/(\d{1,2})/$', horas_adelante),
    ]

Como se explicó en él :doc:`capítulo 3<chapter03>`, cada entrada en una
URLconf debe incluir una función vista asociada, que se pasa directamente como
un método. Esto significa que es necesario importar cada una de las funciones
de vista o ``views``  en la parte superior del módulo.

Sin embargo a medida que las aplicaciones Django crecen en complejidad, sus
URLconf crecen también, por lo que mantener esos import puede ser tedioso de
manejar. (Por cada nueva función vista, tienes que recordar importarla y la
declaración de importaciones tiende a volverse demasiado larga si se utiliza
este método). Es posible evitar esa tarea tediosa importando el módulo
``views`` directamente.

Este ejemplo de URLconf es equivalente al anterior:

.. parsed-literal::

    from django.conf.urls import url
    **from misitio import views**

    urlpatterns = [
       url(r'^hola/$', **views.hola**),
       url(r'^fecha/$', **views.fecha_actual**),
       url(r'^fecha/mas/(\d{1,2})/$', **views.horas_adelante**),
    ]

Como puedes observar la sintaxis para la variable urlpatterns, siempre es una
lista Python de una instancia de una url().

Django ofrece otra forma de especificar la función vista para un patrón en
particular en la URLconf: se le puede pasar un string que contiene el nombre del
módulo y el nombre de la función en lugar del método.

Continuando con el ejemplo:

.. parsed-literal::

    from django.conf.urls import url

    urlpatterns = [
       url(r'^hola/$', **'misitio.views.hola'**),
       url(r'^fecha/$', **'misitio.views.fecha_actual'**),
       url(r'^fecha/mas/(\d{1,2})/$', **'misitio.views.horas_adelante'**),
    ]

(Nota que los nombres de las vistas están entre comillas. Estamos usando
``'misitio.views.hola'`` -- con comillas, en lugar de usar
``misitio.views.hola`` directamente.)

Al usar esta técnica ya no es necesario importar las funciones vista;
Django importa automáticamente la función vista apropiada, la primera vez que
sea necesite, según la cadena que describa el nombre y la ruta de la función
vista.

Casos especiales de URLs en modo Debug
--------------------------------------

Otra forma muy común de construir ``urlpatterns`` de forma dinámica, es
simplemente comprobando  el valor de la configuración ``DEBUG`` en
tiempo de ejecución, para alterar el comportamiento de las URLconf mientras
se desarrolla en el modo de depuración de Django así:

.. code-block:: python

    from django.conf import settings
    from django.conf.urls import url
    from misitio import views

    urlpatterns =[
        url(r'^$', views.indice),
        url(r'^(\d{4})/([a-z]{3})/$', views.archivos_mes),
    }

    if settings.DEBUG:
        urlpatterns += [
           url (r'^debuginfo/$', views.debug),
        ]

En este ejemplo, la URL ``/debuginfo/`` sólo estará disponible si tu
configuración ``DEBUG`` tiene el valor ``True``.

Trabajar en modo ``DEBUG``, significa sobre todo depurar, por lo que Django,
nos provee de herramientas para manejar los casos más comunes del desarrollo
Web, como manejar archivos estáticos (hojas de estilo, java script) y archivos
media (imágenes, pdf), de forma local. Django hace una gran distinción en el
manejo de estos dos tipos de contenido, mientras que se encarga de servir los
archivos estáticos de forma automática, para servir los archivos media de forma
local, es necesario habilitar una vista opcional y enlazarla a una URLconf en
modo ``DEBUG``.

.. code-block:: python

    from django.views.static import serve
    from django.conf import settings
    from django.conf.urls import url
    from misitio import views

    urlpatterns =[
        url(r'^$', views.indice),
        url(r'^(\d{4})/([a-z]{3})/$', views.archivos_mes),
    }

    if settings.DEBUG:
        urlpatterns += [
            url(r'^media/(?P<path>.*)$', serve, {
                'document_root': settings.MEDIA_ROOT,
            }),
    ]

En este ejemplo, llamamos a la vista ``serve``, que pertenece al paquete
``static``, que se encarga de servir directorios, solo le pasamos la ruta
especificada en ``MEDIA_ROOT``, la cual contiene la raíz de los archivos media,
esta vista se encargara de servir  archivos (por ejemplo imágenes, videos)
siempre y cuando el modo ``DEBUG`` este activado. En este ejemplo la variable
``MEDIA_URL`` asume que el valor es 'media', aunque  podemos cambiarlo segun
nuestras necesidades. De esta forma la URL ``/media/`` sólo estará disponible
si la configuración ``DEBUG`` tiene asignado el valor ``True``.

.. Warning::

    Esta vista es ineficiente y no debe ser usada en producción, por lo que
    asegúrate de usarla solo en el desarrollo de tus aplicaciones de forma local.
    Para servir archivos en producción utiliza un servidor dedicado, consulta
    él :doc:`capítulo 12<chapter12>`, para conocer algunos servidores que te pueden
    ayudar en esa tarea.

Usar grupos con nombre
----------------------

Hasta ahora en todos nuestros ejemplos URLconf hemos usado, grupos de
expresiones regulares *sin nombre* -- es decir, ponemos paréntesis en las partes
de la URL que queremos capturar y Django le pasa ese texto capturado a la
función vista como un argumento posicional. En un uso más avanzado, es posible
usar grupos de expresiones regulares *con nombre* para capturar partes de la URL
y pasarlos como argumentos *clave* a una vista.

.. admonition:: Argumentos claves vs. Argumentos posicionales

    A una función de Python se la puede llamar usando argumentos clave o
    argumentos posicionales -- y, en algunos casos, los dos al mismo
    tiempo. En una llamada por argumentos clave, se especifican los
    nombres de los argumentos junto con los valores que se le pasan. En una
    llamada por argumento posicional, sencillamente pasas los argumentos sin
    especificar explícitamente qué argumento concuerda con cual valor; la
    asociación está implícita en el orden de los argumentos.

    Por ejemplo, considera esta sencilla función::

        def venta(articulo, precio, cantidad):
            print ("Vendidos: %s unidad(es) de %s a %s" % (cantidad, articulo, precio))

    Para llamarla con argumentos posicionales, se especifican los argumentos
    en el orden en que están listados en la definición de la función::

        venta('Calcetines', '$2.50', 6)

    Para llamarla con argumentos de palabra clave, se especifican los nombres de
    los argumentos junto con sus valores. Las siguientes sentencias son
    equivalentes::

        venta(articulo='Calcetines', precio='$2.50', cantidad=6)
        venta(articulo='Calcetines', cantidad=6, precio='$2.50')
        venta(precio='$2.50', articulo='Calcetines', cantidad=6)
        venta(precio='$2.50', cantidad=6, articulo='Calcetines')
        venta(cantidad=6, articulo='Calcetines', precio='$2.50')
        venta(cantidad=6, precio='$2.50', articulo='Calcetines')

    Finalmente, se pueden mezclar los argumentos posicionales y por palabra
    clave, siempre y cuando los argumentos posicionales estén listados antes que
    los argumentos por palabra clave. Las siguientes sentencias son equivalentes
    a los ejemplos anteriores::

        venta('Calcetines', '$2.50', cantidad=6)
        venta('Calcetines', precio='$2.50', cantidad=6)
        venta('Calcetines', cantidad=6, precio='$2.50')

En las expresiones regulares de Python, la sintaxis para los grupos de
expresiones regulares con nombre es ``(?P<nombre>patrón)``, donde ``nombre`` es
el nombre del grupo y ``patrón`` es algún patrón a buscar.

Aquí hay un ejemplo de URLconf que usa grupos sin nombre, en el primer patrón
captura el año, para mostrar una lista de libros por año, en el segundo captura
el año y el mes, para mostrar una lista de libros de acuerdo a un año y mes en
especifico, el ultimo muestra una lista de libros de acuerdo al año, el mes y
el dia:

.. code-block:: python

    from django.conf.urls import url
    from libros import views

    urlpatterns = [
        url(r'^libros/(\d{4})/$', views.libros_año),
        url(r'^libros/(\d{4})/(\d{2})/$', views.libros_mensuales),
        url(r'^libros/(\d{4})/(\d{2})/(\d{2})/$', views.libros_diarios),
    ]

Aquí está la misma URLconf, reescrita para usar grupos con nombre:

.. code-block:: python

    from django.conf.urls import url
    from libros import views

    urlpatterns = [
        url(r'^libros/(?P<año>\d{4})/$', views.libros_año),
        url(r'^libros/(?P<año>\d{4})/(?P<mes>\w{3})/$', views.libros_mes),
        url(r'^libros/(?P<año>\d{4})/(?P<mes>\w{3})/(?P<dia>\d{2})/$', views.libros_dia),
    ]

.. La ñ solo es para demostracion, no funcionan

.. Warning::

    ¡Ten cuidado con las "ñ"!

Esto produce exactamente el mismo resultado que el ejemplo anterior, con una
sutil diferencia: se le pasa a las funciones vista los valores capturados como
argumentos clave en lugar de argumentos posicionales.

Por ejemplo, con los grupos sin nombre una petición a ``/libros/2006/03/``
resultaría en una llamada de función equivalente a esto::

    libros_mensuales(request, '2006', '03')

Sin embargo, con los grupos con nombre, la misma petición resultaría en esta
llamada de función::

    libros_mensuales(request, año='2006', mes='03')

En la práctica, usar grupos con nombres hace que tus URLconfs sean un poco más
explícitas y menos propensas a errores causados por argumentos -- y puedes
reordenar los argumentos en las definiciones de tus funciones vista. Siguiendo
con el ejemplo anterior, si quisiéramos cambiar las URLs para incluir el mes
*antes* del año, y estuviéramos usando grupos sin nombre, tendríamos que
acordarnos de cambiar el orden de los argumentos en la vista ``libros_mes``.
Si estuviéramos usando grupos con nombre, cambiar el orden de los parámetros
capturados en la URL no tendría ningún efecto sobre la vista.

Por supuesto, los beneficios de los grupos con nombre tienen el costo de la
falta de brevedad; algunos desarrolladores opinan que la sintaxis de los grupos
con nombre es fea y larga.  Aún así, otra ventaja de los grupos con nombres es
la facilidad de lectura, especialmente para las personas que no están
íntimamente relacionadas con las expresiones regulares o con tu aplicación
Django en particular. Es más fácil ver lo que está pasando, a primera vista, en
una URLconf que usa grupos con nombre.

.. Warning::

    Una advertencia al usar grupos con nombre en una URLconf es que un simple
    patrón URLconf no puede contener grupos con nombre y sin nombre. Si haces
    eso, Django no generará ningún mensaje de error, pero probablemente
    descubras que tus URLs no se están disparando de la forma esperada.

El algoritmo de combinación/agrupación
--------------------------------------

Aquí está específicamente el algoritmo que sigue el parser URLconf, con respecto
a grupos con nombre vs. grupos sin nombre en una expresión regular:

* Si existe algún argumento con nombre, usará esos, ignorando los argumentos
  sin nombre.

* Además, pasará todos los argumentos sin nombre como argumentos
  posicionales.

* En ambos casos, pasará cualquier opción extra como argumentos de palabra
  clave. Ver la próxima sección para más información.

Pasarle opciones extra a las funciones vista
--------------------------------------------

A veces te encontrarás escribiendo funciones vista que son bastante similares,
con tan sólo algunas pequeñas diferencias. Por ejemplo, digamos que tienes dos
vistas cuyo contenido es idéntico excepto por la plantilla que utilizan:

.. snippet::
   :filename: urls.py

    from django.conf.urls import url
    from biblioteca import views

    urlpatterns = [
        url(r'^inicio/$', views.vista_inicio),
        url(r'^indice/$', views.vista_indice),
    ]

.. snippet::
   :filename: views.py

    from django.shortcuts import render
    from biblioteca.models import Libro

    def vista_inicio(request):
        libros = Libro.objects.all()
            return render(request, 'bienvenidos.html', {'libros': libros})

    def vista_indice(request):
        libros = Libro.objects.all()
            return render(request, 'indice.html', {'libros': libros})

Con este codigo nos estamos repitiendo y eso no es elegante. Al comienzo,
podrías pensar en reducir la redundancia usando la misma vista para ambas URLs,
poniendo paréntesis alrededor de la URL para capturarla y comprobando la URL
dentro de la vista para determinar la plantilla, como mostramos a continuación:

.. snippet::
   :filename: urls.py

    from django.conf.urls import url
    from biblioteca import views

    urlpatterns = [
        url(r'^inicio/$', views.vista_indice),
        url(r'^indice/$', views.vista_indice),
    ]

.. snippet::
   :filename: views.py

    from django.shortcuts import render
    from biblioteca.models import Libro

    def vista_indice(request, url):
        libros = Libro.objects.all()
        if url == 'inicio':
            plantilla = 'bienvenidos.html'
        elif url == 'indice':
            plantilla = 'indice.html'
        return render(request, plantilla, {'libros': libros})


Sin embargo, el problema con esa solución es que acopla fuertemente tus URLs y
tu codigo Si decides renombrar ``/inicio/`` a ``/bienvenidos/``, tienes que
recordar cambiar el codigo de la vista.

La solución elegante involucra un parámetro URLconf opcional. Cada patrón en una
URLconf puede incluir un tercer ítem: un diccionario de argumentos de palabra
clave para pasarle a la función vista.

Con esto en mente podemos reescribir nuestro ejemplo anterior así:

.. snippet::
   :filename: urls.py

    from django.conf.urls import url
    from biblioteca import views

    urlpatterns = [
        url(r'^inicio/$', views.vista_indice, {'plantilla': 'bienvenidos.html'}),
        url(r'^indice/$', views.vista_indice, {'plantilla': 'indice.html'}),
    ]


.. snippet::
   :filename: views.py

    from django.shortcuts import render
    from biblioteca.models import Libro

    def vista_inicio(request, plantilla):
        libros = Libro.objects.all()
            return render(request, plantilla, {'libros': libros})

Como puedes ver, la URLconf en este ejemplo especifica ``plantilla`` en la
URLconf. La función vista lo trata como a cualquier otro parámetro.

Esta técnica de la opción extra en la URLconf es una bonita forma de enviar
información adicional a tus funciones vista sin tanta complicación. Por ese
motivo es que es usada por algunas aplicaciones incluidas en Django, más
notablemente el sistema de vistas genéricas, que tratamos en el
:doc:`capítulo 11<chapter11>`.

La siguiente sección contiene algunas ideas sobre cómo puedes usar la técnica
de la opción extra en la URLconf como parte de tus proyectos.

Simulando valores capturados en URLconf
---------------------------------------

Supongamos que posees un conjunto de vistas que son disparadas vía un patrón y
otra URL que no lo es pero cuya lógica de vista es la misma. En este caso puedes
"simular" la captura de valores de la URL usando opciones extra de URLconf para
manejar esa URL extra con una única vista.

Por ejemplo, podrías tener una aplicación que muestra algunos datos para un día
en particular, con URLs tales como::

    /libros/enero/01/
    /libros/enero/02/
    /libros/enero/03/
    # ...
    /libros/abril/30/
    /libros/abril/31/

A primera vista parece algo complicado, sin embargo esto es simple de manejar
-- puedes capturar los parámetros en una URLconf como esta (usando sintaxis de
grupos con nombre)::

    urlpatterns = [
        url(r'^libros/(?P<mes>\w{3})/(?P<dia>\d{2})/$', views.libros_dia),
        ]

Y la declaración de la función vista se vería así::

    def libros_dia(request, mes, dia):
        # ....

Este enfoque es simple y directo -- no hay nada que no hayamos visto antes. El
truco entra en juego cuando quieres agregar otra URL que usa ``libros_dia``
pero cuya URL no incluye un ``mes`` ni/o un ``dia``.

Por ejemplo, podrías querer agregar otra URL, ``/libros/favoritos/``, que sería
equivalente a ``/libros/enero/06/``. Puedes sacar provecho de las opciones extra
de las URLconf de la siguiente forma::

    urlpatterns = [
        url(r'^libros/favoritos/$', views.libros_dia, {'mes': 'enero', 'dia': '06'}),
        url(r'^libros/(?P<mes>\w{3})/(?P<dia>\d){2}/$', views.libros_dia),
    ]

El detalle genial aquí es que no necesitas cambiar tu función vista para nada. A
la función vista sólo le incumbe el obtener los parámetros ``mes`` y ``dia``
-- no importa si los mismos provienen de la captura de la URL o de parámetros
extra.

Convirtiendo una vista en genérica
----------------------------------

Factorizar, es una buena práctica de programación, ya que nos permite aislar las
partes comunes del codigo. Tomemos por ejemplo  estas dos funciones Python::

    def di_hola(nombre_persona):
        print ('Hola, %s' % nombre_persona)

    def di_adios(nombre_persona):
        print ('Adios, %s' % nombre_persona)

Podemos extraer el saludo para convertirlo en un parámetro::

    def saludar(nombre_persona, saludo):
        print ('%s, %s' % (saludo, nombre_persona))

Puedes aplicar la misma filosofía a tus vistas Django,  usando los parámetros
extra de URLconf.

Con esto en mente, puedes comenzar a hacer abstracciones al nivel más alto de
tus vistas. En lugar de pensar "Esta vista muestra una lista de objetos
``Libro``" y "Esta otra vista muestra una lista de objetos ``Editor``",
descubre que ambas son casos específicos de "Una vista que muestra una lista de
objetos, donde el tipo de objeto es variable".

Usemos este codigo como ejemplo:

.. snippet::
   :filename: urls.py

    from django.conf.urls import url
    from biblioteca import views

    urlpatterns = [
        url(r'^inicio/$', views.lista_libros)
        url(r'^indice/$', views.lista_editores),
    ]

.. snippet::
   :filename:  views.py

    from django.shortcuts import render
    from biblioteca.models import Libro, Editor

    def lista_libros(request):
        lista_libros = Libro.objects.all()
        return render(request, 'biblioteca/lista_libros.html', {'lista_libros': lista_objetos})

    def lista_editores(request):
        lista_editores = Editor.objects.all()
        return render(request, 'biblioteca/lista_editores.html', {'lista_editores': lista_objectos})

Ambas vistas hacen esencialmente lo mismo: muestran una lista de objetos.
Refactoricemos el codigo para extraer el tipo de objetos que muestran:

.. snippet::
   :filename: urls.py

    from django.conf.urls import url
    from biblioteca import views

    urlpatterns = [
        url(r'^lista_libros/$', views.lista_objectos, {'model': models.Libro}),
        url(r'^lista_editores/$', views.lista_objectos, {'model': models.Editor}),
    ]

.. snippet::
   :filename:  views.py

    from django.shortcuts import render

    def lista_objectos(request, model):
        lista_objectos = model.objects.all()
        plantilla = 'biblioteca/%s_lista.html' % model.__name__.lower()
        return render(request, plantilla, {'lista_objectos': lista_objectos})

Con esos pequeños cambios tenemos de repente, una vista reusable e
independiente del modelo. De ahora en adelante, cada vez que necesitemos  una
lista que muestre un listado de objetos, podemos simplemente rehusar esta vista
``lista_objectos`` en lugar de escribir mas codigo.

A continuación, un par de notas acerca de lo que hicimos:

* Estamos pasando las clases de modelos directamente, como el parámetro
  ``model``. El diccionario de opciones extra de URLconf puede pasar
  cualquier tipo de objetos Python -- no sólo cadenas.

* La línea ``model.objects.all()`` es un ejemplo de tipado de pato (*duck
  typing*): "Si camina como un pato, y habla como un pato, podemos tratarlo
  como un pato." Nota que el codigo no conoce de qué tipo de objeto se trata
  ``model``; el único requerimiento es que ``model`` tenga un atributo
  ``objects``, el cual a su vez tiene un método ``all()``.

* Estamos usando ``model.__name__.lower()`` para determinar el nombre de la
  plantilla. Cada clase Python tiene un atributo ``__name__`` que retorna el
  nombre de la clase. Esta característica es útil en momentos como este,
  cuando no conocemos el tipo de clase hasta el momento de la ejecución. Por
  ejemplo, el ``__name__`` de la clase ``BlogEntry`` es la cadena
  ``BlogEntry``.

* En una sutil diferencia entre este ejemplo y el ejemplo previo, estamos
  pasando a la plantilla el nombre de variable genérico ``lista_objectos``.
  Podemos fácilmente cambiar este nombre de variable a ``lista_libros`` o
  ``lista_editores``, pero hemos dejado eso como un ejercicio para el lector.

Debido a que los sitios Web impulsados por bases de datos tienen varios patrones
comunes, Django incluye un conjunto de "vistas genéricas" que usan justamente
esta técnica para ahorrarte tiempo. Nos ocuparemos de las vistas genéricas
incluidas con Django en capítulos siguientes.

Pasando opciones de configuración a una vista
---------------------------------------------

Si estás distribuyendo una aplicación Django, es probable que tus usuarios
deseen cierto grado de configuración. En este caso, es una buena idea agregar
puntos de extensión a tus vistas para las opciones de configuración que piensas
que la gente pudiera desear cambiar. Puedes usar los parámetros extra de URLconf
para este fin.

Una parte de una aplicación que normalmente se hace configurable es el nombre
de la plantilla::

    def una_vista(request, plantilla):
        var = haz_algo()
        return render_to_response(plantilla, {'var': var})

Entendiendo la precedencia entre valores capturados vs. opciones extra
----------------------------------------------------------------------

Cuando se presenta un conflicto, los parámetros extra de la URLconf tiene
precedencia sobre los parámetros capturados. En otras palabras, si tu URLconf
captura una variable de grupo con nombre y un parámetro extra de URLconf incluye
una variable con el mismo nombre, se usará el parámetro extra de la URLconf.

Por ejemplo, analicemos esta URLconf::

    from django.conf.urls import url

    urlpatterns = [
        url(r'^libros/(?P<id>\d+)/$', views.lista_libros, {'id': 3}),
    )

Aquí, tanto la expresión regular como el diccionario extra incluye un ``id``.
Tiene precedencia el ``id`` fijo especificado en la URL. Esto significa que
cualquier petición (por ej. ``/libros/2/`` o ``/libros/432432/``) serán tratados
como si ``id`` estuviera fijado a ``3``, independientemente del valor capturado
en la URL.

Los lectores atentos notarán que en este caso es una pérdida de tiempo y de
tipeo capturar ``id`` en la expresión regular, porque su valor será siempre
descartado en favor del valor proveniente del diccionario. Esto es correcto;
lo traemos a colación sólo para ayudarte a evitar el cometer este error.

Usando argumentos de vista por omisión
--------------------------------------

Otro truco comun es el de especificar parámetros por omisión para los
argumentos de una vista. Esto le indica a la vista qué valor usar para un
parámetro por omisión si es que no se especifica ninguno.

Veamos un ejemplo:

.. snippet::
   :filename: urls.py

    from django.conf.urls import url
    from biblioteca import views

    urlpatterns = [
        (r'^libros/$', views.pagina),
        (r'^libros/pagina(?P<num>\d+)/$', views.pagina),
    ]

.. snippet::
   :filename: views.py

    def pagina(request, num='1'):
        # La salida apropiada de pagina de acuerdo a num.
        # ...

Aquí, ambos patrones de URL apuntan a la misma vista -- ``views.pagina`` pero
el primer patrón no captura nada de la URL. Si el primer patrón es disparado, la
función ``pagina()`` usará su argumento por omisión para ``num``, ``"1"``. Si el
segundo patrón es disparado, ``pagina()`` usará el valor de ``num`` que se haya
capturado mediante la expresión regular.

Es común usar esta técnica en combinación con opciones de configuración,
como explicamos previamente. Este  ejemplo implementa una pequeña mejora al
ejemplo de la sección "`Pasando opciones de configuración a una vista`_":
provee un valor por omisión para la ``plantilla``::

    def una_vista(request, plantilla='biblioteca/mi_vista.html'):
        var = haz_algo()
        return render_to_response(plantilla, {'var': var})

Manejando vistas en forma especial
----------------------------------

En algunas ocasiones tendrás un patrón en tu URLconf que maneja un gran número
de URLs, pero necesitarás realizar un manejo especial en una de ellas. En este
caso, saca provecho de la forma lineal en la que son procesadas la URLconfs y
coloca el caso especial primero.

Por ejemplo, las páginas "agregar un objeto" en el sitio de administración de
Django están representadas por la siguiente línea de URLconf::

    urlpatterns = [
        # ...
        url('^([^/]+)/([^/]+)/add/$', views.add_stage),
        # ...
    ]

Esto se disparará con URLs como ``/libros/entradas/add/`` y
``/auth/groups/add/``. Sin embargo, la página "agregar" de un objeto usuario
(``/auth/user/add/``) es un caso especial -- la misma no muestra todos los
campos del formulario, muestra dos campos de contraseña, etc. Podríamos resolver
este problema tratando esto como un caso especial en la vista, de esta manera::

    def add_stage(request, app_label, model_name):
        if app_label == 'auth' and model_name == 'user':
            # do special-case code
        else:
            # do normal code

Pero eso es poco elegante por una razón que hemos mencionado en múltiples
oportunidades en este capítulo: Incrusta la lógica de las URLs en la vista. Una
manera más elegante sería la de hacer uso del hecho que las URLconfs se procesan
desde arriba hacia abajo::

    urlpatterns = [
        # ...
        url('^auth/user/add/$', views.user_add_stage),
        url('^([^/]+)/([^/]+)/add/$', views.add_stage),
        # ...
    ]

Con esto, una petición a ``/auth/user/add/`` será manejada por la vista
``user_add_stage``. Aunque dicha URL coincide con el segundo patrón, coincide
primero con el patrón ubicado más arriba. (Esto es lógica de corto circuito).

Capturando texto en URLs
------------------------

Cada argumento capturado es enviado a la vista como una cadena Python, sin
importar qué tipo de coincidencia se haya producido con la expresión regular.
Por ejemplo en esta línea de URLconf::

    url(r'^libros/(?P<año>\d{4})/$', views.libros_por_año),

el argumento ``año`` de ``views.libros_por_año()`` será una cadena, no un
entero, aun cuando ``\d{4}`` sólo coincidirá con cadenas que representen enteros.

Es importante tener esto presente cuando estás escribiendo codigo de vistas.
Muchas funciones incluidas con Python son exigentes (y eso es bueno) acerca de
aceptar objetos de cierto tipo. Un error común es intentar crear un objeto
``datetime.date`` con valores de cadena en lugar de valores enteros::

    >>> import datetime
    >>> datetime.date('1993', '7', '9')
    Traceback (most recent call last):
        ...
    TypeError: an integer is required
    >>> datetime.date(1993, 7, 9)
    datetime.date(1993, 7, 9)

Traducido a una URLconf y una vista, este error se vería así::

    from django.conf.urls import url
    from biblioteca import views

    urlpatterns = [
        url(r'^libros/(\d{4})/(\d{2})/(\d{2})/$', views.libros_dia),
    ]

    import datetime

    def librosdiarios(request, año, mes, dia):
        # Lo siguiente lanza un error del "TypeError"
        fecha = datetime.date(añor, mes, dia)

En cambio ``librosdiarios`` puede ser escrito correctamente de la siguiente
forma:

.. snippet::
   :filename: librosdiarios.py

    def librosdiarios(request, año, mes, dia):
        fecha = datetime.date(int(año), int(mes), int(dia))

Observa que ``int()`` lanza un ``ValueError`` cuando le pasas una cadena que no
está compuesta únicamente de dígitos, pero estamos evitando ese error en este
caso porque la expresión regular en nuestra URLconf ya se ha asegurado que sólo
se pasen a la función vista cadenas que contengan dígitos.

Entendiendo dónde busca una URLconf
-----------------------------------

Cuando llega una petición, Django intenta comparar los patrones de la URLconf
con la URL solicitada como una cadena Python normal (no como una cadena
Unicode). Esto no incluye los parámetros de ``GET`` o ``POST`` o el nombre del
dominio. Tampoco incluye la barra inicial porque toda URL tiene una barra
inicial.

Por ejemplo, en una petición del tipo  ``http://www.example.com/entrada/``
Django tratará de encontrar una coincidencia para ``entrada/``. En una petición
para ``http.//www.example.com/entrada/?pagina3`` Django tratará de buscar una
coincidencia para ``entrada/``.

El método de la petición (por ejemplo  ``POST``, ``GET``, ``HEAD``) *no*  se
tiene en cuenta cuando se recorre la URLconf. En otras palabras, todos los
métodos serán encaminados hacia la misma función para la misma URL. Es
responsabilidad de una función vista manejar de forma distinta en base
al método de la petición.


Abstracciones de alto nivel en las funciones vista
--------------------------------------------------

Como se menciona anteriormente, es responsabilidad de una vista manejar de
forma distinta cualquier peticion, por lo que es necesario tratar de forma
distinta los metodos ``POST``, ``GET``. Veamos como construir una vista que
trate esto de forma agradable. Considera este diseño: URLconf/view:

.. snippet::
   :filename: urls.py

    from django.conf.urls import url
    from biblioteca import views

    urlpatterns = [
        # ...
        url(r'^indice/$', views.indice),
        # ...
    ]

.. snippet::
   :filename: views.py

    from django.http import Http404, HttpResponseRedirect
    from django.shortcuts import render

    def indice(request):
        if request.method == 'POST':
            haz_algo_para_post()
            return HttpResponseRedirect('/inicio/')
        elif request.method == 'GET':
            haz_algo_para_get()
            return render(request, 'pagina.html')
        else:
            raise Http404()

En este ejemplo, la vista ``indice()`` se encarga de manejar  tanto peticiones
``POST`` como ``GET``, que son totalmente distintas. La única cosa que
comparten en común es la misma URL: ``/inicio/``. Como tal es poco elegante
manejar ambas peticiones ``POST`` y ``GET`` en la misma función de vista. Seria
más agradable tener dos funciones de vista separadas -- una que maneje las
peticiones ``GET`` y la otra que se encargue de las peticiones  ``POST`` -- por
lo que solo debes asegurarte de llamar apropiadamente a la que necesites.

Podemos hacer esto escribiendo una función de vista que delegue la
responsabilidad a otra vista, antes o después de ejecutar la lógica definida.
Este ejemplo muestra como esta técnica nos puede ayudar a simplificar la
vista ``indice()``:

.. snippet::
   :filename: views.py

    from django.http import Http404, HttpResponseRedirect
    from django.shortcuts import render

    def vista_divida(request, GET=None, POST=None):
        if request.method == 'GET' and GET is not None:
            return GET(request)
        elif request.method == 'POST' and POST is not None:
            return POST(request)
        raise Http404

    def peticion_get(request):
        assert request.method == 'GET'
        haz_algo_para_get()
        return render(request, 'pagina.html')

    def peticion_post(request):
        assert request.method == 'POST'
        haz_algo_para_post()
        return HttpResponseRedirect('/indice/')

.. snippet::
   :filename: urls.py

    from django.conf.urls import url
    from biblioteca import views

    urlpatterns = [
        # ...
        (r'^indice/$', views.vista_divida, {'GET': views.peticion_get, 'POST': views.peticion_post}),
        # ...
    ]

Veamos lo que hicimos:

* Escribimos una nueva vista, llamada ``vista_divida()``,  que delega la
  responsabilidad a dos vistas mas basadas en el tipo de petición
  mediante el método ``request.method``. Este busca dos argumentos clave,
  ``GET`` y ``POST``,  los cuales deben ser *funciones vista*. Si
  ``request.method`` es ``'GET'``, entonces se llama a la vista ``GET``. Si
  ``request.method`` es ``'POST'``, entonces llama a la vista ``POST``. Si
  ``request.method`` es algo como (``HEAD``, etc.), o si  ``GET`` o  ``POST``
  no son proporcionados a la función, entonces se lanza un error del tipo
  ``Http404`` (pagina no encontrada).

* En la URLconf, conectamos ``/indice/`` con  ``vista_divida()`` y pasamos
  los argumentos extras -- la función de vista para usar ``GET`` y ``POST``,
  respectivamente.

* Finalmente,  separamos la vista ``vista_divida()`` en dos funciones --
  ``peticion_get()`` y ``peticion_post()``. Esto es mucho más agradable que
  empaquetar  toda la lógica en una simple vista.

  Observa que esta función de vista, técnicamente ya  no tiene que comprobar
  ``request.method``, porque  la ``vista_divida()`` lo hace. (En el momento en
  que se llame a ``peticion_post()``, por ejemplo, podemos confiar que
  ``request.method`` es ``'post'`` ). No obstante, para estar seguros y para
  que sirva como comprobación,  agregamos un ``assert`` solo para asegurarnos
  que ``request.method`` haga lo esperado.

Hemos creado una vista genérica agradable que encapsula la lógica y delega el
método de petición o ``request.method`` a la vista. Nada en este método:
``vista_divida()`` ata a nuestra aplicación en particular, por lo que
que podemos rehusarla en otros proyectos.

Podemos encontrar una forma de perfeccionar ``vista_divida()``. Rescribiendo
el método, ya que este asume que las vistas ``GET`` y ``POST`` no toman mas
argumentos que un ``request``. Entonces ¿Qué pasa si quisiéramos usar
``vista_divida()`` con otra vista,  por ejemplo para capturar el texto de
una URLs, o para que tome argumentos clave opcionales?

Para hacer eso podemos usar una característica agradable de Python: que nos
permite usar argumentos variables definidos con asteriscos. Dejaremos primero
que el ejemplo lo  explique::

    def vista_divida(request, *args, **kwargs):
        vista_get = kwargs.pop('GET', None)
        vista_post = kwargs.pop('POST', None)
        if request.method == 'GET' and vista_get is not None:
            return vista_get(request, *args, **kwargs)
        elif request.method == 'POST' and vista_post is not None:
            return vista_post(request, *args, **kwargs)
        raise Http404

Refactorizamos el método ``vista_divida``  para remover los argumentos clave
``GET`` y ``POST``, y para poder usar ``*args`` y ``**kwargs`` (Observa los
asteriscos). Esta es una característica de Python que permite a las funciones
aceptar de forma dinámica y arbitraria un numero de argumentos desconocidos,
cuyos nombres no se conocen, hasta en tiempos de ejecución. Con un simple
asterisco en la parte superior del parámetro, definimos cualquier argumento
*posicional*, por lo que la función se comportara como una tupla. Si usamos dos
asteriscos en la parte  superior del parámetro en la definición de la función,
cualquier *argumento clave* que pasemos a la función se comportara como un
diccionario.

Por ejemplo, con esta función::

    def vista(*args, **kwargs):
        print ("Los argumentos posicionales son:")
        print (args)
        print ("Los argumentos clave son:")
        print (kwargs)

Por convención ``*args`` se refiere a parámetros posicionales, mientras que
``**kwargs`` se refiere a argumentos clave. Esta es la forma en que trabajaría::

    >>> vista(1, 2, 3)
    Los argumentos posicionales son:
    (1, 2, 3)
    Los argumentos clave son:
    {}
    >>> vista(1, 2, name='Adrian', framework='Django')
    Los argumentos posicionales son:
    (1, 2)
    Los argumentos clave son:
    {'framework': 'Django', 'name': 'Adrian'}

.. comprobado en python 3.4

Volviendo a ``dividir_vista()``, puedes usar ``*args`` y ``**kwargs``
para aceptar *cualquiera* de los argumentos en la función y pasárselos a  la
vista apropiada. Pero antes de hacer esto, es necesario llamar  a
``kwargs.pop()`` para obtener los argumentos ``GET`` y ``POST``, si están
disponibles. (Usamos ``pop()`` con un  valor predeterminado y ``None`` para
evitar un error del tipo ``KeyError`` si uno de los otros no está definido.)

Empacando Funciones de Vista
----------------------------

.. Wrapping:  empaque, envoltorio, envoltura
.. Título original: Wrapping View Functions

Nuestro truco final toma la ventaja de las técnicas avanzadas de Python.
Digamos que encontramos un montón de codigo repetitivo a lo largo de varias
vistas, como en este ejemplo::

    def vista1(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        # ...
        return render(request, 'plantilla1.html')

    def vista2(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        # ...
        return render(request, 'plantilla2.html')

    def vista3(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        # ...
        return render(request, 'plantilla3.html')

Tenemos aquí, que cada vista empieza comprobando que ``request.user`` este
autentificado -- estos es, que el usuario actual se haya identificado
correctamente en el sitio -- si no se redirecciona  a  ``/accounts/login/``.
(Observa que aun no cubrimos ``request.user``  --El cual veremos en el
capitulo 14  pero tal como imaginas ``request.user``  representa al usuario
actual, ya sea anónimo o registrado.)

Seria agradable si quitaramos un poco de codigo repetitivo de cada una de estas
vistas, simplemente marcándolas como vistas que requieren autentificación.
Podemos hacer esto haciendo un **wrapper**. Tomate un momento para estudiar lo
siguiente::

    def requiere_login(view):
        def vista_nueva(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return HttpResponseRedirect('/accounts/login/')
            return view(request, *args, **kwargs)
        return vista_nueva

La función ``requiere_login``, toma una función vista (``view``)  y retorna
una nueva función vista (``vista_nueva``). La nueva función ``vista_nueva`` esta
definida  *dentro*  de ``requiere_login``y maneja la lógica comprobando que
``request.user.is_authenticated()`` (el usuario este identificado) y delegándolo
a la vista original (``view``).

Ahora, podemos remover la comprobación ``if not request.user.is_authenticated()``
de nuestras vistas y simplemente envolviéndolas con ``requiere_login`` en
nuestra URLconf::

    from django.conf.urls import urls
    from .views import requiere_login, vista1, vista2, vista3

    urlpatterns = [
        url(r'^vista1/$', requiere_login(vista1)),
        url(r'^vista2/$', requiere_login(vista2)),
        url(r'^vista3/$', requiere_login(vista3)),
    ]

Esto tiene el mismo efecto que el codigo anterior, pero con menos codigo redundante.
Acabamos de crear una agradable función genérica -- ``requiere_login()`` que
podemos usar para envolver (wrapping) en torno a cualquier vista para hacer que
esta requiera autentificación.

Incluyendo otras URLconfs
=========================

Si tu intención es que tu codigo sea usando en múltiples sitios implementados
con Django, debes considerar el organizar tus URLconfs en una manera que permita
el uso de inclusiones.

Una URLconf puede, en cualquier punto, "incluir" otros módulos URLconf. Esto se
trata, en esencia, de "enraizar" un conjunto de URLs debajo de otras. Por
ejemplo, esta URLconf incluye otras URLconfs::

    from django.conf.urls import include, url

    urlpatterns =  [
        url(r'^weblog/', include('misitio.blog.urls')),
        url(r'^fotos/', include('misitio.fotos.urls')),
        url(r'^acerca/$', 'misitio.views.acerca'),
    ]

Existe aquí un detalle importante: en este ejemplo, la expresión regular que
apunta a un ``include()`` *no* tiene un ``$`` (carácter que coincide con un fin
de cadena) pero *si* incluye una barra al final. Cuando Django encuentra
``include()``, elimina todo el fragmento de la URL que ya ha coincidido hasta
ese momento y envía la cadena restante a la URLconf incluida para su
procesamiento subsecuente.

Continuando con este ejemplo, esta es la URLconf para ``misitio.blog.urls``::

    from django.conf.urls import url

    urlpatterns = [
        url(r'^(\d\d\d\d)/$', 'misitio.blog.views.entrada_año'),
        url(r'^(\d\d\d\d)/(\d\d)/$', 'misitio.blog.views.entrada_mes'),
    ]

Con esas dos URLconfs, veremos aquí cómo serían manejadas algunas peticiones de
ejemplo:

* Con una peticion a ``/weblog/2007/``: en la primera URLconf, el patrón
  ``r'^weblog/'`` coincide. Debido a que es un ``include()``, Django quita todo
  el texto coincidente, que en este caso es ``'weblog/'``. La parte restante de
  la   URL es ``2007/``, la cual coincide con la primera línea en la URLconf
  ``misitio.blog.urls``.

* Con una peticion a ``/weblog//2007/``: En la primera URLconf, el patrón
  ``r'^weblog/'``   coincide. Debido a que es un ``include()``, Django quita
  todo el texto   coinciente, que en este caso es ``weblog/``. La parte restante
  de la URL es ``/2007/`` (con una barra inicial), la cual no coincide con
  ninguna de las líneas en la URLconf ``misitio.blog.urls``.

* ``/acerca/``: Este coincide con el patrón de la vista ``misitio.views.acerca``
  en la primera URLconf, demostrando que puedes combinar patrones ``include()``
  con patrones no ``include()``.

Otra posibilidad para incluir patrones adicionales en una URL, es usando una
lista de instancias de la :func:`~django.conf.urls.url`. Por ejemplo, considera
esta URLconf.::

    from django.conf.urls import include, url

    from apps.main import views as vista_principal
    from credito import views as vista_credito

    patrones_extra = [
        url(r'^reportes/(?P<id>[0-9]+)/$', vista_credito.reportes),
        url(r'^cargos/$', vista_credito.cargos),
    ]

    urlpatterns = [
        url(r'^$', vista_principal.indice),
        url(r'^ayuda/', include('apps.ayuda.urls')),
        url(r'^credito/', include(patrones_extra)),
    ]

En este ejemplo la URL ``/credito/reportes/``, sera manejada por la vista
``vista_credito.reportes()``.

Esto también puede ser usado para remover redundancia en las URLconfs, mediante
un simple prefijo en un patrón usado repetidamente. Por ejemplo, considera esta
URLconf::

    from django.conf.urls import url
    from . import views

    urlpatterns = [
        url(r'^(?P<pagina_slug>\w+)-(?P<pagina_id>\w+)/historia/$', views.historia),
        url(r'^(?P<pagina_slug>\w+)-(?P<pagina_id>\w+)/editar/$', views.editar),
        url(r'^(?P<pagina_slug>\w+)-(?P<pagina_id>\w+)/discusiones/$', views.discusiones),
        url(r'^(?P<pagina_slug>\w+)-(?P<pagina_id>\w+)/permisos/$', views.permisos),
    ]

Podemos perfeccionar esta URLconf declarando un prefijo común una vez, agrupando
los sufijos que tienen la misma ruta y excluyendo los que son diferentes.::

    from django.conf.urls import include, url
    from . import views

    urlpatterns = [
        url(r'^(?P<pagina_slug>\w+)-(?P<pagina_id>\w+)/', include([
            url(r'^historia/$', views.historia),
            url(r'^editar/$', views.editar),
            url(r'^discusiones/$', views.discusiones),
            url(r'^permisos/$', views.permisos),
        ])),
    ]

Cómo trabajan los parámetros capturados con include()
-----------------------------------------------------

Una URLconf incluida recibe todo parámetro que se haya capturado desde las
URLconf padres, por ejemplo:

.. snippet::
   :filename: root urls.py

   from django.conf.urls import url

    urlpatterns = [
        url(r'^(?P<username>\w+)/blog/', include('misitio.urls.blog')),
    ]


.. snippet::
   :filename: misitio/urls/blog.py

    from django.conf.urls import url

    urlpatterns = [
        url(r'^$', 'misitio.views.indice_blog'),
        url(r'^archivos/$', 'misitio.views.archivos_blog'),
    ]

En este ejemplo, la variable capturada ``username()`` es pasada a la URLconf
incluida y, por lo tanto es pasada  a *todas*  las funciones vista en dicha
URLconf.

Nota que los parámetros capturados son  pasados *siempre* a *todas* las líneas
en la URLconf incluida, con independencia de si la vista realmente acepta estos
parámetros como válidos. Por esta razón esta técnica solamente es útil si estás
seguro de que cada vista en la URLconf incluida acepta los parámetros que le
estás pasando.

Cómo funcionan las opciones extra de URLconf con include()
----------------------------------------------------------

De manera similar, puedes pasar opciones extra de URLconf a ``include()`` así
como puedes pasar opciones extra de URLconf a una vista normal -- como un
diccionario. Cuando haces esto, *las opciones extra serán pasadas a todas* las
líneas en la URLconf incluida.

Por ejemplo, los siguientes dos conjuntos de URLconfs son funcionalmente
idénticos.

Conjunto uno:


.. snippet::
   :filename: urls.py

    from django.conf.urls import url

    urlpatterns = [
        (r'^blog/', include('url-interna'), {'blogid': 3}),
    ]

.. snippet::
   :filename: url-interna.py

    from django.conf.urls import url

    urlpatterns = [
        (r'^archivos/$', 'misitio.views.archivos'),
        (r'^acerca/$', 'misitio.views.acerca'),
        (r'^rss/$', 'misitio.views.rss'),
    ]

Conjunto dos:

.. snippet::
   :filename: urls.py

    from django.conf.urls import url

     urlpatterns = [
        (r'^blog/', include('url-interna')),
    }

.. snippet::
   :filename: url-interna.py

    from django.conf.urls import url

    urlpatterns = [
        (r'^archivos/$', 'misitio.views.archivos', {'blogid': 3}),
        (r'^acerca/$', 'misitio.views.acerca', {'blogid': 3}),
        (r'^rss/$', 'misitio.views.rss', {'blogid': 3}),
    ]

Como en el caso de los parámetros capturados (sobre los cuales se explicó en la
sección anterior), las opciones extra se pasarán *siempre* a *todas*  las URLconf
incluidas, sin importar si la vista, realmente acepta estas opciones como
válidas. Por esta razón esta técnica es útil sólo si estás seguro que todas las
vistas en la URLconf incluida acepta las opciones extra que les estás pasando.

Resolución inversa de URLs
==========================

Una necesidad muy común al trabajar en un proyecto Django es la posibilidad de
obtener URLs finales, para incrustar en el contenido generado(vistas y URLs
activas, así como URLs para mostrar a los usuarios, etc.) o para manejar el
flujo de navegación de el lado del servidor(tal como redirecionamientos, etc.)

Es altamente recomendable evitar codificar en duro las URLs(ya que esta sería
una estrategia muy laboriosa, propensa a errores y poco escalable) o tener
que idear mecanismos para generar URLs que sean paralelas al diseño descrito
por la URLconf, algo semejante podría echar a perder las URLs en algún punto.

En otras palabras, es necesario usar un mecanismo DRY (no te repitas).
Entre otras ventajas permitiría la evolución del diseño de URL sin tener que
explorar en todas partes del codigo fuente, buscando y remplazando URLs obsoletas.

Como punto de partida para diseñar una URL, podemos empezar usando la información
disponible, como puede ser la identificación (el nombre) de la vista a cargo de
manejar la URL, otra pieza de información necesaria que podemos anticipar son
los tipos (posicional, palabra clave) y los valores y argumentos de la vista,
para tomar en cuenta en la URL.

Django ofrece una solución semejante al mapear una URL, únicamente en un solo
lugar. Solo la defines en la URLconf y entonces puede usarla en ambas
direcciones.

Funciona de dos formas:

* La primera forma comienza con una petición del usuario/navegador, este llama
  a la vista correcta de Django y provee cualquier argumento que pueda necesitar
  así como los  valores extraídos del URL.

* La segunda forma comienza con la identificación de la vista correspondiente
  de Django más los valores de los argumentos que le son pasados, obtenidos
  de la URL  asociada.

El primero es el usado en las discusiones previas, el segundo es llamado
*resolución inversa de URLs*, *búsqueda inversa de URL*  *coincidencias inversas
de URLs* o simplemente *URL inversa*.

Django proporciona herramientas para optimizar las coincidencias de URL inversas
en las distintas capas donde sean necesario.

* En las plantillas: Usando la etiqueta de plantillas ``url``

* En el codigo Python: Usando la función ``django.core.urlresolvers.reverse``

* En codigo de alto nivel, para relacionar el manejo de URLs de instancias de
  modelos: por ejemplo el método ``get_absolute_url`` en los modelos.

Ejemplos
--------

Considera esta entrada de una URLconf, a la que le hemos agregado un nombre al
patron URL, llamado 'libros-anuales', asi::

    from django.conf.urls import url

    from biblioteca import views

    urlpatterns = [
        #...
        url(r'^libros/([0-9]{4})/$', views.libros_anuales, name='libros-anuales'),
        #...
    ]

De acuerdo al diseño, la URL para la entrada  correspondiente al año *nnnn*
es  ``/libros/nnnn/``.

Para obtener lo mismo en la plantilla usamos este codigo:

.. code-block:: html

    <a href="{% url 'libros-anuales' 2014 %}">Libros del 2014</a>
    {# o sin el año en el contexto de la variable de la plantilla: #}
    <ul>
    {% for año in lista_anual %}
        <li><a href="{% url 'libros-anuales' año %}">{{ año }} Libros</a></li>
    {% endfor %}
    </ul>

O en el codigo Python:

.. code-block:: python

    from django.core.urlresolvers import reverse
    from django.http import HttpResponseRedirect

    def redireccionar_libros_anuales(request):
        # ...
        year = 2014
        # ...
        return HttpResponseRedirect(reverse('libros-anuales', args=(año,)))

¿Qué sigue?
===========

Uno de los principales objetivos de Django es reducir la cantidad de codigo
que los desarrolladores deben escribir y en este capítulo hemos sugerido formas
en las cuales se puede reducir el codigo de tus vistas y URLconfs,
proporcionándote muchas de las ventajas, tips y trucos  para vistas y URLconfs,
en él :doc:`capítulo 9<chapter09>`, le daremos este tratamiento avanzado al
sistema de plantilla de Django.

