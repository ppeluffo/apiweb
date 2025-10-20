#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python3

import pickle
import datetime as dt

class RepoDatos:
    """
    Repositorio que se encarga de consultar las apis de redis y datossql
    """
    
    def __init__(self, ds_pgsql, ds_redis, logger):
        self.ds_pgsql = ds_pgsql
        self.ds_redis = ds_redis
        self.logger = logger

    def ping_redis(self):
        """
        """
        self.logger.debug("")
        return self.ds_redis.ping()
    
    def ping_pgsql(self):
        """
        """
        self.logger.debug("")
        return self.ds_pgsql.ping()
        
    #####################################################################################
    # PGSQL

    def get_configuracion_unidad(self, unit=None):
        """
        Pide la configuracion a la pgsql.
        """
        self.logger.debug("")

        return self.ds_pgsql.load_configuracion_unidad(unit)
    
    def set_configuracion_unidad(self, unit=None, d_config=None):
        """
        Guarda la configuracion a la pgsql.
        """
        self.logger.debug("")

        return self.ds_pgsql.save_configuracion_unidad(unit, d_config)

    #####################################################################################
    # REDIS
    
    def get_ordenes(self, unit=None):
        """
        """
        self.logger.debug("")
        return self.ds_redis.get_ordenes(unit)

    def set_ordenes(self, unit=None, pk_ordenes=None):
        """
        """
        self.logger.debug("")
        return self.ds_redis.set_ordenes(unit, pk_ordenes)

    def delete_ordenes(self, unit=None):
        """
        """
        self.logger.debug("")
        return self.ds_redis.delete_ordenes(unit)

    #####################################################################################
    # REDIS

    def get_ordenesplc(self, unit=None):
        """.
        """
        self.logger.debug("")

        return self.ds_redis.get_ordenesplc(unit)
    
    def set_ordenesplc(self, unit=None, pk_ordenes=None):
        """
        """
        self.logger.debug("")
        return self.ds_redis.set_ordenesplc(unit, pk_ordenes)
   
    def delete_ordenesplc(self, unit=None):
        """.
        """
        self.logger.debug("")

        return self.ds_redis.delete_ordenesplc(unit)

    #####################################################################################
    # PGSQL
   
    def read_user_configuration(self, user=None):
        """
        """
        self.logger.debug("")
        
        return self.ds_pgsql.read_user_configuration(user)
    
    def create_new_user(self, user_id=None, label=None):
        """
        """
        self.logger.debug("")
        
        return self.ds_pgsql.create_new_user(user_id, label)
    
    def delete_user(self, user_id=None):
        """
        """
        self.logger.debug("")
        
        return self.ds_pgsql.delete_user(user_id)
    
    #####################################################################################
    # PGSQL

    def listar_usuarios(self):
        """
        """
        self.logger.debug("")
        
        return self.ds_pgsql.listar_usuarios()
    
    #####################################################################################
    # PGSQL

    def listar_configuracion_dlgs(self):
        """
        """
        self.logger.debug("")
        
        return self.ds_pgsql.listar_configuracion_dlgs()
        
    def listar_configuracion_plcs(self):
        """
        """
        self.logger.debug("")
        
        return self.ds_pgsql.listar_configuracion_plcs()

