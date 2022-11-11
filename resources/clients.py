from datetime import datetime
from flask_restful import Resource, reqparse
from models.client import ClientModel
from flask_jwt_extended import jwt_required


class Clients(Resource):
    def get(self):
        return [client.json() for client in ClientModel.query.all()]


class Client(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('nome', type=str, required=True, help="nome is required")
    minha_requisicao.add_argument('sobrenome', type=str, required=True, help="sobrenome is required")
    minha_requisicao.add_argument('telefone', type=str, required=True, help="telefone is required")
    minha_requisicao.add_argument('rua', type=str, required=True, help="rua is required")
    minha_requisicao.add_argument('bairro', type=str, required=True, help="bairro etaria is required")
    minha_requisicao.add_argument('cidade', type=str, required=True, help="cidade is required")
    minha_requisicao.add_argument('estado', type=str, required=True, help="estado is required")

    #@jwt_required()
    def get(self, id):
        client = ClientModel.find_client_by_id(id)
        if client:
            return [client.json()]
        return {'message':'Client not found'}, 204

    #@jwt_required()
    def post(self):
        client_id = ClientModel.find_last_client()
        dados = Client.minha_requisicao.parse_args()
        new_movie = ClientModel(client_id, **dados)
        
        try:
            new_movie.save_client()
        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_movie.json(), 201

    #@jwt_required()
    def put(self, id):
        dados = Client.minha_requisicao.parse_args()
        client = ClientModel.find_client_by_id(id)

        if client:
            client.update_client(**dados)
            client.save_client()
            return client.json(), 200

        client_id = ClientModel.find_last_client()
        new_movie = ClientModel(client_id, **dados)
        new_movie.save_client()
        return new_movie.json(), 201

    #@jwt_required()
    def delete(self, id):
        client = ClientModel.find_client_by_id(id)
        if client:
            client.delete_client()
            return {'message' : 'Client deleted.'}
        return {'message' : 'Client not founded'}, 204
