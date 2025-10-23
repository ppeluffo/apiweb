#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.datos_service import DatosService

class DatosResource(Resource):

    @inject
    def __init__(self, service: DatosService = Provide[Container.datos_service], logger = Provide[Container.logger]):
        self.datos_service = service
        self.logger = logger
        
    def get(self):
        """
        Pide datos.
        Se entrega un chunk de datos y se marca en la tabla de usuarios
        """
        self.logger.debug("")

        parser = reqparse.RequestParser()
        parser.add_argument('user',type=str,location='args',required=True)
        args=parser.parse_args()
        user_id = args['user']
        
        d_rsp = self.datos_service.read_data_chunk(user_id)
        status_code = d_rsp.pop('status_code', 500)

        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 200:
            l_datos = d_rsp.get('l_datos',[])
            d_rsp = l_datos
        elif status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = { }
    
        return d_rsp, status_code




