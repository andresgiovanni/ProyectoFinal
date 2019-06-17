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
   # output=RunCLI.runCommand("cat %s"%(config.VAGRANTSERVICEHOME))
    ruta= config.VAGRANTSERVICEHOME + proyecto   
    if os.path.isdir(ruta):
        
        thread1= threading.Thread(target = opSlave.enviarVM, args=(proyecto,config.VAGRANTSLAVE1))
        thread1.start()
        thread1.join()
        return  jsonify("se inicia tarea")
    else:
        return jsonify("Error 400, no se ha subido VagranFile")    


#Metodo para consultar estado de un proyecto
@app.route("/estadoProyecto/<proyecto>")
def estadoProyecto(proyecto):
    ruta= config.VAGRANTSERVICEHOME + proyecto 
    if os.path.isdir(ruta):
        thread1= threading.Thread(target = opSlave.enviarEstadoProyecto, args=(proyecto,config.VAGRANTSLAVE1))
        thread1.start()
#        opSlave.enviarEstadoProyecto(proyecto,config.VAGRANTSLAVE1)
        return jsonify()
    else:
        return jsonify("Error 400, el proyecto no existe")