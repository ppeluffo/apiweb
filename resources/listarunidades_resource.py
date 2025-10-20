#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.listarunidades_service import ListarUnidadesService

class ListarUnidadesResource(Resource):

    @inject
    def __init__(self, service: ListarUnidadesService = Provide[Container.listarunidades_service], logger = Provide[Container.logger]):
        self.listarunidades_service = service
        self.logger = logger
        
    def get(self):
        """
        Lectura de todos los usuarios de la BD
        Implementa el acceso a todos los datos de usuarios.
        Es con el fin de manejar el respaldo de estos.
        """
        self.logger.debug(f"")

        d_rsp = self.listarunidades_service.listar_configuracion_unidades()
        status_code = d_rsp.pop('status_code', 500)
    
        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 200:
            pass
        elif status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = { }
    
        return d_rsp, status_code 
    
