#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse, request
from dependency_injector.wiring import inject, Provide
from utilidades.tolerant_json_load import tolerant_json_load
from container import Container
from servicios.ordenesplc_service import OrdenesPlcService

class OrdenesPlcResource(Resource):

    @inject
    def __init__(self, service: OrdenesPlcService = Provide[Container.ordenesplc_service], logger = Provide[Container.logger]):
        self.ordenesplc_service = service
        self.logger = logger

    def get(self):
        """
        Retorna un diccionario con la ultima linea de ordenes para un PLC

        Testing:
        req=requests.get('http://127.0.0.1:5100/apiredis/ordenesplc',params={'unit':'PLCTEST'})
        json.loads(req.json())
        {'ordenes_atvise': {'UPA1_ORDER_1': 101, 'UPA1_CONSIGNA_6': 102, 'ESP_ORDER_8': 103}}
        """

        self.logger.debug("")

        parser = reqparse.RequestParser()
        parser.add_argument('unit',type=str,location='args',required=True)
        args=parser.parse_args()
        unit = args['unit']

        d_rsp = self.ordenesplc_service.get_ordenesplc(unit)
        assert isinstance(d_rsp, dict)

        status_code = d_rsp.pop('status_code', 500)
        ordenes_plc = d_rsp.get('ordenes_plc',{})

        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = ordenes_plc
            
        return d_rsp, status_code 
      
    def put(self):
        """
        Actualiza(override) la configuracion de ordenes de atvise para la unidad
        NO CHEQUEA EL FORMATO
        Como es PUT, la configuracion la mandamos en un json { ordenes_atvise }

        Testing:
        jat=json.dumps({'ordenes_atvise':{"UPA1_ORDER_1": 101, "UPA1_CONSIGNA_6": 102, "ESP_ORDER_8": 103}})
        req=requests.put('http://127.0.0.1:5100/apiredis/ordenesplc', params={'unit':'PLCTEST'}, json=jat)

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

        ordenes_plc = d_params.get('ordenes_atvise',"")
        assert isinstance(ordenes_plc, dict)
        self.logger.debug(f"ordenes_plc={ordenes_plc}")

        d_rsp = self.ordenesplc_service.set_ordenesplc(unit, ordenes_plc)
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

        d_rsp = self.ordenesplc_service.delete_ordenesplc(unit)
        assert isinstance(d_rsp, dict)

        self.logger.debug(f"d_rsp={d_rsp}")

        status_code = d_rsp.pop('status_code', 500)

        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
            
        return d_rsp, status_code