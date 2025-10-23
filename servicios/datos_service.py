#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python


class DatosService:
    """
    """
    def __init__(self, repositorio, logger):
        self.repo = repositorio
        self.logger = logger
    
    def read_data_chunk(self, user_id=None):
        """
        """
        self.logger.debug("")

        # Determino el puntero del ultimo registro leido por el usuario
        d_rsp = self.repo.read_user_configuration(user_id)

        if d_rsp.get('status_code',0) == 200:
            usuario = d_rsp['usuario']
            data_ptr = usuario.data_ptr
        else:
            return d_rsp

        # Tenemos el ultimo registro accedido por el usuario
        # Leo a partir de este
        d_rsp = self.repo.read_data_chunk(data_ptr)
        if d_rsp.get('status_code',0) == 200:

            l_results = []
            chunk_data = d_rsp.get('chunk_data',[])
            for element in chunk_data:
                data_ptr = element.id
                fechadata = element.fechadata.strftime("%m/%d/%Y, %H:%M:%S")
                fechasys = element.fechasys.strftime("%m/%d/%Y, %H:%M:%S")
                equipo = element.equipo
                tag = element.tag
                valor = element.valor
                rcd = (fechadata, fechasys,equipo,tag, valor)
                l_results.append(rcd)
            #
            # Actualizo el ultimo data_ptr
            d_rsp = self.repo.update_data_ptr(user_id, data_ptr )
            if d_rsp.get('status_code',0) == 200:
                d_rsp = {'status_code':200, 'l_datos':l_results}

        return d_rsp
        