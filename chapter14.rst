==============================================
Capítulo 14: Sesiones, usuario e inscripciones
==============================================

Tenemos que confesar algo: hasta el momento hemos ignorado un aspecto 
absolutamente importante del desarrollo web. Hemos hecho la suposición de que 
el tráfico que visita nuestra web está compuesto por una masa amorfa de 
usuarios anónimos, que se precipitan contra nuestras cuidadosamente diseñadas 
páginas.

Esto no es verdad, claro. Los navegadores que consultan nuestras páginas 
tienen a personas reales detrás (la mayor parte del tiempo, al menos). Este es 
un hecho importantísimo y que no debemos ignorar: Lo mejor de Internet es que 
**sirve para conectar personas**, no máquinas. Si queremos desarrollar un sitio 
web realmente competitivo, antes o después tendremos que plantearnos como 
tratar a las personas que están detrás del navegador.

Por desgracia, no es tan fácil como podría parecer. El protocolo HTTP
se diseñó específicamente para que fuera un protocolo *sin estado*, es
decir, que cada petición y respuesta está totalmente aislada de las
demás. No hay persistencia entre una petición y la siguiente, y ninguno
de los atributos de la petición (dirección IP, identificador del
agente, etc...) nos permite discriminar de forma segura y consistente
las peticiones de una persona de las del resto.

En este capítulo aprenderemos como solucionar esta carencia de estados. 
Empezaremos al nivel más bajo (*cookies*), e iremos ascendiendo hasta las 
herramientas de alto nivel que nos permitirán gestionar sesiones, usuarios y 
altas o inscripciones de los mismos.

Cookies
=======

Los desarrolladores de navegadores hace tiempo que se dieron cuenta de que esta
carencia de estados iba a representar un problema para los desarrolladores
web, y así fue como nacieron las *cookies* (literalmente *galleta*). Una
cookie es una pequeña cantidad de información que el servidor delega
en el navegador, de forma que este la almacena. Cada vez que el cliente
web solicita una página del servidor, se le envía de
vuelta la cookie.

Veamos con un poco más de detalle el funcionamiento. Cuando abrimos nuestro 
navegador y escribimos ``google.com``, el navegador envía una solicitud HTTP a 
Google que empieza más o menos así::

    GET / HTTP/1.1
    Host: google.com
    ...

Cuando Google responde, la respuesta contiene algo parecido a esto::

    HTTP/1.1 200 OK
    Content-Type: text/html
    Set-Cookie: PREF=ID=5b14f22bdaf1e81c:TM=1167000671:LM=1167000671;
                expires=Sun, 17-Jan-2038 19:14:07 GMT;
                path=/; domain=.google.com
    Server: GWS/2.1
    ...

Fíjate en la línea que comienza con ``Set-Cookie``. El navegador almacenará
el valor indicado (``PREF=ID=5b14f22bdaf1e81c:TM=1167000671:LM=1167000671``) y
se lo volverá a enviar a Google cada vez que vuelva a acceder a alguna de
sus páginas; de esa forma, la próxima vez que vuelvas a Google, la petición
que enviará el navegador se parecerá a esta::

    GET / HTTP/1.1
    Host: google.com
    Cookie: PREF=ID=5b14f22bdaf1e81c:TM=1167000671:LM=1167000671
    ...

Google puede saber ahora, gracias al valor de la *Cookie*, que eres la misma
persona que accedió anteriormente. Este valor puede ser, por ejemplo, una
clave en una tabla de la base de datos que almacene los datos del usuario. Con 
esa información, Google puede hacer aparecer tu nombre en la página (de hecho, 
lo hace).

Cómo definir y leer los valores de las cookies
----------------------------------------------

A la hora de utilizar las capacidades de persistencia de Django, lo más
probable es que uses las prestaciones de alto nivel para la gestión de
sesiones y de usuarios, prestaciones que discutiremos un poco más adelante en 
este mismo capítulo. No obstante, ahora vamos a hacer una breve parada y veremos
cómo leer y definir *cookies* a bajo nivel. Esto debería ayudarte a entender 
cómo funcionan el resto de las herramientas que veremos en el capítulo, y te 
será de utilidad si alguna vez tienes que trabajar con las cookies directamente.

Obtener los valores de las cookies que ya están definidas es muy fácil. Cada
objeto de tipo petición, ``request``, contiene un objeto ``COOKIES`` que se
comporta como un diccionario; puedes usarlo para leer cualquier *cookie* que el
navegador haya enviado a la vista::

    def mostrar_color(request):
        if "color_favorito" in request.COOKIES:
            return HttpResponse("Tu color favorito es %s" % \
                request.COOKIES["color_favorito"])
        else:
            return HttpResponse("No tienes un color favorito.")

Definir los valores de las cookies es sólo un poco más complicado. Debes
usar el método ``set_cookie()`` en un objeto de tipo ``HttpResponse``. He
aquí un ejemplo que define la *cookie* ``color_favorito`` utilizando
el valor que se le pasa como parámetro ``GET``::

    def set_color(request):
        if "color_favorito" in request.GET:

            # Crea un objeto  HttpResponse...
            response = HttpResponse("Tu color favorito es ahora %s" % \
                request.GET["color_favorito"])

            # ... y definimos la cookie en la respuesta
            response.set_cookie("color_favorito",
                                request.GET["color_favorito"])

            return response

        else:
            return HttpResponse("No haz elegido un color favorito.")

Hay una serie de parámetros opcionales que puedes pasar
a ``response.set_cookie()`` y que te permiten controlar determinadas
características de la *cookie*, tal y como se muestra en la
tabla 14-1.

.. table:: Tabla 14-1: Opciones de las Cookies

    ==============  =================  ===================================================
    Parámetro       Valor por omisión  Descripción
    ==============  =================  ===================================================
      ``max_age``       ``None``       El tiempo (en segundos) que la cookie
                                       debe permanecer activa. Si este
                                       parámetro es la *cookie*, desaparecerá
                                       automáticamente cuando se cierre el
                                       navegador.


     ``expires``       ``None``        La fecha y hora en que la cookie debe
                                       expirar. Debe estar en el formato
                                       ``"Wdy, DD-Mth-YY HH:MM:SS GMT"``. Si
                                       se utiliza este parámetro, su valor
                                       tiene preferencia sobre el definido
                                       mediante ``max_age``.

        ``path``        ``"/"``        La ruta o *path* para la cual es válida la
                                       cookie. Los navegadores solo reenviarán la
                                       cookie a las páginas que estén en dicha
                                       ruta. Esto impide que se envíe esta cookie
                                       a otras secciones de la web.

                                       Es especialmente útil si no se tiene el control
                                       del nivel superior de directorios del
                                       servidor web.

     ``domain``         ``None``       El dominio para el cual es válida la cookie. Se
                                       puede usar este parámetro para definir una
                                       cookie que sea apta para varios dominios. Por
                                       ejemplo, definiendo ``domain=".example.com"``
                                       la cookie será enviada a los dominios
                                       ``www.example.com``, ``www2.example.com`` y
                                       ``aun.otro.subdominio.example.com``.

                                       Si a este parámetro no se le asigna ningún valor, 
                                       la cookie solo será enviada al dominio que la
                                       definió.

        ``secure``      ``False``      Si este valor se define como ``True``, se le indica
                                       al navegador que sólo retorne esta cookie a las 
                                       páginas que se accedan de forma segura
                                       (protocolo HTTPS en vez de   HTTP).
    ==============  =================  ===================================================

