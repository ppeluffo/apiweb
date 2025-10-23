#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import pickle

class DebugIdService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger

    def get_debug_unit(self):
        """
        """
        self.logger.debug("")
        return self.repo.get_debug_unit()
    
    def set_debug_unit(self, unit=None):
        """
        """
        self.logger.debug("")
        return self.repo.set_debug_unit(unit)


 