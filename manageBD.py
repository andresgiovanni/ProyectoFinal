import opJson
import config
import os
import logging
import sys
import RunCLI



def addProyecto(proyecto):
    llave = {}
    if os.path.isfile(config.BDProyectos) == True:
        llave={"PROYECTO": proyecto, "SLAVE": "0", "VM1": {"NAME": "None", "IP": "0", "STATUS": "not created"}}
        if opJson.addLlave(config.BDProyectos,llave,proyecto):
           return True
        else:
            return False
  
    else:
        return False


def buscarProyecto(llave):
    if os.path.isfile(config.BDProyectos) == True:
        data=opJson.abrirArchivo(config.BDProyectos)
        if llave in data.keys():
            return True
        else:
            return False


def rmProyecto(proyecto):
    llave=proyecto
    if opJson.removeLLave(config.BDProyectos,llave):
        return True
    else:
        return False




   