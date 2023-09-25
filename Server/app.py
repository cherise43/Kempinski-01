from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

from sqlalchemy import CheckConstraint

class Restaurant_Pizza(db.Model):
    __tablename__ = 'restaurant_pizza'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)


    __table_args__ = (
        CheckConstraint('price >= 1 AND price <= 30', name='check_price_range'),
    )

resturant=relationship('Restaurant',back_populates='pizzas')
pizza=relationship('Pizza',back_populates='restaurants')

class Restaurant(db.Model):
    __tablename__ ='restaurant_pizza'
    id =db.Column(db.integer,primary_key=True)
    name=db.Column(db.String(50),unique_key=True,nullable=False)
    address=db.Column(db.String(55),unique_key=True,nullable=False)

    __table_arg__ = (
        CheckConstraint('price >=1 AND price<=50',name='check_price_range')
    )

    class Pizza(db.Model):
          __tablename__ ='pizza'
    id =db.Column(db.Interger,primary_key=True)
    name=db.column(db.String(255),nullable=False)
    ingredients=db.Column(db.text,nullable=False)

resturant = relationship('Restaurant_Pizza',back_populates='pizza')     


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.serialize() for restaurant in restaurants])


@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        return jsonify(restaurant.serialize_with_pizzas())
    else:
        return jsonify({"error": "Restaurant not found"}), 404


@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
    
        for rp in restaurant.pizzas:
            db.session.delete(rp)
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({"error": "Restaurant not found"}), 404


@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = pizza.query.all()
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
    pizza = pizza.query.get(pizza_id)

    if not (restaurant and pizza):
        return jsonify({"errors": ["Restaurant or Pizza not found"]}), 404

    restaurant_pizza = Restaurant_Pizza(restaurant=restaurant, pizza=pizza, price=price)
    db.session.add(restaurant_pizza)
    db.session.commit()

    return jsonify(pizza.serialize()), 201

if __name__ == '__main__':
    app.run(debug=True)


