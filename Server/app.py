from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.serialize() for restaurant in restaurants])

@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        return jsonify(restaurant.serialize())
    else:
        return jsonify({"error": "Restaurant not found"}), 404

@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"error": "Restaurant not found"}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.serialize() for pizza in pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    if not data:
        return jsonify({"errors": ["Invalid request data"]}), 400

    restaurant_id = data.get("restaurant_id")
    pizza_id = data.get("pizza_id")
    price = data.get("price")

    restaurant = Restaurant.query.get(restaurant_id)
    pizza = Pizza.query.get(pizza_id)

    if not (restaurant and pizza):
        return jsonify({"errors": ["Restaurant or Pizza not found"]}), 404

    existing_relationship = RestaurantPizza.query.filter_by(restaurant_id=restaurant_id, pizza_id=pizza_id).first()

    if existing_relationship:
        existing_relationship.price = price
    else:
        new_relationship = RestaurantPizza(restaurant=restaurant, pizza=pizza, price=price)
        db.session.add(new_relationship)

    db.session.commit()

    return jsonify(pizza.serialize()), 201

if __name__ == '__main__':
    app.run(debug=True)



