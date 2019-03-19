from factory import create_app
from flask_cors import CORS


app = create_app()
CORS(app)


@app.route(app.config['APPLICATION_ROOT'] + '/')
def index():
    return "Flask/sqlite API"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
