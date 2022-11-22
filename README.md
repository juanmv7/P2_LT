# P2 Laboratorio de Telemática

## 1. Introducción
Este repositorio contiene un VoIP Network Designer que se basa en un caso práctico donde una empresa ofrece servicio de VoIP a empresas a nivel nacional. Este servicio consiste en hosting de la PBX y acceso al Proveedor de Servicio VoIP(PROVOIP) mediante SIP TRUNK. Se quiere un diseño de red escalable capaz de ofrecer los parámetros de QoE, QoS y GoS requeridos a las empresas cliente. Por eso el programa recibe como entradas las siguientes variables:

### Llamadas:
- Número de empresas cliente (Nc)
- Número de líneas (Nl)
- Tiempo por llamada (Tpll)
- Ancho de banda de reserva (BWres)
- Tipo de encapsulación utilizada (Ethernet, Ethernet 802.1q, Ethernet q-in-q, PPPOE, PPPOE 802.1q)
- Se considerará el caso peor en cuanto a la probabilidad de que una línea realice una llamada durante la hora cargada
### QoE:
- Mean Opinion Score (MOS)
### QoS:
- Retardo total (Rt)
- Retardo de red (Rr)
- Jitter (J)
- Se considera el uso de RTP o cRTP
- Se considera sólo los retardos por Codecs, paquetización, buffer anti-jitter. Considere un 10% el tiempo de compresión y descompresión
### GoS:
- Probabilidad de bloqueo (Pb)
### Ancho de banda:
- Ancho de Banda SIPTRUNK (BWst)

El programa devolverá una serie de parámetros en función de las entradas introducidas. Estos parámetros o resultados son los que se listan a continuación:

- MOS y Codec elegido en función del MOS introducido.
- Retardo resultante del codec elegido y del retardo del que depende introducido.
- Indicación de si este retardo devuelto cumple o no con el deseado.
- El número de líneas (recursos) necesarias para ofrecer el servicio dada una probabilidad de bloqueo y un número de Erlangs en la hora cargada BHT.
- El ancho de banda necesario según el tipo de encapsulación, la compresión de RTP, el número de líneas  y el codec elegido 
- Indicación de si el ancho de banda resultante cumple con el introducido o no.

A continuación se pasa a explicar cómo los diferentes módulos interaccionan entre sí y pasaremos a ver un diagrama de flujo y a estudiar cada módulo por separado con sus diversas funciones y variables
## 2. Interacción entre módulos (Diagrama de flujo)
En este proyecto tenemos 3 módulos principales: Back End, cliente + GUI y Server. La definición de la GUI y el cliente se encuentran en el mismo módulo. La GUI es la interfaz gráfica que va pidiendo los diferentes datos al usuario. En cada frame se pide un tipo de dato y es muy importante mantener esto en mente. A la hora de pasar de frame se envía el dato introducido en el frame anterior. Esto lo hace el propio cliente conectando al server y enviando un string que contiene una cabecera y un dato separados por un guión. Más adelante, hablaremos de esta cabecera. El servidor almacena este dato en una lista, la cuál tiene 13 posiciones, una por cada tipo de dato y a su vez por cada frame. Después de esto el servidor realiza una operación en función del tipo de dato que haya recibido, ya sea calcular el MOS o calcular el retardo, por ejemplo. Para esto llama al módulo del Back End, que consiste en una librería con diversas funciones para el cálculo de los resultados. Tras todo esto se cierra la conexión y se pasa de frame. Decir que cuando se pasa del frame 11 al 12 y por tanto se envía el dato correspondiente a ese frame y además el último dato pedido, el servidor devuelve un string con todos los resultados en orden al cliente. Además, en el cliente se carga el último frame donde se muestra un resumen de todos los valores obtenidos y la posibilidad de enviar un correo con un informe detallado. Al pulsar este botón, se realiza la última conexión al servidor donde por medio de la cabecera que se explicará más adelante se llama al back end para realizar el envío de un correo con un informe detallado de los diferentes valores que el usuario ha ido introduciendo además de sus respectivos resultados y de los valores y resultados finales. Finalmente se cierra el programa.

