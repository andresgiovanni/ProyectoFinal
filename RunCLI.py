#!/usr/bin/env python
#
# Este script en Python implementa una funcion llamada runCommand que recibe
# como argumento una cadena que representa una ejecucion de un comando regular
# en el shell y retorna la salida de la ejecucion de dicho comando. El objetivo
# de esta funcion es procesar aquellas lineas de comando que tienen el simbolo 
# 'pipe' o '|'.
#
# Author: John Sanabria - john.sanabria@gmail.com
# Date: 2019_05_17
#
#
import subprocess
import re

#
# Esta funcion elimina los espacios adicionales que contenga una linea de 
# comando que se quiere ejecutar desde el shell. Por ejemplo una linea de 
# comando como esta "    ls    -l     README.md   " la convierte en 
# "ls -l README.md"
#
def subprocesos(command,sep="|"):
  command = re.sub(' +', ' ', command).strip()
  return command.split(sep)

#
# Esta es la funcion "core" y es la que se encarga de recibir una lista de
# comandos en Unix y donde cada comando no tiene un '|'. 
#
# Ejemplo, si se ingresa el comando "ls -la | grep README"; esta funcion recibe
# una lista que contiene [ "ls -la", "grep README" ]. Esta funcion de forma
# recursiva procesa cada comando y se asegura que la salida del comando mas a
# la izquierda sea la entrada del comando a la derecha.
#
def runPipe(subprocesos, prevEntry = None):
  if (len(subprocesos) == 1):
    if (prevEntry is None):
      return subprocess.check_output(subprocesos[0].strip().split(' '))
    else:
      ps = subprocess.Popen(subprocesos[0].strip().split(' '), stdin = prevEntry.stdout, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
      prevEntry.stdout.close()
      out, err = ps.communicate()
      return out
  if (prevEntry is None):
    ps = subprocess.Popen(subprocesos[0].strip().split(' '), stdout = subprocess.PIPE)
  else:
    ps = subprocess.Popen(subprocesos[0].strip().split(' '), stdin = prevEntry.stdout, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    prevEntry.stdout.close()
  return runPipe(subprocesos[1:],ps)

#
# Esta funcion integra las dos funciones anteriores. Recibe como argumento una
# linea de comando arbitraria en Unix, la procesa y devuelve la cadena de 
# caracteres que representa la salida de ejecucion de dicho comando.
#
def runCommand(command):
  return runPipe(subprocesos(command)).decode("utf-8")

#
# Pruebas
#
command = "   ls     -la     "
print("[1] %s"%runCommand(command))

command = "ls -la | grep README | grep May | grep vagrant| grep XXX | grep 123 "
print("[2] %s"%runCommand(command))

command = "ls -la | grep README | grep May | grep vagrant"
print("[3] %s"%runCommand(command))
