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
        manageBD.addProyecto(proyecto)
        thread1= threading.Thread(target = opSlave.enviarVM, args=(proyecto,config.VAGRANTSLAVE1))
        thread1.start()
        return  jsonify("se inicia tarea")
    else:
        return jsonify("Error 400, no se ha subido VagranFile")    


#Metodo para consultar estado de un proyecto
@app.route("/estadoProyecto/<proyecto>")
def estadoProyecto(proyecto):
    if manageBD.buscarProyecto(proyecto)==True:
        thread1= threading.Thread(target = opSlave.preguntarEstadoProyecto, args=(proyecto,config.VAGRANTSLAVE1))
        thread1.start()
        while os.stat(config.MSGSlave).st_size == 0:
            time.sleep(5)
        return jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify("Error 400, el proyecto no existe")


#Metodo para Borrar un proyecto
@app.route("/borrarProyecto/<proyecto>")
def borrarProyecto(proyecto):
    if manageBD.buscarProyecto(proyecto)==True:
        opSlave.enviarBorrarProyecto(proyecto,config.VAGRANTSLAVE1)
        while os.stat(config.MSGSlave).st_size == 0:
            time.sleep(5)
# <PENDIENTE CREAR METODO PARA BORAR BD DEL MASTER      >     
        return jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify("Error 400, el proyecto no existe")  


#Metodo para LEVANTAR  una VM de un proyecto
@app.route("/levantarVM/<proyecto>/<VM>")
def levantarVM(proyecto,VM):
    if manageBD.buscarProyecto(proyecto)==True:
        opSlave.enviarLevantarVM(proyecto,VM,config.VAGRANTSLAVE1)
        while os.stat(config.MSGSlave).st_size == 0:
            time.sleep(5)
# <PENDIENTE CREAR METODO PARA CAMBIAR ESTADO VM EN BD DEL MASTER      >     
        return jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify("Error 400, el proyecto no existe")  