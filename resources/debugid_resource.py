#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse, request
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.debugid_service import DebugIdService


class DebugIdResource(Resource):

    @inject
    def __init__(self, service: DebugIdService = Provide[Container.debugid_service], logger = Provide[Container.logger]):
        self.debugid_service = service
        self.logger = logger

    def get(self):
        """
        Devuelve las ordenes para la unidad en un json
            Invocacion: /apiredis/ordenes?unit=DLGID

            Testing:
            req=requests.get('http://127.0.0.1:5100/apiredis/ordenes',params={'unit':'DLGTEST'})
            json.loads(req.json())
            {'ordenes': 'RESET;PRENDER_BOMBA'}

        """
        self.logger.debug("")

        d_rsp = self.debugid_service.get_debug_unit()
        assert isinstance(d_rsp, dict)

        #self.logger.debug(f"D_RSP={d_rsp}")
        status_code = d_rsp.pop('status_code', 0)
        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            debug_id = d_rsp.get('debug_id',None) 
            debug_id = debug_id.decode('utf-8')
            d_rsp = {"debug_id":debug_id }
            
        return d_rsp, status_code 
    
    def put(self):
        """
        """
        self.logger.debug("")
        
        # Solo leo de args. Del json body uso el bloque faul tolerant
        parser = reqparse.RequestParser()
        parser.add_argument('unit',type=str,location='args',required=True)
        args=parser.parse_args()
        debug_id = args['unit']

        d_rsp = self.debugid_service.set_debug_unit(debug_id)
        assert isinstance(d_rsp, dict)
        
        status_code = d_rsp.pop('status_code', 500)
        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = {}

        return d_rsp, status_code 
    
 