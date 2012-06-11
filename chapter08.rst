=======================================
Capítulo 8: Vistas avanzadas y URLconfs
=======================================

En el :doc:`Capítulo 3<chapter03>`, explicamos las bases de las funciones 
vista de Django y las URLconfs.  Este capítulo entra en detalle sobre 
funcionalidad avanzada en esas dos partes del framework.

Trucos de URLconf
=================

No hay nada de "especial" con las URLconfs -- como cualquier otra cosa en
Django, son sólo código Python --. Puedes aprovecharte de esto de varias
maneras, como se describe las secciones que siguen.

Importación de funciones de forma efectiva
------------------------------------------

Considera esta URLconf, que se basa en el ejemplo del 
:doc:`Capítulo 3`<chapter03>:

.. code-block:: python

    from django.conf.urls.defaults import *
    from mysite.views import current_datetime, hours_ahead, hours_behind, 
        now_in_chicago, now_in_london

    urlpatterns = patterns('',
        (r'^now/$', current_datetime),
        (r'^now/plus(\d{1,2})hours/$', hours_ahead),
        (r'^now/minus(\d{1,2})hours/$', hours_behind),
        (r'^now/in_chicago/$', now_in_chicago),
        (r'^now/in_london/$', now_in_london),
    )

Como se explicó en el :doc:`Capítulo 3<chapter03>`, cada entrada de la 
URLconf incluye su función vista asociada, que se pasa directamente como
un método. Esto significa que es necesario importar las funciones 
view en la parte superior del módulo.

Pero a medida que las aplicaciones Django crecen en complejidad, sus URLconf
crecen también, y mantener esos import puede ser tedioso de manejar. (Por cada
nueva función vista, tienes que recordar importarla y la declaración de
importaciones tiende a volverse demasiado larga si se utiliza este método). Es
posible evitar esa tarea tediosa importando el módulo ``views`` directamente.
Este ejemplo de URLconf es equivalente al anterior:

.. code-block:: python

    from django.conf.urls.defaults import *
    from mysite import views

    urlpatterns = patterns('',
        (r'^now/$', views.current_datetime),
        (r'^now/plus(\d{1,2})hours/$', views.hours_ahead),
        (r'^now/minus(\d{1,2})hours/$', views.hours_behind),
        (r'^now/in_chicago/$', views.now_in_chicago),
        (r'^now/in_london/$', views.now_in_london),
    )

Django ofrece otra forma de especificar la función vista para un patrón en
particular en la URLconf: se le puede pasar un string que contiene el nombre del
módulo y de la función en lugar del método. Continuando con el ejemplo:

.. code-block:: python

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^now/$', 'mysite.views.current_datetime'),
        (r'^now/plus(\d{1,2})hours/$', 'mysite.views.hours_ahead'),
        (r'^now/minus(\d{1,2})hours/$', 'mysite.views.hours_behind'),
        (r'^now/in_chicago/$', 'mysite.views.now_in_chicago'),
        (r'^now/in_london/$', 'mysite.views.now_in_london'),
    )

(Nota que los nombres de las vistas están entre comillas. Estamos usando
``'mysite.views.current_datetime'`` -- con comillas -- en lugar de
``mysite.views.current_datetime``.)

Al usar esta técnica ya no es necesario importar las funciones vista;
Django importa automáticamente la función vista apropiada la primera vez que
sea necesaria, según el string que describe el nombre y la ruta de la función
vista.

Otro atajo que puedes tomar al usar la técnica del string es sacar factor común
de "prefijos view". En nuestro ejemplo URLconf, cada uno de los strings vista
comienza con ``'mysite.views'``, lo cual es redundante. Podemos factorizar ese
prefijo común y pasarlo como primer argumento de ``patterns()``, así:

.. code-block:: python

    from django.conf.urls.defaults import *

    urlpatterns = patterns('mysite.views',
        (r'^now/$', 'current_datetime'),
        (r'^now/plus(\d{1,2})hours/$', 'hours_ahead'),
        (r'^now/minus(\d{1,2})hours/$', 'hours_behind'),
        (r'^now/in_chicago/$', 'now_in_chicago'),
        (r'^now/in_london/$', 'now_in_london'),
    )

Nota que no se pone un punto detrás del prefijo, ni un punto delante de los
string vista. Django los pone automáticamente.

