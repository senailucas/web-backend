from datetime import datetime
from flask_restful import Resource, reqparse
from models.order import OrderModel
from flask_jwt_extended import jwt_required


class Orders(Resource):
    def get(self):
        return [order.json() for order in OrderModel.query.all()]


class Order(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('produto_id', type=int, required=True, help="produto_id is required")
    minha_requisicao.add_argument('cliente_id', type=int, required=True, help="cliente_id is required")
    minha_requisicao.add_argument('quantidade', type=int, required=True, help="quantidade is required")
    minha_requisicao.add_argument('valor', type=float, required=True, help="valor is required")
    minha_requisicao.add_argument('valor_total', type=float, required=True, help="valor_total is required")
    

    #@jwt_required()
    def get(self, id):
        order = OrderModel.find_order_by_id(id)
        if order:
            return [order.json()]
        return {'message':'order not found'}, 204

    #@jwt_required()
    def post(self):
        order_id = OrderModel.find_last_order()
        dados = Order.minha_requisicao.parse_args()
        new_product = OrderModel(order_id, **dados)
        
        try:
            new_product.save_order()
        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_product.json(), 201

    #@jwt_required()
    def put(self, id):
        dados = Order.minha_requisicao.parse_args()
        order = OrderModel.find_order_by_id(id)

        if order:
            order.update_order(**dados)
            order.save_order()
            return order.json(), 200

        order_id = OrderModel.find_last_order()
        new_movie = OrderModel(order_id, **dados)
        new_movie.save_order()
        return new_movie.json(), 201

    #@jwt_required()
    def delete(self, id):
        order = OrderModel.find_order_by_id(id)
        if order:
            order.delete_order()
            return {'message' : 'Product deleted.'}
        return {'message' : 'Product not founded'}, 204
