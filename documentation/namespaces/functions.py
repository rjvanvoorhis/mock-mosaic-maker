from documentation.models import message_model
from flask_restplus import Namespace

functions_ns = Namespace(
    'function',
    path='/function',
    description='Function operations'
)

for model in [message_model]:
    functions_ns.add_model(model.name, model)
