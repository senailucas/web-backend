from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from resources.users import Users, User, UserLogin
from resources.products import Products, Product
from resources.clients import Clients, Client
from resources.orders import Orders, Order


app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

CORS(app)

DATABASE_URI = 'mysql+pymysql://root@localhost/aula?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "xxxtentacionorvideos?"


@app.before_first_request
def create_database():
    database.create_all()


api.add_resource(Users, '/users')
api.add_resource(User, '/users/<int:id>', '/users')

api.add_resource(Products, '/products')
api.add_resource(Product, '/products/<int:id>', '/products')

api.add_resource(Clients, '/clients')
api.add_resource(Client, '/clients/<int:id>', '/clients')

api.add_resource(Orders, '/orders')
api.add_resource(Order, '/orders/<int:id>', '/orders')

api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from sql_alchemy import database
    database.init_app(app)
    app.run(debug=True)
