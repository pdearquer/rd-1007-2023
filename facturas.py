#
# Funciones comunes para la gestión de la base de datos.
#
import os
import csv
import time
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.exceptions import InvalidSignature
import re
import shutil
import config

OP_ALTA = "Alta"
OP_BAJA = "Baja"

CSV_DIR = os.path.join(config.DIR_BD, "bd.csv")
CSV_CABECERA = [ "FechaReg", "HoraReg","OpReg", "Documento", "FechaFac", "NumFac", "IdSoftware",
      "FechaFacPrev", "NumFacPrev", "HashPrev", "Hash", "Firma" ]

def creaBD():
   os.makedirs(config.DIR_BD, exist_ok=True)
   with open(CSV_DIR, "w", newline="") as fich:
      writer = csv.DictWriter(fich, fieldnames=CSV_CABECERA)
      writer.writeheader()

def listaRegistros(verifica = False, crear_si_no_existe = True):
   if not os.path.isdir(config.DIR_BD) or not os.path.isfile(CSV_DIR):
      if crear_si_no_existe:
         creaBD()
         return []
      else:
         return None

   regs = []
   prev_reg = None
   with open(CSV_DIR, "r", newline="") as fich:
      reader = csv.DictReader(fich)
      for reg in reader:
         regs.append(reg)
         
         if verifica:
            if prev_reg is not None:
               if reg["FechaFacPrev"] != prev_reg["FechaFac"] or reg["NumFacPrev"] != prev_reg["NumFac"] \
                     or reg["HashPrev"] != prev_reg["Hash"]:
                  print("ERROR: Cadena invalida en registro del " + reg["FechaReg"] + " a las " + reg["HoraReg"] + ".")
            hash_bin = calcHash(reg)
            if reg["Hash"] != hash_bin.hex().upper():
               print("ERROR: Hash invalido en registro del " + reg["FechaReg"] + " a las " + reg["HoraReg"] + ".")
            elif not verificaFirma(bytes.fromhex(reg["Firma"]), hash_bin):
               print("ERROR: Firma electrónica invalida en el registro del " + reg["FechaReg"] + " a las " + reg["HoraReg"] + ".")
            prev_reg = reg

   return regs

def listaFacturas(verifica = False, crear_si_no_existe = True):
   regs = listaRegistros(verifica, crear_si_no_existe)
   if regs is None or len(regs) == 0:
      return regs
   
   facs = []
   for reg in regs:
      fac = None
      for f in facs:
         if f["Num"] == reg["NumFac"]:
            fac = f
            break
      evento = {}
      evento["Fecha"] = reg["FechaReg"]
      evento["Hora"] = reg["HoraReg"]
      evento["Op"] = reg["OpReg"]
   
      if reg["OpReg"] == OP_ALTA:
         if fac is not None:
            if fac["Estado"] != OP_BAJA:
               print("ERROR: Factura " + fac["Num"] + " dada de alta más de una vez.")
            else:
               fac["Eventos"].append(evento)
               fac["Estado"] = OP_ALTA
               # Prevalecen los detalles del último alta
               fac["Fecha"] = reg["FechaFac"]
               fac["Num"] = reg["NumFac"]
               fac["Documento"] = reg["Documento"]
         else:
            fac = {}
            fac["Fecha"] = reg["FechaFac"]
            fac["Num"] = reg["NumFac"]
            fac["Documento"] = reg["Documento"]
            fac["Eventos"] = [ evento ]
            fac["Estado"] = OP_ALTA
            facs.append(fac) 
      elif reg["OpReg"] == OP_BAJA:
         if fac is None or fac["Estado"] != OP_ALTA:
            print("ERROR: Factura " + reg["NumFac"] + " dada de baja sin estar dada de alta.")
         else:
            fac["Eventos"].append(evento)
            fac["Estado"] = OP_BAJA
      else:
         print("ERROR: Operación de entrada del " + reg["FechaReg"] + " a las " + reg["HoraReg"] + " no soportada.")
   
   def ordena_por_fecha(fac):
      return time.strptime(fac["Fecha"], "%d/%m/%Y")
   facs.sort(key=ordena_por_fecha)
   
   return facs

