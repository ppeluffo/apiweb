#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import pickle


class OrdenesPlcService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    def get_ordenesplc(self, unit):
        """
        """
        self.logger.debug("")
        d_rsp = self.repo.get_ordenesplc(unit)
    
        if d_rsp.get('status_code',0) == 200:
            pk_ordenes_plc = d_rsp['pk_ordenes_plc']
            try:
                pk_ordenes_plc = pickle.loads(pk_ordenes_plc) 
                d_rsp = {'status_code':200, 'ordenes_plc':pk_ordenes_plc}
                
            except Exception as e:
                self.logger.error( f"OrdenesPlcService:get_ordenesplc: {e}")
                d_rsp = {'status_code':502, 'msg':f"{e}"}

        return d_rsp
    
    def set_ordenesplc(self, unit=None, ordenes_plc=None):
        """
        """
        self.logger.debug("")

        try:
            pk_ordenes_plc = pickle.dumps(ordenes_plc)
            
        except Exception as e:
            self.logger.error( f"OrdenesPlcService:set_ordenesplc: {e}")
            d_rsp = {'status_code':502, 'msg':f"{e}"}
            return d_rsp
        #
        d_rsp = self.repo.set_ordenesplc(unit, pk_ordenes_plc)
        
        return d_rsp

    def delete_ordenesplc(self, unit=None):
        """
        """
        self.logger.debug("")

        return self.repo.delete_ordenesplc(unit)      