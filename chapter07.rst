========================================
Capítulo 7: Procesamiento de formularios
========================================

**Autor invitado: Simon Willison**

Si has estado siguiendo el capítulo anterior, ya deberías tener un
sitio completamente funcional, aunque un poco simple. En este capítulo
trataremos con la próxima pieza del juego: cómo construir vistas que
obtienen entradas desde los usuarios.

Comenzaremos haciendo un simple formulario de búsqueda "a mano",
viendo cómo manejar los datos suministrados al navegador. Y a partir
de ahí, pasaremos al uso del *framework* de formularios que trae
Django.

Búsquedas
=========

En la Web todo se trata de búsquedas. Dos de los casos de éxito más
grandes, Google y Yahoo, han construido sus empresas multimillonarias
alrededor de las búsquedas. Casi todos los sitios observan un gran
porcentaje de tráfico viniendo desde y hacia sus páginas de
búsqueda. A menudo, la diferencia entre el éxito y el fracaso de un
sitio, lo determina la calidad de su búsqueda. Así que sería mejor que
agreguemos un poco de búsqueda a nuestro pequeño sitio de libros, ¿no?

Comenzaremos agregando la vista para la búsqueda a nuestro URLconf
(``mysite.urls``). Recuerda que esto se hace agregando algo como
``(r'^search/$', 'mysite.books.views.search')`` al conjunto de URL patterns
(patrones).

A continuación, escribiremos la vista ``search`` en nuestro módulo de vistas
(``mysite.books.views``)::

    from django.db.models import Q
    from django.shortcuts import render_to_response
    from models import Book

    def search(request):
        query = request.GET.get('q', '')
        if query:
            qset = (
                Q(title__icontains=query) |
                Q(authors__first_name__icontains=query) |
                Q(authors__last_name__icontains=query)
            )
            results = Book.objects.filter(qset).distinct()
        else:
            results = []
        return render_to_response("books/search.html", {
            "results": results,
            "query": query
        })

Aquí han surgido algunas cosas que todavía no hemos vimos. La primera, ese
``request.GET``. Así es cómo accedes a los datos del GET desde Django;
Los datos del POST se acceden de manera similar, a través de un objeto
llamado ``request.POST``. Estos objetos se comportan exactamente como
los diccionarios estándar de Python, y tienen además otras
capacidades, que se cubren en el :doc:`apéndice H<appendixH>`.

.. admonition:: ¿Qué son estos datos del GET y del POST?

    GET y POST son los dos métodos que emplean los navegadores para
    enviar datos a un servidor. Los encontrarás con frecuencia en los
    elementos *form* de HTML::

        <form action="/books/search/" method="get">

    Esto le indica al navegador que suministre los datos del
    formulario a la URL ``/books/search/`` empleando el método GET.

    Hay diferencias de semántica importantes entre el GET y el POST,
    que no vamos a ver ahora mismo, pero diríjete a
    http://www.w3.org/2001/tag/doc/whenToUseGet.html si quieres
    aprender más.

Así que la línea::

    query = request.GET.get('q', '')

busca un parámetro del GET llamado ``q`` y retorna una cadena de texto
vacía si este parámetro no fue suministrado. Observa que estamos
usando el método ``get()`` de ``request.GET``, algo potencialmente
confuso. Este método ``get()`` es el mismo que posee cualquier
diccionario de Python. Lo estamos usando aquí para ser precavidos:
*no* es seguro asumir que ``request.GET`` tiene una clave ``'q'``, así
que usamos ``get('q', '')`` para proporcionar un valor por omisión,
que es ``''`` (el string vacío). Si hubiéramos intentado acceder a la
variable simplemente usando ``request.GET['q']``, y ``q`` no hubiese
estado disponible en los datos del GET, se habría lanzado un
``KeyError``.

Segundo, ¿qué es ese ``Q``? Los objetos ``Q`` se utilizan para ir
construyendo consultas complejas -- en este caso, estamos buscando los
libros que coincidan en el título o en el nombre con la
consulta. Técnicamente, estos objetos ``Q`` consisten de un QuerySet,
y puede leer más sobre esto en el apéndice C.

