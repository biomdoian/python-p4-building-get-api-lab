#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list = Bakery.query.all()
    bakeries_data = [bakery.to_dict() for bakery in bakeries_list]
    
    response = make_response(
        jsonify(bakeries_data),
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if not bakery:
        return make_response(jsonify({"error": "Bakery not found"}), 404)
    
    bakery_data = bakery.to_dict()
    
    response = make_response(
        jsonify(bakery_data),
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_list = BakedGood.query.order_by(BakedGood.price.desc()).all()
    
    baked_goods_data = [good.to_dict() for good in baked_goods_list]
    
    response = make_response(
        jsonify(baked_goods_data),
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Query baked goods, order by price descending, and take only the first result
    most_expensive_item = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if not most_expensive_item:
        # If no baked goods are found at all, return a 404
        return make_response(jsonify({"message": "No baked goods found"}), 404)
    
    # Serialize the single most expensive baked good
    most_expensive_data = most_expensive_item.to_dict()
    
    response = make_response(
        jsonify(most_expensive_data),
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
