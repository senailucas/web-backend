from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token


minha_requisicao = reqparse.RequestParser()
minha_requisicao.add_argument('username', type=str, required=True, help="username is required")
minha_requisicao.add_argument('password', type=str, required=True, help="password is required")


class Users(Resource):
    def get(self):
        return [user.json() for user in UserModel.query.all()]


class User(Resource):
    def get(self, id):
        user = UserModel.find_user_by_id(id)
        if user:
            return [user.json()]
        return {'message': 'user not found'}, 204

    def post(self):
        if UserModel.find_user_by_username(dados['username']):
            return {'message':'Login {} already exists'.format(dados['username'])}, 200

        user_id = UserModel.find_last_user()
        dados = User.minha_requisicao.parse_args()
        new_user = UserModel(user_id, **dados)

        try:
            new_user.save_user()
        except:
            return {'message': 'An internal error ocurred.'}, 500

        return new_user.json(), 201

    def put(self, id):
        dados = User.minha_requisicao.parse_args()
        user = UserModel.find_user_by_id(id)

        if user:
            user.update_user(**dados)
            user.save_user()
            return user.json(), 200

        user_id = UserModel.find_last_user()
        new_user = UserModel(user_id, **dados)
        new_user.save_user()
        return new_user.json(), 201

    def delete(self, id):
        user = UserModel.find_user_by_id(id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not founded'}, 204


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = minha_requisicao.parse_args()
        user = UserModel.find_user_by_username(dados['username'])

        if user and user.password == dados['password']:
            token_acesso = create_access_token(identity=user.id)
            return {'access_token': token_acesso}, 200
        return {'message': 'User or password is not correct.'}
