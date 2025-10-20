#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python


from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from servicios.ping_service import PingService
from servicios.config_service import ConfigService
from servicios.ordenes_service import OrdenesService
from servicios.ordenesplc_service import OrdenesPlcService
from servicios.usuarios_service import UsuariosService
from servicios.listarusuarios_service import ListarUsuariosService
from servicios.listarunidades_service import ListarUnidadesService

from repositorios.repodatos import RepoDatos

from datasources.ds_pgsql.apibdpgsql import ApiBdPgsql
from datasources.ds_redis.apibdredis import ApiBdRedis

from utilidades.login_config import configure_logger

from config import settings

class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(
        modules=["resources.ping_resource",
                 "resources.help_resource",
                 "resources.config_resource",
                 "resources.ordenes_resource",
                 "resources.ordenesplc_resource",
                 "resources.usuarios_resource",
                 "resources.listarusuarios_resource",
                 "resources.listarunidades_resource",
                 
                 ]
    )
    
    # Logger (singleton compartido)
    logger = providers.Singleton(configure_logger, name="api-redis")

    # Engine y session factory BDLOCAL
    engine_pgsql = providers.Singleton(
        create_engine,
        url=settings.PGSQL_URL, 
        echo=False, 
        isolation_level="AUTOCOMMIT", 
        connect_args={'connect_timeout': 5}
    )

    session_pgsql = providers.Singleton(
        sessionmaker,
        bind = engine_pgsql
    )
    
    # Datasources
    ds_pgsql = providers.Factory( ApiBdPgsql, session_factory = session_pgsql, logger=logger )
    ds_redis = providers.Factory(ApiBdRedis, logger=logger )
    
    # Repositorios
    repo = providers.Factory(RepoDatos, ds_pgsql=ds_pgsql, ds_redis=ds_redis, logger=logger)
        
    # Servicios
    ping_service = providers.Factory(PingService, repositorio=repo, logger=logger)
    config_service = providers.Factory(ConfigService, repositorio=repo, logger=logger)
    ordenes_service = providers.Factory(OrdenesService, repositorio=repo, logger=logger)
    ordenesplc_service = providers.Factory(OrdenesPlcService, repositorio=repo, logger=logger)
    usuarios_service = providers.Factory(UsuariosService, repositorio=repo, logger=logger)
    listarusuarios_service = providers.Factory(ListarUsuariosService, repositorio=repo, logger=logger)
    listarunidades_service = providers.Factory(ListarUnidadesService, repositorio=repo, logger=logger)

    