Las cookies tienen doble filo
-----------------------------

Puede que te hayas dado cuenta de algunos de los problemas potenciales
que se presentan con esto de las cookies; vamos a ver algunos de los
más importantes:

* El almacenamiento de los cookies es voluntario; los navegadores
  no dan ninguna garantía. De hecho, los navegadores permiten al
  usuario definir una política de aceptación o rechazo de las
  mismas. Para darte cuenta de lo muy usadas que son las cookies
  en la web actual, simplemente activa la opción de "Avisar antes
  de aceptar cualquier cookie" y date un paseo por Internet.

  A pesar de su uso habitual, las cookies son el ejemplo perfecto
  de algo que no es confiable. Esto significa que el desarrollador debe
  comprobar que el usuario está dispuesto a aceptar las cookies
  antes de confiar en ellas.

  Aún más importante, *nunca* debes almacenar información fundamental
  en las cookies. La Web rebosa de historias de terror acerca
  de desarrolladores que guardaron información irrecuperable
  en las cookies del usuario, solo para encontrarse con que el
  navegador había borrado todos esos datos por cualquier razón.

* Las Cookies (especialmente aquellas que no se envían mediante HTTPS)
  no son seguras. Dado que los datos enviados viajan en texto claro,
  están expuestas a que terceras personas lean esa información, lo
  que se llama ataques de tipo *snooping* (por *snoop*, fisgonear, husmear).
  Por lo tanto, un atacante que tenga acceso al medio puede interceptar la
  cookie y leer su valor. El resultado de esto es que nunca se debe almacenar
  información confidencial en una cookie.

  Hay otro tipo de ataque, aún más insidioso, conocido como
  ataque *man-in-the-middle* o MitM (ataque de tipo Hombre-en-medio o
  Intermediario). Aquí, el atacante no solo intercepta la cookie,
  sino que además la usa para actuar ante el servidor como si fuera
  el usuario legítimo. Él :doc:`capítulo 19<chapter19>` describe en profundidad
  este tipo de ataques, así como formas de prevenirlo.

