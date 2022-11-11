from sql_alchemy import database
from sqlalchemy.sql.expression import func


class ClientModel(database.Model):
    __tablename__ = 'clients'
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(50))
    sobrenome = database.Column(database.String(50))
    telefone = database.Column(database.String(50))
    rua = database.Column(database.String(50))
    bairro = database.Column(database.String(50))
    cidade = database.Column(database.String(50))
    estado = database.Column(database.String(50))

    def __init__(self, id, nome, sobrenome, telefone, rua, bairro, cidade, estado):
        self.id = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado


    def json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'telefone': self.telefone,
            'rua': self.rua,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'estado': self.estado
        }

    @classmethod
    def find_client_by_id(cls, id):
        client = cls.query.filter_by(id=id).first()
        if client:
            return client
        return None

    def save_client(self):
        database.session.add(self)
        database.session.commit()

    def update_client(self, nome, sobrenome, telefone, rua, bairro, cidade, estado):
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado

    def delete_client(self):
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def find_last_client(cls):
        client_id = database.session.query(cls).order_by(cls.id.desc()).first()
        if client_id:
            return client_id.id + 1
        return 1
