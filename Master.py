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
        try:
            f = request.files['file']
            filename = secure_filename (f.filename )
            SLAVE=manageBD.seleccionarSlave()
            if SLAVE:
                if os.path.isdir( ruta )==False:
                    os.mkdir( ruta )
                    f.save(os.path.join( ruta, filename ))
                    opJson.limpiarJson( config.MSGSlave )
                    thread1= threading.Thread(target = opSlave.enviarVM, args=(proyecto,SLAVE['IP']))
                    thread1.start()
                    manageBD.addProyecto( proyecto, SLAVE['id'] ) 
                    while os.stat( config.MSGSlave ).st_size == 2:
                        time.sleep(5)

                    return  jsonify(opJson.abrirArchivo( config.MSGSlave ))

                else:
                    return jsonify("Error 400, Ya exite el proyecto")    
            return jsonify("No hay host disponibles para crear el proyecto")
        except Exception as e:
            logger.error(sys.exc_info()[1])
    else:
        return jsonify("Error 400, no se adjunto VagranFile") 


#Metodo para consultar estado de un proyecto
@app.route("/estadoProyecto/<proyecto>")
def estadoProyecto( proyecto ):
    data={}
    data=manageBD.getProyecto( proyecto )
#    if manageBD.buscarProyecto(proyecto)==True:
    if data:
        opJson.limpiarJson( config.MSGSlave )
        thread2= threading.Thread( target = opSlave.preguntarEstadoProyecto, args=( proyecto, data['SLAVE'] ) )
        thread2.start()
#        thread2.join()
        while os.stat( config.MSGSlave ).st_size == 2:
            time.sleep( 3 )
        while len(opJson.abrirArchivo( config.MSGSlave ) )==0:
            time.sleep( 3 )

        return jsonify( manageBD.getProyecto( proyecto ) )
#        return jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify( "Error 400, el proyecto no existe" )


#Metodo para Borrar un proyecto
@app.route("/borrarProyecto/<proyecto>")
def borrarProyecto( proyecto ):
    data={}
    data=manageBD.getProyecto( proyecto )
    if data:
        opJson.limpiarJson( config.MSGSlave )
        thread3= threading.Thread( target = opSlave.enviarBorrarProyecto, args=( proyecto,data['SLAVE'] ) )
        thread3.start()
#        thread3.join()
        while os.stat(config.MSGSlave).st_size == 2:
            time.sleep(5)

        while len(opJson.abrirArchivo(config.MSGSlave))==0:
            time.sleep(3)

        manageBD.rmProyecto( proyecto, data['SLAVE'] )
        ruta= config.VAGRANTSERVICEHOME + proyecto
        os.remove( ruta + "/Vagrantfile" )
        os.rmdir(ruta)
        return jsonify(opJson.abrirArchivo(config.MSGSlave))
    else:
        return jsonify( "Error 400, el proyecto no existe" )  


#Metodo para LEVANTAR  una VM de un proyecto
@app.route("/levantarVM/<proyecto>/<VM>")
def levantarVM( proyecto, VM ):
    data={}
    data=manageBD.getProyecto( proyecto )    
    if data:
        opJson.limpiarJson( config.MSGSlave )
        thread4= threading.Thread( target = opSlave.enviarLevantarVM, args=( proyecto, VM, data['SLAVE'] ) )
        thread4.start()
#        thread4.join()
        while os.stat( config.MSGSlave ).st_size == 2:
            time.sleep( 3 )
# <PENDIENTE CREAR METODO PARA CAMBIAR ESTADO VM EN BD DEL MASTER      >     
        while len( opJson.abrirArchivo( config.MSGSlave ) )==0:
            time.sleep(3)
        manageBD.addVM( proyecto, VM,  data['SLAVE'] )
        return jsonify( opJson.abrirArchivo( config.MSGSlave ) )
    else:
        return jsonify( "Error 400, el proyecto no existe" )  



#Metodo para Apagar un VM
@app.route("/apagarVM/<proyecto>/<VM>")
def apagarVM( proyecto, VM ):
    data={}
    data=manageBD.getProyecto( proyecto )    
    if data:
        opJson.limpiarJson( config.MSGSlave )
        thread6= threading.Thread( target = opSlave.enviarApagarVM, args=( proyecto, VM, data['SLAVE'] ) )
        thread6.start()
#        thread6.join()
        while os.stat( config.MSGSlave ).st_size == 2:
            time.sleep( 5 )
# <PENDIENTE CREAR METODO PARA CAMBIAR ESTADO VM EN BD DEL MASTER      >        
        while len(opJson.abrirArchivo( config.MSGSlave ) )==0:
            time.sleep( 3 )
        return jsonify( opJson.abrirArchivo( config.MSGSlave ) )
    else:
        return jsonify( "Error 400, el proyecto no existe" )  


#Metodo para Borrar un VM
@app.route("/borrarVM/<proyecto>/<VM>")
def borrarVM( proyecto, VM ):
    data={}
    data=manageBD.getProyecto( proyecto )
    if data:
        opJson.limpiarJson( config.MSGSlave )
        thread7= threading.Thread( target = opSlave.enviarBorrarVM, args=( proyecto, VM, data['SLAVE'] ) )
        thread7.start()
#        thread7.join()
        while os.stat( config.MSGSlave ).st_size == 2:
            time.sleep( 5 )
# <PENDIENTE CREAR METODO PARA BORRAR  VM EN BD DEL MASTER      >   
        while len(opJson.abrirArchivo( config.MSGSlave ) )==0:
            time.sleep( 3 )     
        return jsonify( opJson.abrirArchivo( config.MSGSlave ) )
    else:
        return jsonify( "Error 400, el proyecto no existe" ) 



#Metodo para registrar Slave en BD maestro
#curl -H "Content-Type: application/json" -X POST -d '{"name": "slavePrueba1", "port": 8000, "mem": 5000 }'  http://localhost:5000/registrarSlave
@app.route("/registrarSlave", methods=["POST"])
def registrarSlave(  ):
    IP = str(request.remote_addr)
    try:
        content = request.json
        name = str(content['name'])
        port = content['port']
        mem = content['mem']

        if name and port and mem:
            logger.warning('Ingresando a regisrar SLAVE: ' + name)
            if manageBD.addSlave( IP, name, mem, port ):
                return jsonify( "se ha registrado correctamente")
        else:
            return jsonify( "parametros post invalidos")
    except Exception as e:
        logger.error(sys.exc_info()[1])
        


