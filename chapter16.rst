====================================================================
Capítulo 16: Integración con Base de datos y Aplicaciones existentes
====================================================================

Django es el más adecuado para el desarrollo denominado de campo verde -- es
decir, comenzar proyectos desde cero, como si estuviéramos construyendo un
edificio en un campo de verde pasto fresco. Pero a pesar de que Django favorece
a los proyectos iniciados desde cero, es posible integrar el framework con bases
de datos y aplicaciones existentes [#]_. Este capítulo explica algunas de las
estrategias de integración.

Integración con una base de datos existente
===========================================

La capa de base de datos de Django genera esquemas SQL desde código Python --
pero con una base de datos existente, tú ya tienes los esquemas SQL. En tal
caso, necesitas crear modelos para tus tablas de la base de datos existente.
Para este propósito, Django incluye una herramienta que puede generar el código
del modelo leyendo el diseño de las tablas de la base de datos. Esta herramienta
se llama ``inspectdb``, y puedes llamarla ejecutando el comando ``manage.py
inspectdb``.

Empleo de ``inspectdb``
-----------------------

La utilidad ``inspectdb`` realiza una introspección de la base de datos a la que
apunta tu archivo de configuración, determina una representación del modelo que
usará Django para cada una de tus tablas, e imprime el código Python del modelo
a la salida estándar.

Esta es una guía de un proceso típico de integración con una base de datos
existente desde cero. Las únicas suposiciones son que Django esta instalado y
tienes una base de datos existente.

1. Crea un proyecto Django ejecutando ``django-admin.py startproject
   mysite`` (donde ``mysite`` es el nombre de tu proyecto). Usaremos
   ``mysite`` como nombre de proyecto en este ejemplo.

2. Edita el archivo de configuración en ese proyecto,
   ``mysite/settings.py``, para decirle a Django cuáles son los parámetros
   de conexión a tu base de datos y cuál es su nombre. Específicamente,
   provee las configuraciones de ``DATABASE_NAME``, ``DATABASE_ENGINE``,
   ``DATABASE_USER``, ``DATABASE_PASSWORD``, ``DATABASE_HOST``, y
   ``DATABASE_PORT``.  (Ten en cuenta que algunas de estas configuraciones
   son opcionales. Mira el :doc:`Capítulo 5<chapter05>` para más información).

3. Crea una aplicación dentro de tu proyecto ejecutando ``python
   mysite/manage.py startapp myapp`` (donde ``myapp`` es el nombre de tu
   aplicación). Usaremos ``myapp`` como el nombre de aplicación aquí.

4. Ejecuta el comando ``python mysite/manage.py inspectdb``. Esto examinará
   las tablas en la base de datos ``DATABASE_NAME`` e imprimirá para cada
   tabla el modelo de clase generado. Hecha una mirada a la salida para
   tener una idea de lo que puede hacer ``inspectdb``.

5. Guarda la salida en el archivo ``models.py`` dentro de tu aplicación
   usando la redirección de salida estándar de la shell::

   python mysite/manage.py inspectdb > mysite/myapp/models.py

6. Edita el archivo ``mysite/myapp/models.py`` para limpiar los modelos
   generados y realiza cualquier personalización necesaria. Te daremos
   algunas sugerencias para esto en la siguiente sección.

Limpiar los modelos generados
-----------------------------

Como podrías esperar, la introspección de la base de datos no es perfecta, y
necesitarás hacer una pequeña limpieza al código del modelo resultante. Aquí hay
algunos apuntes para lidiar con los modelos generados:

1. Cada tabla de la base de datos es convertida en una clase del modelo (es
   decir, hay un mapeo de uno-a-uno entre las tablas de la base de datos y
   las clases del modelo). Esto significa que tendrás que refactorizar los
   modelos para tablas con relaciones muchos-a-muchos en objetos
   ``ManyToManyField``.

2. Cada modelo generado tiene un atributo para cada campo, incluyendo campos
   de clave primaria ``id``. Sin embargo, recuerda que Django agrega
   automáticamente un campo de clave primaria ``id`` si un modelo no tiene
   una clave primaria. Por lo tanto, querrás remover cualquier línea que se
   parezca a ésta::

       id = models.IntegerField(primary_key=True)

   No solo estas líneas son redundantes, sino que pueden causar problemas si
   tu aplicación agregara *nuevos* registros a estas tablas. El comando
   ``inspectdb`` no puede detectar si un campo es autoincrementado, así que
   está en tí cambiar esto a ``AutoField``, si es necesario.

3. Cada tipo de campo (ej., ``CharField``, ``DateField``) es determinado
   mirando el tipo de la columna de la base de datos (ej., ``VARCHAR``,
   ``DATE``). Si ``inspectdb`` no puede mapear un tipo de columna a un tipo
   de campo del modelo, usará ``TextField`` e insertará el comentario Python
   ``'This field type is a guess.'`` a continuación del campo en el modelo
   generado. Mantén un ojo en eso, y cambia el tipo de campo adecuadamente
   si es necesario.

   Si un campo en tu base de datos no tiene un buen equivalente en Django,
   con seguridad puedes dejarlo fuera. La capa de modelo de Django no
   requiere que incluyas todos los campos de tu(s) tabla(s).

4. Si un nombre de columna de tu base de datos es una palabra reservada de
   Python (como ``pass``, ``class`` o ``for``), ``inspectdb`` agregará
   ``'_field'`` al nombre del atributo y establecerá el atributo
   ``db_column`` al nombre real del campo (ej., ``pass``, ``class``, o
   ``for``).

   Por ejemplo, si una tabla tiene una columna ``INT`` llamada ``for``, el
   modelo generado tendrá un campo como este::

      for_field = models.IntegerField(db_column='for')

   ``inspectdb`` insertará el comentario Python ``'Field renamed because it
   was a Python reserved word.'`` a continuación del campo.

5. Si tu base de datos contiene tablas que hacen referencia a otras tablas
   (como la mayoría de las bases de datos lo hacen), tal vez tengas que
   re-acomodar el orden de los modelos generados, de manera que los modelos
   que hacen referencia a otros modelos estén ordenados apropiadamente. Por
   ejemplo, si un modelo ``Book`` tiene una ``ForeignKey`` al modelo
   ``Author``, el modelo ``Author`` debe ser definido antes del modelo
   ``Book``. Si necesitas crear una relación en un modelo que todavía no
   esta definido, puedes usar el nombre del modelo, en vez del objeto modelo
   en sí.
   
6. ``inspectdb`` detecta claves primarias para PostgreSQL, MySQL y SQLite.
   Es decir, inserta ``primary_key=True`` donde sea necesario. Para otras
   bases de datos, necesitarás insertar ``primary_key=True`` para al menos
   un campo en cada modelo, ya que los modelos Django requieren tener un
   campo ``primary_key=True``.

7. La detección de claves foráneas sólo funciona con PostgreSQL y con
   ciertos tipos de tablas MySQL. En otros casos, los campos de clave
   foránea serán generados como campos ``IntegerField``, asumiendo que la
   columna de clave foránea fue una columna ``INT``.

Integración con un sistema de autentificación
=============================================

Es posible integrar Django con un sistema de autentificación existente -- otra
fuente de nombres de usuario y contraseñas o métodos de autentificación.

Por ejemplo, tu compañía ya puede tener una configuración LDAP que almacena un
nombre de usuario y contraseña para cada empleado. Sería una molestia tanto para
el administrador de red como para los usuarios, si cada uno de ellos tiene
cuentas separadas en LDAP y en las aplicaciones basadas en Django.

Para manejar situaciones como ésta, el sistema de autentificación de Django te
permite conectarte con otras fuentes de autentificación. Puedes anular el
esquema por omisión de Django basado en base de datos, o puedes usar el sistema
por omisión en conjunto con otros sistemas.

Especificar los back-ends de autentificación
--------------------------------------------

Detrás de escena, Django mantiene una lista de "back-ends de autentificación"
que utiliza para autentificar. Cuando alguien llama a
``django.contrib.auth.authenticate()`` (como se describió en el :doc:`Capítulo 12<chapter12>`),
Django intenta autentificar usando todos sus back-ends de autentificación. Si el
primer método de autentificación falla, Django intenta con el segundo, y así
sucesivamente, hasta que todos los back-ends han sido intentados.

La lista de back-ends de autentificación a usar se especifica en la
configuración ``AUTHENTICATION_BACKENDS``. Ésta debe ser una tupla de nombres de
ruta Python  que apuntan a clases que saben cómo autentificar. Estas clases
pueden estar en cualquier lugar de tu ruta Python [#]_.

Por omisión, ``AUTHENTICATION_BACKENDS`` contiene lo siguiente::

    ('django.contrib.auth.backends.ModelBackend',)

Ese es el esquema básico de autentificación que verifica la base de datos de
usuarios de Django.

El orden de ``AUTHENTICATION_BACKENDS`` se tiene en cuenta, por lo que si el
mismo usuario y contraseña son válidos en múltiples back-ends, Django detendrá
el procesamiento en la primera coincidencia positiva.

Escribir un back-end de autentificación
---------------------------------------

Un back-end de autentificación es un clase que implementa dos métodos:
``get_user(id)`` y ``authenticate(**credentials)``.

El método ``get_user`` recibe un ``id`` -- el cual podría ser un nombre de
usuario, un ID de la base de datos o cualquier cosa -- y devuelve un objeto
``User``.

El método ``authenticate`` recibe credenciales como argumentos de palabras
clave. La mayoría de las veces se parece a esto:

.. code-block:: python 

    class MyBackend(object):
        def authenticate(self, username=None, password=None):
            # Check the username/password and return a User.

Pero podría tambien autentificar un *token*, como se muestra a continuación:

.. code-block:: python 

    class MyBackend(object):
        def authenticate(self, token=None):
            # Check the token and return a User.

De cualquier manera, ``authenticate`` debe verificar las credenciales que
recibe, y debe retornar un objeto ``User`` que coincide con esas credenciales,
si las credenciales son válidas. Si no son válidas, debe retornar ``None``.

El sistema de administración de Django esta altamente acoplado a su propio
objeto ``User`` respaldado por base de datos descripto en el :doc:`Capítulo 12<chapter12>`. La
mejor manera de lidiar con esto es crear un objeto ``User`` de Django para cada
usuario que existe en tu back-end (ej., en tu directorio LDAP, tu base de datos
SQL externa, etc.). De cualquier manera puedes escribir un script para hacer
esto por adelantado o tu método de autentificación puede hacerlo la primera vez
que el usuario ingresa al sistema.

Aquí está un ejemplo de back-end que autentifica contra unas variables de
usuario y contraseña definidas en tu archivo ``settings.py`` y crea un objeto
``User`` de Django la primera vez que un usuario se autentifica::

    from django.conf import settings
    from django.contrib.auth.models import User, check_password

    class SettingsBackend(object):
        """
        Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

        Use the login name, and a hash of the password. For example:

        ADMIN_LOGIN = 'admin'
        ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
        """
        def authenticate(self, username=None, password=None):
            login_valid = (settings.ADMIN_LOGIN == username)
            pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
            if login_valid and pwd_valid:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    # Create a new user. Note that we can set password
                    # to anything, because it won't be checked; the password
                    # from settings.py will.
                    user = User(username=username, password='get from settings.py')
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                return user
            return None

        def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None

Integración con aplicaciones web existentes
===========================================

Es posible ejecutar una aplicación Django en el mismo servidor de una aplicación
impulsada por otra tecnología. La manera más directa de hacer esto es usar el
archivo de configuración de Apache, ``httpd.conf``, para delegar patrones de URL
diferentes a distintas tecnologías (Nota que el :doc:`Capítulo 20<chapter20>` cubre el despliegue
con Django en Apache/mod_python, por lo tanto tal vez valga la pena leer ese
capítulo primero antes de intentar esta integración).

La clave está en que Django será activado para un patrón particular de URL sólo
si tu archivo ``httpd.conf`` lo dice. El despliegue por omisión explicado en el
:doc:`Capítulo 20<chapter20>` ,asume que quieres que Django impulse
todas las páginas en un dominio particular:

.. code-block:: html

    <Location "/">
        SetHandler python-program
        PythonHandler django.core.handlers.modpython
        SetEnv DJANGO_SETTINGS_MODULE mysite.settings
        PythonDebug On
    </Location>

Aquí, la línea ``<Location "/">`` significa "maneja cada URL, comenzando en la
raíz", con Django.

Esta perfectamente bien limitar esta directiva ``<Location>`` a cierto árbol de
directorio. Por ejemplo, digamos que tienes una aplicación PHP existente que
impulsa la mayoría de las páginas en un dominio y quieres instalar el sitio de
administración de Django en ``/admin/`` sin afectar el código PHP. Para hacer
esto, sólo configura la directiva ``<Location>`` a ``/admin/``:

.. code-block:: html

    <Location "/admin/">
        SetHandler python-program
        PythonHandler django.core.handlers.modpython
        SetEnv DJANGO_SETTINGS_MODULE mysite.settings
        PythonDebug On
    </Location>

Con esto en su lugar, sólo las URLs que comiencen con ``/admin/`` activarán
Django. Cualquier otra página usará cualquier infraestructura que ya exista.

Nota que adjuntar Django a una URL calificada (como ``/admin/`` en el ejemplo de
esta sección) no afecta a Django en el análisis de las URLs. Django trabaja con
la URL absoluta (ej., ``/admin/people/person/add/``), no con una versión
"recortada" de la URL (ej., ``/people/person/add/``). Esto significa que tu
URLconf raíz debe incluir el prefijo ``/admin/``.

¿Qué sigue?
===========

Hablando del sitio de administración de Django y sobre cómo acomodar el
framework para encajar con necesidades existentes, otra tarea común es
personalizar el sitio de administración de Django. 
El :doc:`próximo capítulo<chapter17>` se enfoca en dicha personalización.



.. [#] \N. del T.: del inglés "legacy databases and applications", 
       aplicaciones y base de datos que ya están en uso en entornos
       de producción.
.. [#] \N. del T.: del inglés "Python path".


