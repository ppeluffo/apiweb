#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
"""

from .models import Usuarios, Configuraciones, Online, RecoverId, Historica
from sqlalchemy import text
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import insert

from datetime import datetime, timedelta

from config import settings

class ApiBdPgsql:

    def __init__(self, session_factory, logger):
        self.session_factory = session_factory
        self.logger = logger

    def ping(self):
        """
        Si el server responde, el ping da True.
        Si no responde, sale por exception.
        """
        self.logger.debug(f"")

        try:
            with self.session_factory() as session:
                session.execute(text("SELECT 1"))
                d_rsp = {'status_code': 200,
                         'version': settings.API_VERSION,
                         "SQL_HOST": settings.PGSQL_HOST,
                         "SQL_PORT": settings.PGSQL_PORT }
        except Exception as e:
            self.logger.error(f"PgSQL Error: {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp

    def load_configuracion_unidad(self, unit=None):
        """
        Retorna la configuracion de la unidad tal cual se lee.
        Retorna el campo jconfig de la base de datos.
        JCONFIG_RAW=(
            {'version': '1.1.0', 
             'BASE': {'ALMLEVEL': '10', 'SAMPLES': '1', 'PWRS_HHMM1': '1530', 'PWRS_HHMM2': '1550', 'PWRS_MODO': '1', 'TDIAL': '900', 'TPOLL': ..
             . (1784 characters truncated) ... LOT10': {'PRES': 0.0, 'TIME': '0000'}, 'SLOT11': {'PRES': 0.0, 'TIME': '0000'}}, 
             'CONSIGNA': {'ENABLE': 'FALSE', 'DIURNA': '730', 'NOCTURNA': '2300'}
             },)
        La respuesta es una tupla por lo tanto el valor real es t[0]

        SIEMPRE EL DATASOURCE DEVUELVE LO QUE OBTIENE DE LA BASE DE DATOS !!.
        LO MODIFICA EL SERVICIO !!.
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                jconfig_raw = session.query(Configuraciones.jconfig).filter(Configuraciones.unit_id == unit).first()
                if jconfig_raw is None:
                    status_code = 204
                else:
                    status_code = 200
                d_rsp = {'status_code': status_code, 'jconfig_raw': jconfig_raw }

        except Exception as e:
            self.logger.error(f"{e}")
            d_rsp = { 'status_code': 400, 'msg': e}

        return d_rsp
        
    def save_configuracion_unidad(self, unit=None, d_config=None):
        """
        Guarda (actualiza) el dconfig de la unidad
       
        Puede generar el error:
        there is no unique or exclusion constraint matching the ON CONFLICT specification
        que indica que la tabla no tiene una restriccion correcta.
        Hay que dar el comando:
        ALTER TABLE configuraciones
        ADD CONSTRAINT configuraciones_unit_id_key UNIQUE (unit_id);
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                stmt = insert(Configuraciones).values(unit_id=unit, jconfig=d_config)
                stmt = stmt.on_conflict_do_update( 
                                    index_elements=['unit_id'],        # campo que define el conflicto
                                    set_={'jconfig': d_config}      # qué actualizar si ya existe
                                    )
                session.execute(stmt)
                session.commit()
                d_rsp = {'status_code': 200 }

        except Exception as e:
            self.logger.error(f" {str(e)}")
            d_rsp = { 'status_code': 502, 'msg':e }

        return d_rsp

    ########################################################################

    def read_user_configuration(self, user=None):
        """
        Lee toda la tabla de usuarios los datos del usuario user.
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                usuario = session.query(Usuarios).filter(Usuarios.user_id == user).first()
                if usuario is None:            
                    d_rsp = { 'status_code': 204 }
                else:
                    d_rsp = {'status_code': 200, 'usuario': usuario}

        except Exception as e:
            self.logger.error(f"{e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp

    def create_new_user(self, user_id=None, label=None):
        """
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                new_user = Usuarios(user_id=user_id, label=label)
                _ = session.add(new_user)
                session.commit()
                d_rsp = {'status_code': 200, 'user_id': user_id}

        except Exception as e:
            self.logger.error(f"{e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp

    def delete_user(self, user_id=None):
        """
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                session.query(Usuarios).filter(Usuarios.user_id == user_id).delete(synchronize_session=False)
                session.commit()
                d_rsp = {'status_code': 200}

        except Exception as e:
            self.logger.error(f"{e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp
 
    ########################################################################

    def listar_usuarios(self):
        """
        Lee toda la tabla de usuarios y la devuelve tal cual.
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                usuarios = session.query(Usuarios).all()
                if len(usuarios) == 0:
                    d_rsp = {'status_code': 204, 'usuarios': usuarios}
                else:
                    d_rsp = {'status_code': 200, 'usuarios': usuarios}

        except Exception as e:
            self.logger.error(f"{e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        return d_rsp
    
    ########################################################################

    def listar_configuracion_plcs(self):
        """
        Lee toda la tabla de configuraciones y la devuelve solo la lista de PLC.
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                plcs_raw = session.query(Configuraciones.unit_id).where(cast(Configuraciones.jconfig, JSONB).has_key("MEMBLOCK")).all()
                if len(plcs_raw) == 0:
                    d_rsp = {'status_code': 204, 'plcs_raw': plcs_raw }
                else:
                    d_rsp = {'status_code': 200, 'plcs_raw': plcs_raw }

        except Exception as e:
            self.logger.error(f"PgSQL {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        #self.logger.debug(f"d_rsp={d_rsp}")

        return d_rsp

    def listar_configuracion_dlgs(self):
        """
        Lee toda la tabla de configuraciones y la devuelve solo la lista de DLG.
        """
        self.logger.debug("")

        try:
            with self.session_factory() as session:
                dlgs_raw = session.query(Configuraciones.unit_id).where(cast(Configuraciones.jconfig, JSONB).has_key("BASE")).all()
                if len(dlgs_raw) == 0:
                    d_rsp = {'status_code': 204, 'dlgs_raw': dlgs_raw }
                else:
                    d_rsp = {'status_code': 200, 'dlgs_raw': dlgs_raw }

        except Exception as e:
            self.logger.error(f"PgSQL {e}")
            d_rsp = {'status_code': 502,  'msg':f"{e}" }

        #self.logger.debug(f"d_rsp={d_rsp}")

        return d_rsp

    ########################################################################

