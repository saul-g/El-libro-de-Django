============================
Apéndice A: Casos de estudio
============================

Para ayudar a responder las preguntas acerca de cómo funciona Django en el
"mundo real", hablamos (bueno, nos escribimos) con un puñado de personas que
tienen sitios completos y funcionales desarrollados en Django. La mayor parte de
este apéndice son sus palabras, que han sido ligeramente editadas para mayor
claridad.

Elenco
======

Conozcamos a nuestros personajes y sus proyectos.

* *Ned Batchelder* es el ingeniero principal de Tabblo.com. Tabblo comenzó
  su vida como una herramienta para contar historias basadas en fotos
  compartidas, pero recientemente fue comprado por Hewlett-Packard para
  propósitos de mayor alcance:

  HP vio valor real en nuestro estilo de desarrollo web, y en la forma en
  que tendimos puentes entre el mundo virtual y el mundo físico. Nos
  adquirieron de modo que pudiéramos llevar esa tecnología a otros sitios
  en la Web. Tabblo.com todavía es un gran sitio para contar historias,
  pero ahora también estamos trabajando en separar componentes y reutilizar
  las piezas más importantes de nuestra tecnología.

* *Johannes Beigel* es uno de los principales desarrolladores en Brainbot
  Technologies AG. El sitio Django más orientado al público de Brainbot es
  http://pediapress.com/, donde se pueden solicitar versiones impresas de
  artículos de Wikipedia. El equipo de Johannes actualmente está trabajando
  en un programa de gestión de conocimiento para empresas conocido como
  Brainfiler.

  Johannes nos cuenta que Brainfiler

  [...] es una solución de software para gestionar, buscar, categorizar y
  compartir información de fuentes distribuidas. Está construido para el
  uso empresarial tanto en entornos de intranet como internet y es
  altamente escalable y personalizable. El desarrollo de los conceptos y
  componentes medulares comenzó en el 2001. Recientemente hemos
  rediseñado/reimplementado el servidor y el cliente web, que [ahora] está
  basado en Django.

* *David Cramer* es el desarrollador principal de Curse, Inc. Él desarrolló
  Curse.com, un sitio para devotos a los videojuegos multijugador masivos
  como World of Warcraft, Ultima Online, y otros.

  Curse.com es uno de los sitios sobre Django más grandes de Internet:

  Tenemos aproximadamente entre 60 y 90 millones de visitas a la página en
  promedio por mes,y tuvimos picos de más de 130 millones de visitas (en un
  mes) usando Django. Somos un sitio web muy dinámico y orientado al usuario
  específicamente enfocado en juegos multijugador masivos, y uno de los
  sitios web más grandes acerca de World of Warcraft globalmente.
  Nuestro sitio web se estableció a principios de 2005, y desde finales de
  2006 nos hemos estado expandiendo a juegos más allá de World of Warcraft.