Con estos dos enfoques en mente, ¿cuál es mejor? Realmente depende de tu estilo
personal de programación y tus necesidades.

Las siguientes son ventajas del enfoque string:

    * Es más compacto, porque no requiere que importes las funciones vista.

    * Resulta en URLconfs más fáciles de leer y de manejar si tus funciones
      vista están extendidas por varios módulos Python diferentes.

Las siguientes son ventajas del enfoque del método:

    * Permite un fácil "empaquetado" de funciones vista. Ver la sección
      "Empaquetado de funciones vista" más adelante en este capítulo.

    * Es más "Pythónico" -- es decir, está más en línea con las tradiciones
      Python, como la de pasar funciones como objetos.

Ambos enfoques son válidos e incluso puedes mezclarlos dentro de la misma
URLconf.  La elección es tuya.

Usar múltiples prefijos de vista
--------------------------------

En la práctica, si usas la técnica del string, probablemente termines mezclando
vistas hasta el punto en que las vistas de tu URLconf no tengan un prefijo
común.  Sin embargo, todavía puedes sacar provecho del atajo del prefijo de las
vistas para remover esta duplicación. Simplemente junta los objetos
``patterns()``, así:

Antes:

.. code-block:: python

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^/?$', 'mysite.views.archive_index'),
        (r'^(\d{4})/([a-z]{3})/$', 'mysite.views.archive_month'),
        (r'^tag/(\w+)/$', 'weblog.views.tag'),
    )

Después::

    from django.conf.urls.defaults import *

    urlpatterns = patterns('mysite.views',
        (r'^/?$', 'archive_index'),
        (r'^(\d{4})/([a-z]{3})/$', 'archive_month'),
    )

    urlpatterns += patterns('weblog.views',
        (r'^tag/(\w+)/$', 'tag'),
    )

Lo único que le importa al framework es que existe una variable a nivel módulo
llamada ``urlpatterns``. Esta variable puede ser construida de forma dinámica,
como lo hacemos en este ejemplo.

Casos especiales de URLs en modo Debug
--------------------------------------

Hablando de construir ``urlpatterns`` de forma dinámica, quizás quieras
aprovechar esta técnica para alterar el comportamiento de tu URLconf mientras
estás en el modo depuración de Django. Para hacer eso simplemente comprueba el
valor de la configuración ``DEBUG`` en tiempo de ejecución, así::

    from django.conf.urls.defaults import*
    from django.conf import settings

    urlpatterns = patterns('',
        (r'^$', 'mysite.views.homepage'),
        (r'^(\d{4})/([a-z]{3})/$', 'mysite.views.archive_month'),
    )

    if settings.DEBUG:
        urlpatterns += patterns('',
            (r'^debuginfo/$', 'mysite.views.debug'),
        )

En este ejemplo, la URL ``/debuginfo/`` sólo estará disponible si tu
configuración ``DEBUG`` tiene el valor ``True``.

Usar grupos con nombre
----------------------

Hasta ahora en todos nuestros ejemplos URLconf hemos usado, grupos de
expresiones regulares *sin nombre* -- es decir, ponemos paréntesis en las partes
de la URL que queremos capturar y Django le pasa ese texto capturado a la
función vista como un argumento posicional. En un uso más avanzado, es posible
usar grupos de expresiones regulares *con nombre* para capturar partes de la URL
y pasarlos como argumentos *clave* a una vista.

.. admonition:: Argumentos claves vs. Argumentos posicionales

    A una función de Python se la puede llamar usando argumentos de palabra
    clave o argumentos posicionales -- y, en algunos casos, los dos al mismo
    tiempo. En una llamada por argumentos de palabra clave, se especifican los
    nombres de los argumentos junto con los valores que se le pasan. En una
    llamada por argumento posicional, sencillamente pasas los argumentos sin
    especificar explícitamente qué argumento concuerda con cual valor; la
    asociación está implícita en el orden de los argumentos.

Por ejemplo, considera esta sencilla función::

    def sell(item, price, quantity):
        print "Selling %s unit(s) of %s at %s" % (quantity, item, price)

Para llamarla con argumentos posicionales, se especifican los argumentos
en el orden en que están listados en la definición de la función::

        sell('Socks', '$2.50', 6)

