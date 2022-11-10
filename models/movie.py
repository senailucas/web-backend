from sql_alchemy import database


class MovieModel (database.Model):
    __tablename__ = 'movies'
    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(50))
    rating = database.Column(database.Float(10))
    duration = database.Column(database.Integer)
    lancamento = database.Column(database.String(50))
    faixa_etaria = database.Column(database.String(2))
    trailer = database.Column(database.String(50))

    def __init__(self, id, name, rating, duration, lancamento, faixa_etaria, trailer):
        self.id = id
        self.name = name
        self.rating = rating
        self.duration = duration
        self.lancamento = lancamento
        self.faixa_etaria = faixa_etaria
        self.trailer = trailer


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'rating': self.rating,
            'duration': self.duration,
            'lancamento': self.lancamento,
            'faixa_etaria': self.faixa_etaria,
            'trailer': self.trailer
        }

    @classmethod
    def find_movie_by_id(cls, id):
        movie = cls.query.filter_by(id=id).first()
        if movie:
            return movie
        return None

    def save_movie(self):
        database.session.add(self)
        database.session.commit()

    def update_movie(self, name, rating, duration, lancamento, faixa_etaria, trailer):
        self.name = name
        self.rating = rating
        self.duration = duration
        self.lancamento = lancamento
        self.faixa_etaria = faixa_etaria
        self.trailer = trailer

    def delete_movie(self):
        database.session.delete(self)
        database.session.commit()

    @classmethod
    def find_last_movie(cls):
        movie_id = database.session.query(cls).order_by(cls.id.desc()).first()
        if movie_id:
            return movie_id.id + 1
        return 1
