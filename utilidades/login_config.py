#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python

import logging
import threading
import time
import sys

from config import settings

def set_log_level(level=None, timeout=60):
    """
    Cambia el nivel de log de un equipo en runtime.
    Si timeout está definido, revierte automáticamente a INFO luego de ese tiempo.
    """

    if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Nivel inválido: {level}")

    logger = logging.getLogger('api-datos')
    logger.setLevel(getattr(logging, level))

    print(f"[LOGGER] Nivel revertido a {level}")

    # Si hay timeout, crear un hilo que lo revierta
    if timeout and timeout > 0:
        threading.Thread(
            target=_revert_after_timeout,
            args=(timeout,),
            daemon=True
        ).start()

    return

def _revert_after_timeout(timeout):
    """
    Espera 'timeout' segundos y revierte el nivel a INFO.
    """
    time.sleep(timeout)
    logger = logging.getLogger('api-datos')
    logger.setLevel(logging.INFO)

    print(f"[LOGGER] Nivel revertido automáticamente a INFO después de {timeout} s")


def configure_logger(name: str = "api-datos", gunicorn: bool = False) -> logging.Logger:
    
    logger = logging.getLogger(name)
    
    # Leer nivel de logs desde variable de entorno (default: INFO)
    #logger.setLevel(logging.INFO)
    #log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = settings.LOG_LEVEL.upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    # Si la app corre bajo gunicorn → reutilizamos sus handlers
    if gunicorn:
        gunicorn_logger = logging.getLogger("gunicorn.error")
        logger.handlers = gunicorn_logger.handlers
        logger.setLevel(gunicorn_logger.level)
    else:
        # Configuración estándar cuando corre standalone
        # Sólo añadir handler si no hay
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - [%(module)s.%(funcName)s] - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    return logger

