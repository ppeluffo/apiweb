#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.ping_service import PingService

class PingResource(Resource):

    @inject
    def __init__(self, service: PingService = Provide[Container.ping_service], logger = Provide[Container.logger]):
        self.ping_service = service
        self.logger = logger
        
    def get(self):
        # Solicito el servicio correspondiente.
        self.logger.debug("")
            
        d_rsp = self.ping_service.ping()

        status_code = d_rsp.pop('status_code', 500)
        assert isinstance(d_rsp, dict)
        
        return d_rsp, status_code
    


