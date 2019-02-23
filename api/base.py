import json
from flask_restplus import Resource
from documentation.namespaces import functions_ns as ns
from documentation.models import message_model
from handler import Environment, handle


@ns.doc(security='apiKey')
@ns.route('/mosaic-maker')
class MosaicMaker(Resource):
    @ns.expect(message_model)
    def post(self):
        env = Environment()
        payload = ns.payload
        resp = handle(json.dumps(payload))
        payload.update({'mosaic_api': env.mosaic_api_ur})
        # payload['received'] = str(request.headers)
        return resp


@ns.route('/mosaic-healthcheck')
class HealthCheck(Resource):
    def get(self):
        return {'message': 'mock-mosaic-maker up'}
