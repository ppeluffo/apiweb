#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import json

class ConfigService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    def get_configuracion_unidad(self, unit=None):
        """
        Recibe una tupla y devuelve un diccionario.
        IN=(
            {'version': '1.1.0', 
             'BASE': {'ALMLEVEL': '10', 'SAMPLES': '1', 'PWRS_HHMM1': '1530', 'PWRS_HHMM2': '1550', 'PWRS_MODO': '1', 'TDIAL': '900', 'TPOLL': ..
             . (1784 characters truncated) ... LOT10': {'PRES': 0.0, 'TIME': '0000'}, 'SLOT11': {'PRES': 0.0, 'TIME': '0000'}}, 
             'CONSIGNA': {'ENABLE': 'FALSE', 'DIURNA': '730', 'NOCTURNA': '2300'}
             },)
        OUT= {'version': '1.1.0', 
             'BASE': {'ALMLEVEL': '10', 'SAMPLES': '1', 'PWRS_HHMM1': '1530', 'PWRS_HHMM2': '1550', 'PWRS_MODO': '1', 'TDIAL': '900', 'TPOLL': ..
             . (1784 characters truncated) ... LOT10': {'PRES': 0.0, 'TIME': '0000'}, 'SLOT11': {'PRES': 0.0, 'TIME': '0000'}}, 
             'CONSIGNA': {'ENABLE': 'FALSE', 'DIURNA': '730', 'NOCTURNA': '2300'}
             }

        """
        self.logger.debug("")
        
        d_rsp = self.repo.get_configuracion_unidad(unit)
        assert isinstance(d_rsp, dict)
        
        status_code = d_rsp.get('status_code', 500)
        if status_code == 200:
            # La BD devuelve una tupla !!
            d_config = d_rsp['jconfig_raw'][0]
            self.logger.debug(f"Pgsql d_config={d_config}")
            assert isinstance(d_config, dict)
            d_rsp = { 'status_code':200, 'd_config': d_config}

        return d_rsp
      
    def set_configuracion_unidad(self, unit=None, d_config=None):
        """
        """
        self.logger.debug("")      

        #    
        return self.repo.set_configuracion_unidad(unit, d_config)

