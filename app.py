from flask import Flask
from flask_restx import Api
from api.routes import config_routes, model_routes, scan_routes
from config.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api = Api(app, version='1.0', title='Garak Security Scanner API',
              description='API for running Garak security scans on AWS Bedrock models')

    api.add_namespace(config_routes.ns_configs)
    api.add_namespace(model_routes.ns_models)
    api.add_namespace(scan_routes.ns_scans)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