def calcHash(reg, doc_ruta = None):
   if doc_ruta is None:
      doc_ruta = os.path.join(config.DIR_BD, reg["Documento"])
   with open(doc_ruta, mode = "rb") as file:
      doc_datos = file.read()

   hasher = hashes.Hash(hashes.SHA256())
   hasher.update(reg["FechaReg"].encode("UTF-8"))
   hasher.update(reg["HoraReg"].encode("UTF-8"))
   hasher.update(reg["OpReg"].encode("UTF-8"))
   hasher.update(doc_datos)
   hasher.update(reg["FechaFac"].encode("UTF-8"))
   hasher.update(reg["NumFac"].encode("UTF-8"))
   hasher.update(reg["IdSoftware"].encode("UTF-8"))
   hasher.update(reg["FechaFacPrev"].encode("UTF-8"))
   hasher.update(reg["NumFacPrev"].encode("UTF-8"))
   hasher.update(reg["HashPrev"].encode("UTF-8"))
   return hasher.finalize()

def calcFirma(hash_bin):
   curva = ec.SECP256R1()
   ec_priv = ec.derive_private_key(int(config.CLAVE_FIRMA, 0), curva, default_backend())	
   firma_der = ec_priv.sign(hash_bin, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
   firma_dec = utils.decode_dss_signature(firma_der)
   return firma_dec[0].to_bytes(32, "big") + firma_dec[1].to_bytes(32, "big")

def verificaFirma(firma_bin, hash_bin):
   curva = ec.SECP256R1()
   ec_priv = ec.derive_private_key(int(config.CLAVE_FIRMA, 0), curva, default_backend())	
   ec_pub = ec_priv.public_key()
   firma_der = utils.encode_dss_signature(int.from_bytes(firma_bin[:32], "big"), int.from_bytes(firma_bin[32:], "big"))
   try:
      ec_pub.verify(firma_der, hash_bin, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
   except InvalidSignature:
      return False
   return True

def creaRegistro(op, doc_ruta, fac_fecha, fac_num, copiar_doc=True):
   # Crear campos del registro
   reg = {}
   fecha_reg = time.localtime()
   reg["FechaReg"] = time.strftime("%d/%m/%Y", fecha_reg)
   reg["HoraReg"] = time.strftime("%H:%M:%S", fecha_reg)
   reg["OpReg"] = op
   if copiar_doc:
      fac_fecha_struc = time.strptime(fac_fecha, "%d/%m/%Y")
      doc_nombre = time.strftime("%Y.%m.%d", fac_fecha_struc) + " " + re.sub(r"\W", "_", fac_num) \
            + " " + time.strftime("%Y%m%d%H%M%S", fecha_reg) + os.path.splitext(doc_ruta)[1]
      reg["Documento"] = doc_nombre
   else:
      reg["Documento"] = doc_ruta
      doc_ruta = os.path.join(config.DIR_BD, doc_ruta)
   reg["FechaFac"] = fac_fecha
   reg["NumFac"] = fac_num
   reg["IdSoftware"] = config.SOFTWARE_CODE
   
   # Buscar un registro anterior y extraer los metadatos
   regs = listaRegistros()
   if len(regs) == 0:
      reg["FechaFacPrev"] = ""
      reg["NumFacPrev"] = ""
      reg["HashPrev"] = ""
   else:
      prev_reg = regs[-1]
      reg["FechaFacPrev"] = prev_reg["FechaFac"]
      reg["NumFacPrev"] = prev_reg["NumFac"]
      reg["HashPrev"] = prev_reg["Hash"]

   # Calcular hash y firma del registro
   hash_bin = calcHash(reg, doc_ruta)
   reg["Hash"] = hash_bin.hex().upper()
   reg["Firma"] = calcFirma(hash_bin).hex().upper()
   
   # Guardar entrada
   if copiar_doc:
      shutil.copyfile(doc_ruta, os.path.join(config.DIR_BD, reg["Documento"]))
   with open(CSV_DIR, "a", newline="") as fich:
      writer = csv.DictWriter(fich, fieldnames=CSV_CABECERA)
      writer.writerow(reg)

