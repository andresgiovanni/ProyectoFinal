import opJson
import config
import os
import logging
import sys
import RunCLI
import logging

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

def addProyecto(proyecto, slave):
    estructura = {}
    if os.path.isfile(config.BDProyectos) == True:
#        estructura={"PROYECTO": proyecto, "SLAVE": "0", "VM1": {"NAME": "None", "IP": "0", "STATUS": "not created"}}
        estructura={"PROYECTO": proyecto, "SLAVE": slave }
        if opJson.addLlave(config.BDProyectos,estructura,proyecto):
            data={}
            data=opJson.leerLlave(config.BDSlave,slave)
            if data:
                data['Proyectos']=data['Proyectos'] + 1
                if opJson.addLlave( config.BDSlave, data, slave ):
                    return True
        else:
            
            return False
  
    else:
        return False


def rmProyecto(proyecto, slave):
    llave=proyecto
    if opJson.removeLLave(config.BDProyectos,llave):
        data={}
        data=opJson.leerLlave(config.BDSlave,slave)
        if data:
            data['Proyectos']=data['Proyectos'] - 1
            if opJson.addLlave( config.BDSlave, data, slave ):
                return True        
    else:
        return False


def addVM(proyecto,VM, slave):
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

def getProyecto(llave):
    data={}
    if os.path.isfile(config.BDProyectos) == True:
        if buscarProyecto(llave):
            data=opJson.leerLlave(config.BDProyectos,llave)
            return data
        else:
            return data



#Metodo para seleccionar slave al que se le asignara
# un proyecto. La seleccion se realiza basado en Memoria        
def seleccionarSlave():
    slave={}
    memoria=0
    Proyectos=0
    if os.path.isfile( config.BDSlave ) == True:
        data=opJson.abrirArchivo( config.BDSlave )
        for key,estructura in data.items():
            if estructura and 'MemLibre' in estructura.keys():
                if estructura['MemLibre'] > memoria:
                    memoria=estructura['MemLibre']
                    slave={ "id": key, "IP": estructura['IP']}
        return slave
    return slave
   


def addSlave( slave, name, mem, port ):
    #estructura = {}
    if os.path.isfile( config.BDSlave ) == True:
        logger.warning('ingresando a addslave')
        estructura={"Nombre": name, "MemLibre": mem, "Port": port, "Proyectos": 0, "IP": slave}
        if opJson.addLlave(config.BDSlave, estructura, slave):
            return True
        else:
            return False
    else:
        return False


def buscarSlave(llave):
    if os.path.isfile(config.BDSlave) == True:
        data=opJson.abrirArchivo(config.BDSlave)
        if llave in data.keys():
            return True
        else:
            return False

#Metodo para obtener la ip del slave, recibe el id del slave
def getIpSlave(slave):
    data={}
    if os.path.isfile(config.BDSlave) == True:
        if buscarProyecto(llave):        
            data=opJson.leerLlave(config.BDSlave, slave )
            return data['IP']
        else:
            return ''
    else:
        return ''