En estas consultas, ``icontains`` es una búsqueda en la que no se
distinguen mayúsculas de minúsculas (*case-insensitive*), y que
internamente usa el operador ``LIKE`` de SQL en la base de datos.

Dado que estamos buscando en campos de muchos-a-muchos, es posible que
un libro se obtenga más de una vez (por ej: un libro que tiene dos
autores, y los nombres de ambos concuerdan con la consulta). Al
agregar ``.distinct()`` en el filtrado, se eliminan los resultados
duplicados.

Todavía no hay una plantilla para esta vista. Esto lo solucionará:

.. code-block:: html+django

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
    <html lang="en">
    <head>
        <title>Search{% if query %} Results{% endif %}</title>
    </head>
    <body>
      <h1>Search</h1>
      <form action="." method="GET">
        <label for="q">Search: </label>
        <input type="text" name="q" value="{{ query|escape }}">
        <input type="submit" value="Search">
      </form>
    
      {% if query %}
        <h2>Results for "{{ query|escape }}":</h2>
    
        {% if results %}
          <ul>
          {% for book in results %}
            <li>{{ book|escape }}</l1>
          {% endfor %}
          </ul>
        {% else %}
          <p>No books found</p>
        {% endif %}
      {% endif %}
    </body>
    </html>

A esta altura, lo que esto hace debería ser obvio. Sin embargo, hay
unas pocas sutilezas que vale la pena resaltar:

    * *action* es ``.`` en el formulario, esto significa "la URL
      actual". Esta es una buena práctica estándar: no utilices vistas
      distintas para la página que contiene el formulario y para la
      página con los resultados; usa una página única para las dos
      cosas.

    * Volvemos a insertar el texto de la consulta en el
      ``<input>``. Esto permite a los usuarios refinar fácilmente sus
      búsquedas sin tener que volver a teclear todo nuevamente.

    * En todo lugar que aparece ``query`` y ``book``, lo pasamos por
      el filtro ``escape`` para asegurarnos de que cualquier búsqueda
      potencialmente maliciosa sea descartada antes de que se inserte
      en la página

      ¡Es *vital* hacer esto con todo el contenido suministrado por el
      usuario! De otra forma el sitio se abre a ataques de cross-site
      scripting (XSS). El :doc:`Capítulo 19<chapter19>` discute XSS y la
      seguridad con  más detalle.

    * En cambio, no necesitamos preocuparnos por el contenido
      malicioso en las búsquedas de la base de datos -- podemos pasar
      directamente la consulta a la base de datos. Esto es posible
      gracias a que la capa de base de datos de Django se encarga de
      manejar este aspecto de la seguridad por ti.

Ahora ya tenemos la búsqueda funcionando. Se podría mejorar más el
sitio colocando el formulario de búsqueda en cada página (esto es, en
la plantilla base). Dejaremos esto de tarea para el hogar.

A continuación veremos un ejemplo más complejo. Pero antes de hacerlo,
discutamos un tópico más abstracto: el "formulario perfecto".

El "formulario perfecto"
========================

Los formularios pueden ser a menudo una causa importante de
frustración para los usuarios de tu sitio. Consideremos el
comportamiento de un hipotético formulario perfecto:

    * Debería pedirle al usuario cierta información, obviamente. La
      accesibilidad y la usabilidad importan aquí. Así que es
      importante el uso inteligente del elemento ``<label>`` de HTML,
      y también lo es proporcionar ayuda contextual útil.

    * Los datos suministrados deberían ser sometidos a una validación
      extensiva. La regla de oro para la seguridad de una aplicación
      web es *"nunca confíes en la información que ingresa"*. Así que la
      validación es esencial.

    * Si el usuario ha cometido algún error, el formulario debería
      volver a mostrarse, junto a los mensajes de error detallados e
      informativos. Los campos deberían rellenarse con los datos
      previamente suministrados, para evitarle al usuario tener que
      volver a tipear todo nuevamente.

    * El formulario debería volver a mostrarse una y otra vez, hasta
      que todos los campos se hayan rellenado correctamente.

