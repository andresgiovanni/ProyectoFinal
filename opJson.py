#!/usr/bin/env python

import json
import os, logging


# Este metodo recibe un nombre de archivo y devuelve un diccionario que contiene
# informacion asociada a un archivo JSON
def abrirArchivo(f):
  with open(f,"r") as json_file:
    return json.load(json_file)


# Esta es una funcion mas generica que dado un diccionario y la llave entrega
# el valor asociado a esa llave
def leerLlave(j,key):
  return j[key]



#Metodo generico para escribir en archivo Json una estructura en formato JSON
def escribirJson(f,llave,obj):
  data = {}
  logging.warning(obj)
  with open(f, "w") as json_file:
    data[llave]=json.loads(obj)
    json.dump(data, json_file, indent=4)
    json_file.close()  



#Metodo generico para verificar que archivo json existente
def verificarJson(ruta,f):
  if os.path.isdir(ruta):
    if os.path.isfile(f) == True:
      return True
    else:
      return False
  else:
    return False    

#Metodo generico para adicionar key a un archivo json existente
def addLlave(f,estructura,nombre):
  data = {}
  if os.stat(f).st_size > 0:
    data = abrirArchivo(f)
#  obj=json.loads(llave)
  if nombre not in data:
    with open(f, "w") as json_file:
      data[nombre]=estructura
      json.dump(data, json_file, indent=4)
      json_file.close()
    return True
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