### 2.1 Protocolo (Cabecera)
En este apartado se va explicar la cabecera que hemos utilizado para el intercambio de datos entre servidor y cliente. La cabecera se basa en el principio de que cada frame “i” se corresponde con un tipo de dato, así i=0 se corresponde con el MOS, i=1 con el retardo requerido, etc. Esto nos simplifica mucho todo ya que sólo necesitamos fijarnos en i para saber que tipo de dato es. Por tanto, lo que pasamos de cliente a servidor tiene el siguiente formato: “i-data”. En el servidor lo único que tenemos que hacer es separar “i” de “data”. De esta forma guardamos en la lista “resultados” en la posición “i” el “data” que recibimos. Y solo necesitamos mirar “i” para ver a qué funciones del Back End llamar. 

### 2.2 Diagrama de Flujo
## 3. Cliente_GUI
### 3.1. Descripción
El programa primeramente crea una ventana raíz donde estarán todas las páginas o frames (estarán vacíos). Tiene varias funciones para crear elementos básicos como botones, cajas de texto, avisos…, y varias funciones lógicas como conectar con el servidor o comprobar errores. Crea automáticamente con un for todos los frames que se van a utilizar, y luego se van rellenando uno a uno de forma secuencial, ya que algunos tienen necesidades gráficas distintas que no se pueden automatizar. Por ejemplo, en el 0 y 1 añadimos fotos por lo que el código es distinto a los demás frames. En el 11 y 12 ocurre lo mismo ya que tenemos necesidades de tamaño diferentes.
###3.2. Variables
Las variables globales que contiene son:

- i=0: variable global para iterar entre frames.
- root: objeto de tkinter que corresponde a la ventana principal de nuestro programa donde guardaremos los distintos frames o páginas.
- frames=[]: vector global de objetos de la clase tkinter donde guardaremos los distintos frames o páginas del programa.
- valores=[]: vector global donde guardaremos los valores numéricos que le vamos a pasar al servidor.
- cuadroTexto=[]: vector global de objetos hijos de frames donde guardaremos las respuestas del usuario (luego lo pasamos a valores).
- mensaje=[]: vector global de strings que se mostrarán por pantalla en cada frame.
- solucion: Una lista con los resultados enviados por el servidor. Se usará en “label_solucion”.
- message: Contiene el dato a enviar en formato string. Se pasa junto a la cabecera al server.
- cabecera: String formado por “i” y “-”.
### 3.3. Funciones
Las funciones utilizadas son:

- crear_frame(): crea objeto de la clase tkinter y lo añade al vector frames. Cada objeto tiene unos atributos con los cuales podemos modificar la apariencia (color, tamaño, etc). Todos los frames se crean al principio.
- retroceder_pagina(): retrocede una posición del vector frames y lo muestra por pantalla. Cada vez que volvamos atrás y vayamos de nuevo hacia adelante, debemos volver a rellenar (y por tanto reescribir) el frame.
- crear_boton(k): crea “widgets” (objetos hijos de un frame), serán los botones de siguiente y atrás para cada página, de entrada se le introduce el número de la página donde se debe añadir.
- crear_etiqueta(k): crea un “widget”, será el mensaje que veremos por pantalla gracias al vector mensaje,  de entrada se le introduce el número de la página donde se debe añadir. 
- crear_entry(k): crear un “widget”, será el recuadro donde introduciremos los datos. Se guarda en “cuadroTexto” para luego poder coger lo que se ha escrito con el método get,de entrada se le introduce el número de la página donde se debe añadir.
- codigo_boton(): función que se ejecuta cuando pulsamos el botón. Guardamos el dato en valores para usarlo en el servidor, checkeamos errores, conectamos con el servidor servidor y pasamos de frame (iteramos i).
- check_errors(): función para comprobar si los datos introducidos por el usuario son correctos. Si los datos son incorrectos, salta un error (messagebox) y permanece en el frame. Además, diferencia entre no escribir nada, escribir espacios y escribir letras cuando se esperan números.
- conectar_server(): función para establecer conexión TCP con el servidor por el puerto 10800 en nuestro caso, envía datos al servidor con el formato del protocolo que inventamos. Este protocolo consiste en enviar una cabecera compuesta por un número dependiendo del dato enviado, se separa la cabecera del dato por “-”. Cada vez que se envía un dato la conexión entre cliente y servidor se cierra, para no congestionar la red cuando no se están enviando datos. Además  no solo envía datos sino también recibe la solución elegida por el servidor. En conclusión, esta función actúa como cliente de nuestra aplicación.
label_solucion(solucion): esta función nos muestra en el último frame el informe con los resultados enviados por el servidor al cliente de una manera correcta y de una forma fácil para visualizar.
- enviar_correo(): es la última función que se ejecuta en el programa. Recoge el dato del correo electrónico que escribe el usuario.Llama a la función conectar_server() para enviarle este dato y que el servidor envíe el correo electrónico con el informe final . Se muestra un aviso de que todo ha funcionado correctamente y finalmente cierra el programa.
- Bloque de creación de frames: Parte donde definimos el root del que cuelgan todos los frames, los cuales creamos manualmente, ya que hay algunos frames que tienen dimensiones diferentes ya sea porque añaden imágenes, las cuales también se deben definir en ese mismo bloque o porque añade  más texto que los otros frames.