Para llamarla con argumentos de palabra clave, se especifican los nombres de
los argumentos junto con sus valores. Las siguientes sentencias son
equivalentes::

        sell(item='Socks', price='$2.50', quantity=6)
        sell(item='Socks', quantity=6, price='$2.50')
        sell(price='$2.50', item='Socks', quantity=6)
        sell(price='$2.50', quantity=6, item='Socks')
        sell(quantity=6, item='Socks', price='$2.50')
        sell(quantity=6, price='$2.50', item='Socks')

Finalmente, se pueden mezclar los argumentos posicionales y por palabra
clave, siempre y cuando los argumentos posicionales estén listados antes que
los argumentos por palabra clave. Las siguientes sentencias son equivalentes
a los ejemplos anteriores::

        sell('Socks', '$2.50', quantity=6)
        sell('Socks', price='$2.50', quantity=6)
        sell('Socks', quantity=6, price='$2.50')

En las expresiones regulares de Python, la sintaxis para los grupos de
expresiones regulares con nombre es ``(?P<nombre>patrón)``, donde ``nombre`` es
el nombre del grupo y ``patrón`` es algún patrón a buscar.

Aquí hay un ejemplo de URLconf que usa grupos sin nombre::

    from django.conf.urls.defaults import *
    from mysite import views

    urlpatterns = patterns('',
        (r'^articles/(\d{4})/$', views.year_archive),
        (r'^articles/(\d{4})/(\d{2})/$', views.month_archive),
    )

