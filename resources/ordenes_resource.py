#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse, request
from dependency_injector.wiring import inject, Provide
from utilidades.tolerant_json_load import tolerant_json_load
from container import Container
from servicios.ordenes_service import OrdenesService


class OrdenesResource(Resource):

    @inject
    def __init__(self, service: OrdenesService = Provide[Container.ordenes_service], logger = Provide[Container.logger]):
        self.ordenes_service = service
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

        parser = reqparse.RequestParser()
        parser.add_argument('unit',type=str,location='args',required=True)
        args=parser.parse_args()
        unit = args['unit']

        d_rsp = self.ordenes_service.get_ordenes(unit)
        assert isinstance(d_rsp, dict)

        status_code = d_rsp.pop('status_code', 500)
        ordenes = d_rsp.get('ordenes',"")

        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            ordenes 
            d_rsp = {"ordenes": ordenes }
            
        return d_rsp, status_code 
    
    def put(self):
        """
          Actualiza(override) las ordenes para la unidad
            NO CHEQUEA EL FORMATO DE LA LINEA DE ORDENES
            Invocacion: /apiredis/ordenes?unit=DLGID
            Como es PUT, la orden la mandamos en un json {'ordenes':orden }

            Testing:
            d={'ordenes':'Reset;Apagar;Prender'}
            jd=json.dumps(d)
            req=requests.put('http://127.0.0.1:5100/apiredis/ordenes', params={'unit':'DLGTEST'}, json=jd)
            json.loads(req.json())

        """
        self.logger.debug("")
        
        # Solo leo de args. Del json body uso el bloque faul tolerant
        parser = reqparse.RequestParser()
        parser.add_argument('unit',type=str,location='args',required=True)
        args=parser.parse_args()
        unit = args['unit']

        # Safe json loads
        try:
            raw_body = request.data.decode("utf-8")
            if not raw_body:
                return {},400 
            d_params, reparado = tolerant_json_load(raw_body)

        except Exception as e:
            self.logger.error( f"{e}")
            return {}, 400

        if reparado:
            self.logger.info(f"d_params Reparado JSON !!")    
        self.logger.debug(f"d_params={d_params}")

        ordenes = d_params.get('ordenes',"")
        assert isinstance(ordenes, str)

        d_rsp = self.ordenes_service.set_ordenes(unit, ordenes)
        assert isinstance(d_rsp, dict)
        
        status_code = d_rsp.pop('status_code', 500)
        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = {}

        return d_rsp, status_code 
    
    def delete(self):
        """
        """
        self.logger.debug("")

        parser = reqparse.RequestParser()
        parser.add_argument('unit',type=str,location='args',required=True)
        args=parser.parse_args()
        unit = args['unit']

        d_rsp = self.ordenes_service.delete_ordenes(unit)
        assert isinstance(d_rsp, dict)

        self.logger.debug(f"d_rsp={d_rsp}")

        status_code = d_rsp.pop('status_code', 500)

        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
            
        return d_rsp, status_code 