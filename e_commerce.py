from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from marshmallow import ValidationError
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/e_commerce'
db = SQLAlchemy(app)

class CustomerSchema (ma.Schema):
    name = fields.String(required=True)
    email=fields.String(required=True)
    phone=fields.String(required=True)
         
class CustomerAccountSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "customer_id")
    
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=6))


class Meta:
    fields ("name", "email", "phone", "id")

class ProductSchema (ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min-1)) 
    price=fields. Float (required=True, validate=validate. Range (min=0))

class OrderSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "customer_id", "products")
    
    date = fields.Date(required=True)
    customer_id = fields.Integer(required=True)
    products = fields.List(fields.Integer(), required=True)

product_schema = ProductSchema()
products_schema = ProductSchema (many=True) 
customer_schema =CustomerSchema()
customers_schema=CustomerSchema (many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
customer_account_schema = CustomerAccountSchema()
customer_accounts_schema = CustomerAccountSchema(many=True)

class Customer(db.Model):
    tablename = 'Customers'
    id =db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(255), nullable=False)
    email=db.Column (db.String(320))
    phone =db.Column (db.String(15))
    orders=db.relationship('Order', backref='customer')


class Order (db.Model):
    _tablename='Orders'
    id= db.Column (db.Integer, primary_key=True)
    date=db.Column (db.Date, nullable=False)
    customer_id=db.Column(db.Integer, db.ForeignKey('Customers.id'))


class CustomerAccount (db.Model):
    tablename = 'Customer_Accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password=db.Column(db.String(255), nullable=False)
    customer_id = db.Column (db.Integer, db.ForeignKey('Customers.id'))
    customer = db.relationship('Customer', backref='customer_account', uselist=False)

order_product=db.Table('Order_Product',
db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key=True), 
db.Column('product_id', db.Integer, db.ForeignKey('Products.id'), primary_key=True)
)

class Product (db.Model):
    _tablename_ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column (db.Float, nullable=False)
    orders = db.relationship('Order', secondary=order_product, backref=db.backref ('products'))

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        data = request.get_json()
        validated_data = customer_schema.load(data)
        new_customer = Customer(**validated_data)
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.jsonify(new_customer), 400
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        data = request.get_json()
        validated_data = customer_schema.load(data, partial=True)
        for key, value in validated_data.items():
            setattr(customer, key, value)
        db.session.commit()
        return customer_schema.jsonify(customer)
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        customer = Customer.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/customer_accounts', methods=['POST'])
def add_customer_account():
    try:
        data = request.get_json()
        validated_data = customer_account_schema.load(data)
        new_account = CustomerAccount(**validated_data)
        db.session.add(new_account)
        db.session.commit()
        return customer_account_schema.jsonify(new_account), 400
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@app.route('/customer_accounts/<int:id>', methods=['GET'])
def get_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    return customer_account_schema.jsonify(account)


@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    try:
        account = CustomerAccount.query.get_or_404(id)
        data = request.get_json()
        validated_data = customer_account_schema.load(data, partial=True)
        for key, value in validated_data.items():
            setattr(account, key, value)
        db.session.commit()
        return customer_account_schema.jsonify(account)
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    try:
        account = CustomerAccount.query.get_or_404(id)
        db.session.delete(account)
        db.session.commit()
        return '', 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    try:
        validated_data = product_schema.load(data)
        new_product = Product(**validated_data)
        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(new_product), 400
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)


@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    try:
        validated_data = product_schema.load(data, partial=True)
        for key, value in validated_data.items():
            setattr(product, key, value)
        db.session.commit()
        return product_schema.jsonify(product)
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    try:
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return '', 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return products_schema.jsonify(products)


@app.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    try:
        validated_data = order_schema.load(data)
        new_order = Order(
            date=datetime.strptime(validated_data['date'], '%Y-%m-%d'),
            customer_id=validated_data['customer_id']
        )
        db.session.add(new_order)
        db.session.commit()
        for product_id in validated_data['products']:
            product = Product.query.get(product_id)
            if not product:
                raise ValidationError(f"Product with ID {product_id} not found")
            new_order.products.append(product)
        db.session.commit()
        return order_schema.jsonify(new_order), 400
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return order_schema.jsonify(order)


@app.route('/orders/<int:id>/track', methods=['GET'])
def track_order(id):
    order = Order.query.get_or_404(id)
    order_status = {
        "order_id": order.id,
        "order_date": order.date,
        "expected_delivery_date": order.date + timedelta(days=5) 
    }
    return jsonify(order_status)

with app.app_context():
      db.create_all()

if __name__ == '__main__':
  
    app.run(debug=True)