Aquí está la misma URLconf, reescrita para usar grupos con nombre::

    from django.conf.urls.defaults import *
    from mysite import views

    urlpatterns = patterns('',
        (r'^articles/(?P<year>\d{4})/$', views.year_archive),
        (r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
    )

Esto produce exactamente el mismo resultado que el ejemplo anterior, con una
sutil diferencia: se le pasa a las funciones vista los valores capturados como
argumentos clave en lugar de argumentos posicionales.

Por ejemplo, con los grupos sin nombre una petición a ``/articles/2006/03/``
resultaría en una llamada de función equivalente a esto::

    month_archive(request, '2006', '03')

Sin embargo, con los grupos con nombre, la misma petición resultaría en esta
llamada de función::

    month_archive(request, year='2006', month='03')

En la práctica, usar grupos con nombres hace que tus URLconfs sean un poco más
explícitas y menos propensas a bugs causados por argumentos -- y puedes
reordenar los argumentos en las definiciones de tus funciones vista. Siguiendo
con el ejemplo anterior, si quisiéramos cambiar las URLs para incluir el mes
*antes* del año, y estuviéramos usando grupos sin nombre, tendríamos que
acordarnos de cambiar el orden de los argumentos en la vista ``month_archive``.
Si estuviéramos usando grupos con nombre, cambiar el orden de los parámetros
capturados en la URL no tendría ningún efecto sobre la vista.

Por supuesto, los beneficios de los grupos con nombre tienen el costo de la
falta de brevedad; algunos desarrolladores opinan que la sintaxis de los grupos
con nombre es fea y larga.  Aún así, otra ventaja de los grupos con nombres es
la facilidad de lectura, especialmente para las personas que no están
íntimamente relacionadas con las expresiones regulares o con tu aplicación
Django en particular. Es más fácil ver lo que está pasando, a primera vista, en
una URLconf que usa grupos con nombre.

Comprender el algoritmo de combinación/agrupación
-------------------------------------------------

Una advertencia al usar grupos con nombre en una URLconf es que un simple patrón
URLconf no puede contener grupos con nombre y sin nombre. Si haces eso, Django
no generará ningún mensaje de error, pero probablemente descubras que tus URLs
no se están disparando de la forma esperada. Aquí está específicamente el algoritmo
que sigue el parser URLconf, con respecto a grupos con nombre vs. grupos sin
nombre en una expresión regular:

    * Si existe algún argumento con nombre, usará esos, ignorando los argumentos
      sin nombre.

    * Además, pasará todos los argumentos sin nombre como argumentos
      posicionales.

    * En ambos casos, pasará cualquier opción extra como argumentos de palabra
      clave.  Ver la próxima sección para más información.

Pasarle opciones extra a las funciones vista
--------------------------------------------

A veces te encontrarás escribiendo funciones vista que son bastante similares,
con tan sólo algunas pequeñas diferencias. Por ejemplo, digamos que tienes dos
vistas cuyo contenido es idéntico excepto por la plantilla que utilizan::

    # urls.py

    from django.conf.urls.defaults import *
    from mysite import views

    urlpatterns = patterns('',
        (r'^foo/$', views.foo_view),
        (r'^bar/$', views.bar_view),
    )

    # views.py

    from django.shortcuts import render_to_response
    from mysite.models import MyModel

    def foo_view(request):
        m_list = MyModel.objects.filter(is_new=True)
        return render_to_response('template1.html', {'m_list': m_list})

    def bar_view(request):
        m_list = MyModel.objects.filter(is_new=True)
        return render_to_response('template2.html', {'m_list': m_list})

Con este código nos estamos repitiendo y eso no es elegante. Al comienzo,
podrías pensar en reducir la redundancia usando la misma vista para ambas URLs,
poniendo paréntesis alrededor de la URL para capturarla y comprobando la URL
dentro de la vista para determinar la plantilla, como mostramos a continuación::

    # urls.py

    from django.conf.urls.defaults import *
    from mysite import views

    urlpatterns = patterns('',
        (r'^(foo)/$', views.foobar_view),
        (r'^(bar)/$', views.foobar_view),
    )

    # views.py

    from django.shortcuts import render_to_response
    from mysite.models import MyModel

    def foobar_view(request, url):
        m_list = MyModel.objects.filter(is_new=True)
        if url == 'foo':
            template_name = 'template1.html'
        elif url == 'bar':
            template_name = 'template2.html'
        return render_to_response(template_name, {'m_list': m_list})

Sin embargo, el problema con esa solución es que acopla fuertemente tus URLs y
tu código Si decides renombrar ``/foo/`` a ``/fooey/``, tienes que recordar
cambiar el código de la vista.

La solución elegante involucra un parámetro URLconf opcional. Cada patrón en una
URLconf puede incluir un tercer ítem: un diccionario de argumentos de palabra
clave para pasarle a la función vista.

Con esto en mente podemos reescribir nuestro ejemplo anterior así::

    # urls.py

    from django.conf.urls.defaults import *
    from mysite import views

    urlpatterns = patterns('',
        (r'^foo/$', views.foobar_view, {'template_name': 'template1.html'}),
        (r'^bar/$', views.foobar_view, {'template_name': 'template2.html'}),
    )

    # views.py

    from django.shortcuts import render_to_response
    from mysite.models import MyModel

    def foobar_view(request, template_name):
        m_list = MyModel.objects.filter(is_new=True)
        return render_to_response(template_name, {'m_list': m_list})

Como puedes ver, la URLconf en este ejemplo especifica ``template_name`` en la
URLconf. La función vista lo trata como a cualquier otro parámetro.

Esta técnica de la opción extra en la URLconf es una linda forma de enviar
información adicional a tus funciones vista sin tanta complicación. Por ese
motivo es que es usada por algunas aplicaciones incluidas en Django, más
notablemente el sistema de vistas genéricas, que tratamos en el
::doc`Capítulo 9<chapter09>`.

La siguiente sección contiene algunas ideas sobre cómo puedes usar la técnica de
la opción extra en la URLconf como parte de tus proyectos.

Simulando valores capturados en URLconf
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Supongamos que posees un conjunto de vistas que son disparadas vía un patrón y
otra URL que no lo es pero cuya lógica de vista es la misma. En este caso puedes
"simular" la captura de valores de la URL usando opciones extra de URLconf para
manejar esa URL extra con una única vista.

Por ejemplo, podrías tener una aplicación que muestra algunos datos para un día
particular, con URLs tales como::

    /mydata/jan/01/
    /mydata/jan/02/
    /mydata/jan/03/
    # ...
    /mydata/dec/30/
    /mydata/dec/31/

Esto es lo suficientemente simple de manejar -- puedes capturar los mismos en
una URLconf como esta (usando sintaxis de grupos con nombre)::

    urlpatterns = patterns('',
        (r'^mydata/(?P<month>\w{3})/(?P<day>\d\d)/$', views.my_view),
    )

Y la ***signature*** de la función vista se vería así::

    def my_view(request, month, day):
        # ....

Este enfoque es simple y directo -- no es nada que no hayamos visto antes. El
truco entra en juego cuando quieres agregar otra URL que usa ``my_view`` pero
cuya URL no incluye un ``month`` ni/o un ``day``.

Por ejemplo, podrías querer agregar otra URL, ``/mydata/birthday/``, que sería
equivalente a ``/mydata/jan/06/``. Puedes sacar provecho de opciones extra de
las URLconf de la siguiente forma::

    urlpatterns = patterns('',
        (r'^mydata/birthday/$', views.my_view, {'month': 'jan', 'day': '06'}),
        (r'^mydata/(?P<month>\w{3})/(?P<day>\d\d)/$', views.my_view),
    )

El detalle genial aquí es que no necesitas cambiar tu función vista para nada. A
la función vista sólo le incumbe el obtener los parámetros ``month`` y ``day``
-- no importa si los mismos provienen de la captura de la URL o de parámetros
extra.

Convirtiendo una vista en genérica
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Es una buena práctica de programación el "factorizar"  para aislar las partes
comunes del código. Por ejemplo, con estas dos funciones Python::

    def say_hello(person_name):
        print 'Hello, %s' % person_name

    def say_goodbye(person_name):
        print 'Goodbye, %s' % person_name

podemos extraer el saludo para convertirlo en un parámetro::

    def greet(person_name, greeting):
        print '%s, %s' % (greeting, person_name)

Puedes aplicar la misma filosofía a tus vistas Django usando los parámetros
extra de URLconf.

Con esto en mente, puedes comenzar a hacer abstracciones de nivel más alto de
tus vistas. En lugar de pensar "Esta vista muestra una lista de objetos
``Event``" y "Esta otra vista muestra una lista de objetos ``BlogEntry``",
descubre que ambas son casos específicos de "Una vista que muestra una lista de
objetos, donde el tipo de objeto es variable".

Usemos este código como ejemplo::

    # urls.py

    from django.conf.urls.defaults import *
    from mysite import views

    urlpatterns = patterns('',
        (r'^events/$', views.event_list),
        (r'^blog/entries/$', views.entry_list),
    )

    # views.py

    from django.shortcuts import render_to_response
    from mysite.models import Event, BlogEntry

    def event_list(request):
        obj_list = Event.objects.all()
        return render_to_response('mysite/event_list.html', {'event_list': obj_list})

    def entry_list(request):
        obj_list = BlogEntry.objects.all()
        return render_to_response('mysite/blogentry_list.html', {'entry_list': obj_list})

Ambas vistas hacen esencialmente lo mismo: muestran una lista de objetos.
Refactoricemos el código para extraer el tipo de objetos que muestran::

    # urls.py

    from django.conf.urls.defaults import *
    from mysite import models, views

    urlpatterns = patterns('',
        (r'^events/$', views.object_list, {'model': models.Event}),
        (r'^blog/entries/$', views.object_list, {'model': models.BlogEntry}),
    )

    # views.py

    from django.shortcuts import render_to_response

    def object_list(request, model):
        obj_list = model.objects.all()
        template_name = 'mysite/%s_list.html' % model.__name__.lower()
        return render_to_response(template_name, {'object_list': obj_list})

Con esos pequeños cambios tenemos, de repente, una vista reusable e
independiente del modelo. De ahora en adelante, cada vez que necesitemos una
lista que muestre una listado de objetos, podemos simplemente reusar esta vista
``object_list`` en lugar de escribir código de vista. A continuación, un par de
notas acerca de lo que hicimos:

    * Estamos pasando las clases de modelos directamente, como el parámetro
      ``model``. El diccionario de opciones extra de ULconf puede pasar
      cualquier tipo de objetos Python -- no sólo strings.

    * La línea ``model.objects.all()`` es un ejemplo de tipado de pato (*duck
      typing*): "Si camina como un pato, y habla como un pato, podemos tratarlo
      como un pato." Nota que el código no conoce de qué tipo de objeto se trata
      ``model``; el único requerimiento es que ``model`` tenga un atributo
      ``objects``, el cual a su vez tiene un método ``all()``.

    * Estamos usando ``model.__name__.lower()`` para determinar el nombre de la
      plantilla. Cada clase Python tiene un atributo ``__name__`` que retorna el
      nombre de la clase. Esta característica es útil en momentos como este,
      cuando no conocemos el tipo de clase hasta el momento de la ejecución. Por
      ejemplo, el ``__name__`` de la clase ``BlogEntry`` es la cadena
      ``BlogEntry``.

    * En una sutil diferencia entre este ejemplo y el ejemplo previo, estamos
      pasando a la plantilla el nombre de variable genérico ``object_list``.
      Podemos fácilmente cambiar este nombre de variable a ``blogentry_list`` o
      ``event_list``, pero hemos dejado eso como un ejercicio para el lector.

Debido a que los sitios Web impulsados por bases de datos tienen varios patrones
comunes, Django incluye un conjunto de "vistas genéricas" que usan justamente
esta técnica para ahorrarte tiempo. Nos ocupamos de las vistas genéricas
incluidas con Django en el próximo capítulo.

Pasando opciones de configuración a una vista
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Si estás distribuyendo una aplicación Django, es probable que tus usuarios
deseen cierto grado de configuración. En este caso, es una buena idea agregar
puntos de extensión a tus vistas para las opciones de configuración que piensas
que la gente pudiera desear cambiar. Puedes usar los parámetros extra de URLconf
para este fin.

Una parte de una aplicación que normalmente se hace configurable es el nombre
de la plantilla::

    def my_view(request, template_name):
        var = do_something()
        return render_to_response(template_name, {'var': var})

Entendiendo la precedencia entre valores captuardos vs. opciones extra
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cuando se presenta un conflicto, los parámetros extra de la URLconf tiene
precedencia sobre los parámetros capturados. En otras palabras, si tu URLconf
captura una variable de grupo con nombre y un parámetro extra de URLconf incluye
una variable con el mismo nombre, se usará el parámetro extra de la URLconf.

Por ejemplo, analicemos esta URLconf::

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^mydata/(?P<id>\d+)/$', views.my_view, {'id': 3}),
    )

