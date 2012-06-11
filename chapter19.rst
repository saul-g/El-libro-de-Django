======================
Capítulo 19: Seguridad
======================

Internet puede ser un lugar aterrador.

En estos tiempos, los papelones de seguridad con alta exposición pública parecen
ser cosa de todos los días. Hemos visto virus propagarse con una velocidad
asombrosa, ejércitos de computadoras comprometidas ser empuñados como armas, una
interminable *carrera armamentista* contra los *spammers*, y muchos, muchos
reportes de robos de identidad de sitios Web *hackeados*.

Parte de las tareas de un desarrollador Web es hacer lo que esté en sus manos
para combatir esas fuerzas de la oscuridad. Todo desarrollador Web necesita
considerar la seguridad como un aspecto fundamental de la programación Web.
Desafortunadamente, se da el caso de que implementar la seguridad es *difícil*
-- los atacantes sólo necesitan encontrar una única vulnerabilidad, pero los
defensores deben proteger todas y cada una.

Django intenta mitigar esta dificultad. Está diseñado para protegerte
automáticamente de muchos de los errores de seguridad comunes que cometen los
nuevos (e incluso los experimentados) desarrolladores Web. Aun así, es
importante entender de qué se tratan dichos problemas, cómo es que Django te
protege, y -- esto es lo más importante -- los pasos que puedes tomar para hacer
tu código aun más seguro.

Antes, sin embargo, una importante aclaración: No es nuestra intención
presentar una guía definitiva sobre todos los exploits de seguridad Web
conocidos, y tampoco trataremos de explicar cada vulnerabilidad en una forma
completa. En cambio, presentaremos una breve sinopsis de problemas de
seguridad que son relevantes para Django.

El tema de la seguridad en la Web
=================================

Si aprendes sólo una cosa de este capítulo, que sea esto::

    Nunca -- bajo ninguna circunstancia -- confíes en datos enviados por un navegador.

*Nunca* sabes quién está del otro lado de esa conexión HTTP. Podría tratarse de
uno de tus usuarios, pero con igual facilidad podría tratarse de un vil cracker
buscando un resquicio.

Cualquier dato de cualquier naturaleza que arriba desde el navegador necesita
ser tratado con una generosa dosis de paranoia. Esto incluye tanto datos que se
encuentran *"in band"* (por ejemplo enviados desde formularios Web) como *"out
of band"* (por ejemplo cabeceras HTTP, cookies, y otra información de petición).
Es trivial falsificar los metadatos de la petición que los navegadores
usualmente agregan automáticamente.

Todas las vulnerabilidades tratadas en este capítulo derivan directamente de
confiar en datos que arriban a través del cable y luego fallar a la hora
de limpiar esos datos antes de usarlos. Debes convertir en una práctica
general el preguntarte "¿De donde vienen estos datos?"

Inyección de SQL
================

La *inyección de SQL*  es un exploit común en el cual un atacante altera los
parámetros de la página (tales como datos de ``GET``/``POST`` o URLs) para
insertar fragmentos arbitrarios de SQL que una aplicación Web ingenua ejecuta
directamente en su base de datos. Es probablemente la más peligrosa -- y,
desafortunadamente una de las más comunes -- vulnerabilidad existente.

Esta vulnerabilidad se presenta más comúnmente cuando se está construyendo SQL
"a mano" a partir de datos ingresados por el usuario. Por ejemplo, imaginemos
que se escribe una función para obtener una lista de información de contacto
desde una página de búsqueda. Para prevenir que los spammers lean todas las
direcciones de email en nuestro sistema, vamos a exigir al usuario que escriba
el nombre de usuario del cual quiere conocer sus datos antes de proveerle la
dirección de email respectiva::

    def user_contacts(request):
        user = request.GET['username']
        sql = "SELECT * FROM user_contacts WHERE username = '%s';" % username
        # execute the SQL here...

.. admonition:: Nota:

    En este ejemplo, y en todos los ejemplos similares del tipo "no hagas esto"
    que siguen, hemos omitido deliberadamente la mayor parte del código
    necesario para hacer que el mismo realmente funcione. No queremos que este
    código sirva si accidentalmente alguien lo toma fuera de contexto y lo
    usa.

A pesar de que a primera vista eso no parece peligroso, realmente lo es.

