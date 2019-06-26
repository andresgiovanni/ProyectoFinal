#!/usr/bin/env python
from flask import Flask, jsonify, request, render_template
from werkzeug import secure_filename
from shutil import rmtree
import config, opSlave, opJson, manageBD
import os, threading, logging, sys, time


app = Flask(__name__)

#virtualenv venv
#. venv/bin/activate
#pip install Flask
#export FLASK_APP=Master.py
#export FLASK_ENV=development
#flask run

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


#Metodo para ordenar creacion de VM
#un archivo vagranfile
#curl -F 'file=@/home/admred/Documentos/Vagrantfile' http://127.0.0.1:5000/CrearProyecto/Lili
@app.route('/crearProyecto', methods=['POST'])
@app.route("/crearProyecto/<proyecto>", methods=['POST'])
def crearProyecto(proyecto='default'):
    ruta= config.VAGRANTSERVICEHOME + proyecto  
    if request.method == 'POST': 
        logger.warning('Ingresando a POST')
        try:
            logger.warning('Ingresando al try')
            os.mkdir(ruta)
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(os.path.join(ruta, filename))

            if os.path.isdir(ruta):
                opJson.limpiarJson(config.MSGSlave)
                thread1= threading.Thread(target = opSlave.enviarVM, args=(proyecto,config.VAGRANTSLAVE1))
                thread1.start()

                while os.stat(config.MSGSlave).st_size == 0:
                    time.sleep(5)

                manageBD.addProyecto(proyecto) 

                return  jsonify(opJson.abrirArchivo(config.MSGSlave))
            else:
                return jsonify("Error 400, no se ha subido VagranFile")    
        except Exception as e:
            logger.error(sys.exc_info()[1])
    else:
        return jsonify("Error 400, no se adjuntó VagranFile") 


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