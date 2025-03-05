from flask import Flask
from controllers.product_controller import product_controller
from db import db
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'secret123'
app.config.from_object('config.Config')
db.init_app(app)

# Registrar blueprint
app.register_blueprint(product_controller)
CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