Aquí, tanto la expresión regular como el diccionario extra incluye un ``id``.
Tiene precedencia el ``id`` fijo especificado. Esto significa que cualquier
petición (por ej. ``/mydata/2/`` o ``/mydata/432432/``) serán tratados como si
``id`` estuviera fijado a ``3``, independientemente del valor capturado en la
URL.

Los lectores atentos notarán que en este caso es una pérdida de tiempo y de
tipeo capturar ``id`` en la expresión regular, porque su valor será siempre
descartado en favor del valor proveniente del diccionario. Esto es correcto;
lo traemos a colación sólo para ayudarte a evitar el cometer ese error.

Usando argumentos de vista por omisión
--------------------------------------

Otro truco cómodo es el de especificar parámetros por omisión para los
argumentos de una vista. Esto le indica a la vista qué valor usar para un
parámetro por omisión si es que no se especifica ninguno.

Veamos un ejemplo::

    # urls.py

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^blog/$', views.page),
        (r'^blog/page(?P<num>\d+)/$', views.page),
    )

    # views.py

    def page(request, num="1"):
        # Output the appropriate page of blog entries, according to num.
        # ...

Aquí, ambos patrones de URL apuntan a la misma vista -- ``views.page`` -- pero
el primer patrón no captura nada de la URL. Si el primer patrón es disparado, la
función ``page()`` usará su argumento por omisión para ``num``, ``"1"``. Si el
segundo patrón es disparado, ``page()`` usará el valor de ``num`` que se haya
capturado mediante la expresión regular.

