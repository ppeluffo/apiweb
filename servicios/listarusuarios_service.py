#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python


import random, string
import datetime as dt
from datasources.ds_pgsql.models import Usuarios

class ListarUsuariosService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    def listar_usuarios(self):
        """
        Lee todos los usuarios de la BD
        """
        self.logger.debug("")

        d_rsp =  self.repo.listar_usuarios()

        if d_rsp.get('status_code',0) == 200:
            l_usuarios = []
            for usuario in d_rsp['usuarios']:
                user_id = usuario.user_id
                fecha_ultimo_acceso = usuario.fecha_ultimo_acceso.strftime("%Y-%m-%d %H:%M:%S")
                data_ptr = usuario.data_ptr
                label = usuario.label
                l_usuarios.append( {'user':user_id, 'date': fecha_ultimo_acceso, 'ptr': data_ptr, 'label':label })
            d_rsp = {'status_code':200, 'l_usuarios': l_usuarios}

        return d_rsp

    