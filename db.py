import sqlite3
from flask import g
from utils import hash_password


class DB:

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    @staticmethod
    def col_names(cursor):
        return [i[0] for i in cursor.description]

    def init_app(self, app):
        self.app = app

    def create_schema(self):
        with open("schema.sql", 'r') as sql_file:
            sql = sql_file.read()
            # sql_commands = sql.split(';')
            # for command in sql
            db = self._get_db(self.app.config['DATABASE_PATH'])
            c = db.cursor()
            c.execute(sql)
            db.commit()
            db.close()

    def drop_all(self):
        db = self._get_db(self.app.config['DATABASE_PATH'])
        c = db.cursor()
        c.execute("INSERT INTO posts (header, body) VALUES (?,?)", (data['header'], data['body']))
        db.commit()
        db.close()

    def _get_db(self, db_path):
        return sqlite3.connect(db_path)

    def create_post(self, data):
        db = self._get_db(self.app.config['DATABASE_PATH'])
        c = db.cursor()
        c.execute("INSERT INTO posts (header, body) VALUES (?,?)", (data['header'], data['body']))
        db.commit()
        db.close()

    def get_posts(self, limit, offset):
        db = self._get_db(self.app.config['DATABASE_PATH'])
        c = db.cursor()
        c.execute("SELECT * FROM posts ORDER BY id DESC LIMIT ? OFFSET ?", (limit, offset))
        columns = self.col_names(c)
        list_dic = []
        for r in c.fetchall():
            row = dict(zip(columns, r))
            list_dic.append(row)
        return list_dic

    def update_post(self, data, post_id):
        db = self._get_db(self.app.config['DATABASE_PATH'])
        c = db.cursor()
        c.execute("UPDATE posts SET header = ?, body = ? WHERE id=? ", (data['header'], data['body'], post_id))
        db.commit()
        db.close()

    def delete_post(self, post_id):
        # brisanje vise ?
        db = self._get_db(self.app.config['DATABASE_PATH'])
        c = db.cursor()
        c.execute("DELETE FROM posts WHERE id=?", (post_id))
        db.commit()
        db.close()

    def get_post_by_id(self, post_id):
        db = self._get_db(self.app.config['DATABASE_PATH'])
        c = db.cursor()
        c.execute("SELECT * FROM posts WHERE id=?", (post_id,))
        columns = self.col_names(c)
        return dict(zip(columns, c.fetchone()))

    def get_user(self, data):
        db = self._get_db(self.app.config['DATABASE_PATH'])
        c = db.cursor()
        c.execute("SELECT * FROM user WHERE username=? AND password=?",
                  (data["username"], hash_password(data["password"])))
        columns = self.col_names(c)
        list_dic = []
        for r in c.fetchall():
            row = dict(zip(columns, r))
            list_dic.append(row)
        return list_dic

    def get_user_by_id(self, user_id):
        db = self._get_db(self.app.config['DATABASE_PATH'])
        c = db.cursor()
        c.execute("SELECT * FROM user WHERE id=?", (user_id,))
        columns = self.col_names(c)
        return dict(zip(columns, c.fetchone()))

    def create_user(self, data):
        db = self._get_db(self.app.config['DATABASE_PATH'])
        c = db.cursor()
        c.execute("INSERT INTO user(username, password) VALUES (?,?)",
                  (data['username'], hash_password(data["password"])))
        db.commit()
        db.close()

    # KURSKO #
    def write_kurs(self, data):
        db = self._get_db(self.app.config['DATABASE_PATH'])
        c = db.cursor()
        c.execute("INSERT INTO kursevi(valuta, srednji_kurs, datum) VALUES (?,?,?)",
                  (data['valuta'], data["srednji_kurs"], data['datum']))
        db.commit()
        db.close()

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
#
# def query_db(query, args=(), one=False):
#     cur = get_db().execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv
