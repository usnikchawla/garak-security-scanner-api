from flask_restx import Namespace, Resource, fields
from api.models import Session, Scan, Model, Config
from celery_worker import run_garak_scan

ns_scans = Namespace('scans', description='Scan operations')

scan_request = ns_scans.model('ScanRequest', {
    'model_id': fields.Integer(required=True, description='Model identifier'),
    'config_id': fields.Integer(required=True, description='Configuration identifier'),
    'prompt': fields.String(required=True, description='Prompt to test')
})

scan_result = ns_scans.model('ScanResult', {
    'id': fields.Integer(required=True, description='Scan identifier'),
    'status': fields.String(required=True, description='Scan status'),
    'results': fields.Raw(description='Scan results')
})

@ns_scans.route('/')
class ScanList(Resource):
    @ns_scans.doc('list_scans')
    @ns_scans.marshal_list_with(scan_result)
    def get(self):
        session = Session()
        scans = session.query(Scan).all()
        session.close()
        return [scan.__dict__ for scan in scans], 200

    @ns_scans.doc('create_scan')
    @ns_scans.expect(scan_request)
    @ns_scans.marshal_with(scan_result, code=201)
    def post(self):
        data = ns_scans.payload
        
        session = Session()
        model = session.query(Model).get(data['model_id'])
        config = session.query(Config).get(data['config_id'])
        
        if not model:
            session.close()
            ns_scans.abort(404, "Model not found")
        if not config:
            session.close()
            ns_scans.abort(404, "Configuration not found")
        
        new_scan = Scan(
            model_id=data['model_id'],
            config_id=data['config_id'],
            prompt=data['prompt'],
            status='pending'
        )
        session.add(new_scan)
        session.commit()
        
        run_garak_scan.delay(new_scan.id, model.model_id, config.probes, config.detectors, data['prompt'])
        
        result = new_scan.__dict__
        session.close()
        return result, 201

@ns_scans.route('/<int:id>')
@ns_scans.doc(params={'id': 'The scan identifier'})
class ScanResource(Resource):
    @ns_scans.doc('get_scan')
    @ns_scans.marshal_with(scan_result)
    def get(self, id):
        session = Session()
        scan = session.query(Scan).get(id)
        session.close()
        if not scan:
            ns_scans.abort(404, "Scan not found")
        return scan.__dict__, 200
