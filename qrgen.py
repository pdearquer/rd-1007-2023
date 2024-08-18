#!/usr/bin/python3
#
# Generador de códigos QR para facturas.
#
import sys
import time
import qrcode

if len(sys.argv) != 2:
   print("Generador de códigos QR para facturas.")
   sys.exit("Uso: qrgen.py <imagen.png>")
salida = sys.argv[1]

datos = []

fecha_def = time.strftime("%d/%m/%Y")
fecha = input("Fecha de la factura [" + fecha_def + "]: ")
if fecha == "":
   datos.append(fecha_def)
else:
   datos.append(fecha)
   
numero = input("Número o código de factura [Omitir]: ")
if numero != "":
   datos.append(numero)

nif_emisor = input("NIF del emisor [Omitir]: ")
if nif_emisor != "":
   datos.append(nif_emisor)
   
nif_receptor = input("NIF del receptor [Omitir]: ")
if nif_receptor != "":
   datos.append(nif_receptor)
   
importe = input("Importe total en euros [Omitir]: ")
if importe != "":
   datos.append(importe)

texto = ",".join(datos)
img = qrcode.make(texto)
img.save(salida)