Primero, nuestro intento de proteger nuestra lista de emails completa va a
fallar con una consulta construida en forma ingeniosa. Pensemos acerca de qué
sucede si un atacante escribe ``"'OR 'a'='a"`` en la caja de búsqueda. En ese
caso, la consulta que la interpolación construirá será::

    SELECT * FROM user_contacts WHERE username = '' OR 'a' = 'a';

Debido a que hemos permitido SQL sin protección en la string, la cláusula
``OR`` agregada por el atacante logra que se retornen todas los registros.

Sin embargo, ese es el *menos* pavoroso de los ataques. Imaginemos qué sucedería
si el atacante envía ``"'; DELETE FROM user_contacts WHERE 'a' = 'a'"``. Nos
encontraríamos con la siguiente consulta completa::

    SELECT * FROM user_contacts WHERE username = ''; DELETE FROM user_contacts WHERE 'a' = 'a';

¡Ouch! ¿Donde iría a parar nuestra lista de contactos?

La solución
-----------

Aunque este problema es insidioso y a veces difícil de detectar la solución es
simple: *nunca* confíes en datos provistos por el usuario y *siempre*
*escapa* el mismo cuando lo conviertes en SQL.

La API de base de datos de Django hace esto por ti. Escapa automáticamente
todos los parámetros especiales SQL, de acuerdo a las convenciones
de uso de comillas del servidor de base de datos que estés usando (por
ejemplo, PostgreSQL o MySQL).

Por ejemplo, en esta llamada a la API::

    foo.get_list(bar__exact="' OR 1=1")

Django *escapará* la entrada apropiadamente, resultando en una sentencia
como esta::

    SELECT * FROM foos WHERE bar = '\' OR 1=1'

que es completamente inocua.

Esto se aplica a la totalidad de la API de base de datos de Django, con un par de
excepciones:

    * El argumento ``where`` del método ``extra()`` (ver Apéndice C). Dicho
      parámetro acepta, por diseño, SQL crudo.

    * Consultas realizadas "a mano" usando la API de base de datos de nivel más
      bajo.

En tales casos, es fácil mantenerse protegido. para ello evita realizar
interpolación de strings y en cambio usa *parámetros asociados* (*bind
parameters*). Esto es, el ejemplo con el que comenzamos esta sección debe ser
escrito de la siguiente manera::

    from django.db import connection

    def user_contacts(request):
        user = request.GET['username']
        sql = "SELECT * FROM user_contacts WHERE username = %s;"
        cursor = connection.cursor()
        cursor.execute(sql, [user])
        # ... do something with the results

El método de bajo nivel ``execute`` toma un string SQL con marcadores de
posición ``%s`` y automáticamente *escapa* e inserta parámetros desde la lista
que se le provee como segundo argumento. Cuando construyas SQL en forma manual
hazlo *siempre* de esta manera.

Desafortunadamente, no puedes usar *parámetros asociados* en todas partes en
SQL; no son permitidos como identificadores (esto es, nombres de tablas o
columnas).  Así que, si, por ejemplo, necesitas construir dinámicamente una
lista de tablas a partir de una variable enviada mediante ``POST``, necesitarás
*escapar* ese nombre en tu código.  Django provee una función,
``django.db.backend.quote_name``, la cual *escapará* el identificador de acuerdo
al esquema de uso de comillas de la base de datos actual.

Cross-Site Scripting (XSS)
==========================

El *Cross-site scripting* (XSS) (Scripting inter-sitio), puede encontrarse en
aplicaciones Web que fallan a la hora de *escapar* en forma correcta
contenido provisto por el usuario antes de renderizarlo en HTML. Esto le
permite a un atacante insertar HTML arbitrario en tu página Web, usualmente en
la forma de etiquetas ``<script>``.

Los atacantes a menudo usan ataques XSS para robar información de cookies y
sesiones, o para engañar usuarios y lograr que proporcionen información
privada a la persona equivocada (también conocido como *phishing*).

Este tipo de ataque puede tomar diferentes formas y tiene prácticamente
infinitas permutaciones, así que sólo vamos a analizar un ejemplo típico.
Consideremos esta simple vista "Hola mundo"::

    def say_hello(request):
        name = request.GET.get('name', 'world')
        return render_to_response("hello.html", {"name" : name})

Esta vista simplemente lee un nombre desde un parámetro ``GET`` y pasa dicho
nombre a la plantilla ``hello.html``. Podríamos escribir una plantilla para esta
vista de la siguiente manera::

    <h1>Hello, {{ name }}!</h1>

