from flask import Blueprint, request, jsonify, session
from orders.models.order_model import Order
from db.db import db  # Asegurar importación correcta
import requests

order_controller = Blueprint('order_controller', __name__)  # Definir antes de usarlo

@order_controller.route('/api/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    result = [{'id': o.id, 'userName': o.userName, 'userEmail': o.userEmail, 'saleTotal': o.saleTotal, 'date': o.date} for o in orders]
    return jsonify(result), 200

@order_controller.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({'id': order.id, 'userName': order.userName, 'userEmail': order.userEmail, 'saleTotal': order.saleTotal, 'date': order.date}), 200

@order_controller.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    userName = session.get('username')  # Cambiar user_name → userName
    userEmail = session.get('email')  # Cambiar user_email → userEmail
    if not userName or not userEmail:
        return jsonify({'message': 'Información de usuario inválida'}), 400

    products = data.get('products')
    if not products or not isinstance(products, list):
        return jsonify({'message': 'Falta o es inválida la información de los productos'}), 400

    # Obtener los productos desde el microservicio de productos
    saleTotal = 0  # Cambiar total_price → saleTotal
    for product in products:
        product_id = product.get('id')
        quantity = product.get('quantity')

        product_response = requests.get(f'http://microproducts:5003/api/products/{product_id}')
        if product_response.status_code != 200:
            return jsonify({'message': f'Producto con ID {product_id} no encontrado'}), 404

        product_data = product_response.json()
        if product_data['quantity'] < quantity:
            return jsonify({'message': f'No hay suficiente stock para el producto {product_data["name"]}'}), 400

        saleTotal += product_data['price'] * quantity

        # Actualizar inventario
        update_data = {'name': product_data['name'], 'price': product_data['price'], 'quantity': product_data['quantity'] - quantity}
        requests.put(f'http://microproducts:5003/api/products/{product_id}', json=update_data)

    new_order = Order(userName=userName, userEmail=userEmail, saleTotal=saleTotal)  # Cambiar nombres
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Orden creada exitosamente', 'order_id': new_order.id}), 201

