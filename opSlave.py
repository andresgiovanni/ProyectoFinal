#!/usr/bin/env python

import config
import os
import threading
import logging
import sys
import RunCLI
import opJson, json


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
def enviarVM(proyecto,slave):
    comando="curl -F file=@" + config.VAGRANTSERVICEHOME + proyecto + "/Vagrantfile" + " http://" + slave + ":" + config.SLAVE1PORT +"/CrearProyecto/" + proyecto
    logger.warning('Ingresando a enviarVM')
    try:
#        Cmd= "echo 'en ejecucion..:' " + comando + " >> " + config.MSGlog 
        logger.warning('Ejecutando..' + comando)
#        myCmd = os.popen(Cmd).read()
        output=RunCLI.runCommand(comando)
       
    except Exception as e:
#        logger.warning(sys.exc_info()[1])
        logger.error(sys.exc_info()[1])


#Metodo de envio consulta de estado proyecto al esclavo
#comando="curl http://192.168.19.251:8000/StatusProyecto/andres" 
def preguntarEstadoProyecto(proyecto,slave):
    comando="curl http://" + slave + ":" + config.SLAVE1PORT + "/StatusProyecto/" + proyecto
    logger.warning('Ingresando a preguntarEstadoProyecto')
    try:
#        Cmd= "echo 'en ejecucion..:' " + comando + " >> " + config.MSGlog 
#        myCmd = os.popen(Cmd).read()
        logger.warning('Ejecutando..' + comando)
        output=RunCLI.runCommand(comando)
        opJson.escribirJson(config.MSGSlave,proyecto,output) 

    except Exception as e:
#        logger.warning(sys.exc_info()[1])
        logger.error(sys.exc_info()[1])


#Metodo de envio solicitud borrado proyecto al esclavo
#comando="curl http://192.168.19.251:8000/BorrarProyecto/andres" 
def enviarBorrarProyecto(proyecto,slave):
    comando="curl http://" + slave + ":" + config.SLAVE1PORT + "/BorrarProyecto/" + proyecto
    logger.warning('Ingresando a enviarBorrarProyecto')
    try:
        logger.warning('Ejecutando..' + comando)
        output=RunCLI.runCommand(comando)
        opJson.escribirJson(config.MSGSlave,proyecto,output)       
    except Exception as e:
        logger.error(sys.exc_info()[1])



#Metodo de envio solicitud levantar VM de un proyecto al esclavo
#comando="curl http://192.168.19.251:8000/LevantarVM/andres/VM" 
def enviarLevantarVM(proyecto,VM,slave):
    comando="curl http://" + slave + ":" + config.SLAVE1PORT + "/LevantarVM/" + proyecto + "/" + VM
    logger.warning('Ingresando a enviarLevantarVM')
    try:
        logger.warning('Ejecutando..' + comando)
        output=RunCLI.runCommand(comando)
        opJson.escribirJson(config.MSGSlave,proyecto,output)       
    except Exception as e:
        logger.error(sys.exc_info()[1])        