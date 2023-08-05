from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_restful import Api

from openfabric_pysdk.json import PyJSON
from openfabric_pysdk.manifest import manifest


class OpenfabricService:
    __app = None
    __api = None
    __docs = None

    input_type: PyJSON = None
    output_type: PyJSON = None
    execution_function = None

    def __init__(self, app: Flask):
        self.__app = app
        self.__install_specs()
        self.__register = dict()
        self.__api = Api(app)
        self.__docs = FlaskApiSpec(app)

    def __install_specs(self):
        specs = {
            'APISPEC_SPEC': APISpec(
                title=manifest.get('name'),
                version=manifest.get('version'),
                plugins=[MarshmallowPlugin()],
                openapi_version='2.0.0',
                info=dict(
                    termsOfService='https://openfabric.ai/terms/',
                    contact=dict(name=manifest.get('organization'), url="https://openfabric.ai"),
                    description=manifest.get('description')),
            ),
            'APISPEC_SWAGGER_URL': '/spec/',  # URI to access API Doc JSON
            'APISPEC_SWAGGER_UI_URL': '/spec-ui/'  # URI to access UI of API Doc
        }
        self.__app.config.update(specs)

    def install(self, target, endpoint):
        self.__api.add_resource(target, endpoint)
        self.__docs.register(target)

    def run(self, debug, host):
        self.__app.run(debug=debug, host=host)
