#!/usr/bin/python3
#
# Anula (da de baja) una factura de la base de datos.
#
import sys
import facturas
import config
import os.path

from config import *

# Argumentos de entrada
fac_num = input("Introduce el número de factura: ")
if fac_num == "":
   sys.exit("Número de factura requerido.")

# Buscar el registro a eliminar y extraer los metadatos y ruta
facs = facturas.listaFacturas(crear_si_no_existe=False)
if facs is None:
   sys.exit("Base de datos no encontrada.")
fac = None
for f in facs:
   if f["Num"] == fac_num:
      fac = f
      break
if fac is None:
   sys.exit("Factura no encontrada.")

# Crear entrada en la base de datos
facturas.creaRegistro(facturas.OP_BAJA, fac["Documento"], fac["Fecha"], fac["Num"], False)
print("Factura anulada correctamente.")

