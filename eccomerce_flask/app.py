from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Product(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json

    with app.app_context():
        if 'name' in data and 'price' in data:
            product = Product(
                name=data['name'], 
                price=data['price'], 
                description=data.get("description", "")
            )
            db.session.add(product)
            db.session.commit()

        return jsonify({"message": "Product added sucessfully"}), 

    return jsonify({"Message": "Invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if product:
        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Product deleted sucessfully"}),

    return jsonify({"Message": "Product not found"}), 404


@app.route('/')
def main():
    return {'msg': 'Hello World'}

if __name__ == '__main__':
    app.run(debug=True)

    