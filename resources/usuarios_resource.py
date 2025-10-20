#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

from flask_restful import Resource, reqparse, request
from utilidades.tolerant_json_load import tolerant_json_load
from dependency_injector.wiring import inject, Provide
from container import Container
from servicios.usuarios_service import UsuariosService


class UsuarioResource(Resource):
    """
    Los usuarios son los que pueden leer los datos de la BD.
    Son solo para poder tener un control de cuanto han bajado de la bd y entonces
    poder tenerla en tamaño optimo
    """

    @inject
    def __init__(self, service: UsuariosService = Provide[Container.usuarios_service], logger = Provide[Container.logger]):
        self.usuarios_service = service
        self.logger = logger
        
    def get(self):
        '''
        Recibe un user id y devuelve los datos que tiene configurados en la BD.
        '''
        self.logger.debug("")

        parser = reqparse.RequestParser()
        parser.add_argument('user',type=str,location='args',required=True)
        args=parser.parse_args()
        user = args['user']

        d_rsp = self.usuarios_service.read_user_configuration(user)
        
        status_code = d_rsp.pop('status_code', 500)

        # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 200:
            userdata = d_rsp.get('user',0) 
            d_rsp = userdata
        elif status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = { }
    
        return d_rsp, status_code
    
    def post(self):
        '''
        Creamos un usuario nuevo.
        Recibe solo la label que se va a usar. El user id lo crea el sistema
        '''
        self.logger.debug("")
 
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
       
        label = d_params.get('label',"")
        assert isinstance(label, str)

        d_rsp = self.usuarios_service.create_new_user(label)
        status_code = d_rsp.pop('status_code', 500)

         # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 200:
            user_id = d_rsp.get('user_id',None) 
            d_rsp = {'user_id':user_id }
        elif status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = { }
    
        return d_rsp, status_code
    
    def delete(self):
        """
        Eliminamos un usuario de la BD.
        """

        self.logger.debug("")
 
        parser = reqparse.RequestParser()
        parser.add_argument('user',type=str,location='args',required=True)
        args=parser.parse_args()
        user_id = args['user']

        d_rsp = self.usuarios_service.delete_user(user_id)
        status_code = d_rsp.pop('status_code', 500)

          # No mando detalles de los errores en respuestas x seguridad.
        if status_code == 200:
            d_rsp = {}
        elif status_code == 502:
            d_rsp = {'msg':"SERVICIO NO DISPONIBLE TEMPORALMENTE"}
        else:
            d_rsp = {}
    
        return d_rsp, status_code