¡Construir el formulario perfecto pareciera llevar mucho trabajo! Por
suerte, el *framework* de formularios de Django está diseñado para
hacer la mayor parte del trabajo por ti. Se le proporciona una
descripción de los campos del formulario, reglas de validación, y una
simple plantilla, y Django hace el resto. El resultado es un
"formulario perfecto" que requiere de muy poco esfuerzo.

Creación de un formulario para comentarios
==========================================

La mejor forma de construir un sitio que la gente ame es atendiendo a
sus comentarios. Muchos sitios parecen olvidar esto; ocultan los
detalles de su contacto en *FAQs*, y parecen dificultar lo más posible
el encuentro con las personas.

Cuando tu sitio tiene millones de usuarios, esto puede ser una
estrategia razonable. En cambio, cuando intentas formarte una
audiencia, deberías pedir comentarios cada vez que se presente la
oportunidad. Escribamos entonces un simple formulario para
comentarios, y usémoslo para ilustrar al *framework* de Django en
plena acción.

Comenzaremos agregando ``(r'^contact/$',
'mysite.books.views.contact')`` al URLconf, y luego definamos nuestro
formulario. Los formularios en Django se crean de una manera similar a
los modelos: declarativamente, empleando una clase de Python. He aquí
la clase para nuestro simple formulario. Por convención, lo
insertaremos en un nuevo archivo ``forms.py`` dentro del directorio de
nuestra aplicación::

    from django import newforms as forms

    TOPIC_CHOICES = (
        ('general', 'General enquiry'),
        ('bug', 'Bug report'),
        ('suggestion', 'Suggestion'),
    )

    class ContactForm(forms.Form):
        topic = forms.ChoiceField(choices=TOPIC_CHOICES)
        message = forms.CharField()
        sender = forms.EmailField(required=False)

.. admonition:: *¿"New" Forms?* ¿Qué?

    Cuando Django fue lanzado al público por primera vez, poseía un
    sistema de formularios complicado y confuso. Como hacía muy
    dificultosa la producción de formularios, fue rescrito y ahora se
    llama *"newforms"* (nuevos formularios). Sin embargo, como todavía
    hay cierta cantidad de código que depende del "viejo" sistema de
    formularios, Django actualmente viene con ambos paquetes.

    Al momento de escribir ese libro, el viejo sistema de formularios
    de Django sigue disponible como ``django.forms``, y el nuevo
    paquete como ``django.newforms``. En algún momento esto va a
    cambiar, y ``django.forms`` hará referencia al nuevo paquete de
    formularios. Sin embargo, para estar seguros de que los ejemplos
    de este libro funcionen lo más ampliamente posible, todos harán
    referencia a ``django.newforms``.

Un formulario de Django es una subclase de ``django.newforms.Form``,
tal como un modelo de Django es una subclase de
``django.db.models.Model``. El módulo ``django.newforms`` también
contiene cierta cantidad de clases ``Field`` para los campos. Una
lista completa de éstas últimas se encuentra disponible en la
documentación de Django, en
http://www.djangoproject.com/documentation/

Nuestro ``ContactForm`` consiste de tres campos: un tópico, que se
puede elegir entre tres opciones; un mensaje, que es un campo de
caracteres; y un emisor, que es un campo de correo electrónico y es
opcional (porque incluso los comentarios anónimos pueden ser
útiles). Hay una cantidad de otros tipos de campos disponibles, y
puedes escribir nuevos tipos si ninguno cubre tus necesidades.

El objeto formulario sabe cómo hacer una cantidad de cosas útiles por
sí mismo. Puede validar una colección de datos, puede generar sus
propios *"widgets"* de HTML, puede construir un conjunto de mensajes
de error útiles. Y si estás en perezoso, puede incluso dibujar el
formulario completo por ti. Incluyamos esto en una vista y veámoslo en
acción. En ``views.py``:

.. code-block:: python

    from django.db.models import Q
    from django.shortcuts import render_to_response
    from models import Book
    **from forms import ContactForm**

    def search(request):
        query = request.GET.get('q', '')
        if query:
            qset = (
                Q(title__icontains=query) |
                Q(authors__first_name__icontains=query) |
                Q(authors__last_name__icontains=query)
            )
            results = Book.objects.filter(qset).distinct()
        else:
            results = []
        return render_to_response("books/search.html", {
            "results": results,
            "query": query
        })

    **def contact(request):**
        **form = ContactForm()**
        **return render_to_response('contact.html', {'form': form})**

y en ``contact.html``::

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
    <html lang="en">
    <head>
        <title>Contact us</title>
    </head>
    <body>
        <h1>Contact us</h1>
        <form action="." method="POST">
            <table>
                {{ form.as_table }}
            </table>
            <p><input type="submit" value="Submit"></p>
        </form>
    </body>
    </html>

La línea más interesante aquí es ``{{ form.as_table }}``. ``form`` es
nuestra instancia de ContactForm, que fue pasada al
``render_to_response``. ``as_table`` es un método de ese objeto que
reproduce el formulario como una secuencia de renglones de una tabla
(también pueden usarse ``as_ul`` y ``as_p``). El HTML generado se ve
así::

    <tr>
        <th><label for="id_topic">Topic:</label></th>
        <td>
            <select name="topic" id="id_topic">
                <option value="general">General enquiry</option>
                <option value="bug">Bug report</option>
                <option value="suggestion">Suggestion</option>
            </select>
        </td>
    </tr>
    <tr>
        <th><label for="id_message">Message:</label></th>
        <td><input type="text" name="message" id="id_message" /></td>
    </tr>
    <tr>
        <th><label for="id_sender">Sender:</label></th>
        <td><input type="text" name="sender" id="id_sender" /></td>
    </tr>

Observa que las etiquetas ``<table>`` y ``<form>`` no se han incluido;
debes definirlas por tu cuenta en la plantilla. Esto te da control
sobre el comportamiento del formulario al ser suministrado. Los
elementos *label* sí se incluyen, y proveen a los formularios de
accesibilidad "desde fábrica".

Nuestro formulario actualmente utiliza un *widget* ``<input
type="text">`` para el campo del mensaje. Pero no queremos restringir
a nuestros usuarios a una sola línea de texto, así que la cambiaremos
por un *widget* ``<textarea>``:

.. code-block:: python

    class ContactForm(forms.Form):
        topic = forms.ChoiceField(choices=TOPIC_CHOICES)
        message = forms.CharField(**widget=forms.Textarea()**)
        sender = forms.EmailField(required=False)

El *framework* de formularios divide la lógica de presentación para
cada campo, en un conjunto de *widgets*. Cada tipo de campo tiene un
*widget* por defecto, pero puedes sobreescribirlo fácilmente, o
proporcionar uno nuevo de tu creación.

