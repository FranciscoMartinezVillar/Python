# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Nombre:       GestordeBateriaIFTTT.py
# Autor:        Miguel Andres Garcia Niño y Francisco Martinez Villar
# Creado:       18 de Mayo 2018
# Modificado:   18 de Mayo 2018
# Copyright:    (c) 2018 by Miguel Andres Garcia Niño, 2018
# License:      Apache License 2.0
# ----------------------------------------------------------------------------

#__versión__ = "1.0"

"""
El módulo *GestordeBateria* permite ver el porcentaje de carga de la batería y si
está recibiendo carga.
 Francisco Martinez añade la funcionalidad de control de un SmartPlug a traves de un
 Webhook de IFTTT, para saber como usarlo ir a  https://ifttt.com/maker_webhooks

"""

from ctypes import Structure, wintypes, POINTER, windll, pointer, WinError
# importing time library 
import time
# importing the requests library 
import requests
# ===================== FUNCIÓN cargaBateria =======================

def cargaBateria():
   class ESTADO_ENERGIA_SISTEMA(Structure):
       _fields_ = [
           ("ACLineStatus", wintypes.BYTE),
           ("BatteryFlag", wintypes.BYTE),
           ("BatteryLifePercent", wintypes.BYTE),
           ]

   ESTADO_ENERGIA_SISTEMA_P = POINTER(ESTADO_ENERGIA_SISTEMA)

   GetSystemPowerStatus = windll.kernel32.GetSystemPowerStatus
   GetSystemPowerStatus.argtypes = [ESTADO_ENERGIA_SISTEMA_P]
   GetSystemPowerStatus.restype = wintypes.BOOL

   estado = ESTADO_ENERGIA_SISTEMA()
   if not GetSystemPowerStatus(pointer(estado)):
      raise WinError()

   cargador, carga = estado.ACLineStatus, estado.BatteryLifePercent
   return (cargador, carga)

        
# ==================== FUNCIÓN estadoBateria =======================

def estadoBateria():
   cargadorCarga = cargaBateria()
   cargador = cargadorCarga[0]
   carga = cargadorCarga[1]
   maxNivel = 80
   minNivel = 30
   if cargador == 0:
      print("La batería no esta recibiendo carga.")
      if carga <= minNivel:
         print("La carga de la batería está por debajo o igual al {}%, conectando el SmartPlug".format(minNivel))
         r = requests.get('https://maker.ifttt.com/trigger/{evento que conecta}/with/key/{yours key}')
      else:
         print("Carga de la batería: {}%.".format(carga))
         
   elif cargador == 1:
      print("La batería esta recibiendo carga.")
      if carga >= maxNivel:
         print("La carga de la batería está por encima o igual al {}%, desconectando el SmartPlug".format(maxNivel))
         r = requests.get('https://maker.ifttt.com/trigger/{evento que desconecta}/with/key/{yours key}')
 
         
      else:
         print("Carga de la batería: {}%.".format(carga))
   else:
      print("Este sistema solo funciona en ordenadores portatiles.")


# ======================== LLAMAR FUNCIÓN ==========================
# Bucle infinito gestionando la carga y descarga del ordenador
# Envia un webhooks a IFTTT y conecta y desconecta el SmartPlug

while True:
    estadoBateria()
    # Wait for 5 seconds
    time.sleep(30)
 
