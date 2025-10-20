#!/home/pablo/Spymovil/python/proyectos/APICOMMS_2025/.venv/bin/python
"""
API REST para acceder a los servicios de REDIS del servidor de comunicaciones

"""

import logging
from config import settings
from flask import Flask
from flask_restful import Api


from resources import help_resource
from resources import ping_resource
from resources import config_resource
from resources import ordenes_resource
from resources import ordenesplc_resource
from resources import usuarios_resource
from resources import listarusuarios_resource
from resources import listarunidades_resource

from container import Container

from utilidades.login_config import configure_logger

def create_app(gunicorn: bool = False):

    app = Flask(__name__)
    api = Api(app)

    container = Container()

    # Sobrescribir logger según modo
    container.logger.override(configure_logger("api-web", gunicorn=gunicorn))
    container.init_resources()
    container.wire(modules=[__name__])

    api.add_resource( ping_resource.PingResource, '/apiweb/ping')
    api.add_resource( help_resource.HelpResource, '/apiweb/help')
    api.add_resource( config_resource.ConfigResource, '/apiweb/config_equipos')
    api.add_resource( ordenes_resource.OrdenesResource, '/apiweb/ordenes')
    api.add_resource( ordenesplc_resource.OrdenesPlcResource, '/apiweb/ordenesplc')
    api.add_resource( usuarios_resource.UsuarioResource, '/apiweb/usuarios')
    api.add_resource( listarusuarios_resource.ListarUsuariosResource, '/apiweb/listarusuarios')
    api.add_resource( listarunidades_resource.ListarUnidadesResource, '/apiweb/listarunidades')

    return app

# Lineas para cuando corre en gurnicorn
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app = create_app(gunicorn=True)
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info(f'Starting APIWEB...')


# Lineas para cuando corre en modo independiente
if __name__ == '__main__':
    app = create_app(gunicorn=False)
    app.run(host='0.0.0.0', port=5500, debug=True)


