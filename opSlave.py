#!/usr/bin/env python

import config
import os
import threading
import logging
import sys
import RunCLI
import opJson


# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
d_handler = logging.FileHandler(config.FILELOG)
f_handler = logging.FileHandler(config.FILELOG)

c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)
d_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
d_format = logging.Formatter('[%(levelname)s] - %(threadName)-10s : %(message)s')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
d_handler.setFormatter(d_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.addHandler(d_handler)

   
#Metodo de envio creacion Proyecto a esclavo
def enviarVM(proyecto,slave):
#comando="curl -F file=@/home/admred/Documentos/vagrant/andres/Vagranfile http://192.168.19.251:8000/CrearProyecto/andres"
    comando="curl -F file=@" + config.VAGRANTSERVICEHOME + proyecto + "/Vagrantfile" + " http://" + slave + ":" + config.SLAVE1PORT +"/CrearProyecto/" + proyecto
    logger.debug('Ingresando a enviarVM')
    try:
#        Cmd= "echo 'en ejecucion..:' " + comando + " >> " + config.MSGlog 
        logger.debug('Ejecutando..' + comando)
#        myCmd = os.popen(Cmd).read()
        output=RunCLI.runCommand(comando)
       
    except Exception as e:
        logger.warning(sys.exc_info()[1])
        logger.error(sys.exc_info()[1])


#Metodo de consulta estado proyecto a esclavo
def enviarEstadoProyecto(proyecto,slave):
#comando="curl http://192.168.19.251:8000/StatusProyecto/andres" 
    comando="curl http://" + slave + ":" + config.SLAVE1PORT + "/StatusProyecto/" + proyecto
    logger.debug('Ingresando a enviarEstadoProyecto')
    try:
#        Cmd= "echo 'en ejecucion..:' " + comando + " >> " + config.MSGlog 
#        myCmd = os.popen(Cmd).read()
        logger.debug('Ejecutando..' + comando)
        output=RunCLI.runCommand(comando)
        return output

    except Exception as e:
        logger.warning(sys.exc_info()[1])
        logger.error(sys.exc_info()[1])