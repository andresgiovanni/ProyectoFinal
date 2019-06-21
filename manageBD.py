import opJson
import config
import os
import logging
import sys
import RunCLI



def addProyecto(proyecto):
    estructura = {}
    if os.path.isfile(config.BDProyectos) == True:
#        estructura={"PROYECTO": proyecto, "SLAVE": "0", "VM1": {"NAME": "None", "IP": "0", "STATUS": "not created"}}
        estructura={"PROYECTO": proyecto, "SLAVE": "0" }
        if opJson.addLlave(config.BDProyectos,estructura,proyecto):
           return True
        else:
            return False
  
    else:
        return False

def addVM(proyecto,VM):
    estructura = {}
    if os.path.isfile(config.BDProyectos) == True:
        estructura={VM: {"IP": "0", "STATUS": "not created"}}
        if opJson.addLlave(config.BDProyectos,estructura,proyecto):
           return True
        else:
            return False
  
    else:
        return False


def modificarVM(proyecto,VM,IP,STATUS):
    estructura={}
    if not IP:
        IP=""
    if not STATUS:
        STATUS="not created"
    if os.path.isfile(config.BDProyectos) == True:
        estructura={VM: {"IP": IP, "STATUS": STATUS}}
        if opJson.modElemento(config.BDProyectos,proyecto,estructura):
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




   