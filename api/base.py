# import json
from flask_restplus import Resource
from documentation.namespaces import functions_ns as ns
from documentation.models import message_model
from resources.image_processor import ImageProcessor
# from handler import Environment, handle


@ns.doc(security='apiKey')
@ns.route('/mosaic-maker')
class MosaicMaker(Resource):
    @ns.expect(message_model)
    def post(self):
        payload = ns.payload
        processor = ImageProcessor(
            payload['username'],
            payload['file'],
            payload['filename']
        )
        return processor.process_image(
            tile_size=payload.get('tile_size', 8),
            enlargement=payload.get('enlargement', 1)
        )
        # env = Environment()
        # payload = ns.payload
        # resp = handle(json.dumps(payload))
        # payload.update({'mosaic_api': env.mosaic_api_ur})
        # payload['received'] = str(request.headers)
        # return resp


@ns.route('/mosaic-healthcheck')
class HealthCheck(Resource):
    def get(self):
        return {'message': 'mock-mosaic-maker up'}
