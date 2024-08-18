
# Software de Facturación Libre Compatible con el RD 1007/2023
Este proyecto permite construir fácilmente un sistema de gestión de facturas que cumpla con los requisitos establecidos por el [Real Decreto 1007/2023, del 5 de diciembre, del gobierno de España](https://www.boe.es/buscar/act.php?id=BOE-A-2023-24840). Se trata de una implementación mínima escrita en Python y publicada aquí con la intención de aliviar el peso regulatorio de nuestro país a los profesionales y pequeñas empresas.

> **AVISO LEGAL**
> La información aquí recogida esta escrita con la mejor intención pero no constituye consejo legal. Por favor, lee todo el documento (en concreto la sección Declaración Responsable) y habla con un abogado de confianza antes de usar este sistema.

Los comentarios, sugerencias y Pull requests son bienvenidos.

## Instalación y Configuración
Las dependencias se instalan con el comando:
```
sudo apt install python3-qrcode python3-cryptography
```
en los sistemas basados en Debian, o con:
```
pip3 qrcode cryptography
```
en cualquier otro.

A continuación revisa los parámetros de configuración de `config.py` y ajústalos tu gusto. Debes configurar el sistema antes de empezar a crear registros en la base de datos. El sistema se usa a través de los comandos o herramientas que se describen en este documento.

## Acerca del Real Decreto 1007/2023
Publicado el 6 de diciembre de 2023, empieza con un preámbulo en el que alude a la "urgente adaptación" a la digitalización y a un "significativo ahorro de costes". Después encontramos los siguientes artículos de interés:

* Se modifica el [Real Decreto 1619/2012](https://www.boe.es/buscar/act.php?id=BOE-A-2012-14696) (que regula  las obligaciones de facturación) para incluir el requisito de poner un código QR con el "contenido parcial de la factura" en todas las facturas. Este código se añade para "incentivar al consumidor final para que solicite los comprobantes de sus operaciones y pueda remitir\[los\] voluntariamente a la Administración tributaria", lo que técnicamente es una denuncia.

* Se establece que los sistemas de facturación tienen que cumplir este Real Decreto **antes del 1 de julio de 2025**.

Y posteriormente pasa a detallar el Reglamento con los requisitos para los sistemas de facturación, donde destaco:

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

* El proveedor del sistema informático debe emitir una declaración responsable certificando que cumple con este reglamento. Nadie podrá dudar la casi ilimitada "capacidad de dinamizar con ello la modernización y digitalización de la gestión empresarial privada y la mejora del cumplimiento fiscal" de este requisito.

* Remitir los registros de facturación a la Agencia Tributaria es voluntario (hasta que se apruebe la ley de facturación electrónica). Por su parte, la Agencia Tributaria deberá tener listo el sistema de recepción el 6 de septiembre del 2024...

Como se ha visto, y a pesar de lo expuesto en el preámbulo, las acciones del RD 1007/2023 tienen el único objetivo de aumentar el control fiscal a costa de añadir otra carga reglamentaria a las empresas. En la práctica, las empresas que ya usan un software de facturación tendrán un impacto menor, mientras que los autónomos y pequeñas empresas acostumbradas a hacer facturas a mano o con un editor de texto, se verán obligados a comprar o contratar un sistema que cumpla con el reglamento.

En España hay unos 3 millones de autónomos y, haciendo una búsqueda rápida de software de facturación, se encuentran soluciones desde 10-15€ al mes. Si hacemos una estimación a la baja excluyendo a las pequeñas empresas y aceptando que el 50% de los autónomos ya utilicen un programa de facturación, el impacto del RD 1007/2023 se puede estimar en un gasto inútil de mínimo 180 millones de euros al año. Esto sin considerar la pérdida de tiempo que requiere seleccionar, contratar y utilizar un sistema de facturación ajeno al día a día del negocio (por ejemplo teniendo que registrar las facturas en la base de datos regularmente), sin que le aporte ningún valor para su actividad. Además, esta carga se le está imponiendo a los autónomos y empresas más pequeñas españolas. Aún así, el Real Decreto no tiene reparos en afirmar que se conseguirá "una mejora acelerada de la competitividad" y contribuirá a "una mayor igualdad ante la ley y a un reforzamiento de los principios de equidad y capacidad contributiva en el reparto de las cargas tributarias".

Por último, quiero destacar la tremenda ineficacia técnica del RD 1007/2023 de cara a conseguir los objetivos realmente buscados de reducir el fraude fiscal:
1. En primer lugar los sistemas informáticos almacenan su información en discos duros, que se usan precisamente por no son inalterables y permitir el tratamiento y modificación de los datos. Es decir que un segundo programa que quisiese modificar los datos siempre sería capaz de hacerlo y eso es inevitable.
2. Contra esto el RD 1007/2023 impone que los registros deben guardarse con una cadena de hashes y firmas, intentando imitar las blockchains. El problema es que la inalterabilidad que consiguen las blockchains no se puede lograr sin la red de nodos y el sistema de consenso. En otras palabras, un software que quiera falsificar una factura podrá recalcular toda la cadena de hashes y firmas en unos pocos segundos.
3. Además, en mi opinión, nadie se dedicará a notificar a la Agencia Tributaria con las tickets que recibe. Primero porque es tedioso y no aporta nada al ciudadano, y segundo por la falta de privacidad que supone informar a Hacienda de los gastos que hace. Probablemente solo los propios funcionarios de la Agencia Tributaria se molestarán en hacerlo, quienes de hecho ya lo están haciendo mediante una app que hace una foto.
4. En cualquier caso, al no haberse definido un formato concreto de la información contenida en el código QR, estos códigos no permitirán automatizar la tarea de registrar facturas, resultando inservibles.

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
Fíjate que este proyecto no es una solución comercial, sino que es una base libre que permite crear un sistema mínimo fácilmente, por lo que no incluyo declaración responsable. Sin embargo, la declaración responsable no es más que un documento de texto en el que tú mismo puedes certificar que tu sistema cumple con los requisitos. Fíjate que la declaración debe contener toda la información indicada en el Artículo 13 del reglamento.

## Formato de la Base de Datos
La base de datos del registro de facturación se implementa sobre un directorio en el que se copian los documentos de las facturas y se crea y mantiene un fichero CSV (tabla en texto separado por comas).

Fíjate que la mayoría de los datos requeridos por el RD 1007/2023 ya se encuentran disponibles en el propio documento de una factura válida, que forma parte del registro (y del hash). El resto se guardan en un CSV llamado `bd.csv` junto con la cadena de hashes y firmas electrónicas. El algoritmo utilizado para el hash es el SHA256, y para la firma electrónica es la curva elíptica SECP256R1, ambos considerados seguros a la fecha de escritura.

