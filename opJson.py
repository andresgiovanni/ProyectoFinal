#!/usr/bin/env python

import json, config
import os, logging, threading, sys


# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.FileHandler(config.FILELOG)
f_handler = logging.FileHandler(config.FILELOG)


c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)


# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)


# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)


# Este metodo recibe un nombre de archivo y devuelve un diccionario que contiene
# informacion asociada a un archivo JSON
def abrirArchivo(f):
  try:
    with open(f,"r") as json_file:
      return json.load(json_file)
  except Exception as e:
    logger.error(sys.exc_info()[1])


# Esta es una funcion mas generica que dado un diccionario y la llave entrega
# el valor asociado a esa llave
def leerLlave(f,key):
  data=abrirArchivo(f)
  try:
    if key in data.keys():
      return data[key]
    else:
      data={}
      return data
  except Exception as e:
    logger.error(sys.exc_info()[1])
  

#Metodo generico para escribir en archivo Json una estructura en formato JSON
def escribirJson(f,llave,obj):
  data = {}
  with open(f, "w") as json_file:
    data[llave]=json.loads(obj)
    json.dump(data, json_file, indent=4)
    json_file.close()  


def limpiarJson(f):
  data={}
  try:
    data = abrirArchivo(f)
    for llave in data.keys():
      del data[llave]
    with open(f, "w") as json_file:
      json.dump(data, json_file, indent=4)
      json_file.close()
      return True
  except Exception as e:
    logger.error(sys.exc_info()[1])
    escribirJson(f,'master','{}')
    limpiarJson(f)


#Metodo generico para verificar que archivo json existente
def verificarJson(ruta,f):
  if os.path.isdir(ruta):
    if os.path.isfile(f) == True:
      return True
    else:
      return False
  else:
    return False    



#Metodo generico para remover key a un archivo json existente
def removeLLave(f,llave):
  data = {}
  data = abrirArchivo(f)
  if llave in data:
    del data[llave]
    with open(f, "w") as json_file:
      json.dump(data, json_file, indent=4)
      json_file.close()
    return True
  else:
    return False  



#Metodo generico para obtener valor de un elemento
def getElemento(f,llave,elemento):
    if os.path.isfile(f) == True:
        data=abrirArchivo(f)
        if llave in data.keys():
            return True
        else:
            return False

#Metodo generico para adicionar key a un archivo json existente
def addLlave(f,estructura,nombre):
  data = {}
  if os.stat(f).st_size > 0:
    data = abrirArchivo(f)
  with open(f, "w") as json_file:
    if nombre not in data:
      data[nombre]=estructura
      json.dump(data, json_file, indent=4)
      json_file.close()
      return True
    else:
      logger.warning('ingresando a addLLave')
      data[nombre].update(estructura)
      json.dump(data, json_file, indent=4)
      json_file.close()
      return True



def modElemento(f,llave,estructura):
  data = {}
  if os.stat(f).st_size > 0:
    data = abrirArchivo(f)
  with open(f, "w") as json_file:
  #  obj=json.loads(llave)
    if llave not in data:
      return False
    else:
      logger.warning('Modificando Elemento Json..')
      data[llave].update(estructura)
      json.dump(data, json_file, indent=4)
      json_file.close()
      return True

#Metodo Generico para modificar valor de un elemento de una key particular
#Por ejemplo una key puede ser un proyecto y el elemento la ip del slave
#f=archivo json, elemento= elemento a modificar
def modElementoNivel1(f,llave,elemento,valor):
  data = {}
  data = abrirArchivo(f)
  if llave in data:
    data[llave][elemento]=valor
    with open(f, "w") as json_file:
      json.dump(data, json_file, indent=4)
      json_file.close()
    return True  
  else:
    return False


def modElementoNivel2(f,llave,elemento1,elemento2,valor):
  data = {}
  data = abrirArchivo(f)
  if llave in data:
    data[llave][elemento1][elemento2]=valor
    with open(f, "w") as json_file:
      json.dump(data, json_file, indent=4)
      json_file.close()
    return True  
  else:
    return False