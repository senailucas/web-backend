from datetime import datetime
from flask_restful import Resource, reqparse
from models.products import ProductModel
from flask_jwt_extended import jwt_required


class Products(Resource):
    def get(self):
        return [product.json() for product in ProductModel.query.all()]


class Product(Resource):
    minha_requisicao = reqparse.RequestParser()
    minha_requisicao.add_argument('nome', type=str, required=True, help="nome is required")
    minha_requisicao.add_argument('valor', type=float, required=True, help="valor is required")
    minha_requisicao.add_argument('quantidade', type=int, required=True, help="quantidade is required")

    #@jwt_required()
    def get(self, id):
        product = ProductModel.find_product_by_id(id)
        if product:
            return [product.json()]
        return {'message':'product not found'}, 204

    #@jwt_required()
    def post(self):
        product_id = ProductModel.find_last_product()
        dados = Product.minha_requisicao.parse_args()
        new_product = ProductModel(product_id, **dados)
        
        try:
            new_product.save_product()
        except:
            return {'message':'An internal error ocurred.'}, 500

        return new_product.json(), 201

    #@jwt_required()
    def put(self, id):
        dados = Product.minha_requisicao.parse_args()
        product = ProductModel.find_product_by_id(id)

        if product:
            product.update_product(**dados)
            product.save_product()
            return product.json(), 200

        product_id = ProductModel.find_last_product()
        new_movie = ProductModel(product_id, **dados)
        new_movie.save_product()
        return new_movie.json(), 201

    #@jwt_required()
    def delete(self, id):
        product = ProductModel.find_product_by_id(id)
        if product:
            product.delete_product()
            return {'message' : 'Product deleted.'}
        return {'message' : 'Product not founded'}, 204
