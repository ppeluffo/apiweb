#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.listarusuarios_service import ListarUsuariosService

class ListarUsuariosResource(Resource):
    """
    Los usuarios son los que pueden leer los datos de la BD.
    Son solo para poder tener un control de cuanto han bajado de la bd y entonces
    poder tenerla en tamaño optimo
    """

    @inject
    def __init__(self, service: ListarUsuariosService = Provide[Container.listarusuarios_service], logger = Provide[Container.logger]):
        self.listarusuarios_service = service
        self.logger = logger
        
    def get(self):
        """
        Lectura de todos los usuarios de la BD
        Implementa el acceso a todos los datos de usuarios.
        Es con el fin de manejar el respaldo de estos.
        """
        self.logger.debug("")

        d_rsp = self.listarusuarios_service.listar_usuarios()
        status_code = d_rsp.pop('status_code', 500)

        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 200:
            l_usuarios = d_rsp.get('l_usuarios',0) 
            d_rsp = l_usuarios
        elif status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = { }
    
        return d_rsp, status_code 