* *Christian Hammond* es un ingeniero senior en VMware (un desarrollador líder
  de software de virtualización). También es el desarrollador principal de
  Review Board (http://www.review-board.org/), un sistema de revisión de
  código basado en Web. Review Board nació como un proyecto interno de VMware,
  pero ahora es open source:

  A finales de 2006, David Trowbridge y yo discutíamos el proceso que
  usabamos en VMware para manejar la revisión de código. Antes de que
  la gente enviara código al repositorio, se suponía que enviaran un diff
  de los cambios a una lista de correo para ser revisado. Todo se manejaba
  por email, y por supuesto, se volvió difícil seguir las revisiones que
  necesitaban mayor atención. Fue entonces que comenzamos a discutir potenciales
  soluciones para este problema.
   
  En vez de escribir mis ideas, las puse en código. En poco tiempo, nació
  Review Board. Review Board ayuda a los desarrolladores, contribuidores y
  revisores a seguir la evolución del código propuesto a revisión y a mejorar
  la comunicación entre unos y otros. En vez de hacer una vaga referencia a
  una parte del código en un email, el revisor puede comentar directamente
  sobre el código. El código, junto a los comentarios, aparecerá entonces
  en las revisiones, dando a los desarrolladores suficiente contexto para
  trabajar más rápidamente en los cambios que hagan falta.

  Review Board creció rápidamente en VMware. De hecho, mucho más rápido
  de lo esperado. En unas pocas semanas, tuvimos diez equipos usando Review
  Board. Sin embargo, este proyecto no es interno para VMware. Se decidió
  desde el día uno que debería ser open source y estar disponible para ser
  usado por cualquier compañía o proyecto.

  Hicimos un anuncio de open source y habilitamos el sitio conjuntamente,
  que está disponible en http://www.review-board.org/. La respuesta a nuestro
  anuncio público fue tan impresionante como nuestro anuncio interno a VMware.
  En poco tiempo, nuestro servidor de demostración recibió más de 600
  usuarios, y la gente comenzó a contribuir al proyecto en sí.

  Review Board no es la única herramienta de revisión de código del mercado,
  pero es la primera que hemos visto que es abierta y tiene el extenso
  conjunto de características en el que hemos trabajado para que incluya.
  Esperamos que esto repercuta en beneficios de tiempo para muchos proyectos
  (open source o no).


¿Por qué Django?
================

Le preguntamos a cada desarrollador por qué decidió usar Django, qué otras
opciones fueron consideradas, y cómo se tomó la decisión definitiva de usar Django.

*Ned Batchelder*:

Antes de unirme a Tabblo, Antonio Rodriguez (fundador/CTO de Tabblo) hizo una
evaluación de Rails y Django, y encontró que ambos proveían un gran ambiente
de desarrollo rápido *quick-out-of-the-blocks*. Comparando ambos, encontró que
Django tenía una mayor profundidad técnica que haría más fácil construir un
sitio robusto y escalable. También, el que Django esté basado en Python
significó que tendríamos toda la riqueza del ecosistema Python para soportar
nuestro trabajo. Esto definitivamente quedó demostrado a medida que
construimos Tabblo.
       
*Johannes Beigel*:

Como hemos estado codificando en Python por muchos años ya, y rápidamente
comenzamos a usar el framework Twisted, Nevow era la solución más *natural*
para resolver nuestras aplicaciones web. Pero pronto nos dimos cuenta que
-- a pesar de la integración perfecta con Twisted -- muchas cosas eran un poco
incómodas de realizar dentro de nuestros procesos de desarrollo ágil.

Luego de investigar un poco en Internet, nos quedó claro que Django era el
framework de desarrollo web más prometedor para nuestros requerimientos.

Lo que nos condujo a Django fue la sintaxis de sus templates, pero pronto
apreciamos todas las otras características que estaban incluidas, y así fue
que "compramos" rápidamente a Django.

Después de algunos años de desarrollo e implementación en paralelo de sistemas
(Nevow todavía está en uso para algunos proyectos en sitios de clientes),
llegamos a la conclusión de que Django es mucho menos incómodo, resultando en
un código mucho mejor para mantener, y que es mucho más divertido para trabajar.

*David Cramer*:

Escuché sobre Django en el verano de 2006, momento en que estabamos listos para
hacer un reacondicionamiento de Curse, y decidimos investigarlo. Quedamos muy
impresionado de lo que podía hacer, y todos los aspectos donde podía ahorrarnos tiempo.
Lo conversamos y al decidirnos por Django comenzamos a escribir la tercera
revisio del sitio web casi inmediatamente.

*Christian Hammond*:

Había jugado con Django en un par de pequeños proyectos y quedé muy impresionado
con él. Está basado en Python, del que soy un gran fanático, y esto lo hace fácil
no sólo para desarrollar sitios y aplicaciones web, sino que también mantiene
el trabajo organizado y mantenible. Esto siempre es un problema en PHP y Perl.
Basado en experiencias del pasado, no necesité pensar mucho para meterme con Django.


Comenzando
==========

Como Django es una herramienta relativamente nueva, no hay muchos desarrolladores
experimentados ahí afuera que lo dominen ampliamente. Le preguntamos a nuestro
"panel" cómo consiguieron que su equipo adquiriese velocidad con Django y qué
consejos querrían compartir con nuevos desarrolladores Django.

*Johannes Beigel*:

Luego de programar principalmente en C++ y Perl, nos cambiamos a Python y
continuamos usando C++ para el código computacionalmente intensivo.

[Aprendimos Django mientras] trabajamos con el tutorial, navegando la
documentación para obtener una idea de lo que es posible (es fácil perderse
muchas característica si sólo se sigue el tutorial), e intentando comprender
los conceptos básicos detrás del middleware, objetos request, modelos de base
de datos, etiquetas de plantillas, filtros  personalizados,
los formularios, autorización, localización... Luego podríamos revisar más
profundamente esos tópicos cuando realmente los necesitáramos.


*David Cramer*:

La documentación del sitio web es grandiosa. Pégate a ella.

*Christian Hammond*:

David y yo teníamos una experiencia previa con Django, aunque era limitada.
Hemos aprendido mucho mientras desarrollábamos Review Board. Le aconsejaría
a los nuevos usuarios que lean la tan bien escrita documentación de Django y
el libro que ahora están leyendo, ya que ambos han sido inestimables para
nosotros.

No tuvimos que sobornar a Christian para conseguir esa declaración -- ¡lo juramos!

Portando código existente
=========================

Aunque Review Board y Tabblo fueron desarrollos desde cero, los otros sitios fueron
portados desde código ya existente. Estábamos interesados en escuchar como 
fue ese proceso.


*Johannes Beigel*:

Comenzamos a "migrar" el sitio desde Nevow, pero pronto nos dimos cuenta de
que queríamos cambiar tantos aspectos conceptuales (tanto en la interfaz de
usuario como en la parte del servidor de aplicación) que empezamos todo de
nuevo usando el código que teníamos meramente como una referencia.


*David Cramer*:

El sitio anterior estaba escrito en PHP. Ir de PHP a Python fue grandioso
programáticamente. El único detalle es que hay que tener mucho más cuidado
con la gestión de memoria [ya que los procesos Django permanecen mucho más
tiempo que los procesos PHP (que son simples ciclos)].


¿Cómo les fue?
==============

Ahora la pregunta del millón: ¿Cómo los trató Django? Estabamos especialmente
interesados en escuchar dónde Django perdió fuerza -- es importante conocer en que
aspectos tus armas son débiles *antes* de usarlas en la barricada.

*Ned Batchelder*:

Django realmente nos permitió experimentar con las funcionalidades de
nuestro sitio web. Tanto antes como una startup en busca del calor de
clientes y negocios, como ahora como parte de HP y trabajando con un número
de socios, tuvimos que ser muy ágiles cuando hubo que adaptar el software a
nuevas demandas. La separación de la funcionalidad en modelos, vistas y
controladores nos brindó una modularidad que permitió elegir apropiadamente
dónde extender y modificar.
El ambiente Python de trasfondo nos dio la oportunidad de utilizar bibliotecas
existentes para resolver problemas sin reinventar la rueda. PIL, PDFlib,
ZSI, JSmin, y BeautifulSoup son sólo un puñado de bibliotecas que agregamos
para hacer algunas tareas que eran engorrosas para nosotros.

La parte más difícil del nuestro uso de Django ha sido la relación entre
los objetos de memoria y lo objetos de la base de datos, de algunas maneras.
Primero, el Mapeo Objeto-relacional (ORM) de Django no asegura que dos
referencias a la misma entrada en la base de datos sean el mismo objeto
Python, por lo que puedes verte en situaciones donde dos partes del código
intentan modificar la misma entrada y una de las copias está anticuada.
Segundo, el modelo de desarrollo de Django te anima a basar tus modelos de
objetos de datos en objetos de base de datos. A lo largo del tiempo hemos
encontrado más y más usos de objetos de datos que no se ajustan a la base de
datos, y tenemos que migrarlos desde su naturaleza asumiendo que su
información se almacenará en una base.

Para una base de código grande y que se utilizará por mucho tiempo,
definitivamente tiene sentido gastar tiempo estudiando las formas en que tus
datos serán almacenados y accedidos, y construyendo alguna infraestructura
que soporte esas formas.

También hemos agregado nuestra propia facilidad para la migración de la base
por lo que los desarrolladores no tienen que aplicar parches SQL para mantener
los actuales esquemas de base de datos funcionando.
Los desarrolladores que cambian el esquema escriben una función Python para
actualizar la base, y eso se aplica automáticamente cuando el servidor se
inicia.
    
*Johannes Beigel*:

Consideramos Django como una plataforma muy satisfactoria que encaja perfectamente
con la manera Pythonica de pensar. Casi todo simplemente funciona según lo previsto.

Una cosa que necesitó un poco de trabajo en nuestro proyecto en curso fue
ajustar la configuración del archivo ``settings.py`` y la estructura de
directorios/configuración (para aplicaciones, plantilla, datos locales, etc),
porque implementamos un sistema altamente modular y configurable, donde todas
las vistas de Django son métodos de algunas instancias de clase. Pero con la
omnipotencia del dinámico código Python, fue posible hacerlo.

*David Cramer*:

Gestionamos la implementación de grandes aplicaciones de base de datos en
un fin de semana. Esto nos hubiera llevado una o dos semanas hacerlo en
el sitio web previo, en PHP. Django ha brillado exactamente donde queríamos
que lo haga.

Ahora, aunque Django es una gran plataforma, es evidente que no está construido
para las necesidades especificas que cualquiera necesite. Al tiempo del
lanzamiento inicial del sitio web sobre Django, tuvimos nuestro mayor tráfico
mensual del año, y no podíamos continuar. Durante los meses siguientes
ajustamos algunos detalles, mayormente el hardware y el software que
servía las peticiones a Django. Esto incluyó modificaciones de nuestra
configuración de hardware, optimización de Django, y perfeccionar el software
servidor que usábamos, que en ese entonces era lighttpd y FastCGI.

En mayo de 2007, Blizzard (los creadores de World of Warcraft) lanzaron
otro parche bastante grande, como el que habían lanzado en diciembre cuando
nuestro sitio fue lanzado en Django. La primer cosa que pasó por nuestras
cabezas fue, "hey, si soportamos el aluvión de diciembre, esto de ninguna manera puede
ser tan grande, deberíamos estar bien". Perdimos cerca de 12 horas antes de que
los servidores comenzaran a sentir el calor. La pregunta surgió de nuevo:
¿Realmente era Django la mejor solución para lo que nosotros queríamos lograr?

Gracias a todo el gran apoyo de la comunidad, y largas noches, pudimos
implementar varios arreglos "en caliente" sobre el sitio durante esos días.
Los cambios introducidos (que con suerte estarán incorporados a Django en el
momento que este libro vea la luz) permiten que con completa tranquilidad,
aquellos (no cualquiera) que tengan que lidiar con 300 peticiones web por
segundo, puedan hacerlo, con Django.

*Christian Hammond*:

Django nos permitió construir Review Board bastante rápidamente forzándonos
a estar organizados a través de la separación de URL, vistas y plantillas,
y proveyéndonos útiles componentes listos para usar, como la aplicación de
autenticación, cacheo, y la abstracción de base de datos. La mayor parte de
esto funcionó realmente bien para nosotros.

Siendo un aplicación web dinámica, tuvimos que escribir un montón de
código JavaScript. Esta es una área en la que Django no ha podido ayudarnos
realmente mucho. El soporte que provee Django para el uso de plantillas,
etiquetas, filtros y formularios son grandiosos, pero no son fácilmente
utilizables desde código JavaScript. Hay veces que quisiéramos usar una
plantilla en particular o un filtro, pero no hay manera de usarlo desde
JavaScript. Personalmente me gustaría ver que se incorporen a Django algunas
soluciones creativa para esto.


Estructura de Equipo
====================

A menudo, los proyectos son exitosos gracias a sus equipos, y no a tecnología
elegida. Consultamos a nuestro panel sobre sus equipos de trabajo, y qué
herramientas y técnicas utilizan para permanecer en carrera.

*Ned Batchelder*:

Somos un ambiente de Startup Web bastante estándar: Trac/SVN, cinco
desarrolladores. Tenemos un servidor de desarrollo, un servidor de
producción, un script desarrollado ad hoc, y así.
Ah, y amamos Memcached.

*Johannes Beigel*:

Usamos Trac como nuestro bug tracker y wiki, y recientemente reemplazamos
Subversion+SVK por Mercurial (un sistema de control de versiones distribuido
escrito en Python que maneja la ramificación y fusión con encanto)

Pienso que tenemos un proceso de desarrollo muy ágil, pero no seguimos una
metodología "rígida" como Extreme Programming (aunque tomamos prestadas
muchas ideas de ahí). Somos más bien programadores pragmáticos.

Tenemos un sistema de construcción automatizada (personalizado pero basado
en SCons), y pruebas unitarias para casi todo.

*David Cramer*:

Nuestro equipo consiste en cuatro desarrolladores web, todos trabajando en
la misma oficina de modo que es bastante fácil comunicarse. Nos basamos en
herramientas comunes como SVN y Trac.

*Christian Hammond*:

Review Board tiene actualmente dos desarrolladores principales (David
Trowbridge y yo) y un par de contribuidores. Estamos hospedados en Google
Code y usamos su repositorio Subversion, issue tracker, y wiki. De hecho,
usamos Review Board para revisar nuestros cambios antes de incorporarlos.
Hacemos pruebas en nuestras computadores locales, tanto manualmente como por
pruebas de unidad. Nuestros usuarios en VMware que usan Review Board todos
los días nos proveen de un montón de feedback útil y reportes de errores,
que intentamos incorporar en el programa.

Implementación
==============

Los desarrolladores de Django toman la facilidad de implementación y escalamiento
muy seriamente, por lo que siempre estamos interesados en escuchar sobre ensayos
y tribulaciones del mundo real.

*Ned Batchelder*:

Hemos usado cacheo tanto en la capa de consulta como de respuesta para agilizar
los tiempos de respuesta. Tenemos una configuración clásica: un multiplexor,
varios servidores de aplicación, un servidor de base de datos. Eso ha funcionado
bien para nosotros, porque podemos usar cacheo sobre el servidor de aplicación
para evitar el acceso a la base de datos, y luego agregar tantos servidores de
aplicación como necesitemos para manejar la demanda.

*Johannes Beigel*:

Servidores Linux, preferentemente Debian, con muchos gigas de RAM. Lighttpd
como servidor Web, Pound como front-end HTTPS y balanceador de carga si
se necesita, y Memcached como sistema de caché. SQLite para pequeñas bases
de datos, Postgres si los datos crecen mucho, y cosas altamente
especializadas de base de datos para nuestros componentes de búsqueda y de
gestión de conocimiento.

*David Cramer*:

Nuestra estructura todavía está para debatirse... (pero es esto actualmente):

Cuando un usuario solicita el sitio se lo envía a un cluster de servidores
Squid usando Lighttpd. Allí, los servidores verifican si el usuario está
registrado en el sistema. Si no lo está, se le sirve una página cacheada.
Un usuario autenticado es reenviado a un cluster de servidores corriendo
Apache2 con mod_python (cada uno con una gran cantidad de memoria), donde
luego cada uno hace uso de en un sistema Memcached distribuido y un bestial
servidor de base de datos MySQL. Los datos estáticos, como archivos grandes
o videos, (actualmente) estan hospedados en un servidor corriendo una
instalación mínima de Django usando lighttpd con fastcgi. Más adelante,
migraremos todos esos datos a un servicio similar al S3 de Amazon.

*Christian Hammond*:

Hay dos servidores de producción en este momento. Uno está en VMware y
consiste en una maquina virtual Ubuntu corriendo en VMware ESX. Usamos MySQL
para la base de datos, Memcached para nuestro back-end de cacheo, y actualmente
Apache para el servidor Web. Tenemos varios servidores potentes que pueden
escalarse cuando lo requiramos. También podemos mudar MySQL o Memcached a otra
maquina virtual a medida que nuestra base de usuarios crece.

El segundo servidor de producción es el de Review Board mismo. La configuración
es casi idéntica al anterior, excepto que la maquina virtual se basa en
VMware Server.