Es común usar esta técnica en combinación con opciones de configuración,
como explicamos previamente. Este  ejemplo implementa una pequeña mejora al
ejemplo de la sección "`Pasando opciones de configuración a una vista`_": provee un
valor por omisión para ``template_name``::

    def my_view(request, template_name='mysite/my_view.html'):
        var = do_something()
        return render_to_response(template_name, {'var': var})

Manejando vistas en forma especial
----------------------------------

En algunas ocasiones tendrás un patrón en tu URLconf que maneja un gran número
de URLs, pero necesitarás realizar un manejo especial en una de ellas. En este
caso, saca provecho de la forma lineal en la que son procesadas la URLconfs y
coloca el caso especial primero.

Por ejemplo, las páginas "agregar un objeto" en el sitio de administración de
Django están representadas por la siguiente línea de URLconf::

    urlpatterns = patterns('',
        # ...
        ('^([^/]+)/([^/]+)/add/$', 'django.contrib.admin.views.main.add_stage'),
        # ...
    )

Esto se disparará con URLs como ``/myblog/entries/add/`` y
``/auth/groups/add/``. Sin embargo, la página "agregar" de un objeto usuario
(``/auth/user/add/``) es un caso especial -- la misma no muestra todos los
campos del formulario, muestra dos campos de contraseña, etc. Podríamos resolver
este problema tratando esto como un caso especial en la vista, de esta manera::

    def add_stage(request, app_label, model_name):
        if app_label == 'auth' and model_name == 'user':
            # do special-case code
        else:
            # do normal code

