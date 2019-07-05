#Libreria con Métodos para gestión de BD

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

#Metodo usado para adicionar proyecto a la BD
#
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

#Metodo usado para borrar un proyecto de la BD
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

#Metodo usado para modificar la BD, adicionando VM a un proyecto
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

#Metodo usado para modificar la BD, modifica atributos VM de un proyecto
#parametros obj corresponde a los atributos en formato JSON que se adicionaran
def modificarVM(proyecto,VM,obj):
    estructura={}
#    if not IP:
#        IP=""
#    if not STATUS:
#        STATUS="not created"
    if os.path.isfile(config.BDProyectos) == True:
        estructura['VMs']={VM: obj}
        if opJson.modElemento(config.BDProyectos,proyecto,estructura):
           return True
        else:
            return False
  
    else:
        return False

#Metodo para consultar si existe proyecto en la BD
#parametro llave corresponde al nombre del proyecto
def existeProyecto(llave):
    if os.path.isfile(config.BDProyectos) == True:
        data=opJson.abrirArchivo(config.BDProyectos)
        if llave in data.keys():
            return True
        else:
            return False

#Metodo que devuelve atributos de un proyecto almancenado en BD
#parametro llave corresponde al nombre del proyecto
def getProyecto(llave):
    data={}
    if os.path.isfile(config.BDProyectos) == True:
        if existeProyecto(llave):
            data=opJson.leerLlave(config.BDProyectos,llave)
            return data
        else:
            return data

#Metodo usado para modificar la BD, modifica atributos RAM de un host tipo Slave  
def modificarSlaveRAM(slave,RAM):
    if os.path.isfile(config.BDSlave) == True:
       data=opJson.leerLlave(config.BDSlave,slave)
       if data:
            data['MemLibre']=int(RAM)
            if opJson.addLlave( config.BDSlave, data, slave ):
                return True
            else:
                return False
       else:
            return False


#Metodo para seleccionar slave al que se le asignara
# un proyecto. La seleccion se realiza basado en Memoria  y cantidad
#de proyecto =4
def seleccionarSlave():
    slave={}
    memoria=0
    cantProyecto=4
    Proyectos=0
    if os.path.isfile( config.BDSlave ) == True:
        data=opJson.abrirArchivo( config.BDSlave )
        for key,estructura in data.items():
            if estructura and 'MemLibre' in estructura.keys():
                if estructura['MemLibre'] > memoria and estructura['Proyectos'] <= cantProyecto:
                    memoria=estructura['MemLibre']
                    cantProyecto=estructura['Proyectos']
                    slave={ "id": key, "IP": estructura['IP'], "Port": estructura["Port"]}
        return slave
    return slave
   

#Metodo para adicionar a la BD un host tipo SLAVE
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

#Metodo para retornar un host tipo slave de la BD
def buscarSlave(llave):
    data={}
    if os.path.isfile(config.BDSlave) == True:
        data=opJson.leerLlave(config.BDSlave,llave)
        return data
    else:
        return data


#Metodo para obtener la ip del slave, recibe el id del slave
def getIpSlave(slave):
    data={}
    if os.path.isfile(config.BDSlave) == True:
        if existeProyecto(llave):        
            data=opJson.leerLlave(config.BDSlave, slave )
            return data['IP']
        else:
            return ''
    else:
        return ''
