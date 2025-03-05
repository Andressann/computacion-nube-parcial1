from flask import Flask
from orders.controllers.order_controller import order_controller
from db.db import db  
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'secret123'
app.config.from_object('config.Config')

# Inicializar SQLAlchemy con Flask
db.init_app(app)  

# Registrar el blueprint del controlador de órdenes
app.register_blueprint(order_controller)
CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)

