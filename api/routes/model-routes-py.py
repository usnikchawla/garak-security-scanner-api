from flask_restx import Namespace, Resource, fields
from api.models import Session, Model
from api.utils import validate_bedrock_model

ns_models = Namespace('models', description='Model operations')

model = ns_models.model('Model', {
    'id': fields.Integer(readOnly=True, description='Model identifier'),
    'name': fields.String(required=True, description='Model name'),
    'model_id': fields.String(required=True, description='Bedrock model ID')
})

@ns_models.route('/')
class ModelList(Resource):
    @ns_models.doc('list_models')
    @ns_models.marshal_list_with(model)
    def get(self):
        session = Session()
        models = session.query(Model).all()
        session.close()
        return [model.__dict__ for model in models], 200

    @ns_models.doc('create_model')
    @ns_models.expect(model)
    @ns_models.marshal_with(model, code=201)
    def post(self):
        data = ns_models.payload
        
        if not validate_bedrock_model(data['model_id']):
            ns_models.abort(400, f"Invalid Bedrock model ID: {data['model_id']}")
        
        session = Session()
        new_model = Model(**data)
        session.add(new_model)
        session.commit()
        result = new_model.__dict__
        session.close()
        
        return result, 201

@ns_models.route('/<int:id>')
@ns_models.doc(params={'id': 'The model identifier'})
class ModelResource(Resource):
    @ns_models.doc('get_model')
    @ns_models.marshal_with(model)
    def get(self, id):
        session = Session()
        model = session.query(Model).get(id)
        session.close()
        if not model:
            ns_models.abort(404, "Model not found")
        return model.__dict__, 200

    @ns_models.doc('delete_model')
    @ns_models.response(204, 'Model deleted')
    def delete(self, id):
        session = Session()
        model = session.query(Model).get(id)
        if not model:
            session.close()
            ns_models.abort(404, "Model not found")
        session.delete(model)
        session.commit()
        session.close()
        return '', 204
