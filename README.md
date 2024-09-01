
# Software de Facturación Libre Compatible con el RD 1007/2023
Este proyecto permite construir fácilmente un sistema de gestión de facturas que cumpla con los requisitos establecidos por el [Real Decreto 1007/2023, del 5 de diciembre, del gobierno de España](https://www.boe.es/buscar/act.php?id=BOE-A-2023-24840). Se trata de una implementación mínima, escrita en Python y publicada aquí, con la intención de aliviar el peso regulatorio de nuestro país a los profesionales y pequeñas empresas.

> **AVISO LEGAL**
> La información que se recoge está escrita con la mejor intención, pero no constituye consejo legal. Por favor, lee todo el documento (en concreto la sección Declaración Responsable) y habla con un abogado de confianza antes de usar este sistema.

Los comentarios, sugerencias y Pull Requests son bienvenidos.

## Instalación y Configuración
Las dependencias se instalan en los sistemas basados en Debian con el comando:
```
sudo apt install python3-qrcode python3-cryptography
```
En cual quier otro sistema con el comando:
```
pip3 qrcode cryptography
```

A continuación revisa los parámetros de configuración de `config.py` y ajústalos a tu gusto. Debes configurar el sistema antes de empezar a crear registros en la base de datos. El sistema se usa a través de los comandos o herramientas que se describen en este documento.

## Acerca del Real Decreto 1007/2023
Publicado el 6 de diciembre de 2023, empieza con un preámbulo en el que alude a la "urgente adaptación" a la digitalización y a un "significativo ahorro de costes". Después encontramos los siguientes artículos de interés:

* Se modifica el [Real Decreto 1619/2012](https://www.boe.es/buscar/act.php?id=BOE-A-2012-14696) (que regula  las obligaciones de facturación) para incluir el requisito de poner un código QR con el "contenido parcial de la factura" en todas las facturas. Este código se añade para "incentivar al consumidor final para que solicite los comprobantes de sus operaciones y pueda remitir\[los\] voluntariamente a la Administración tributaria", lo que técnicamente es una denuncia.

* Se establece que los sistemas de facturación tienen que cumplir este Real Decreto **antes del 1 de julio de 2025**.

Posteriormente pasa a detallar el Reglamento con los requisitos para los sistemas de facturación, donde destaco:

* En general el Reglamento solo aplica a aquellos "que utilicen sistemas informáticos de facturación" y define dichos sistemas como el "conjunto de hardware y software utilizado para expedir facturas", recogiendo, almacenando y procesando su información.

* El software debe tener un registro de "facturación de alta" que incluya la siguiente información (omito los casos excepcionales):
   * NIF y razón social del emisor y del receptor.
   * Número de factura y fecha de expedición.
   * Descripción del concepto.
   * Importe total y detalle de los impuestos en euros.
   * Número de factura, fecha de factura y hash del registro anterior.
   * Código de identificación del sistema informático.
   * Fecha, hora, minuto y segundo en que se generó el registro.

* Los registros de anulación de facturas deben contener esta información:
   * NIF y razón social del obligado a realizar la anulación, es decir normalmente el emisor de la factura.
   * Número de factura y fecha de expedición.
   * Número de factura, fecha de factura y hash del registro anterior.
   * Código de identificación del sistema informático.
   * Fecha, hora, minuto y segundo en que se generó el registro.

* El sistema deberá añadir un hash y una firma electrónica a cada registro.

* El proveedor del sistema informático debe emitir una declaración responsable certificando que cumple con este Reglamento. Nadie podrá dudar de la casi ilimitada "capacidad de dinamizar con ello la modernización y digitalización de la gestión empresarial privada y la mejora del cumplimiento fiscal" de este requisito.

* Remitir los registros de facturación a la Agencia Tributaria es voluntario (hasta que se apruebe la ley de facturación electrónica). Por su parte, la Agencia Tributaria deberá tener listo el sistema de recepción el 6 de septiembre del 2024...

### ¿A Quién Afecta?
Llegado este punto lo primero que cabe plantearse es si de verdad nos afecta, ya que solo aplica a aquellos "que utilicen sistemas informáticos de facturación".

El [RD 1619/2012, que regula las obligaciones de facturación](https://www.boe.es/buscar/act.php?id=BOE-A-2012-14696), dice en su [Artículo 8](https://www.boe.es/buscar/act.php?id=BOE-A-2012-14696#a8) que "las facturas podrán expedirse por cualquier medio, en papel o en formato electrónico, que permita garantizar al obligado a su expedición la autenticidad de su origen, la integridad de su contenido y su legibilidad". Acto seguido concreta que "la autenticidad del origen y la integridad del contenido de la factura podrán garantizarse mediante los controles de gestión usuales de la actividad empresarial o profesional del sujeto pasivo", siempre y cuando dichos controles permitan "crear una pista de auditoría fiable que establezca la necesaria conexión entre la factura y la entrega de bienes o prestación de servicios". También deja claro que los requisitos se presumen acreditados cuando se utilice un software que cumpla el Reglamento.

Por otro lado la [Ley 58/2003 General Tributaria](https://www.boe.es/buscar/act.php?id=BOE-A-2003-23186) añade en su [Artículo 29](https://www.boe.es/buscar/act.php?id=BOE-A-2003-23186#a29) Apartado 2.j, la obligación de que los "sistemas y programas informáticos o electrónicos que soporten los procesos contables, de facturación o de gestión de quienes desarrollen actividades económicas, garanticen la integridad, conservación, accesibilidad, legibilidad, trazabilidad e inalterabilidad de los registros", pero no hace obligatorio el uso de estos sistemas.

Hasta aquí mi interpretación de la ley es que, o bien usamos un software que cumpla el Reglamento, o bien expedimos facturas manualmente garantizando la autenticidad e integridad de contenido (o inalterabilidad) de manera auditable o comprobable por una persona externa. Fíjate que, a papel, estos requisitos se pueden justificar usando un talonario de facturas corporativo (solo el profesional puede expedir facturas válidas), numerado (no se pueden crear facturas en el pasado) y con copia de carbón (cualquier modificación posterior haría que no coincidiese con la copia del cliente). Sin embargo no será así por mucho tiempo.

La [Ley 56/2007 de Medidas de Impulso de la Sociedad de la Información](https://www.boe.es/buscar/act.php?id=BOE-A-2007-22440) ha incorporado en 2022 la obligación de que "todos los empresarios y profesionales deberán expedir, remitir y recibir facturas electrónicas en sus relaciones comerciales con otros empresarios y profesionales" ([Artículo 2 bis](https://www.boe.es/buscar/act.php?id=BOE-A-2007-22440#a2bis)). Lógicamente no se pueden expedir facturas electrónicas sin un software de facturación, pero por suerte esté artículo entrará en vigor para las empresas y profesionales que facturen menos de 8 millones a los dos años de aprobarse el desarrollo reglamentario, que [a día de hoy no se ha hecho](https://www.cuatrecasas.com/es/spain/fiscalidad/art/facturacion-electronica-obligatoria-operaciones-b2b) (ver [Disposición final octava de la Ley 18/2022 de creación y crecimiento de empresas](https://www.boe.es/buscar/act.php?id=BOE-A-2022-15818#df-8)). Ten en cuenta que la factura electrónica de momento solo aplicará a las facturas entre empresas, no a consumidores.

El Reglamento permite también una tercera vía de cumplimiento (Artículo 7) y es mediante "la aplicación informática que a tal efecto pueda desarrollar la Administración tributaria". Esta aplicación puede ser una buena opción para aquellos que emitan pocas facturas al año (por ejemplo porque tengan un piso en alquiler).

En el caso de muchas tiendas, tal y como yo lo entiendo, las máquinas registradoras o básculas que imprimen tickets, es decir que expiden facturas simplificadas, quedarían también sujetas al Reglamento, ya que éste incluye el "hardware" en su definición.

Los autónomos societarios que se encuentran en relación laboral (que trabajan solo para su propia empresa con los medios de la empresa y facturando sin IVA) creo que también están afectados, ya que el Reglamento obliga a "los contribuyentes del Impuesto sobre la Renta de las Personas Físicas que desarrollen actividades económicas", pero lo cierto es que no estoy seguro.

Finalmente falta analizar el caso de facturas creadas con un editor de texto en un ordenador. En mi opinión la cuestión aquí está en cuándo se considera que una factura es "expedida". No es delito tener borradores o plantillas de facturas en documentos de texto, pero la ley exige que cuando una factura se expida se garantice la autenticidad y la inalterabilidad. Por tanto se requiere un procedimiento de expedición de facturas auditable que cumpla con esos requisitos. Una forma de hacerlo sería publicando las facturas expedidas (o un hash de estas) en un registro público e inalterable (como una cadena de bloques o blockchain), pero para eso resulta más sencillo hacer un programa que cumpla el Reglamento (que goza de presunción de acreditación y es más fácil de explicar a un juez).

Este proyecto viene precisamente a cubrir esa necesidad, proporcionando un sistema que cumple con el Reglamento. Fíjate que puedes seguir generando el documento de la factura con tu editor de texto o de gráficos favorito, pero debes asegurarte de registrar el documento en el sistema cada vez que emitas una factura. Es decir, el procedimiento de expedición de facturas de tu empresa debe ser dar de alta el documento en este sistema.

### Crítica
Como se ha visto, y a pesar de lo expuesto en el preámbulo, las acciones del RD 1007/2023 tienen el único objetivo de aumentar el control fiscal a costa de añadir otra carga reglamentaria a las empresas. En la práctica, las empresas que ya usan un software de facturación tendrán un impacto menor, mientras que los autónomos y pequeñas empresas acostumbradas a hacer facturas con un editor de texto, se verán obligados a comprar o contratar un sistema que cumpla con el Reglamento.

En España hay unos 3 millones de autónomos y, haciendo una búsqueda rápida de software de facturación, se encuentran soluciones desde 10-15€ al mes. Si hacemos una estimación a la baja excluyendo a las pequeñas empresas y aceptando que el 50% de los autónomos ya utilizan un programa de facturación o pueden evitar usarlo, el impacto del RD 1007/2023 se puede estimar en un gasto inútil de mínimo 180 millones de euros al año. Esto sin considerar la pérdida de tiempo que requiere seleccionar, contratar y utilizar un sistema de facturación ajeno al día a día del negocio (por ejemplo teniendo que registrar las facturas en la base de datos regularmente), sin que le aporte ningún valor para su actividad. Además, esta carga se le está imponiendo a los autónomos y empresas más pequeñas españolas. Aún así, el Real Decreto no tiene reparos en afirmar que se conseguirá "una mejora acelerada de la competitividad" y contribuirá a "una mayor igualdad ante la ley y a un reforzamiento de los principios de equidad y capacidad contributiva en el reparto de las cargas tributarias".

Por último, quiero resaltar la tremenda ineficacia técnica del RD 1007/2023 de cara a conseguir los objetivos realmente buscados de reducir el fraude fiscal:
1. En primer lugar los sistemas informáticos almacenan su información en discos duros, que permiten el tratamiento y modificación de los datos. Es decir que un segundo programa que quisiese modificar los datos siempre sería capaz de hacerlo y eso es inevitable.
2. Contra esto el RD 1007/2023 impone que los registros deben guardarse con una cadena de hashes y firmas, intentando imitar las blockchains. El problema es que la inalterabilidad que consiguen las blockchains no se puede lograr sin la red de nodos y el sistema de consenso. En otras palabras, un software que quiera falsificar una factura podrá recalcular toda la cadena de hashes y firmas en unos pocos segundos.
3. Además, en mi opinión, nadie se dedicará a notificar a la Agencia Tributaria con los tickets que recibe. Primero porque es tedioso y no aporta nada al ciudadano, y segundo por la falta de privacidad que supone informar a Hacienda de los gastos que hace. Probablemente solo los propios funcionarios de la Agencia Tributaria se molestarán en hacerlo, quienes de hecho ya lo están haciendo mediante una app que registra una fotografía.
4. En cualquier caso, al no haberse definido oficialmente un formato concreto de la información contenida en el código QR, estos códigos no permitirán automatizar la tarea de registrar facturas, resultando inservibles.

En resumen, el RD 1007/2023 no solo supone un gasto inútil para el profesional y la pequeña empresa, sino que también es inútil para la propia Agencia Tributaria. 

## Generador de Códigos QR
El primer requisito que nos impone el RD 1007/2023 es incluir un código QR en la propia factura con los datos de esta. La regulación solo dice que debe contener el "contenido parcial de la factura", sin especificar nada más. Sin embargo, ya que el objetivo es poder usar la información que den los consumidores para detectar fraude fiscal, entiendo que estos campos son suficientes para identificar la factura unívocamente:
* Fecha de la factura.
* Número o código de factura.
* NIF del emisor.
* NIF del receptor.
* Importe total en euros.

No obstante, el comando permite omitir campos. Aparte de que puedes modificar el script fácilmente para añadir otros campos.

El comando `qrgen` pregunta esa información y genera una imagen con un código QR que la contiene. Debes pasarle el nombre del archivo de salida como único argumento, por ejemplo ejecutando:
```
$ ./qrgen.py qr.png
Fecha de la factura [15/08/2024]: 
Número o código de factura [Omitir]: 24001
NIF del emisor [Omitir]: B12345678      
NIF del receptor [Omitir]: B01234567
Importe total en euros [Omitir]: 10.50
```

## Registro de Facturación
Desde el punto de vista del usuario, las facturas se añaden a la base de datos con el comando `altafac.py`, que requiere que se le especifique la ruta del archivo de la factura (se recomienda usar PDF):
```
$ ./altafac.py documento.pdf
Introduce el número de factura: 24001
Fecha de expedición de la factura [15/08/2024]: 
Factura registrada correctamente.
```
Asegurate de añadir el código QR a la factura.

Las facturas registradas y su estado se muestran con `verfacs.py`:
```
$ ./verfacs.py
[x] 15/08/2024 24001: Dada de alta el 15/08/2024 a las 19:38:31
   Dada de baja el 18/08/2024 a las 11:54:45
[✓] 18/08/2024 24002: Dada de alta el 18/08/2024 a las 11:21:36

```
Opcionalmente este comando también verifica la integridad de la base de datos, es decir la cadena de hashes y las firmas electrónicas.

Por último puedes anular o dar de baja una factura con `anulafac.py`.

## Declaración Responsable
Ten en cuenta que este proyecto no es una solución comercial, sino que es una base libre que permite crear un sistema mínimo fácilmente, por lo que no incluyo declaración responsable. Sin embargo, la declaración responsable no es más que un documento de texto en el que tú mismo puedes certificar que tu sistema cumple con los requisitos. No olvides que la declaración debe contener toda la información indicada en el Artículo 13 del Reglamento.

## Formato de la Base de Datos
La base de datos del registro de facturación se implementa sobre un directorio en el que se copian los documentos de las facturas y se crea y mantiene un fichero CSV (tabla en texto separado por comas).

Fíjate que la mayoría de los datos requeridos por el RD 1007/2023 ya se encuentran disponibles en el propio documento de una factura válida, que forma parte del registro (y del hash). El resto se guardan en un CSV llamado `bd.csv` junto con la cadena de hashes y firmas electrónicas. El algoritmo utilizado para el hash es el SHA256, y para la firma electrónica es la curva elíptica SECP256R1, ambos considerados seguros a la fecha de escritura.