Por el momento, si se suministra el formulario, no sucede
nada. Agreguemos nuestras reglas de validación::

    def contact(request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
        else:
            form = ContactForm()
        return render_to_response('contact.html', {'form': form})

Una instancia de formulario puede estar en uno de dos estados: *bound*
(vinculado) o *unbound* (no vinculado). Una instancia *bound* se
construye con un diccionario (o un objeto que funcione como un
diccionario) y sabe cómo validar y volver a representar sus datos. Un
formulario *unbound* no tiene datos asociados y simplemente sabe cómo
representarse a sí mismo.

Intenta hacer clic en *Submit* en el formulario vacío. La página se
volverá a cargar, mostrando un error de validación que informa que
nuestro campo de mensaje es obligatorio.

Intenta también ingresar una dirección de correo electrónico
inválida. El ``EmailField`` sabe cómo validar estas direcciones, por
lo menos a un nivel razonable.

.. admonition:: Cómo especificar datos iniciales

    Al pasar datos directamente al constructor del formulario, estos
    se vinculan, y se indica que la validación debe ser efectuada. A
    menudo, necesitamos mostrar un formulario inicial con algunos
    campos previamente rellenados -- por ejemplo, en un formulario
    "editar". Podemos hacerlo con el argumento de palabras claves
    ``initial``::

        form = CommentForm(initial={'sender': 'user@example.com'})

    Si nuestro formulario *siempre* usará los mismos valores por
    defecto, podemos configurarlos en la definición misma del
    formulario:

    .. code-block:: python 

        message = forms.CharField(widget=forms.Textarea(),
                                  **initial="Replace with your feedback"**)

Procesamiento de los datos suministrados
========================================

Una vez que el usuario ha llenado el formulario al punto de que pasa
nuestras reglas de validación, necesitamos hacer algo útil con los
datos. En este caso, deseamos construir un correo electrónico que
contenga los comentarios del usuario, y enviarlo. Para esto, usaremos
el paquete de correo electrónico de Django.

Pero antes, necesitamos saber si los datos son en verdad válidos, y si
lo son, necesitamos una forma de accederlos. El *framework* de
formularios hace más que validar los datos, también los convierte a
tipos de datos de Python. Nuestro formulario para comentarios sólo
trata con texto, pero si estamos usando campos como ``IntegerField`` o
``DateTimeField``, el *framework* de formularios se encarga de que se
devuelvan como un valor entero de Python, o como un objeto
``datetime``, respectivamente.

Para saber si un formulario está vinculado (*bound*) a datos válidos,
llamamos al método ``is_valid()``::

    form = ContactForm(request.POST)
    if form.is_valid():
        # Process form data

Ahora necesitamos acceder a los datos. Podríamos sacarlos directamente
del ``request.POST``, pero si lo hiciéramos, no nos estaríamos
beneficiando de la conversión de tipos que realiza el *framework* de
formularios. En cambio, usamos ``form.clean_data``::

    if form.is_valid():
        topic = form.clean_data['topic']
        message = form.clean_data['message']
        sender = form.clean_data.get('sender', 'noreply@example.com')
        # ...

Observa que dado que ``sender`` no es obligatorio, proveemos un valor
por defecto por si no fue proporcionado. Finalmente, necesitamos
registrar los comentarios del usuario. La manera más fácil de hacerlo
es enviando un correo electrónico al administrador del sitio. Podemos
hacerlo empleando la función::

    from django.core.mail import send_mail

    # ...

    send_mail(
        'Feedback from your site, topic: %s' % topic,
        message, sender,
        ['administrator@example.com']
    )

La función ``send_mail`` tiene cuatro argumentos obligatorios: el
asunto y el cuerpo del mensaje, la dirección del emisor, y una lista
de direcciones destino. ``send_mail`` es un código conveniente que
envuelve a la clase ``EmailMessage`` de Django. Esta clase provee
características avanzadas como adjuntos, mensajes multiparte, y un
control completo sobre los encabezados del mensaje.

Una vez enviado el mensaje con los comentarios, redirigiremos a
nuestro usuario a una página estática de confirmación. La función de
la vista finalizada se ve así::

    from django.http import HttpResponseRedirect
    from django.shortcuts import render_to_response
    from django.core.mail import send_mail
    from forms import ContactForm

    def contact(request):
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                topic = form.clean_data['topic']
                message = form.clean_data['message']
                sender = form.clean_data.get('sender', 'noreply@example.com')
                send_mail(
                    'Feedback from your site, topic: %s' % topic,
                    message, sender,
                    ['administrator@example.com']
                )
                return HttpResponseRedirect('/contact/thanks/')
        else:
            form = ContactForm()
        return render_to_response('contact.html', {'form': form})

.. admonition:: Redirigir luego del POST

    Si un usuario selecciona actualizar sobre una página que muestra una
    consulta POST, la consulta se repetirá. Esto probablemente lleve a
    un comportamiento no deseado, por ejemplo, que el registro se
    agregue dos veces a la base de datos. Redirigir luego del POST es
    un patrón útil que puede ayudar a prevenir este escenario. Así que
    luego de que se haya procesado el POST con éxito, redirige al
    usuario a otra página en lugar de retornar HTML directamente.

Nuestras propias reglas de validación
=====================================

Imagina que hemos lanzado al público a nuestro formulario de
comentarios, y los correos electrónicos han empezado a llegar. Nos
encontramos con un problema: algunos mensajes vienen con sólo una o
dos palabras, es poco probable que tengan algo interesante. Decidimos
adoptar una nueva póliza de validación: cuatro palabras o más, por
favor.

Hay varias formas de insertar nuestras propias validaciones en un
formulario de Django. Si vamos a usar nuestra regla una y otra vez,
podemos crear un nuevo tipo de campo. Sin embargo, la mayoría de las
validaciones que agreguemos serán de un solo uso, y pueden agregarse
directamente a la clase del formulario.

En este caso, necesitamos validación adicional sobre el campo
``message``, así que debemos agregar un método ``clean_message`` a
nuestro formulario::

    class ContactForm(forms.Form):
        topic = forms.ChoiceField(choices=TOPIC_CHOICES)
        message = forms.CharField(widget=forms.Textarea())
        sender = forms.EmailField(required=False)

        def clean_message(self):
            message = self.clean_data.get('message', '')
            num_words = len(message.split())
            if num_words < 4:
                raise forms.ValidationError("Not enough words!")
            return message

Este nuevo método será llamado después del validador que tiene el
campo por defecto (en este caso, el validador de un ``CharField``
obligatorio). Dado que los datos del campo ya han sido procesados
parcialmente, necesitamos obtenerlos desde el diccionario
``clean_data`` del formulario.

Usamos una combinación de ``len()`` y ``split()`` para contar la
cantidad de palabras. Si el usuario ha ingresado muy pocas palabras,
lanzamos un error ``ValidationError``. El texto que lleva esta
excepción se mostrará al usuario como un elemento de la lista de
errores.

Es importante que retornemos explícitamente el valor del campo al
final del método. Esto nos permite modificar el valor (o convertirlo a
otro tipo de Python) dentro de nuestro método de validación. Si nos
olvidamos de retornarlo, se retornará ``None`` y el valor original
será perdido.

Una presentación personalizada
==============================

La forma más rápida de personalizar la presentación de un formulario
es mediante CSS. En particular, la lista de errores puede dotarse de
mejoras visuales, y el elemento ``<ul>`` tiene asignada la clase
``errorlist`` para ese propósito. El CSS a continuación hace que
nuestros errores salten a la vista::

    <style type="text/css">
        ul.errorlist {
            margin: 0;
            padding: 0;
        }
        .errorlist li {
            background-color: red;
            color: white;
            display: block;
            font-size: 10px;
            margin: 0 0 3px;
            padding: 4px 5px;
        }
    </style>

Si bien es conveniente que el HTML del formulario sea generado por
nosotros, en muchos casos la disposición por defecto no quedaría bien
en nuestra aplicación. ``{{ form.as_table }}`` y similares son atajos
útiles que podemos usar mientras desarrollamos nuestra aplicación,
pero todo lo que concierne a la forma en que nuestro formulario es
representado puede ser sobreescrito, casi siempre desde la plantilla
misma.

Cada *widget* de un campo (``<input type="text">``, ``<select>``,
``<textarea>``, o similares) puede generarse individualmente
accediendo a ``{{ form.fieldname }}``. Cualquier error asociado con un
campo está disponible como ``{{ form.fieldname.errors }}``.  Podemos
usar estas variables para construir nuestra propia plantilla para el
formulario::

    <form action="." method="POST">
        <div class="fieldWrapper">
            {{ form.topic.errors }}
            <label for="id_topic">Kind of feedback:</label>
            {{ form.topic }}
        </div>
        <div class="fieldWrapper">
            {{ form.message.errors }}
            <label for="id_message">Your message:</label>
            {{ form.message }}
        </div>
        <div class="fieldWrapper">
            {{ form.sender.errors }}
            <label for="id_sender">Your email (optional):</label>
            {{ form.sender }}
        </div>
        <p><input type="submit" value="Submit"></p>
    </form>

``{{ form.message.errors }}`` se muestra como un ``<ul
class="errorlist">`` si se presentan errores y como una cadena de
caracteres en blanco si el campo es válido ( o si el formulario no
está vinculado). También podemos tratar a la variable
``form.message.errors`` como a un booleano o incluso iterar sobre la
misma como en una lista, por ejemplo::

    <div class="fieldWrapper{% if form.message.errors %} errors{% endif %}">
        {% if form.message.errors %}
            <ol>
            {% for error in form.message.errors %}
                <li><strong>{{ error|escape }}</strong></li>
            {% endfor %}
            </ol>
        {% endif %}
        {{ form.message }}
    </div>

En caso de que hubieran errores de validación, se agrega la clase
"errors" al ``<div>`` contenedor y se muestran los errores en una
lista ordenada.

Creando formularios a partir de Modelos
=======================================

Construyamos algo un poquito más interesante: un formulario que
suministre los datos de un nuevo publicista a nuestra aplicación de
libros del :doc:`Capítulo 5<chapter05>`.

Una regla de oro que es importante en el desarrollo de software, a la
que Django intenta adherirse, es: no te repitas (del inglés *Don't
Repeat Yourself*, abreviado DRY). Andy Hunt y Dave Thomas la definen
como sigue, en *The Pragmatic Programmer*:

    Cada pieza de conocimiento debe tener una representación única, no
    ambigua, y de autoridad, dentro de un sistema.

Nuestro modelo de la clase ``Publisher`` dice que un publicista tiene
un nombre, un domicilio, una ciudad, un estado o provincia, un país, y
un sitio web. Si duplicamos esta información en la definición del
formulario, estaríamos quebrando la regla anterior. En cambio, podemos
usar este útil atajo: ``form_for_model()``::

    from models import Publisher
    from django.newforms import form_for_model

    PublisherForm = form_for_model(Publisher)

``PublisherForm`` es una subclase de ``Form``, tal como la clase
``ContactForm`` que creamos manualmente con anterioridad. Podemos
usarla de la misma forma::

    from forms import PublisherForm

    def add_publisher(request):
        if request.method == 'POST':
            form = PublisherForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_publisher/thanks/')
        else:
            form = PublisherForm()
        return render_to_response('books/add_publisher.html', {'form': form})

El archivo ``add_publisher.html`` es casi idéntico a nuestra plantilla
``contact.html`` original, así que la omitimos. Recuerda además
agregar un nuevo patrón al URLconf: ``(r'^add_publisher/$',
'mysite.books.views.add_publisher')``.

Ahí se muestra un atajo más. Dado que los formularios derivados de
modelos se emplean a menudo para guardar nuevas instancias del modelo
en la base de datos, la clase del formulario creada por
``form_for_model`` incluye un conveniente método ``save()``. Este
método trata con el uso común; pero puedes ignorarlo si deseas hacer
algo más que tenga que ver con los datos suministrados.

``form_for_instance()`` es un método que está relacionado con el
anterior, y puede crear formularios preinicializados a partir de la
instancia de un modelo. Esto es útil al crear formularios "editar".

¿Qué sigue?
===========

Este capítulo concluye con el material introductorio de este
libro. Los próximos trece capítulos tratan con varios tópicos
avanzados, incluyendo la generación de contenido que no es HTML
(:doc:`Capítulo 11<chapter11>`), seguridad (:doc:`Capítulo 19<chapter19>`), y entrega del servicio
(:doc:`Capítulo 20<chapter20>`).

Luego de estos primeros siete capítulos, deberías saber lo suficiente
como para comenzar a escribir tus propios proyectos en Django. El
resto del material de este libro te ayudará a completar las piezas
faltantes a medida que las vayas necesitando.

Comenzaremos el :doc:`Capítulo 8<chapter08>` yendo hacia atrás, volviendo para darle
una mirada más de cerca a las vistas y a los URLconfs (introducidos
por primera vez en el :doc:`Capítulo 3<chapter03>`).


