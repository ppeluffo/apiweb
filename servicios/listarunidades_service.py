#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

class ListarUnidadesService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger


    def listar_configuracion_unidades(self):
        """
        Generamos 2 listas: de plc y de dataloggers
        """
        self.logger.debug("")
        
        d_rsp = self.repo.listar_configuracion_plcs()
        self.logger.debug(f"d_rsp={d_rsp}")
        l_plcs = []        
        if d_rsp.get('status_code',0) == 200:
            plcs_raw = d_rsp['plcs_raw']
            l_plcs = [ element[0] for element in plcs_raw]
        else:
            return d_rsp

        self.logger.debug(f"l_plcs={l_plcs}")

        d_rsp = self.repo.listar_configuracion_dlgs()
        self.logger.debug(f"d_rsp={d_rsp}")
        l_dlgs = []        
        if d_rsp.get('status_code',0) == 200:
            dlgs_raw = d_rsp['dlgs_raw']
            l_dlgs = [ element[0] for element in dlgs_raw]
        else:
            return d_rsp
        
        self.logger.debug(f"l_dlg={l_dlgs}")

        d_rsp = { 'status_code':200, 
                'nro_plcs': len(l_plcs), 'l_plcs': l_plcs,
                'nro_dlgs': len(l_dlgs), 'l_dlgs': l_dlgs
                }

        return d_rsp
    