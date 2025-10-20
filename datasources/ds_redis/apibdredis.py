#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
"""
import redis
from config import settings

class ApiBdRedis:

    def __init__(self, logger):
        self.logger = logger
        self.rh = redis.Redis( settings.BDREDIS_HOST, settings.BDREDIS_PORT,settings.BDREDIS_DB, socket_connect_timeout=1)
        
    def ping(self):
        """
        Si el server responde, el ping da True.
        Si no responde, sale por exception.
        """
        #self.logger.info("TESTING LOGGER INFO")
        #self.logger.debug("TESTING LOGGER DEBUG")
        #self.logger.error("TESTING LOGGER ERROR")

        self.logger.debug(f"")

        try:
            self.rh.ping()
            ds_rsp = {'status_code': 200,
                      'version':settings.API_VERSION,
                      'REDIS_HOST':settings.BDREDIS_HOST,
                      'REDIS_PORT': settings.BDREDIS_PORT }
        
        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            ds_rsp = {'status_code': 502,  'msg':f"{e}" }
            
        return ds_rsp

    ############################################################
    #     
    def get_ordenes(self, unit=None):
        """
        Devuelve un string pickeado
        """
        self.logger.debug(f"")

        try:
            pk_ordenes = self.rh.hget( unit, 'PKORDENES' )
            if pk_ordenes is None:
                d_rsp = {'status_code': 404 }
            else:
                d_rsp = {'status_code': 200, 'pk_ordenes':pk_ordenes}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp

    def set_ordenes(self, unit=None, pk_ordenes=None):
        """
        """
        self.logger.debug(f"")

        try:
            _ = self.rh.hset(unit, 'PKORDENES', pk_ordenes )
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        return d_rsp
    
    def delete_ordenes(self, unit=None):
        """
        """
        self.logger.debug(f"")

        try:
            _ = self.rh.hdel(unit, 'PKORDENES' )
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        return d_rsp
          
    ############################################################
           
    def get_ordenesplc(self, unit=None):
        """
        """
        self.logger.debug(f"")

        try:
            pk_ordenes_plc = self.rh.hget( unit, 'PKATVISE' )
            if pk_ordenes_plc is None:
                d_rsp = {'status_code': 404 }
            else:
                d_rsp = {'status_code': 200, 'pk_ordenes_plc':pk_ordenes_plc}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp

    def set_ordenesplc(self, unit=None, pk_ordenes_plc=None):
        """
        """
        self.logger.debug(f"")

        try:
            _ = self.rh.hset(unit, 'PKATVISE', pk_ordenes_plc )
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        return d_rsp
    
    def delete_ordenesplc(self, unit=None):
        """
        """
        self.logger.debug(f"")

        try:
            _ = self.rh.hdel(unit, 'PKATVISE' )
            d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error( f"Redis Error {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }
        #
        return d_rsp

    ############################################################


