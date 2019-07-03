#!/usr/bin/env python

import config
import os
import threading
import logging
import sys
import RunCLI
import opJson, json, manageBD


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


   
#Metodo de envio creacion Proyecto a esclavo
#comando="curl -F file=@/home/admred/Documentos/vagrant/andres/Vagranfile http://192.168.19.251:8000/CrearProyecto/andres"
def enviarVM(proyecto,slave,port):
    logger.warning('Ingresando a enviarVM')
    
    try:
        comando="curl -F file=@" + config.VAGRANTSERVICEHOME + proyecto + "/Vagrantfile" + " http://" + slave + ":" + str(port) + "/CrearProyecto/" + proyecto
        logger.warning('Ejecutando..' + comando)
        output=RunCLI.runCommand(comando)
        opJson.escribirJson(config.MSGSlave,proyecto,output) 

    except Exception as e:
        logger.error(sys.exc_info()[1])


#Metodo de envio consulta de estado proyecto al esclavo
#comando="curl http://192.168.19.251:8000/StatusProyecto/andres" 
def preguntarEstadoProyecto(proyecto,slave, port):
    comando="curl http://" + slave + ":" + str(port) + "/StatusProyecto/" + proyecto
    logger.warning('Ingresando a preguntarEstadoProyecto')
    try:
        logger.warning('Ejecutando..' + comando)
        output=RunCLI.runCommand(comando)
        opJson.escribirJson(config.MSGSlave,proyecto,output) 
#del mensaje del slave se saca la info del estado de cada virtual
        data=opJson.abrirArchivo(config.MSGSlave)
        if proyecto in data:
            for VM,atributo in data[proyecto]["VMs"].items():
                logger.warning('Ahora se modificara la BD de proyecto')
                manageBD.modificarVM(proyecto,VM,atributo)
    except Exception as e:
        logger.error(sys.exc_info()[1])


#Metodo de envio solicitud borrado proyecto al esclavo
#comando="curl http://192.168.19.251:8000/BorrarProyecto/andres" 
def enviarBorrarProyecto(proyecto,slave, port):
    comando="curl http://" + slave + ":" + str(port) + "/BorrarProyecto/" + proyecto
    logger.warning('Ingresando a enviarBorrarProyecto')
    try:
        logger.warning('Ejecutando..' + comando)
        output=RunCLI.runCommand(comando)
        opJson.escribirJson(config.MSGSlave,proyecto,output)       
    except Exception as e:
        logger.error(sys.exc_info()[1])



#Metodo de envio solicitud levantar VM de un proyecto al esclavo
#comando="curl http://192.168.19.251:8000/LevantarVM/andres/VM" 
def enviarLevantarVM(proyecto,VM,slave, port):
    comando="curl http://" + slave + ":" + str(port) + "/LevantarVM/" + proyecto + "/" + VM
    logger.warning('Ingresando a enviarLevantarVM')
    try:
        logger.warning('Ejecutando..' + comando)
        output=RunCLI.runCommand(comando)
        opJson.escribirJson(config.MSGSlave,proyecto,output)
    except Exception as e:
        logger.error(sys.exc_info()[1])        




#Metodo de envio solicitud apagar VM de un proyecto al esclavo
#comando="curl http://192.168.19.251:8000/ApagarVM/andres/VM" 
def enviarApagarVM(proyecto,VM,slave, port):
    comando="curl http://" + slave + ":" + str(port) + "/ApagarVM/" + proyecto + "/" + VM
    logger.warning('Ingresando a enviarApagarVM')
    try:
        logger.warning('Ejecutando..' + comando)
        output=RunCLI.runCommand(comando)
        opJson.escribirJson(config.MSGSlave,proyecto,output)

    except Exception as e:
        logger.error(sys.exc_info()[1])   


#Metodo de envio solicitud borrar VM de un proyecto al esclavo
#comando="curl http://192.168.19.251:8000/ApagarVM/andres/VM" 
def enviarBorrarVM(proyecto,VM,slave, port):
    comando="curl http://" + slave + ":" + str(port) + "/BorrarVM/" + proyecto + "/" + VM
    logger.warning('Ingresando a enviarApagarVM')
    try:
        logger.warning('Ejecutando..' + comando)
        output=RunCLI.runCommand(comando)
        opJson.escribirJson(config.MSGSlave,proyecto,output)       
    except Exception as e:
        logger.error(sys.exc_info()[1])   



def consultarSlaveRAM():
    if os.path.isfile( config.BDSlave ) == True:
        try:
            slave=opJson.abrirArchivo( config.BDSlave )
            for key, atributos in slave.items():
                comando='curl http://' + key + ':' + str(atributos['Port']) + '/ObtenerRAM'
                logger.warning('Ejecutando..' + comando)
                output=RunCLI.runCommand(comando)
                opJson.escribirJson(config.MSGSlaveStatus,key,output)
                data=opJson.abrirArchivo(config.MSGSlaveStatus)
                manageBD.modificarSlaveRAM(key, data[str(key)]['MemFree'])
                return True
        except Exception as e:
            logger.error(sys.exc_info()[1])  
            
            

