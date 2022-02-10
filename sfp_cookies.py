# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:         sfp_cookies
# Purpose:      SpiderFoot plug-in for creating new modules.
#
# Author:      Edison Fernando Maisanche López <maisanche45@hotmail.com>
#
# Created:     07/02/2022
# Copyright:   (c) Edison Fernando Maisanche López 2022
# Licence:     GPL
# -------------------------------------------------------------------------------


from spiderfoot import SpiderFootEvent, SpiderFootPlugin

# Se ha añadido el módulo subprocess dado que este nos permitirá generar nuevos procesos.
import subprocess


class sfp_cookies(SpiderFootPlugin):

    meta = {

        # Aquí se especifica el nombre del nuevo modulo a realizar, señalando las caracteriticas del mismo. 
        'name': "Cookies",
        'summary': "Extract Cookies",
        'flags': [""],
        'useCases': ["Footprint", "Investigate"],
        'categories': ["Content Analysis"]
    }

    # Default options
    opts = {
    }

    # Option descriptions
    optdescs = {
    }

    results = None

    def setup(self, sfc, userOpts=dict()):
        self.sf = sfc
        self.results = self.tempStorage()

        for opt in list(userOpts.keys()):
            self.opts[opt] = userOpts[opt]

    # What events is this module interested in for input

    # se da a conocer el parámetro de entrada al módulo WEBSERVER_HTTPHEADERS
    def watchedEvents(self):
        return ["WEBSERVER_HTTPHEADERS"]

    # What events this module produces
    # This is to support the end user in selecting modules based on events
    # produced.
    
    # Se da a conocer el parámetro de salida del módulo, en este caso TARGET_WEB_COOKIE

    def producedEvents(self):
        return ["TARGET_WEB_COOKIE"]

    # Handle events sent to this module
    def handleEvent(self, event):
        eventName = event.eventType
        srcModuleName = event.module
        eventData = event.data

        if eventData in self.results:
            return

        self.results[eventData] = True

        self.sf.debug(f"Received event, {eventName}, from {srcModuleName}")

        try:

            self.sf.debug(f"We use the data: {eventData}")
            print(f"We use the data: {eventData}")

            # Codigo insertado aquí se muestra el proceso que se va realizar para llegar a obtener la cookies necesarias
            # Dentro de la variable data se encuentra el proceso de ejecución que se va llevar, realizando un curl -I y llamando al módulo subprocess
            # Además el resultado de dicho curl en principio, será guardado en el archivo "info"

            data = subprocess.run(["curl","-I", "--output","info", eventData], stdout=subprocess.PIPE)

            # Una vez generado el archivo "info", utilizamos la funcion open para abrir el archivo que contiene la información del dominio ingresado 
            # Como solo se necesita las cookies del dominio, se guarda en una variable la lectura del contenido del archivo, con la funcion for
            # buscaremos la linea de la cual queremos mostrar su información, si existe 'set-cookie' entonces queremos que nos muestre esa linea con su información.

            with open("info", "r") as f:
                datafile = f.readlines()
                for linea in datafile:
                    if 'set-cookie' in linea:
                        cookie = linea

            # En la siguiente linea decimos que si no hay datos del dominio ingresado, devuelva un mensaje.

            if not data:
                self.sf.debug("Information not found for: " + eventData)
                return

        # En la siguiente linea decimos que si el usuario escribe mal la direccíon a ingresar devuelve un error y con ello un mensaje.
        except Exception as e:
            self.sf.error("The following address is not valid: " + eventData + ": " + str(e))
            return

        # A continuación decimos que realice el envio de datos hacia la base de datos y hacia el panel web, señalando las variables.
        evt = SpiderFootEvent("TARGET_WEB_COOKIE", cookie, self.__name__, event)
        self.notifyListeners(evt)

# End of sfp_new_module class