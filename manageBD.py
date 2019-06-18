import opJson
import config
import os
import logging
import sys
import RunCLI



def addProyecto(proyecto):
    llave = {}
    if os.path.isfile(config.BDProyectos) == True:
        llave={"PROYECTO": proyecto, "SLAVE": "0", "VM1": [{"NAME": "None", "IP": "0", "STATUS": "not created"}]}
        opJson.addLlave(config.BDProyectos,llave,proyecto)

    else:
        return False