pero eso es poco elegante por una razón que hemos mencionado en múltiples
oportunidades en este capítulo: Coloca lógica de URLs en la vista. Una manera
más elegante sería la de hacer uso del hecho que las URLconfs se procesan
desde arriba hacia abajo::

    urlpatterns = patterns('',
        # ...
        ('^auth/user/add/$', 'django.contrib.admin.views.auth.user_add_stage'),
        ('^([^/]+)/([^/]+)/add/$', 'django.contrib.admin.views.main.add_stage'),
        # ...
    )

Con esto, una petición de ``/auth/user/add/`` será manejada por la vista
``user_add_stage``. Aunque dicha URL coincide con el segundo patrón, coincide
primero con el patrón ubicado más arriba. (Esto es lógica de corto circuito).

Capturando texto en URLs
------------------------

Cada argumento capturado es enviado a la vista como una cadena Python, sin
importar qué tipo de coincidencia se haya producido con la expresión regular.
Por ejemplo en esta línea de URLconf::

    (r'^articles/(?P<year>\d{4})/$', views.year_archive),

el argumento ``year`` de ``views.year.archive()`` será una cadena, no un entero,
aun cuando ``\d{4}`` sólo coincidirá con cadenas que representen enteros.

Es importante tener esto presente cuando estás escribiendo código de vistas.
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

    # urls.py

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^articles/(\d{4})/(\d{2})/(\d{2})/$', views.day_archive),
    )

    # views.py

    import datetime

    def day_archive(request, year, month, day)
        # The following statement raises a TypeError!
        date = datetime.date(year, month, day)

En cambio ``day_archive`` puede ser escrito correctamente de la siguiente
forma::

    def day_archive(request, year, month, day)
        date = datetime.date(int(year), int(month), int(day))

Notar que ``int()`` lanza un ``ValueError`` cuando le pasas una cadena que no
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

Por ejemplo, en una petición de ``http://www.example.com/myapp/`` Django tratará
de encontrar una coincidencia para ``myapp/``. En una petición de
``http.//www.example.com/myapp/?page3`` Django tratará de buscar una
coincidencia para ``myapp/``.

El método de la petición (por ej. ``POST``, ``GET``, ``HEAD``) *no*  se tiene en
cuenta cuando se recorre la URLconf. En otras palabras, todos los métodos serán
encaminados hacia la misma función para la misma URL. Es responsabilidad de una
función vista el manejar de maneras distintas en base al método de la petición.

Incluyendo otras URLconfs
=========================

Si tu intención es que tu código sea usando en múltiples sitios implementados
con Django, debes considerar el organizar tus URLconfs en una manera que permita
el uso de inclusiones.

Tu URLconf puede, en cualquier punto, "incluir" otros módulos URLconf. Esto se
trata, en esencia, de "enraizar" un conjunto de URLs debajo de otras. Por
ejemplo, esta URLconf incluye otras URLconfs::

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^weblog/', include('mysite.blog.urls')),
        (r'^photos/', include('mysite.photos.urls')),
        (r'^about/$', 'mysite.views.about'),
    )

Existe aquí un detalle importante: en este ejemplo, la expresión regular que
apunta a un ``include()`` *no* tiene un ``$`` (carácter que coincide con un fin
de cadena) pero *si* incluye una barra al final. Cuando Django encuentra
``include()``, elimina todo el fragmento de la URL que ya ha coincidido hasta
ese momento y envía la cadena restante a la URLconf incluida para su procesamiento
subsecuente.

