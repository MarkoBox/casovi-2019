from extensions import db
from utils import hash_password, status_ok


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def init_from_json(json_data):
        """
        should be used for creating a new object from given json data
        :param json_data json representation of object
        :returns new object of User class
        """
        obj = User()
        obj.username = json_data.get('username')
        obj.password = json_data.get('password')
        return obj

    def to_json(self):
        return {'id': self.id, 'username': self.username}

    @classmethod
    def register(cls, json_data):
        json_data['password'] = hash_password(json_data.get('password'))
        new_user = cls.init_from_json(json_data)
        db.session.add(new_user)
        db.session.flush()
        return status_ok(new_user.to_json())
