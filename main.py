from flask import Flask
from controller import api, prediction
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(api.bp)
app.register_blueprint(prediction.bp)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
