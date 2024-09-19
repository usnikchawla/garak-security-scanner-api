from flask_restx import Namespace, Resource, fields
from api.models import Session, Config
import garak

ns_configs = Namespace('configs', description='Configuration operations')

config_model = ns_configs.model('Config', {
    'id': fields.Integer(readOnly=True, description='Configuration identifier'),
    'name': fields.String(required=True, description='Configuration name'),
    'probes': fields.List(fields.String, description='List of probes to use'),
    'detectors': fields.List(fields.String, description='List of detectors to use')
})

@ns_configs.route('/')
class ConfigList(Resource):
    @ns_configs.doc('list_configs')
    @ns_configs.marshal_list_with(config_model)
    def get(self):
        session = Session()
        configs = session.query(Config).all()
        session.close()
        return [config.__dict__ for config in configs], 200

    @ns_configs.doc('create_config')
    @ns_configs.expect(config_model)
    @ns_configs.marshal_with(config_model, code=201)
    def post(self):
        data = ns_configs.payload
        
        valid_probes = set(garak.probes.__all__)
        valid_detectors = set(garak.detectors.__all__)
        
        invalid_probes = set(data['probes']) - valid_probes
        invalid_detectors = set(data['detectors']) - valid_detectors
        
        if invalid_probes:
            ns_configs.abort(400, f"Invalid probes: {', '.join(invalid_probes)}")
        if invalid_detectors:
            ns_configs.abort(400, f"Invalid detectors: {', '.join(invalid_detectors)}")
        
        session = Session()
        new_config = Config(**data)
        session.add(new_config)
        session.commit()
        result = new_config.__dict__
        session.close()
        
        return result, 201

@ns_configs.route('/<int:id>')
@ns_configs.doc(params={'id': 'The configuration identifier'})
class ConfigResource(Resource):
    @ns_configs.doc('get_config')
    @ns_configs.marshal_with(config_model)
    def get(self, id):
        session = Session()
        config = session.query(Config).get(id)
        session.close()
        if not config:
            ns_configs.abort(404, "Configuration not found")
        return config.__dict__, 200

    @ns_configs.doc('delete_config')
    @ns_configs.response(204, 'Configuration deleted')
    def delete(self, id):
        session = Session()
        config = session.query(Config).get(id)
        if not config:
            session.close()
            ns_configs.abort(404, "Configuration not found")
        session.delete(config)
        session.commit()
        session.close()
        return '', 204