* Las Cookies ni siquiera son seguras para los servidores. La mayoría de los
  navegadores permiten manipular y editar de forma sencilla los contenidos
  de cookies individuales, y existen herramientas como mechanize
  (http://wwwsearch.sourceforge.net/mechanize/) que permiten a cualquiera
  que esté lo suficientemente motivado construir solicitudes HTTP
  a mano.

Así que tampoco debemos almacenar en las cookies datos que sean fáciles de 
falsificar. El error habitual en este escenario consiste en almacenar algo así 
como  ``IsLoggedIn=1`` en una cookie cuando el usuario se ha validado. Te 
sorprendería saber cuántos sitios web cometen este tipo de error; no lleva más 
de unos segundos engañar a sus sistemas de "seguridad".

El entorno de sesiones de Django
================================

Con todas estas limitaciones y agujeros potenciales de seguridad, es obvio
que la gestión de las cookies y de las sesiones persistentes es el origen
de muchos dolores de cabeza para los desarrolladores web. Por supuesto, uno de 
los objetivos de Django es evitar eficazmente estos dolores de cabeza, así
que dispone de un entorno de sesiones diseñado para suavizar y facilitar todas
estas cuestiones.

El entorno de sesiones te permite almacenar y recuperar cualquier dato que 
quieras basándote en la sesión del usuario. Almacena la información relevante
solo en el servidor y abstrae todo el problema del envío y recepción de las
cookies. Estas solo almacenan una versión codificada (*hash*) del identificador
de la sesión, y ningún otro dato, lo cual te aísla de la mayoría de los
problemas asociados con las cookies.

Veamos como activar las sesiones, y como usarlas en nuestras vistas.

Activar sesiones
----------------

Las sesiones se implementan mediante un poco de *middleware* y un modelo Django. 
Para activar las sesiones, necesitas seguir los siguientes pasos:

#. Editar el valor de ``MIDDLEWARE_CLASSES`` de forma que contenga
   ``'django.contrib.sessions.middleware.SessionMiddleware'``. 

#. Comprobar que ``'django.contrib.sessions'`` esté incluido
   en el valor de ``INSTALLED_APPS`` (y ejecutar los comandos
   ``manage.py makemigrationes`` y ``migrate``  si lo tuviste que añadir).

El archivo por defecto ``settings.py`` creado por el comando ``startproject`` 
activa estas dos características, así que a menos que las hayas borrado,
es muy probable que no tengas que hacer nada para empezar a usar las
sesiones.

Si lo que quieres en realidad es no usar sesiones, deberías quitar la referencia
a ``SessionMiddleware`` de ``MIDDLEWARE_CLASSES`` y borra
``'django.contrib.sessions'`` de ``INSTALLED_APPS``. Esto te ahorrará sólo un 
poco de sobrecarga, pero toda ayuda es buena.

Usar las sesiones en una vista
------------------------------

Cuando están activadas las sesiones, los objetos ``HttpRequest`` --el primer 
argumento de cualquier función que actúe como una vista en Django tendrán un 
atributo llamado ``session``, que se comporta igual que un diccionario. Se puede
leer y escribir en él de la misma forma en que lo harías con un diccionario 
normal. Por ejemplo, podrías usar algo como esto en una de tus vistas::

    # Set a session value:
    request.session["fav_color"] = "blue"

    # Get a session value -- this could be called in a different view,
    # or many requests later (or both):
    fav_color = request.session["fav_color"]

    # Clear an item from the session:
    del request.session["fav_color"]

    # Check if the session has a given key:
    if "fav_color" in request.session:
        ...

También puedes usar otros métodos propios de un diccionario como ``keys()``
o ``items()`` en ``request.session``.

Hay dos o tres reglas muy sencillas para usar eficazmente las sesiones en Django:

* Debes usar sólo cadenas de texto normales como valores de clave
  en ``request.session``, en vez de, por ejemplo, enteros, objetos, etc. Esto
  es más un convenio que un regla en el sentido estricto, pero merece la pena
  seguirla.

* Los valores de las claves de una sesión que empiecen con el carácter
  subrayado están reservadas para uso interno de Django. En la práctica, sólo
  hay unas pocas variables así, pero, a no ser que sepas lo que estás
  haciendo (y estés dispuesto a mantenerte al día en los cambios internos
  de Django), lo mejor que puedes hacer es evitar usar el carácter subrayado
  como prefijo en tus propias variables; eso impedirá que Django
  pueda interferir con tu aplicación,

* Nunca reemplaces ``request.session`` por otro objeto, y nunca accedas
  o modifiques sus atributos. Utilízalo sólo como si fuera un diccionario.

Veamos un ejemplo rápido. Esta vista simplificada define una variable
``has_commented`` como ``True`` después de que el usuario haya publicado
un comentario. Es una forma sencilla (aunque no particularmente segura) de
impedir que el usuario publique dos veces el mismo comentario::

    def post_comment(request):
        if request.method != 'POST':
            raise Http404('Only POSTs are allowed')

        if 'comment' not in request.POST:
            raise Http404('Comment not submitted')

        if request.session.get('has_commented', False):
            return HttpResponse("You've already commented.")

        c = comments.Comment(comment=request.POST['comment'])
        c.save()
        request.session['has_commented'] = True
        return HttpResponse('Thanks for your comment!')

Esta vista simplificada permite que un usuario se identifique
como tal en nuestras páginas::

    def login(request):
        if request.method != 'POST':
            raise Http404('Only POSTs are allowed')
        try:
            m = Member.objects.get(username=request.POST['username'])
            if m.password == request.POST['password']:
                request.session['member_id'] = m.id
                return HttpResponseRedirect('/you-are-logged-in/')
        except Member.DoesNotExist:
            return HttpResponse("Your username and password didn't match.")

Y esta le permite cerrar o salir de la sesión::

    def logout(request):
        try:
            del request.session['member_id']
        except KeyError:
            pass
        return HttpResponse("You're logged out.")

.. note:: 

    En la práctica, esta sería una forma pésima de validar a tus
    usuarios. El mecanismo de autentificación que presentaremos
    un poco más adelante realiza esta tarea de forma mucho más
    segura y robusta. Los ejemplo son deliberadamente simples
    para que se comprendan con más facilidad.

Comprobar las configuraciones de las *cookies* 
----------------------------------------------

.. Setting Test Cookies

Como ya mencionamos, no se puede confiar en que cualquier navegador
sea capaz de aceptar *cookies*. Por ello, Django incluye una forma fácil
de comprobar que el cliente del usuario disponga de esta capacidad. Sólo
es necesario llamar a la función ``request.session.set_test_cookie()``
en una vista, y comprobar posteriormente, en otra vista distinta, el
resultado de llamar a ``request.session.test_cookie_worked()``.

Esta división un tanto extraña entre las llamadas a ``set_test_cookie()`` 
y ``test_cookie_worked()`` se debe a la forma es que trabajan 
las *cookies*. Cuando se define una *cookie*, no tienes forma de saber
si el navegador la ha aceptado realmente hasta la siguiente solicitud.

Es una práctica recomendable llamar a la función ``delete_test_cookie()`` para
limpiar la cookie de prueba después de haberla usado. Lo mejor es hacerlo
justo después de haber verificado que las *cookies* funcionan.

He aquí un ejemplo típico de uso::

    def login(request):

        # If we submitted the form...
        if request.method == 'POST':

            # Check that the test cookie worked (we set it below):
            if request.session.test_cookie_worked():

                # The test cookie worked, so delete it.
                request.session.delete_test_cookie()

                # In practice, we'd need some logic to check username/password
                # here, but since this is an example...
                return HttpResponse("You're logged in.")

            # The test cookie failed, so display an error message. If this
            # were a real site, we'd want to display a friendlier message.
            else:
                return HttpResponse("Please enable cookies and try again.")

        # If we didn't post, send the test cookie along with the login form.
        request.session.set_test_cookie()
        return render(request, 'foo/login_form.html')


.. admonition:: Nota

    De nuevo, las funciones de autentificación ya definidas en el entorno
    se encargan de realizar estos chequeos por ti.

Usar sesiones fuera de las vistas
---------------------------------

Internamente, cada sesión es simplemente un modelo de entidad de
Django como cualquier otro, definido en ``django.contrib.sessions.models``. Cada
sesión se identifica gracias a un *hash* pseudo-aleatorio de 32 caracteres, que
es el valor que se almacena en la cookie. Dado que es un modelo normal, puedes
acceder a las propiedades de las sesiones usando la API de acceso a la
base de datos de Django::

    >>> from django.contrib.sessions.models import Session
    >>> s = Session.objects.get(pk='2b1189a188b44ad18c35e113ac6ceead')
    >>> s.expire_date
    datetime.datetime(2005, 8, 20, 13, 35, 14)

Para poder acceder a los datos de la sesión, hay que usar el método
``get_decoded()``. Esto se debe a que estos datos, que consistían en
un diccionario, están almacenados codificados::

    >>> s.session_data
    'KGRwMQpTJ19hdXRoX3VzZXJfaWQnCnAyCkkxCnMuMTExY2ZjODI2Yj...'
    >>> s.get_decoded()
    {'user_id': 42}

Cuándo se guardan las sesiones
------------------------------

Django, en principio, solo almacena la sesión en la base de datos si ésta
ha sido modificada; es decir, si cualquiera de los valores almacenados
en el diccionario es asignado o borrado. Esto puede dar lugar a algunos
errores sutiles, como se indica en el último ejemplo::

    # Session is modified.
    request.session['foo'] = 'bar'

    # Session is modified.
    del request.session['foo']

    # Session is modified.
    request.session['foo'] = {}

    # Gotcha: Session is NOT modified, because this alters
    # request.session['foo'] instead of request.session.
    request.session['foo']['bar'] = 'baz'

Se puede cambiar este comportamiento, especificando la opción
``SESSION_SAVE_EVERY_REQUEST`` a ``True``. Si lo hacemos así, Django
almacenará la sesión en la base de datos en cada petición, incluso si
no se ha modificado ninguno de sus valores.

Fíjate que la cookie de sesión sólo se envía cuando se ha creado o
modificado una sesión. Si ``SESSION_SAVE_EVERY_REQUEST`` está como ``True``, la
cookie de sesión será reenviada en cada petición. De forma similar, la sección
de expiración (''expires'') se actualizará cada vez que se reenvíe la
cookie.

Sesiones breves frente a sesiones persistentes
----------------------------------------------

Es posible que te hayas fijado en que la cookie que nos envió Google al
principio del capítulo contenía el siguiente texto ``expires=Sun,
17-Jan-2038 19:14:07 GMT;``. Las Cookies pueden incluir opcionalmente
una fecha de expiración, que informa al navegador el momento en que se
debe desechar por inválida. Si la cookie no contiene ningún
valor de expiración, el navegador entiende que esta debe expirar
en el momento en que se cierra el propio navegador. Se puede controlar
el comportamiento del entorno para que use cookies de este tipo, breves, ajustando
en valor de la opción ``SESSION_EXPIRE_AT_BROWSER_CLOSE``.

El valor por omisión de la opción ``SESSION_EXPIRE_AT_BROWSER_CLOSE`` es
``False``, lo que significa que las cookies serán almacenadas en el
navegador del usuario durante ``SESSION_COOKIE_AGE`` segundos (cuyo
valor por defecto es de dos semanas, o 1.209.600 segundos). Estos
valores son adecuados si no quieres obligar a tus usuarios a validarse
cada vez que abran el navegador y accedan a tu página.

Si ``SESSION_EXPIRE_AT_BROWSER_CLOSE`` se establece a ``True``, Django
usará cookies que se invalidarán cuando el usuario cierre el navegador.

Otras características de las sesiones
-------------------------------------

Además de las características ya mencionadas, hay otros valores de configuración que
influyen en la gestión de sesiones con Django, tal y como se muestra en
la tabla 14-2.

.. table:: Tabla 14-2. Valores de configuración que influyen en el comportamiento de las cookies

    ==========================  =============================  =================
      Opción                      Descripción                  Valor por defecto
    ==========================  =============================  =================
    ``SESSION_COOKIE_DOMAIN``   El Dominio a utilizar por la   ``None``
                                cookie de sesión. Se puede
                                utilizar, por ejemplo, el
                                valor ``".lawrence.com"``
                                para utilizar la cookie en
                                diferentes subdominios. El
                                valor ``None`` indica una
                                cookie estándar.

    ``SESSION_COOKIE_NAME``     El nombre de la cookie de       ``"sessionid"``
                                sesiones. Puede ser cualquier
                                cadena de texto.

    ``SESSION_COOKIE_SECURE``   Indica si se debe usar una       ``False``
                                cookie segura para la cookie
                                de sesión. Si el valor es
                                ``True``, la cookie se
                                marcará como segura, lo que
                                significa que sólo se podrá
                                utilizar mediante el
                                protocolo HTTPS.
    ==========================  =============================  =================

.. admonition:: Detalles técnicos

    Para los más curiosos, he aquí una serie de notas técnicas acerca de algunos
    aspectos interesantes de la gestión interna de las sesiones:

* El diccionario de la sesión acepta cualquier objeto Python capaz de
  ser serializado con ``pickle``. Véase la documentación del módulo
  ``pickle`` incluido en la biblioteca estándar de Python para más información.

* Los datos de la sesión se almacenan en una tabla en la base de datos llamada
  ``django_session``.

* Los datos de la sesión son suministrados bajo demanda. Si nunca accedes al
  atributo ``request.session``, Django nunca accederá a la base de datos.

* Django sólo envía la cookie si tiene que hacerlo. Si no modificas ningún
  valor de la sesión, no reenvía la cookie (a no ser que hayas definido
  ``SESSION_SAVE_EVERY_REQUEST`` como ``True``).

* El entorno de sesiones de Django se basa entera y exclusivamente en
  las cookies. No almacena la información de la sesión en las URL, como recurso
  extremo en el caso de que no se puedan utilizar las cookies, como hacen
  otros entornos (PHP, JSP).

  Esta es una decisión tomada de forma consciente. Poner los
  identificadores de sesión en las URL no solo hace que las
  direcciones sean más feas, también hace que el sistema sea
  vulnerable ante un tipo de ataque en que se roba el
  identificador de la sesión utilizando la cabecera
  ``Referer``.

  Si aun te pica la curiosidad, el código fuente es bastante directo y claro, mira
  en ``django.contrib.sessions`` para más detalles.


Usuarios e identificación
=========================

Estamos ya a medio camino de poder conectar los navegadores con la Gente
de Verdad™. Las sesiones nos permiten almacenar información a lo largo de
las diferentes peticiones del navegador; la segunda parte de la ecuación
es utilizar esas sesiones para validar al usuario, es decir, permitirle
hacer *login*. Por supuesto, no podemos simplemente confiar en que
los usuarios sean quien dicen ser, necesitamos autentificarlos de alguna
manera.

Naturalmente, Django nos proporciona las herramientas necesarias para
tratar con este problema tan habitual (y con muchos otros). El sistema
de autentificación de usuarios de Django maneja cuentas de usuarios, grupos,
permisos y sesiones basadas en cookies. El sistema también es llamada sistema
*aut/aut* (autenticaficación y autorización). El nombre implica que, a
menudo, tratar con los usuarios implica dos procesos. Se necesita:

* Verificar (*autentificación*) que un usuario es quien dice
  ser (Normalmente comprobando un nombre de usuario y una
  contraseña contra una tabla de una base de datos)

* Verificar que el usuario está autorizado (*autorización*) a
  realizar una operación determinada (normalmente
  comprobando una tabla de permisos)

Siguiendo estos requerimientos, el sistema aut/aut de Django consta de los
siguientes componentes:

* *Usuarios*: Personas registradas en tu sitio web

* *Permisos*: Valores binarios (Si/No) que indican si un usuario
  puede o no realizar una tarea determinada.

* *grupos*: Una forma genérica de aplicar etiquetas y permisos a
  más de un usuario.

* *mensajes*: Un mecanismo sencillo que permite enviar y mostrar
  mensajes del sistema usando una cola.

* *Perfiles*: Un mecanismo que permite extender los objetos de
  tipo usuario con campos adicionales.

Si ya has utilizado la herramienta de administración (descrita en el
:doc:`capítulo 6<chapter06>`), habrás visto muchas de estas utilidades, 
y si has modificado usuarios y grupos con dicha herramienta, ya has modificado
las tablas en las que se basa el sistema aut/aut.

Habilitar el soporte para autentificación
-----------------------------------------

Al igual que ocurría con las sesiones, el sistema de autentificación
viene incluido como una aplicación en el módulo ``django.contrib``, y
necesita ser instalado. De igual manera, viene instalado por defecto, por
lo que solo es necesario seguir los siguientes pasos si previamente
la has desinstalado:

* Comprueba que el sistema de sesiones esté activo, tal y como
  se explico previamente en este capítulo. Seguir la pista de
  los usuario implica usar cookies, y por lo tanto necesitamos
  el entorno de sesiones operativo.

* Incluye ``'django.contrib.auth'`` dentro de tu ``INSTALLED_APPS`` y
  ejecuta los comandos ``makemigration`` y ``migrate``.

* Asegúrate de que
  ``'django.contrib.auth.middleware.AuthenticationMiddleware'`` está
  incluido en ``MIDDLEWARE_CLASSES`` *después de*
  ``SessionMiddleware``.

Una vez resuelto este tema, ya estamos preparados para empezar a lidiar
con los usuarios en nuestras vistas. La principal interfaz que
usarás para trabajar con los datos del usuario dentro de una vista es
``request.user``; es un objeto que representa al usuario que está conectado
en ese momento. Si no hay ningún usuario conectado, este objeto será
una instancia de la clase ``AnonymousUser`` (veremos más sobre esta clase
un poco más adelante).

Puedes saber fácilmente si el usuario está identificado o no con el método
``is_authenticated()``::

    if request.user.is_authenticated():
        # Do something for authenticated users.
    else:
        # Do something for anonymous users.

Utilizando usuarios
===================

Una vez que ya tienes un usuario (normalmente mediante ``request.user``, pero
también puede ser por otros métodos, que se describirán en breve) dispondrás
de una serie de campos de datos y métodos asociados al mismo. Los objetos de la 
clase ``AnonymousUser`` emulan *parte* de esta interfaz, pero no toda, por lo
que es preferible comprobar el resultado de ``user.is_authenticated()`` antes
de asumir de buena fe que nos encontramos ante un usuario legítimo. Las tablas
14-3 y 14-4 listan todos los campos y métodos, respectivamente, de los objetos
de la clase ``User``.

Campos de los objetos ``User``

.. table:: Tabla 14-3. Campos de los objetos ``User``

    ==================  =============================================================
        Campo               Descripción
    ==================  =============================================================
        ``username``        Obligatorio; 30 caracteres como máximo. Sólo acepta
                            caracteres alfanuméricos (letras, dígitos y el
                            carácter subrayado).

      ``first_name``        Opcional; 30 caracteres como máximo.

        ``last_name``       Opcional; 30 caracteres como máximo.

        ``email``           Opcional. Dirección de correo electrónico.

        ``password``        Obligatorio. Un código de comprobación (*hash*),
                            junto con otros metadatos de la contraseña. Django
                            nunca almacena la contraseña en crudo. Véase la
                            sección "`Cambia contraseñas`_" para más información

        ``is_staff``        Booleano. Indica que el usuario puede acceder
                            a las secciones de administración.

       ``is_active``        Booleano. Indica que la cuenta puede ser usada para
                            identificarse. Se puede poner a ``False`` para
                            deshabilitar a un usuario sin tener que borrarlo
                            de la tabla.

    ``is_superuser``        Booleano. Señala que el usuario tiene todos los
                            permisos, aún cuando no se le hayan asignado
                            explícitamente

      ``last_login``        Fecha y hora de la última vez que el usuario se
                            identificó. Se asigna automáticamente a la
                            fecha actual por defecto.

     ``date_joined``        Fecha y hora en que fue creada esta cuenta de
                            usuario. Se asigna automáticamente a la
                            fecha actual en su momento.

    ==================  =============================================================

Métodos de los objetos ``User``

.. table:: Tabla 14-4. Métodos de los objetos ``User``

    ================================  ================================================
        Método                            Descripción
    ================================  ================================================
        ``is_authenticated()``            Siempre devuelve ``True`` para usuario
                                          reales. Es una forma de determinar si el
                                          usuario se ha identificado. esto no
                                          implica que posea ningún permiso, y
                                          tampoco comprueba que la cuenta esté
                                          activa. Sólo indica que el usuario se
                                          ha identificado con éxito.

        ``is_anonymous()``                Devuelve ``True`` sólo para usuarios
                                          anónimos, y ``False`` para usuarios
                                          "reales". En general, es preferible
                                          usar el método ``is_authenticated()``.

        ``get_full_name()``               Devuelve la concatenación de los
                                          campos ``first_name`` y
                                          ``last_name``, con un espacio
                                          en medio.

        ``set_password(passwd)``          Cambia la contraseña del usuario a
                                          la cadena de texto en claro indicada,
                                          realizando internamente las
                                          operaciones necesarias para calcular
                                          el código de comprobación o *hash*
                                          necesario. Este método *no* guarda el
                                          objeto ``User``.

        ``check_password(passwd)``        devuelve ``True`` si la cadena de
                                          texto en claro que se le pasa
                                          coincide con la contraseña
                                          del usuario. Realiza internamente
                                          las operaciones necesarias para
                                          calcular los códigos de comprobación
                                          o *hash* necesarios.

        ``get_group_permissions()``       Devuelve una lista con los permisos que
                                          tiene un usuario, obtenidos a través del
                                          grupo o grupos a las que pertenezca.

        ``get_all_permissions()``         Devuelve una lista con los permisos que
                                          tiene concedidos un usuario, ya sea a
                                          través de los grupos a los que pertenece
                                          o bien asignados directamente.

        ``has_perm(perm)``                Devuelve ``True`` si el usuario tiene el
                                          permiso indicado. El valor de ``perm``
                                          está en el
                                          formato ```"package.codename"``. Si el
                                          usuario no está activo, siempre
                                          devolverá ``False``.

        ``has_perms(perm_list)``          Devuelve ``True`` si el usuario tiene
                                          *todos* los permisos indicados. Si el
                                          usuario no está activo, siempre
                                          devolverá ``False``.

     ``has_module_perms(app_label)``      Devuelve ``True`` si el usuario tiene
                                          algún permiso en la etiqueta de
                                          aplicación indicada, ``app_label``. Si
                                          el usuario no está activo, siempre
                                          devolverá ``False``.

     ``get_and_delete_messages()``        Devuelve una lista de mensajes (objetos
                                          de la clase ``Message``) de la cola del
                                          usuario, y los borra posteriormente.

        ``email_user(subj, msg)``         Envía un correo electrónico al usuario.
                                          El mensaje aparece como enviado desde
                                          la dirección indicada en el valor
                                          ``DEFAULT_FROM_EMAIL``. Se le puede
                                          pasar un tercer parámetro opcional,
                                          ``from_email``, para indicar otra
                                          dirección de remite distinta.
    ================================  ================================================

Por último, los objetos de tipo ``User`` mantienen dos campos de relaciones
múltiples o muchos-a-muchos: Grupos y permisos (``groups`` y ``permissions``). 
Se puede acceder a estos objetos relacionados de la misma manera en que se usan 
otros campos múltiples::

        # Set a user's groups:
        myuser.groups = group_list

        # Add a user to some groups:
        myuser.groups.add(group1, group2,...)

        # Remove a user from some groups:
        myuser.groups.remove(group1, group2,...)

        # Remove a user from all groups:
        myuser.groups.clear()

        # Permissions work the same way
        myuser.permissions = permission_list
        myuser.permissions.add(permission1, permission2, ...)
        myuser.permissions.remove(permission1, permission2, ...)
        myuser.permissions.clear()

Iniciar y cerrar sesión
-----------------------

Django proporciona vistas predefinidas para  gestionar la entrada
del usuario, (el momento en que se identifica), y la salida, (es
decir, cuando cierra la sesión), además de otros trucos ingeniosos. Pero
antes de entrar en detalles, veremos como hacer que los usuario puedan
iniciar y cerrar la sesión "a mano". Django incluye dos funciones
para realizar estas acciones, en el módulo ``django.contrib.auth``:
``authenticate()`` y ``login()``.

Para autentificar un identificador de usuario y una contraseña, se utiliza
la función ``authenticate()``. esta función acepta dos parámetros ,
``username`` y ``password``, y devuelve un objeto de tipo ``User`` si la
contraseña es correcta para el identificador de usuario. Si falla la
comprobación (ya sea porque sea incorrecta la contraseña o porque sea
incorrecta la identificación del usuario), la función devolverá ``None``::

    >>> from django.contrib import auth
    >>> user = auth.authenticate(username='john', password='secret')
    >>> if user is not None:
    ...     print "Correct!"
    ... else:
    ...     print "Oops, that's wrong!"

La llamada a ``authenticate()`` sólo verifica las credenciales del
usuario. Todavía hay que realizar una llamada a ``login()`` para
completar el inicio de sesión. La llamada a ``login()`` acepta un
objeto de la clase ``HttpRequest`` y un objeto ``User`` y almacena
el identificador del usuario en la sesión, usando el entorno de
sesiones de Django.

El siguiente ejemplo muestra el uso de ambas funciones, ``authenticate()`` y 
``login()``, dentro de una vista::

    from django.contrib import auth

    def login_view(request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/account/loggedin/")
        else:
            # Show an error page
            return HttpResponseRedirect("/account/invalid/")

Para cerrar la sesión, se puede llamar a ``django.contrib.auth.logout()``
dentro de una vista. Necesita que se le pase como parámetro un objeto
de tipo ``HttpRequest``, y no devuelve ningún valor::

    from django.contrib import auth

    def logout(request):
        auth.logout(request)
        # Redirect to a success page.
        return HttpResponseRedirect("/account/loggedout/")

La llamada a ``logout()`` no produce ningún error, aun si no hubiera
ningún usuario conectado.

En la práctica, no es normalmente necesario escribir tus propias
funciones para realizar estas tareas; el sistema de autentificación
viene con un conjunto de vistas predefinidas para ello.

El primer paso para utilizar las vistas de autentificación es
mapearlas en tu URLconf. Necesitas modificar tu código hasta
tener algo parecido a esto::

    from django.contrib.auth.views import login, logout

    urlpatterns = [
        # mas patrones aqui...
        url(r'^accounts/login/$',  login),
        url(r'^accounts/logout/$', logout),
    ]

``/accounts/login/`` y ``/accounts/logout/`` son las URL por defecto
que usa Django para estas vistas.

Por defecto, la vista de ``login`` utiliza la plantilla definida en
``registration/login.html`` (puedes cambiar el nombre de la plantilla
utilizando un parámetro opcional, ``template_name``). El formulario
necesita contener un campo llamado ``username`` y otro llamado
``password``. Una plantilla de ejemplo podría ser esta:

.. code-block:: html

    {% extends "base.html" %}

    {% block content %}

      {% if form.errors %}
        <p class="error">Sorry, that's not a valid username or password</p>
      {% endif %}

      <form action="" method="post">
        <label for="username">User name:</label>
        <input type="text" name="username" value="" id="username">
        <label for="password">Password:</label>
        <input type="password" name="password" value="" id="password">

        <input type="submit" value="login" />
        <input type="hidden" name="next" value="{{ next|escape }}" />
      </form>

    {% endblock %}

Si el usuario se identifica correctamente, su navegador será redirigido
a ``/accounts/profile/``. Puedes indicar una dirección distinta especificando
un tercer campo (normalmente oculto) que se llame ``next``, cuyo valor
debe ser la URL a redireccionar después de la identificación. También puedes
pasar este valor como un parámetro ``GET`` a la vista de identificación
y se añadirá automáticamente su valor al contexto en una variable
llamada ``next``, que puedes incluir ahora en un campo oculto.

La vista de cierre de sesión se comporta de forma un poco diferente. Por 
defecto utiliza la plantilla definida en ``registration/logged_out.html`` 
(que normalmente contiene un mensaje del tipo "Ha cerrado su sesión"). No 
obstante, se puede llamar a esta vista con un parámetro extra, llamado 
``next_page``, que indicaría la vista a la que se debe redirigir una vez 
efectuado el cierre de la sesión.

Limitar el acceso a los usuarios identificados
----------------------------------------------

Por supuesto, la razón de haber implementado todo este sistema es permitirnos 
limitar el acceso a determinadas partes de nuestro sitio.

La forma más simple y directa de limitar este acceso es comprobar el resultado 
de llamar a la función ``request.user.is_authenticated()`` y redirigir a una 
página de identificación, si procede::

    from django.http import HttpResponseRedirect

    def my_view(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/?next=%s' % request.path)
        # ...

O quizás mostrar un mensaje de error::

    def my_view(request):
        if not request.user.is_authenticated():
            return render_to_response('myapp/login_error.html')
        # ...

Si se desea abreviar, se puede usar el decorador ``login_required``
sobre las vistas que nos interese proteger::

    from django.contrib.auth.decorators import login_required

    @login_required
    def my_view(request):
        # ...

Esto es lo que hace el decorador ``login_required``:

* Si el usuario no está identificado, redirige a la dirección 
  ``/accounts/login/``, incluyendo la url actual como un parámetro con 
  el nombre ``next``, por ejemplo ``/accounts/login/?next=/polls/3/``.

* Si el usuario está identificado, ejecuta la vista sin ningún cambio. La 
  vista puede asumir sin problemas que el usuario está identificado 
  correctamente.

Limitar el acceso a usuarios que pasan una prueba
-------------------------------------------------

Se puede limitar el acceso basándose en ciertos permisos o en algún otro
tipo de prueba, o proporcionar una página de identificación distinta de la 
vista por defecto, y las dos cosas se hacen de manera similar.

La forma más cruda es ejecutar las pruebas que queremos hacer directamente
en el código de la vista. Por ejemplo, para comprobar que el usuario está
identificado y que, además, tenga asignado el permiso ``polls.can_vote``
(se explicará esto de los permisos con más detalle dentro de poco )
haríamos::

    def vote(request):
        if request.user.is_authenticated() and request.user.has_perm('polls.can_vote')):
            # vote here
        else:
            return HttpResponse("You can't vote in this poll.")

De nuevo, Django proporciona una forma abreviada llamada ``user_passes_test``. 
Requiere que se la pasen unos argumentos y genera un decorador especializado 
para cada situación en particular::

    def user_can_vote(user):
        return user.is_authenticated() and user.has_perm("polls.can_vote")

    @user_passes_test(user_can_vote, login_url="/login/")
    def vote(request):
        # Code here can assume a logged-in user with the correct permission.
        ...

El decorador ``user_passes_test`` tiene un parámetro obligatorio: un objeto que
se pueda llamar (normalmente una función) y que a su vez acepte como parámetro 
un objeto del tipo ``User``, y devuelva ``True`` si el usuario puede acceder y 
``False`` en caso contrario. Es importante destacar que ``user_passes_test`` 
no comprueba automáticamente que el usuario esté identificado; esa es una 
comprobación que se debe hacer explícitamente.

En este ejemplo, hemos usado también un segundo parámetro opcional,
``login_url``, que te permite indicar la url de la página que el
usuario debe utilizar para identificarse (``/accounts/login/``
por defecto).

Comprobar si un usuario posee un determinado permiso es una tarea muy frecuente,
así que Django proporciona una forma abreviada para estos casos: El decorador 
``permission_required()``. Usando este decorador, el ejemplo anterior se podría 
codificar así::

    from django.contrib.auth.decorators import permission_required

    @permission_required('polls.can_vote', login_url="/login/")
    def vote(request):
        # ...

El decorador ``permission_required()`` también acepta el parámetro opcional 
``login_url``, de nuevo con el valor ``/accounts/login/`` en caso de omisión.

.. admonition:: Limitar el acceso a vistas genéricas

    Una de las preguntas más frecuentes en la lista de usuarios de
    Django trata de cómo limitar el acceso a una vista genérica. Para
    conseguirlo, tienes que usar un recubrimiento sencillo
    alrededor de la vista que quieres proteger, y apuntar en tu
    URLconf al recubrimiento en vez de a la vista genérica::

        from dango.contrib.auth.decorators import login_required
        from django.views.generic.list_detail import object_detail

        @login_required
        def limited_object_detail(*args, **kwargs):
            return object_detail(*args, **kwargs)

Puedes cambiar el decorador ``login_required`` por cualquier otro
que quieras usar, como es lógico.


Gestionar usuarios, permisos y grupos
-------------------------------------

La forma más fácil de gestionar el sistema de autentificación es a través
de la interfaz de administración ``admin``. Él :doc:`capítulo 6<chapter06>` 
describe como usar esta interfaz para modificar los datos de los usuarios y 
controlar sus permisos y accesos, y la mayor parte del tiempo esa es la forma
más adecuada de gestión.

A veces, no obstante, hace falta un mayor control, y para eso podemos utilizar 
las llamadas a bajo nivel que describiremos en este capítulo.

Crear usuarios
~~~~~~~~~~~~~~

Puedes crear usuarios con el método ``create_user``::

    >>> from django.contrib.auth.models import User
    >>> user = User.objects.create_user(username='john',
    ...                                 email='jlennon@beatles.com',
    ...                                 password='glass onion')

En este momento, ``user`` es una instancia de la clase ``User``, preparada
para ser almacenada en la base de datos (``create_user()`` no llama al
método ``save()``). Este te permite cambiar algunos de sus atributos
antes de guardarlos, si quieres::

    >>> user.is_staff = True
    >>> user.save()

Cambia contraseñas
~~~~~~~~~~~~~~~~~~

Puedes cambiar las contraseña de un usuario llamando a ``set_password()``::

    >>> user = User.objects.get(username='john')
    >>> user.set_password('goo goo goo joob')
    >>> user.save()

No debes modificar directamente el atributo ``password``, a no ser que
tengas muy claro lo que estás haciendo. La contraseña se almacena en
la base de datos en forma de código de comprobación (*salted
hash*) y, por tanto, debe ser modificada sólo a través de este método.

Para ser más exactos, el atributo ``password`` de un objeto ``User`` es una
cadena de texto con el siguiente formato::

    hashtype$salt$hash

Es decir, el tipo de hash, el grano de sal (*salt*) y el código hash
propiamente dicho, separados entre sí por el carácter dólar ($).

El valor de ``hashtype`` puede ser ``sha1`` (por defecto) o ``md5``, el
algoritmo usado para realizar una transformación *hash* de un solo sentido
sobre la contraseña. El grano de sal es una cadena de texto
aleatoria que se utiliza para aumentar la resistencia de esta codificación
frente a un ataque por diccionario. Por ejemplo::

    sha1$a1976$a36cc8cbf81742a8fb52e221aaeab48ed7f58ab4

Las funciones ``User.set_password()`` y ``User.check_password()`` manejan
todos estos detalles y comprobaciones de forma transparente.

.. admonition:: ¿Tengo que echar sal a mi ordenador?

    No, la sal de la que hablamos no tiene nada que ver con ninguna
    receta de cocina; es una forma habitual de aumentar la
    seguridad a la hora de almacenar una contraseña. Una
    función *hash* es una función criptográfica, que se
    caracteriza por ser de un solo sentido; es decir, es fácil
    calcular el código *hash* de un determinado valor, pero es prácticamente
    imposible reconstruir el valor original partiendo únicamente del
    código hash.

    Si almacenáramos las contraseñas como texto en claro, cualquiera que
    pudiera obtener acceso a la base de datos podría saber sin ninguna
    dificultad todas las contraseñas al instante. Al guardar las
    contraseñas en forma de códigos *hash* se reduce el peligro en caso
    de que se comprometa la seguridad de la base de datos.

    No obstante, un atacante que pudiera acceder a la base de datos
    podría ahora realizar un ataque por fuerza bruta, calculando
    los códigos *hash* de millones de contraseñas distintas y comparando
    esos códigos con los que están almacenados en la base de datos. Este
    llevará algo de tiempo, pero menos de lo que parece, los ordenadores
    son increíblemente rápidos.

    Para empeorar las cosas, hay disponibles públicamente lo que se
    conoce como tablas arco iris (*rainbow tables*), que consisten en
    valores *hash* precalculados de millones de contraseñas de uso
    habitual. Usando una tabla arco iris, un atacante puede romper
    la mayoría de las contraseñas en segundos.

    Para aumentar la seguridad, se añade un valor inicial aleatorio
    y diferente a cada contraseña antes de obtener el código *hash*. Este
    valor aleatorio es el "grano de sal". Como cada grano de sal es
    diferente para cada password se evita el uso de tablas arco iris, lo
    que obliga al atacante a volver al sistema de ataque por fuerza
    bruta, que a su vez es más complicado al haber aumentado la entropía
    con el grano de sal. Otra ventaja es que si dos usuarios eligen
    la misma contraseña, al añadir el grano de sal los códigos hash
    resultantes serán diferentes.

    Aunque esta técnica no es, en términos absolutos, la más segura
    posible, ofrece un buen compromiso entre seguridad y conveniencia.

El alta del usuario
~~~~~~~~~~~~~~~~~~~

Podemos usar estas herramientas de bajo nivel para crear vistas que
permitan al usuario darse de alta. Prácticamente todos los desarrolladores
quieren implementar el alta del usuario a su manera, por
lo que Django da la opción de crearte tu propia vista para ello.
Afortunadamente, es muy fácil de hacer.

La forma más sencilla es escribir una pequeña vista que pregunte al
usuario los datos que necesita y con ellos se cree directamente
el usuario. Django proporciona un formulario prefabricado que se puede
usar con este fin, como se muestra en el siguiente ejemplo::

    from django import forms
    from django.contrib.auth.forms import UserCreationForm
    from django.http import HttpResponseRedirect
    from django.shortcuts import render

    def register(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                return HttpResponseRedirect("/books/")
        else:
            form = UserCreationForm()
        return render(request, "registration/register.html", {
            'form': form,
        })

Este formulario asume que existe una plantilla llamada
``registration/register.html``. esa plantilla podría
consistir en algo parecido a esto:

.. code-block:: html

  {% extends "base.html" %}

  {% block title %}Create an account{% endblock %}

  {% block content %}
    <h1>Create an account</h1>

    <form action="" method="post">
        {{ form.as_p }}
        <input type="submit" value="Create the account">
    </form>
  {% endblock %}


Usar información de autentificación en plantillas
-------------------------------------------------

El usuario actual, así como sus permisos, están disponibles
en el contexto de la plantilla cuando usas ``RequestContext`` (véase
:doc:`Capítulo 10<chapter10>`).

.. admonition:: Nota

    Técnicamente hablando, estas variables están disponibles en el contexto
    de la plantilla sólo si usas ``RequestContext`` *y* en la configuración
    está incluido el valor ``"django.core.context_processors.auth"`` en
    la opción ``TEMPLATE_CONTEXT_PROCESSORS``, que es el valor que viene
    predefinido cuando se crea un proyecto. Como ya se comentó, véase
    él :doc:`capítulo 10<chapter10>` para más información.

Cuando se usa ``RequestContext``, el usuario actual (ya sea una instancia de
``User`` o de ``AnonymousUser``) es accesible en la plantilla con el
nombre ``{{ user }}``::

    {% if user.is_authenticated %}
      <p>Welcome, {{ user.username }}. Thanks for logging in.</p>
    {% else %}
      <p>Welcome, new user. Please log in.</p>
    {% endif %}

Los permisos del usuario se almacenan en la variable ``{{ perms }}``. En realidad,
es una forma simplificada de acceder a un par de métodos sobre los permisos
que veremos en breve.

Hay dos formas de usar este objeto ``perms``. Puedes usar ``{{ perms.polls }}`` para
comprobar si un usuario tienen *algún* permiso para una determinada aplicación, o se
puede usar una forma más específica, como ``{{ perms.polls.can_vote }}``, para
comprobar si el usuario tiene concedido un permiso en concreto.

Por lo tanto, se pueden usar estas comprobaciones en sentencias ``{% if %}``:

.. code-block:: html

    {% if perms.polls %}
      <p>You have permission to do something in the polls app.</p>
      {% if perms.polls.can_vote %}
        <p>You can vote!</p>
      {% endif %}
    {% else %}
      <p>You don't have permission to do anything in the polls app.</p>
    {% endif %}

El resto de detalles: permisos, grupos, mensajes
================================================

Hay unas cuantas cosas que pertenecen al entorno de autentificación
y que hasta ahora sólo hemos podido ver de pasada. En esta sección las
veremos con un poco más de detalle.

Permisos
--------

Los permisos son una forma sencilla de "marcar" que determinados usuarios
o grupos pueden realizar una acción. Se usan normalmente para la parte de
administración de Django, pero puedes usarlos también en tu código.

El sistema de administración de Django utiliza  los siguientes permisos:

* Acceso a visualizar el formulario "Añadir", y Añadir objetos, está
  limitado a los usuarios que tengan el permiso *add* para ese
  tipo de objeto.

* El acceso a la lista de cambios, ver el formulario de cambios
  y cambiar un objeto está limitado a los usuarios que tengan
  el permisos *change* para ese tipo de objeto.

* Borrar objetos está limitado a los usuarios que tengan el
  permiso *delete* para ese tipo de objeto.

Los permisos se definen a nivel de las clases o tipos de objetos,
no a nivel de instancias. Por ejemplo, se puede decir "María puede
modificar los reportajes nuevos", pero no "María solo puede
modificar los reportajes nuevos que haya creado ella", ni "María
sólo puede cambiar los reportajes que tengan un determinado
estado, fecha de publicación o identificador".

Estos tres permisos básicos, añadir, cambiar y borrar, se crean
automáticamente para cualquier modelo Django que incluya una
clase ``Admin``. Entre bambalinas, los permisos se agregan a la
tabla ``auth_permission`` cuando ejecutas ``manage.py migrate``.

Estos permisos se crean con el siguiente formato:
``"<app>.<action>_<object_name>"``. Por ejemplo, si tienes una
aplicación llamada ``encuestas``, con un modelo llamado
``Respuesta``, se crearan automáticamente los tres
permisos con los nombres ``"encuestas.add_respuesta"``,
``"encuestas.change_respuesta"`` y
``"encuestas.delete_respuesta"``.

Igual que con los usuarios, los permisos se implementa en un modelo Django
que reside en el módulo ``django.contrib.auth.models``. Esto significa
que puedes usar la API de acceso a la base de datos para interactuar
con los permisos de la forma que quieras.

Grupos
------

Los grupos son una forma genérica de trabajar con varios usuarios
a la vez, de forma que se les pueda asignar permisos o etiquetas
en bloque. Un usuario puede pertenecer a varios grupos a la vez.

Un usuario que pertenezca a un grupo recibe automáticamente todos
los permisos que se la hayan otorgado al grupo. Por ejemplo, si el
grupo ``Editores`` tiene el permiso ``can_edit_home_page``, cualquier
usuario que pertenezca a dicho grupo también tiene ese permiso.

Los grupos también son una forma cómoda de categorizar a los usuarios
para asignarles una determinada etiqueta, o para otorgarles una funcionalidad
extra. Por ejemplo, se puede crear un grupo ``Usuarios especiales``, y
utilizar código para permitir el acceso a determinadas porciones de
tu sitio sólo a los miembros de ese grupo, o para enviarles un correo
electrónico sólo a ellos.

Al igual que con los usuarios, la manera más sencilla de gestionar los
grupos es usando la interfaz de administración de Django. Los grupos, en
cualquier caso, son modelos Django que residen en el módulo
``django.contrib.auth.models`` así que, al igual que en el caso
anterior, puedes usar la API de acceso a la base de datos para trabajar
con los grupos a bajo nivel.

Mensajes
--------

El sistema de mensajes es un forma muy ligera y sencilla de enviarle
mensajes a un usuario. Cada usuario tiene asociada una cola de
mensajes, de forma que los mensajes lleguen en el orden en que fueron
enviados. Los mensajes no tienen ni fecha de caducidad ni fecha de envío.

La interfaz de administración de Django usa los mensajes para notificar
que determinadas acciones han podido ser llevadas a cabo con éxito. Por
ejemplo, al crear un objeto, verás que aparece un mensaje en lo alto
de la página de administración, indicando que se ha podido crear el objeto
sin problemas.

Puedes usar la misma API para enviar o mostrar mensajes en tu propia
aplicación. Las llamadas de la API son bastante simples:

* Para crear un nuevo mensaje usa
  ``user.message_set.create(message='message_text')``.

* Para recuperar/eliminar mensajes usa ``user.get_and_delete_messages()``,
  la cual retorna una lista de objetos ``Message`` en la cola del usuario
  (si es que existiera alguno) y elimina el mensaje de la misma.

En el siguiente ejemplo, la vista guarda un mensaje para el usuario después de
crear una lista de reproducción::

    def create_playlist(request, songs):
        # Create the playlist with the given songs.
        # ...
        request.user.message_set.create(
            message="Your playlist was added successfully."
        )
        return render_to_response("playlists/create.html",
            context_instance=RequestContext(request))

Al usar ``RequestContext``, los mensajes del usuario actual, si los
tuviera, están accesibles desde la variable de contexto usando el
nombre ``{{ messages }}``. El siguiente ejemplo representa un fragmento
de código que muestras los mensajes:

.. code-block:: html

    {% if messages %}
    <ul>
        {% for message in messages %}
        <li>{{ message }}</li>
        {% endfor %}
    </ul>
    {% endif %}

Hay que hacer notar que ``RequestContext`` llama a ``get_and_delete_messages``
de forma implícita, por lo que los mensajes serán borrados, aún si no se
muestran en pantalla.

Por último, el sistema de mensajería sólo funciona para usuarios de la base de
datos. Para enviar mensajes a usuarios anónimos hay que usar en entorno de
sesiones directamente.

¿Qué sigue?
===========

La verdad es que el sistema de autorización tiene tela de donde cortar. 
Sin embargo la mayoría de las veces no tendrás que preocuparte por todos 
los detalles que se describen en este capítulo, pero si alguna vez tienes 
que gestionar interacciones complicadas con los usuarios, agradecerás tener 
a la mano todas estas utilidades disponibles.

En él :doc:`próximo capítulo<chapter15>`, echaremos un vistazo a una parte de 
Django que necesita la infraestructura que proporciona el sistema de cache, el
cual es una forma conveniente para mejorar el funcionamiento de tus
aplicaciones.