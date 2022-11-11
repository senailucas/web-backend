from sql_alchemy import database
from sqlalchemy.sql.expression import func


class OrderModel(database.Model):
    __tablename__ = 'orders'
    id = database.Column(database.Integer, primary_key=True)
    produto_id = database.Column(database.Integer, database.ForeignKey("products.id"))
    cliente_id = database.Column(database.Integer, database.ForeignKey("clients.id"))
    quantidade = database.Column(database.Integer)
    valor = database.Column(database.Float(10))
    valor_total = database.Column(database.Float(10))

    def __init__(self, id, produto_id, cliente_id, quantidade, valor, valor_total):
        self.id = id
        self.produto_id = produto_id
        self.cliente_id = cliente_id
        self.quantidade = quantidade
        self.valor = valor
        self.valor_total = valor_total


    def json(self):
        return {
            'produto_id': self.produto_id,
            'cliente_id': self.cliente_id,
            'quantidade': self.quantidade,
            'valor': self.valor,
            'valor_total': self.valor_total
        }

    @classmethod
    def find_order_by_id(cls, id):
        order = cls.query.filter_by(id=id).first()
        if order:
            return order
        return None

    def save_order(self):
        database.session.add(self)
        database.session.commit()

    def update_order(self, produto_id, cliente_id, quantidade, valor, valor_total):
        self.produto_id = produto_id
        self.cliente_id = cliente_id
        self.quantidade = quantidade
        self.valor = valor
        self.valor_total = valor_total

    def delete_order(self):
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def find_last_order(cls):
        order_id = database.session.query(cls).order_by(cls.id.desc()).first()
        if order_id:
            return order_id.id + 1
        return 1
