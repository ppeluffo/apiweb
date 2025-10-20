#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse
from dependency_injector.wiring import inject, Provide
from container import Container

class HelpResource(Resource):

    @inject
    def __init__(self, logger = Provide[Container.logger]):
        self.logger = logger

    def get(self):
        ''' Retorna la descripcion de los metodos disponibles
        '''
        self.logger.debug("")
        
        d_rsp = {
            'GET /apiweb/ping':'Prueba las respuesta y conexión a los datasources',
            'GET /apiweb/config':'Retorna la configuracion de una unidad',
            'POST /apiweb/config':'Actualiza la configuracion de una unidad',

            'POST /apidatos/usuarios':'Crea un nuevo usuario y retorna su id',
            'GET /apidatos/usuarios?user=USERID':'Devuelve los datos del usuario',
            'DELETE /apidatos/usuarios?user=USERID':'Borra el usuario',
            'GET /apidatos/listarusuarios':'Retorna una lista con todos los usuarios definidos',
            'GET /apidatos/listarunidades':'Retorna una lista con todas las unidades definidas',
            'GET /apidatos/uid2id':'Retorna el ID correspondiente a un UID',
            'PUT /apidatos/uid2id':'Actualiza los datos UID/ID de una unidad',

            'GET /apidatos/datos': 'Retorna una lista de datos enviados por la unidad'
            
        }
        
        return d_rsp , 200
    