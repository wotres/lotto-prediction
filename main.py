from flask import Flask
from controller import api
app = Flask(__name__)

app.register_blueprint(api.bp)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