## 4. Server
### 4.1. Descripción
Este programa no se ha ido separando por diferentes funciones, por lo que para una mejor explicación lo separaremos por bloques. La función general del servidor es la de iniciar y estar escuchando conexiones por el puerto 10800 y enviar la solución elegida al cliente. Tras iniciar la conexión entre cliente y servidor, se recibe cada dato que envía el cliente y se separan los datos de la cabecera. Como cada cabecera está asociada a un dato diferente, se puede saber rápidamente de que se trata cada dato.
### 4.2. Variables
Las variables globales que contiene son:
- datos_vector=[]: vector que se inicializa a cero con 13 posiciones y se va rellenando con los 13 datos finales introducidos por el cliente.
- datos_vector_cte=[]: vector que se va rellenando de todos los datos que introduce el cliente, si en primer lugar se mete un retardo y posteriormente se cambia, ambos datos se incluyen en este vector. Se trata de un tipo de registro.
- resultado_cte[]: vector con todos los resultados posibles que ha calculado el servidor. Si el cliente no realiza ningún cambio en los datos introducidos solo habrá un resultado, en cambio si realiza algún cambio habrá distintas soluciones.
- resultado=” ”: vector con el resultado obtenido a partir de los datos finales, es decir con los datos del vector datos_vector=[].
- bucle=True: variable booleana que se inicializa a True hasta que se envía un correo electrónico.
### 4.3. Funciones
Como indicamos, no tenemos funciones en este programa, por lo que describiremos por bloques su funcionamiento.
- Bloque conexión: En este primer bloque, el servidor se pondrá a escuchar en el puerto que le indiquemos, esperando a una conexión. 
- Bloque menssage: En este bloque se recibe y se decodifica los datos que llegan. Los datos llegan con el formato del protocolo que indicamos anteriormente, por lo que el servidor separa los datos de la cabecera. Pasa los datos a float y va guardando en el vector datos_vector en una posición diferente dependiendo de la cabecera con la que venía el dato.
- Bloque Cálculo de la solución: como la variable “i” nos indica el tipo de dato que es, ya que en esta variable guardamos la cabecera, podemos calcular los diferentes datos gracias a esto. Si i==0, indica que el datos introducido pertenece al MOS, llamamos a la función  indicada del Back_end y guardamos la solución como un string en la variable “resultado”, en la variable “resultado_cte”, guardamos todas las soluciones posibles, si se han pedido más de una, junto a la cabecera para saber a que pertenece cada dato. De igual forma, dependiendo de la cabecera vamos llamando a las diferentes funciones de Back_End, hasta enviar la solución completa “resultado” al cliente.
- Bloque Envío Correo: si la cabecera i=12, significa que ese dato es el correo, por lo que en vez de pasar el dato a float, lo guardamos en “datos_vector” como un string. Llamamos a la función “Envio_correo_informe” del Back_end y por último pasamos la variable “bucle” a False, para que se cierre la conexión.
## 5. Back_end
### 5.1. Descripción
En este programa se ha implementado la parte lógica necesaria para el desarrollo de los diferentes cálculos y requisitos en los que se basa esta aplicación. A partir de los valores de entrada recogidos en la interfaz gráfica, el servidor utiliza las funciones del back_end para calcular los resultados convenientes.

### 5.2. Variables
Las variables globales que contiene son:

- codec_name: vector global que recoge los nombres de los diferentes parámetros que definen un códec (Codec Bit Rate (Kbps), Codec Size Sample (Bytes), Codec Sample Interval (ms), Mean Opinion Score (MOS), Voice Payload Size (Bytes), Voice Payload Size (ms), Packets Per Second (PPS), Retardo (ms))
- G711: vector global que recoge el valor de los parámetros que definen al códec G711.
- G729: vector global que recoge el valor de los parámetros que definen al códec G729.
- G723_1_63: vector global que recoge el valor de los parámetros que definen al códec G723_1_63.
- G723_1_53: vector global que recoge el valor de los parámetros que definen al códec G723_1_53.
- G726_32: vector global que recoge el valor de los parámetros que definen al códec G726_32.
- G726_24: vector global que recoge el valor de los parámetros que definen al códec G726_24.
- G728: vector global que recoge el valor de los parámetros que definen al códec G728.
- G722_64: vector global que recoge el valor de los parámetros que definen al códec G722_64.
- ilbc_mode_20: vector global que recoge el valor de los parámetros que definen al códec ilbc_mode_20.
- ilbc_mode_30: vector global que recoge el valor de los parámetros que definen al códec ilbc_mode_30.
- TABLA: vector global que contiene en cada componente los vectores anteriormente descritos.
- TABLA_NAMES: vector global que contiene los nombres de todos los codecs.


### 5.3. Funciones
Las funciones utilizadas son: 

- eleccion_codec: esta función elige un codec a partir de un MOS requerido. Devolverá el codec elegido, el MOS asociado y la posición de ese codec en el vector TABLA.
- calculo_retardo: Esta función calcula el retardo de un CODEC en específico e indica si este retardo cumple o no con el retardo requerido. Para obtener el retardo y saber si cumple con el retardo requerido, necesitamos obviamente el retardo requerido, el retardo de red, el jitter y qué posición ocupa el codec anteriormente elegido en el vector TABLA. 
- erlang: Esta función calcula la probabilidad de bloqueo a partir de los recursos (lineas) y los Erlangs. 
- Calculo_lineas_BHT: Esta función calcula el número de líneas (Nlineas) necesarias a partir de la probabilidad de bloqueo introducida (que se compara con la probabilidad de bloqueo calculada con la función erlang) y el caso peor en la BHT (Busy Hour Traffic). Esta Busy Hour Traffic se calcula a partir de las entradas: Nc (número de clientes), Nl (número de líneas por cliente) y Tpll (tiempo medio por llamada en minutos). 
- Calculo_BWst: Esta función calcula el ancho de banda necesario para cursar Nlineas llamadas,
a partir del tipo de encapsulación (hay 5 tipos) y del uso de cRTP o no. Además compara con el BW introducido por el cliente y si cumple o no con este. 
Para el cálculo del ancho de banda utilizamos Nlineas previamente calculado, la posición del codec en el vector TABLA para acudir a ciertos valores (dentro de esa posición del vector) necesarios para el cálculo, el ancho de banda de reserva, el ancho de banda del que dispone el cliente, de si es con cRTP y por último el tipo de encapsulación elegida.
- Envio_correo_informe: Esta función envía un correo en el que se deja constancia de los datos que se han ido introduciendo en cada frame de la GUI, los valores finalmente introducidos y sus respectivos resultados parciales y finales. Para ello los valores de entrada son 4 vectores con todos los valores introducidos (entradas_cte), los finalmente introducidos (entradas), todos los resultados acorde a todos los valores aportados (salidas_cte) y los resultados derivados de los últimos valores aportados (salidas).

## 6. Manual de usuario:
Antes de nada aclarar que se trata de un prototipo de programa y por tanto el servidor y cliente hay que arrancarlo manualmente ejecutando ambos ficheros.py. En un caso real, el servidor estaría en una máquina remota y el cliente se ejecutaría de una forma más “agradable”, ya sea con un ejecutable u otro método. Una vez la interfaz gráfica aparezca, el usuario deberá ir introduciendo los diversos datos que le pide el programa pudiendo este ir hacia adelante o atrás en los diferentes frames y por tanto cambiando como desee los parámetros de entrada. El control de errores está implementado por lo que no se deberá preocupar por si introduce un dato no compatible.  Una vez introducidos todos los datos, tendrá la opción de recibir un correo con un informe detallado de los parámetros introducidos y los resultados obtenidos para dichos parámetros.

