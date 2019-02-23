__all__ = ['message_model']
from flask_restplus import fields, Model


message_model = Model('message', {
    'file': fields.String(description='String encoded image'),
    'filename': fields.String(description='The filename'),
    'username': fields.String(description='The user\'s username'),
    'tile_size': fields.Integer(description='The tile_size'),
    'enlargement': fields.Float(description='Image enlargement')
})