De manera que si accediéramos a ``http://example.com/hello/?name=Jacob``, la
página renderizada contendría lo siguiente::

    <h1>Hello, Jacob!</h1>

Pero atención -- ¿qué sucede si accedemos a
``http://example.com/hello/?name=<i>Jacob</i>``? En ese caso obtenemos esto::

    <h1>Hello, <i>Jacob</i>!</h1>

Obviamente, un atacante no usará algo tan inofensivo como etiquetas ``<i>``;
podría incluir un fragmento completo de HTML que se apropiara de tu página
insertando contenido arbitrario. Este tipo de ataques ha sido usado para
engañar a usuarios e inducirlos a introducir datos en lo que parece ser el
sitio Web de su banco, pero en efecto es un formulario saboteado vía XSS que
envía su información bancaria a un atacante.

El problema se complica aun más si almacenas estos datos en la base de datos y
luego la visualizas en tu sitio. Por ejemplo, en una oportunidad se encontró que
MySpace era vulnerable a un ataque XSS de esta naturaleza. Un usuario había
insertado JavaScript en su página de perfil, dicho código agregana lo agregaba a
la lista de amigos de todos los usuarios que visitaran su página de perfil. En
unos pocos días llegó a tener millones de amigos.

Ahora, esto podría sonar relativamente inofensivo, pero no olvides que este
atacante había logrado que *su*  código -- no el código de MySpace -- se
ejecutara en *tu* computadora. Esto viola la confianza asumida acerca de que
todo el código ubicado en MySpace es realmente escrito por MySpace.

MySpace fue muy afortunado de que este código malicioso no hiciera cosas como
borrar automáticamente las cuentas de los usuarios que lo ejecutaran, o cambiar
sus contraseñas, o inundar el sitio con spam, o cualquiera de los otros
escenarios de pesadilla que esta vulnerabilidad hace posibles.

La solución
-----------

La solución es simple: *siempre* *escapa* *todo* el contenido que pudiera haber
sido enviado por un usuario. Si simplemente reescribiéramos nuestra plantilla de
la siguiente manera::

    <h1>Hello, {{ name|escape }}!</h1>

ya no seríamos vulnerables. Debes usar *siempre* la etiqueta ``escape`` (o algo
equivalente) cuando visualizas en tu sitio contenido enviado por el usuario.

.. admonition:: ¿Porqué simplemente Django no hace esto por mí?

    Modificar Django para que *escape* automáticamente todas las variables
    visualizadas en plantillas es un tópico de frecuente tratamiento en la lista
    de correo de desarrollo de Django.

    Hasta ahora, las plantillas Django han evitado este comportamiento debido a
    que esto cambia sutilmente algo que debería ser un comportamiento no
    complejo (la visualización de variables). Es un asunto no trivial y una
    decisión de compromiso difícil de evaluar. Agregando comportamiento
    implícito y oculto va contra los ideales de base de Django (y los de
    Python), pero la seguridad es igual de importante.

    Todo esto nos lleva, entonces, a afirmar que es muy probable que Django
    incorpore alguna forma de comportamiento de *auto-escaping* (o algo cercano
    a *auto-escaping*) en el futuro. Es una buena idea revisar la documentación
    oficial de Django para conocer las novedades respecto a las características
    de Django; esta será siempre más actual que este libro, especialmente que la
    versión impresa.

    Aun si Django incorpora esta característica *debes* formar el hábito de
    preguntarte, en todo momento, "¿De donde provienen estos datos?". Ninguna
    solución automática protegerá tu sitio de ataques XSS el 100% del tiempo.

Cross-Site Request Forgery
==========================

La Cross-site request forgery (CSRF) (Falsificación de peticiones inter-sitio)
sucede cuando un sitio Web malicioso engaña a los usuarios y los induce a
visitar una URL desde un sitio ante el cual ya se han autenticado -- por lo
tanto saca provecho de su condición de usuario ya autenticado.

Django incluye herramientas para proteger ante este tipo de ataques. Tanto el
ataque en sí mismo como dichas herramientas son tratados con gran detalle en
el :doc:`Capítulo 14<chapter14>`.

.. _Capítulo 14: ../chapter14/

Session Forging/Hijacking
=========================

No se trata de un ataque específico, sino una clase general de ataques sobre
los datos de sesión de un usuario. Puede tomar diferentes formas:

* Un ataque del tipo *man-in-the-middle*, en el cual un atacante espía datos
  de sesión mientras estos viajan por la red (cableada o inalámbrica).

