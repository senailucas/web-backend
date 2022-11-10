from sql_alchemy import database
from sqlalchemy.sql.expression import func


class ProductModel(database.Model):
    __tablename__ = 'products'
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(50))
    valor = database.Column(database.Float(50))
    quantidade = database.Column(database.Integer)

    def __init__(self, id, nome, valor, quantidade):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.quantidade = quantidade


    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'valor': self.valor,
            'quantidade': self.quantidade
        }

    @classmethod
    def find_product_by_id(cls, id):
        product = cls.query.filter_by(id=id).first()
        if product:
            return product
        return None

    def save_product(self):
        database.session.add(self)
        database.session.commit()

    def update_product(self, nome, valor, quantidade):
        self.nome = nome
        self.valor = valor
        self.quantidade = quantidade

    def delete_product(self):
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def find_last_product(cls):
        product_id = database.session.query(cls).order_by(cls.id.desc()).first()
        if product_id:
            return product_id.id + 1
        return 1
