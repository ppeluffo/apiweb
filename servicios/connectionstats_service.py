#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import datetime as dt
import pickle

class ConnectionStatsService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    def read_timestamps(self):
        """
        En la redis la configuracion es un dict serializado. 
        """
        self.logger.debug("")

        d_rsp = self.repo.read_timestamps()

        if d_rsp.get('status_code',0) == 200:

            d_pk_timestamp = d_rsp['d_pk_timestamp']
            # Cada key es un dlgid y el valor es un timestamp pickled.   
            d_timestamp = {}
            for k in d_pk_timestamp:
                try:
                    key = k.decode()
                    value = pickle.loads(d_pk_timestamp[k]).strftime("%Y/%m/%d, %H:%M:%S")
                    d_timestamp[key] = value
                
                except Exception as e:
                    self.logger.error( f"ConnectionStatsService:read_timestamps: {e}")

            # Los datetime del diccionario NO son serializables JSON !!.

            d_rsp = {'status_code':200, 'ultima_conexion':d_timestamp }

        return d_rsp

