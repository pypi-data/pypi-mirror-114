import time

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema

from openfabric_pysdk.manifest import manifest
from openfabric_pysdk.schema import DefinitionSchema
from openfabric_pysdk.service import OpenfabricService
from openfabric_pysdk.util import Util


class OpenfabricRestApi(MethodResource, Resource):

    @doc(description="Input/Output definition", tags=[manifest.get("overview")])
    @marshal_with(DefinitionSchema)  # marshalling
    def get(self):
        return {
            'input': Util.get_concept_definition("input"),
            'output': Util.get_concept_definition("output")
        }

    @doc(description="Entrypoint", tags=[manifest.get("overview")])
    @use_kwargs(OpenfabricService.input_type.schema, location='json')
    @marshal_with(OpenfabricService.output_type.schema)  # marshalling
    def post(self, **kwargs) -> OpenfabricService.output_type:
        start = time.time()
        # Input Schema
        schema_clazz = Util.import_class(OpenfabricService.input_type.schema)
        json = schema_clazz(many=False).load(kwargs)

        # Input Object
        object_clazz = Util.import_class(OpenfabricService.input_type)
        instance = object_clazz(json)
        result = OpenfabricService.execution_function(instance)
        end = time.time()
        duration = round(end - start, 2)
        print(f"Processing time: {duration}s")

        return result
