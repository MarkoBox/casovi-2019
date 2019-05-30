from extensions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(200), unique=True, nullable=False)
    body = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.header
