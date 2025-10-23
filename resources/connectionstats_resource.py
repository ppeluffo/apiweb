#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.connectionstats_service import ConnectionStatsService

class ConnectionStatsResource(Resource):

    @inject
    def __init__(self, service: ConnectionStatsService = Provide[Container.connectionstats_service], logger = Provide[Container.logger]):
        self.connectionstats_service = service
        self.logger = logger

    def get(self):
        """
        Leo todos los timestamps de las ultimas conexiones de los equipos
        """
        self.logger.debug("")
        
        #
        d_rsp = self.connectionstats_service.read_timestamps()
        assert isinstance(d_rsp, dict)
        
        status_code = d_rsp.pop('status_code', 500)
         # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 200:
            d_timestamps = d_rsp.get('ultima_conexion', {})
            d_rsp = d_timestamps
        elif status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = {}
    
        return d_rsp, status_code  
 
