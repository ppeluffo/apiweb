#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import pickle

class OrdenesService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    def get_ordenes(self, unit):
        """
        Recive de la BD un string pickeado y lo desempaquete
        """
        self.logger.debug("")
        d_rsp = self.repo.get_ordenes(unit)
    
        if d_rsp.get('status_code',0) == 200:
            pk_ordenes = d_rsp['pk_ordenes']
            try:
                ordenes = pickle.loads(pk_ordenes) 
                d_rsp = {'status_code':200, 'ordenes':ordenes}

            except Exception as e:
                self.logger.error( f"OrdenesService:get_ordenes: {e}")
                d_rsp = {'status_code':502, 'msg':f"{e}"}

        return d_rsp
    
    def set_ordenes(self, unit=None, ordenes=None):
        """
        """
        self.logger.debug("")

        try:
            pk_ordenes = pickle.dumps(ordenes)
        except Exception as e:
            self.logger.error( f"OrdenesService:set_ordenes: {e}")
            d_rsp = {'status_code':502, 'msg':f"{e}"}
            return d_rsp
        #
        d_rsp = self.repo.set_ordenes(unit, pk_ordenes)
        
        return d_rsp

    def delete_ordenes(self, unit=None):
        """
        """
        self.logger.debug("")

        return self.repo.delete_ordenes(unit)
