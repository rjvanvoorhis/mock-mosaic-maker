from flask_restplus import Api
from documentation.models import authorizations
from documentation.namespaces import functions_ns
from . import base


api = Api(title='Mock Mosaic Maker',
          description='Mocks the Open_FaaS service',
          authorizations=authorizations
          )

for ns in [functions_ns]:
    api.add_namespace(ns)
