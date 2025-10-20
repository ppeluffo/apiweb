#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse, request
from utilidades.tolerant_json_load import tolerant_json_load
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.config_service import ConfigService

class ConfigResource(Resource):

    @inject
    def __init__(self, service: ConfigService = Provide[Container.config_service], logger = Provide[Container.logger]):
        self.config_service = service
        self.logger = logger
        
    def get(self):
        """
        Lee la configuracion de un equipo de la SQL
        En la BS almacenamos json.(strings)
        Retornamos un json.
        """
        self.logger.debug("")

        parser = reqparse.RequestParser()
        parser.add_argument('unit',type=str,location='args',required=True)
        args=parser.parse_args()
        unit = args['unit']

        d_rsp = self.config_service.get_configuracion_unidad(unit)
        status_code = d_rsp.get('status_code', 0)
        
        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 200:
            d_rsp = d_rsp.get('d_config',{})
        elif status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = {}
    
        return d_rsp, status_code  

    def post(self):
        """
        Crea/actualiza la configuracion de una unidad.
        Recibimos un json que almacenamos.
        No lo chequeamos !!!
        """
        self.logger.debug("")

        parser = reqparse.RequestParser()
        parser.add_argument('unit',type=str,location='args',required=True)
        args=parser.parse_args()
        unit = args['unit']
        #
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
       
        assert isinstance(d_params, dict )

        d_rsp = self.config_service.set_configuracion_unidad(unit, d_params)
        
        status_code = d_rsp.get('status_code', 500)
        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 200:
            d_rsp = { }
        elif status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = { }
    
        return d_rsp, status_code 
    
    
