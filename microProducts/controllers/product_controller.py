from flask import Blueprint, request, jsonify
from models.product_model import Product
from db import db

product_controller = Blueprint('product_controller', __name__)

@product_controller.route('/api/products', methods=['GET'])
def get_products():
    """Obtiene la lista de productos"""
    try:
        products = Product.query.all()
        result = [{'id': p.id, 'name': p.name, 'price': p.price, 'quantity': p.quantity} for p in products]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener productos: {str(e)}'}), 500

@product_controller.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Obtiene un producto específico por ID"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'quantity': product.quantity}), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener el producto: {str(e)}'}), 500

@product_controller.route('/api/products', methods=['POST'])
def add_product():
    """Agrega un nuevo producto"""
    try:
        data = request.json

        # Validar que los campos obligatorios están presentes
        if not all(k in data for k in ('name', 'price', 'quantity')):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        new_product = Product(name=data['name'], price=data['price'], quantity=data['quantity'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Producto agregado correctamente', 'id': new_product.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al agregar el producto: {str(e)}'}), 500

@product_controller.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Actualiza un producto existente por ID"""
    try:
        product = Product.query.get_or_404(product_id)
        data = request.json

        # Validar que los campos obligatorios están presentes
        if not all(k in data for k in ('name', 'price', 'quantity')):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        product.name = data['name']
        product.price = data['price']
        product.quantity = data['quantity']
        db.session.commit()
        return jsonify({'message': 'Producto actualizado correctamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar el producto: {str(e)}'}), 500

@product_controller.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Elimina un producto por ID"""
    try:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Producto eliminado correctamente'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar el producto: {str(e)}'}), 500

