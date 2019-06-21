#!/usr/bin/env python
from flask import Flask, jsonify, request
import RunCLI
import config
import os
import threading
import logging
import sys
import opSlave
import opJson
import manageBD
import time


app = Flask(__name__)

#virtualenv venv
#. venv/bin/activate
#pip install Flask
#export FLASK_APP=Master.py
#export FLASK_ENV=development
#flask run



#Metodo para ordenar creacion de VM habiendo subido inicialmente
#un archivo vagranfile
@app.route("/crearProyecto/<proyecto>")
def crearProyecto(proyecto):
    ruta= config.VAGRANTSERVICEHOME + proyecto   
    if os.path.isdir(ruta):
        opJson.limpiarJson(config.MSGSlave)
        thread1= threading.Thread(target = opSlave.enviarVM, args=(proyecto,config.VAGRANTSLAVE1))
        thread1.start()
#        thread1.join()
        while os.stat(config.MSGSlave).st_size == 0:
            time.sleep(5)

        manageBD.addProyecto(proyecto)    
        return  jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify("Error 400, no se ha subido VagranFile")    


#Metodo para consultar estado de un proyecto
@app.route("/estadoProyecto/<proyecto>")
def estadoProyecto(proyecto):
    if manageBD.buscarProyecto(proyecto)==True:
        opJson.limpiarJson(config.MSGSlave)
        thread2= threading.Thread(target = opSlave.preguntarEstadoProyecto, args=(proyecto,config.VAGRANTSLAVE1))
        thread2.start()
#        thread2.join()
        while os.stat(config.MSGSlave).st_size == 0:
            time.sleep(3)
        while len(opJson.abrirArchivo(config.MSGSlave))==0:
            time.sleep(3)

#del mensaje del slave se saca la info del estado de cada virtual
#        data=opJson.abrirArchivo(config.MSGSlave)
#        if proyecto in data:
#            for VM,atributo in data[proyecto][0]["VMs"].items():
#                manageBD.modificarVM(proyecto,VM,"",atributo["Status"])

        return jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify("Error 400, el proyecto no existe")


#Metodo para Borrar un proyecto
@app.route("/borrarProyecto/<proyecto>")
def borrarProyecto(proyecto):
    if manageBD.buscarProyecto(proyecto)==True:
        opJson.limpiarJson(config.MSGSlave)
        thread3= threading.Thread(target = opSlave.enviarBorrarProyecto, args=(proyecto,config.VAGRANTSLAVE1))
        thread3.start()
#        thread3.join()
        while os.stat(config.MSGSlave).st_size == 0:
            time.sleep(5)

        while len(opJson.abrirArchivo(config.MSGSlave))==0:
            time.sleep(3)

        manageBD.rmProyecto(proyecto)
        return jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify("Error 400, el proyecto no existe")  


#Metodo para LEVANTAR  una VM de un proyecto
@app.route("/levantarVM/<proyecto>/<VM>")
def levantarVM(proyecto,VM):
    if manageBD.buscarProyecto(proyecto)==True:
        opJson.limpiarJson(config.MSGSlave)
#        opSlave.enviarLevantarVM(proyecto,VM,config.VAGRANTSLAVE1)
        thread4= threading.Thread(target = opSlave.enviarLevantarVM, args=(proyecto,VM,config.VAGRANTSLAVE1))
        thread4.start()
#        thread4.join()
        while os.stat(config.MSGSlave).st_size == 0:
            time.sleep(5)
# <PENDIENTE CREAR METODO PARA CAMBIAR ESTADO VM EN BD DEL MASTER      >     
        while len(opJson.abrirArchivo(config.MSGSlave))==0:
            time.sleep(3)
        manageBD.addVM(proyecto,VM)
        return jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify("Error 400, el proyecto no existe")  



#Metodo para Apagar un VM
@app.route("/apagarVM/<proyecto>/<VM>")
def apagarVM(proyecto,VM):
    if manageBD.buscarProyecto(proyecto)==True:
        opJson.limpiarJson(config.MSGSlave)
        thread6= threading.Thread(target = opSlave.enviarApagarVM, args=(proyecto,VM,config.VAGRANTSLAVE1))
        thread6.start()
#        thread6.join()
        while os.stat(config.MSGSlave).st_size == 0:
            time.sleep(5)
# <PENDIENTE CREAR METODO PARA CAMBIAR ESTADO VM EN BD DEL MASTER      >        
        while len(opJson.abrirArchivo(config.MSGSlave))==0:
            time.sleep(3)
        return jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify("Error 400, el proyecto no existe")  


#Metodo para Borrar un VM
@app.route("/borrarVM/<proyecto>/<VM>")
def borrarVM(proyecto,VM):
    if manageBD.buscarProyecto(proyecto)==True:
        opJson.limpiarJson(config.MSGSlave)
        thread7= threading.Thread(target = opSlave.enviarBorrarVM, args=(proyecto,VM,config.VAGRANTSLAVE1))
        thread7.start()
#        thread7.join()
        while os.stat(config.MSGSlave).st_size == 0:
            time.sleep(5)
# <PENDIENTE CREAR METODO PARA BORRAR  VM EN BD DEL MASTER      >   
        while len(opJson.abrirArchivo(config.MSGSlave))==0:
            time.sleep(3)     
        return jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify("Error 400, el proyecto no existe") 