#!/usr/bin/env python

import json
import os


# Este metodo recibe un nombre de archivo y devuelve un diccionario que contiene
# informacion asociada a un archivo JSON
def abrirArchivo(f):
  with open(f,"r") as json_file:
    return json.load(json_file)


# Esta es una funcion mas generica que dado un diccionario y la llave entrega
# el valor asociado a esa llave
def leerLlave(j,key):
  return j[key]


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
def addLlave(f,key):
  data = {}
  data = abrirArchivo(f)
  with open(f, "w") as json_file:
    data[key]=key
    json.dump(data, json_file, indent=4)
    json_file.close()
    return True


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


#Metodo Generico para modificar valor de un elemento de una key particular
#Por ejemplo una key puede ser un proyecto y el elemento la ip del slave
#f=archivo json, elemento= elemento a modificar
def modElemento(f,llave,elemento,valor):
  data = {}
  data = abrirArchivo(f)
  if llave in data:
    data[llave][0][elemento]=valor
    with open(f, "w") as json_file:
      json.dump(data, json_file, indent=4)
      json_file.close()
    return True  
  else:
    return False