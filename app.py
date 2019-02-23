from flask import Flask
from flask_restplus import api
from flask_cors import CORS
from api import api


def initilize_app():
    app = Flask(__name__)
    api.init_app(app)
    CORS(app, resources={r'*': {'origins': '*'}})
    return app


if __name__ == '__main__':
    app = initilize_app()
    app.run(host='0.0.0.0', port=5030)
