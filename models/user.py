from sql_alchemy import database
from sqlalchemy.sql.expression import func


class UserModel(database.Model):
    __tablename__ = 'users'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50))
    password = database.Column(database.String(50))

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
        }

    @classmethod
    def find_user_by_id(cls, id):
        user = cls.query.filter_by(id=id).first()
        if user:
            return user
        return None

    @classmethod  
    def find_user_by_username(cls, username): 
        user = cls.query.filter_by(username = username).first()
        if user:
            return user
        return None

    def save_user(self):
        database.session.add(self)
        database.session.commit()

    def update_user(self, username, password):
        self.username = username
        self.password = password

    def delete_user(self):
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def find_last_user(cls):
        user_id = database.session.query(cls).order_by(cls.id.desc()).first()
        if user_id:
            return user_id.id + 1
        return 1
