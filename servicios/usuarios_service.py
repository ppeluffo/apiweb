#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python


import random, string
import datetime as dt
from datasources.ds_pgsql.models import Usuarios

class UsuariosService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    def read_user_configuration(self, user=None):
        """
        """
        self.logger.debug("")
    
        d_rsp =  self.repo.read_user_configuration(user)
        
        if d_rsp.get('status_code',0) == 200:
            usuario = d_rsp['usuario']
            fecha_acceso = usuario.fecha_ultimo_acceso.strftime("%Y-%m-%d %H:%M:%S")
            data_ptr = usuario.data_ptr    
            d = { 'user':user , 'fechaUltimoAcceso': fecha_acceso, 'data_ptr': data_ptr }
            d_rsp = { 'status_code': 200, 'user': d }
            
        self.logger.debug(f"D_RSP:{d_rsp}")
        return d_rsp
    
    def create_new_user(self, label=None):
        """
        """
        self.logger.debug("")

        # Creamos un id de 20 caracteres aleatorios.
        random.seed(dt.datetime.now().timestamp())
        user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        #
        d_rsp =  self.repo.create_new_user(user_id, label)
        return d_rsp

    def delete_user(self, user=None):
        """
        """
        self.logger.debug("")

        return self.repo.delete_user(user)
    

    