Continuando con este ejemplo, esta es la URLconf ``mysite.blog.urls``::

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^(\d\d\d\d)/$', 'mysite.blog.views.year_detail'),
        (r'^(\d\d\d\d)/(\d\d)/$', 'mysite.blog.views.month_detail'),
    )

Con esas dos URLconfs, veremos aquí cómo serían manejadas algunas peticiones de
ejemplo:

    * ``/weblog/2007/``: En la primera URLconf, el patrón ``r'^weblog/'``
      coincide. Debido a que es un ``include()``, Django quita todo el texto
      coincidente, que en este caso es ``'weblog/'``. La parte restante de la
      URL es ``2007/``, la cual coincide con la primera línea en la URLconf
      ``mysite.blog.urls``.

    * ``/weblog//2007/``: En la primera URLconf, el patrón ``r'^weblog/'``
      coincide. Debido a que es un ``include()``, Django quita todo el texto
      coinciente, que en este caso es ``weblog/``. La parte restante de la URL
      es ``/2007/`` (con una barra inicial), la cual no coincide con ninguna de
      la líneas en la URLconf ``mysite.blog.urls``.

    * ``/about/``: Esto coincide con el patrón de la vista
      ``mysite.views.about`` en la primera URLconf, demostrando que puedes
      combinar patrones ``include()`` con patrones no ``include()``.

Cómo trabajan los parámetros capturados con include()
-----------------------------------------------------

Una URLconf incluida recibe todo parámetro que se haya capturado desde las
URLconf padres, por ejemplo::

    # root urls.py

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^(?P<username>\w+)/blog/', include('foo.urls.blog')),
    )

    # foo/urls/blog.py

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^$', 'foo.views.blog_index'),
        (r'^archive/$', 'foo.views.blog_archive'),
    )

En este ejemplo, la variable capturada ``username()`` es pasada a la URLconf
incluida y, por lo tanto, a *todas*  las funciones vista en dicha URLconf.

Notar que los parámetros capturados serán pasados *siempre* a *todas* las líneas
en la URLconf incluida, con independencia de si la vista de la línea realmente
acepta esos parámetros como válidos. Por esta razón esta técnica solamente es
útil si estás seguro de que cada vista en la URLconf incluida acepta los
parámetros que estás pasando.

Cómo funcionan las opciones extra de URLconf con include()
----------------------------------------------------------

De manera similar, puedes pasar opciones extra de URLconf a ``include()`` así
como puedes pasar opciones extra de URLconf a una vista normal -- como un
diccionario. Cuando haces esto, *las opciones extra serán pasadas a todas* las
líneas en la URLconf incluida.

Por ejemplo, los siguientes dos conjuntos de URLconfs son funcionalmente
idénticos.

Conjunto uno::

    # urls.py

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^blog/', include('inner'), {'blogid': 3}),
    )

    # inner.py

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^archive/$', 'mysite.views.archive'),
        (r'^about/$', 'mysite.views.about'),
        (r'^rss/$', 'mysite.views.rss'),
    )

Conjunto dos::

    # urls.py

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^blog/', include('inner')),
    )

    # inner.py

    from django.conf.urls.defaults import *

    urlpatterns = patterns('',
        (r'^archive/$', 'mysite.views.archive', {'blogid': 3}),
        (r'^about/$', 'mysite.views.about', {'blogid': 3}),
        (r'^rss/$', 'mysite.views.rss', {'blogid': 3}),
    )

Como en el caso de los parámetros capturados (sobre los cuales se explicó en la
sección anterior), las opciones extra se pasarán *siempre* a *todas*  las líneas
en la URLconf incluida, sin importar de si la vista de la línea realmente acepta
esas opciones como válidas. Por eta razón esta técnica es útil sólo si estás
seguro que todas las vistas en la URLconf incluida acepta las opciones extra que
estás pasando.

¿Qué sigue?
===========

Uno de los principales objetivos de Django es reducir la cantidad de código
que los desarrolladores deben escribir y en este capítulo hemos sugerido formas
en las cuales se puede reducir el código de tus vistas y URLconfs.

El próximo paso lógico en la reducción de código es eliminar completamente la
necesidad de escribir vistas. Ese es el tópico del :doc:`próximo capítulo<chapter09>`.