* *Session forging* (Falsificación de sesión), en la cual un atacante usa un
  identificador de sesión (posiblemente obtenido mediante un ataque
  man-in-the-middle) para simular ser otro usuario.

  Un ejemplo de los dos primeros sería una atacante en una cafetería usando
  la red inalámbrica del lugar para capturar una cookie de sesión. Podría
  usar esa cookie para hacerse pasar por el usuario original.

* Un ataque de falsificación de cookies en el cual un atacante
  sobrescribe los datos almacenados en una cookie que en teoría no son
  modificables. El :doc:`Capítulo 12<chapter12>` explica en detalle cómo funcionan las
  cookies, y uno de los puntos salientes es que es trivial para los
  navegadores y usuarios maliciosos el cambiar las cookies sin tu
  conocimiento.

  Existe una larga historia de sitios Web que han almacenado una cookie del
  tipo ``IsLoggedIn=1`` o aun ``LoggedInAsUser=jacob``. Es trivialmente
  simple sacar provecho de ese tipo de cookies.

  En un nivel aun más sutil, nunca será una buena idea confiar en
  nada que se almacene en cookies; nunca sabes quién puede haber estado
  manoseando las mismas.
 
  * *Session fixation* (fijación de sesión), en la cual un atacante engaña a
  un usuario y logra asignar un nuevo valor o limpiar el valor existente del
  identificador de su sesión.

  Por ejemplo, PHP permite que los identificadores de sesión se pasen en la
  URL (por ejemplo, ``http://example.com/?PHPSESSID=fa90197ca25f6ab40bb1374c510d7a32``).
  Un atacante que logre engañar a un usuario para que haga click en un link
  que posea un identificador de sesión fijo causará que ese usuario comience
  a usar esa sesión.

  La fijación de sesión se ha usado en ataques de *phishing* para engañar a
  usuarios e inducirlos a ingresar información personal en una cuenta que
  está bajo el control de atacante. Este puede luego conectarse al sitio con
  dicho usuario y obtener datos.

  * *Session poisoning* (envenenamiento de sesión), en el cual in atacante
  inyecta datos potencialmente peligrosos en la sesión de un usuario --
  usualmente a través de un formulario que el usuario envía con datos de su
  sesión.

  Un ejemplo canónico es un sitio que almacena un valor de preferencia
  simple (como el color de fondo de una página) en una cookie. Un atacante
  podría engañar a un usuario e inducirlo a hacer click en un link que envía
  un "color" que en realidad contiene un ataque XSS; si dicho color no está
  siendo *escapado*, el usuario podría insertar nuevamente código malicioso
  en el entorno del usuario.

.. _Capítulo 12: ../chapter12/

La solución
-----------

Existe un número de principios generales que pueden protegerte de estos
ataques:

* Nunca permitas que exista información sobre sesiones contenida en las URLs.

  El framework de sesiones de Django (ver `Capítulo 12`_) simplemente no
  permite que las URLs contengan sesiones.

* No almacenes datos en cookies en forma directa; en cambio, almacena un
  identificador de sesión que esté relacionado a datos de sesión almacenados
  en el back-end.

  Si usas el framework de sesiones incluido en Django (o sea
  ``request.session``), eso es manejado en forma automática. La única cookie
  que usa el framework de sesiones es un identificador de sesión; todos los
  datos de la sesiones se almacenan en la base de datos.

* Recuerda *escapar* los datos de la sesión si los visualizas en la
  plantilla.  Revisa la sección previa sobre XSS y recuerda que esto se
  aplica a cualquier contenido creado por el usuario así como a cualquier
  dato enviado por el navegador. Debes considerar la información de sesiones
  como datos creados por el usuario.

* Previene la falsificación de de identificadores de sesión por parte de un
  atacante siempre que sea posible.

  A pesar de que es prácticamente imposible detectar a alguien que se ha
  apropiado de un identificador de sesión, Django incluye protección contra
  un ataque de sesiones de fuerza bruta. Los identificadores de sesión se
  almacenan como hashes (en vez de números secuenciales) lo que previene un
  ataque por fuerza bruta, y un usuario siempre obtendrá un nuevo
  identificador de sesión si intenta usar uno no existente, lo que previene
  la *session fixation*.

Nota que ninguno de estos principios y herramientas previene ante ataques
man-in-the-middle. Dichos tipos de ataques son prácticamente imposibles de
detectar. Si tu sitio permite que usuarios identificados visualicen algún tipo
de datos importantes debes, *siempre*, publicar dicho sitio vía HTTPS.
Adicionalmente, si tienes un sitio con SSL, debes asignar a la variable de
configuración ``SESSION_COOKIE_SECURE`` el valor ``True``; esto hará que Django
envíe las cookies de sesión vía HTTPS.

Inyección de cabeceras de email
===============================

La hermana menos conocida de la inyección de SQL, la *inyección de cabeceras de
email*, toma control de formularios Web que envían emails. Un atacante puede
usar esta técnica para enviar spam mediante tu servidor de email. Cualquier
formulario que construya cabeceras de email a partir de datos de un formulario
Web es vulnerable a este tipo de ataque.

Analicemos el formulario de contacto canónico que puede encontrarse en muchos
sitios. Usualmente el mismo envía un mensaje a una dirección de email fija y,
por lo tanto, a primera vista no parece ser vulnerable a abusos de spam.

Sin embargo, muchos de esos formularios permiten también que los usuarios
escriban su propio asunto para el email (en conjunto con una dirección "de", el
cuerpo del mensaje y a veces algunos otros campos). Este campo asunto es usado
para construir la cabecera "subject" del mensaje de email.

Si dicha cabecera no es *escapada* cuando se construye el mensaje de email, un
atacante podría enviar algo como ``"hello\ncc:spamvictim@example.com"`` (donde
``"\n"`` es un caracter de salto de línea). Eso haría que las cabeceras de email
fueran::

    To: hardcoded@example.com
    Subject: hello
    cc: spamvictim@example.com

Como en la inyección de SQL, si confiamos en la línea de asunto enviada por el
usuario, estaremos permitiéndole construir un conjunto malicioso de cabeceras, y
podrá usar nuestro formulario de contacto para enviar spam.

La solución
-----------

Podemos prevenir este ataque de la misma manera en la que prevenimos la inyección
de SQL: *escapando* o verificando siempre el contenido enviado por el usuario.

Las funciones de mail incluidas en Django (en ``django.core.mail``) simplemente
no permiten saltos de línea en ninguno de los campos usados para construir
cabeceras (las direcciones de y para, más el asunto). Si intentas usar
``django.core.mail.send_mail`` con un asunto que contenga saltos de línea,
Django arrojará una excepción ``BadHeaderError``.

Si no usas las funciones de email de Django para enviar email, necesitarás
asegurarte de que los saltos de línea en las cabeceras o causan un error o son
eliminados. Podrías querer examinar la clase ``SafeMIMEText`` en
``django.core.mail`` para ver cómo implementa esto Django.

Directory Traversal
===================

*Directory traversal* se trata de otro ataque del tipo inyección, en el cual un
usuario malicioso subvierte código de manejo de sistema de archivos para que
lea y/o escriba archivos a los cuales el servidor Web no debería tener acceso.

Un ejemplo podría ser una vista que lee archivos desde disco sin limpiar
cuidadosamente el nombre de archivo::

    def dump_file(request):
        filename = request.GET["filename"]
        filename = os.path.join(BASE_PATH, filename)
        content = open(filename).read()

        # ...

A pesar que parece que la vista restringe el acceso a archivos que se encuentren
más allá que ``BASE_PATH`` (usando ``os.path.join``), si la atacante envía un
``filename`` que contenga ``..`` (esto es, dos puntos, una notación corta para
"el directorio padre"), podría acceder a archivos que se encuentren "más
arriba" que ``BASE_PATH``. De allí en más es sólo una cuestión de tiempo el hecho
que descubra el número correcto de puntos para acceder exitosamente, por ejemplo
a ``../../../../../etc/passwd``.

Todo aquello que lea archivos sin el *escaping* adecuado es vulnerable a este
problema. Las vistas que *escriben* archivos son igual de vulnerables, pero las
consecuencias son doblemente calamitosas.

Otra permutación de este problema yace en código que carga módulos dinámicamente
a partir de la URL u otra información de la petición. Un muy público ejemplo se
presentó en el mundo de Ruby on Rails. Con anterioridad a mediados del 2006,
Rails usaba URLs como ``http://example.com/person/poke/1`` directamente para
cargar módulos e invocar métodos. El resultado fué que una URL cuidadosamente
construida podía cargar automáticamente código arbitrario, ¡incluso un script de
reset de base de datos!

La solución
-----------

Si tu código necesita alguna vez leer o escribir archivos a partir de datos
ingresados por el usuario, necesitas limpiar muy cuidadosamente la ruta
solicitada para asegurarte que un atacante no pueda escapar del directorio base
más allá del cual estás restringiendo el acceso.

.. admonition:: Nota:

    *¡Nunca* debes escribir código que pueda leer
    cualquier área del disco!

Un buen ejemplo de cómo hacer este *escaping* yace en la vista de publicación de
contenido estáticos (en ``django.view.static``). Este es el código relevante:

.. code-block:: python

    import os
    import posixpath

    # ...

    path = posixpath.normpath(urllib.unquote(path))
    newpath = ''
    for part in path.split('/'):
        if not part:
            # strip empty path components
            continue

        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # strip '.' and '..' in path
            continue

        newpath = os.path.join(newpath, part).replace('\\', '/')

Django no lee archivos (a menos que uses la función ``static.serve``, pero
en ese caso está protegida por el código recién mostrado), así que esta
vulnerabilidad no afecta demasiado el código del núcleo.

Adicionalmente, el uso de la abstracción de URLconf significa que Django *solo*
cargará código que le hayas indicado explícitamente que cargue. No existe
manera de crear una URL que cause que Django cargue algo no mencionado en una
URLconf.

Exposición de mensajes de error
===============================

Mientras se desarrolla, tener la posibilidad de ver tracebacks y errores en vivo
en tu navegador es extremadamente útil. Django posee mensajes de depuración
"vistosos" e informativos específicamente para hacer la tarea de depuración más
fácil.

Sin embargo, si esos errores son visualizados una vez que el sitio pasa a
producción, pueden revelar aspectos de tu código o configuración que podrían
ser de utilidad a un atacante.

Es más, los errores y tracebacks no son para nada útiles para los usuarios
finales. La filosofía de Django es que los visitantes al sitio nunca deben ver
mensajes de error relacionados a una aplicación. Si tu código genera una
excepción no tratada, un visitante al sitio no debería ver un traceback
completo -- ni *ninguna* pista de fragmentos de código o mensajes de error
(destinados a programadores) de Python. En cambio, el visitante debería ver un
amistoso mensaje "Esta página no está disponible".

Naturalmente, por supuesto, los desarrolladores necesitan ver tracebacks para
depurar problemas en su código. Así que el framework debería ocultar todos los
mensajes de error al público pero debería mostrarlos a los desarrolladores del
sitio.

La solución
-----------

Django tiene un sencillo control que gobierna la visualización de esos mensajes
de error. Si se fija la variable de configuración ``DEBUG`` al valor ``True``,
los mensajes de error serán visualizados en el navegador. De otra forma, Django
retornará un mensaje HTTP 500 ("Error interno del servidor") y renderizará una
plantilla de error provista por ti. Esta plantilla de error tiene el nombre
``500.html`` y debe estar situada en la raíz de uno de tus directorios de
plantillas.

Dado que los desarrolladores aun necesitan ver los errores que se generan en un
sitio en producción, todos los errores que se manejen de esta manera dispararán
el envío de un email con el traceback completo a las direcciones de correo
configuradas en la variable ``ADMINS``.

Los usuarios que implementen en conjunto con Apache y mod_python deben también
asegurarse que tienen ``PythonDebug Off`` en sus archivos de configuración de
Apache; esto suprimirá cualquier error que pudiera ocurrir aun antes de que
Django se haya cargado.

Palabras finales sobre la seguridad
===================================

Esperamos que toda esta exposición sobre problemas de seguridad no sea
demasiado intimidante. Es cierto que la Web puede ser un mundo salvaje y
confuso, pero con un poco de previsión puedes tener un sitio Web seguro.

Ten en mente que la seguridad Web es un campo en constante cambio; si estás
leyendo la versión en papel de este libro, asegúrate de consultar recursos sobre
seguridad más actuales en búsqueda de nuevas vulnerabilidades que pudieran
haber sido descubiertas. En efecto, siempre es una buena idea dedicar algún
tiempo semanalmente o mensualmente a investigar y mantenerse actualizado acerca
del estado de la seguridad de aplicaciones Web. Es una pequeña inversión a
realizar, pero la protección que obtendrás para ti y tus usuarios no tiene
precio.

¿Qué sigue?
===========

En el :doc:`próximo capítulo<chapter20>`, finalmente trataremos las sutilezas de la
implementación de Django: como lanzar un sitio de producción y como dotarlo de
escalabilidad.

