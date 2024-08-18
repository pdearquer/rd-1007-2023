#!/usr/bin/python3
#
# Muestra las facturas de la base de datos y verifica su integridad.
#
import sys
import facturas

# Argumentos de entrada
verificar = False
if len(sys.argv) == 2:
   if sys.argv[1] == "-v":
      verificar = True
   else:
      sys.exit("Uso: verfacs.py [-v]")
elif len(sys.argv) != 1:
   sys.exit("Uso: verfacs.py [-v]")

# Leer y mostrar base de datos
facs = facturas.listaFacturas(verificar, False)
if facs is None:
   sys.exit("Base de datos no encontrada.")
if len(facs) == 0:
   sys.exit("La base de datos no contiene ningún registro.")

for fac in facs:
   estado = "[\u2713]"
   if fac["Estado"] == facturas.OP_BAJA:
      estado = "[x]"
   eventos = fac["Eventos"]
   print(estado + " " + fac["Fecha"] + " " + fac["Num"] + ": Dada de alta el " + eventos[0]["Fecha"] + " a las " + eventos[0]["Hora"])
   for i in range(1, len(eventos)):
      op = "baja"
      if eventos[i]["Op"] == facturas.OP_ALTA:
         op = "alta"
      print("   Dada de " + op + " el " + eventos[i]["Fecha"] + " a las " + eventos[i]["Hora"])

